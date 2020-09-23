from .message_handler import MessageHandler
from src.models.commands import Commands
from src.exceptions.invalid_message import InvalidMessage
from src.models.game_steps import GameSteps
import random
import time


class CommandHandler(MessageHandler):

    def __init__(self, client_handler):
        super().__init__(client_handler)

    def process_message(self, message):
        self.validate_message(message)
        handlers = {
            Commands.PARTICIPANTS: self.handle_participants,
            Commands.PARTICIPANTS_COUNT: self.handle_participants_count,
            Commands.ROCK_PAPER_SCISSORS: self.handle_rock_paper_scissors,
            Commands.GAME_STEP: lambda: self.handle_game_step(message),
            Commands.PRIVATE_MESSAGE: lambda: self.handle_private_message(message),
            Commands.SERVER_TIME: self.handle_server_time_message
        }
        handler = handlers[message.command]
        handler()

    def handle_participants(self):
        participants = list(self.client_handler.handlers.keys())
        response = self.form_success_server_msg(content=f'List of participants: {", ".join(participants)}')
        self.client_handler.send_message(response)

    def handle_participants_count(self):
        count = len(self.client_handler.handlers)
        response = self.form_success_server_msg(content=f'The number of participants is {count}')
        self.client_handler.send_message(response)

    def handle_rock_paper_scissors(self):
        self.client_handler.active_game = True
        response = self.form_success_server_msg(content='Rock-paper-scissors game started')
        self.client_handler.send_message(response)

    def handle_game_step(self, message):
        beats = {
            GameSteps.ROCK: GameSteps.SCISSORS,
            GameSteps.PAPER: GameSteps.ROCK,
            GameSteps.SCISSORS: GameSteps.PAPER
        }
        client_step = message.content
        server_step = random.choice(GameSteps.list())
        content = f'Server chose {server_step}, '
        if client_step == server_step:
            content += 'dead heat, game is not ended so try again :)'
        elif beats[client_step] == server_step:
            content += 'you won, the game is over'
            self.client_handler.active_game = False
        else:
            content += 'you lost, the game is over'
            self.client_handler.active_game = False
        response = self.form_success_server_msg(content=content)
        self.client_handler.send_message(response)

    def handle_private_message(self, message):
        selected_users = message.selected_users
        handlers = [self.client_handler.handlers[user]
                    for user in selected_users
                    if user in self.client_handler.handlers]
        absent_users = [user for user in selected_users
                        if user not in self.client_handler.handlers]
        broadcast_message = self.form_success_msg(
                sender=self.client_handler.user.name,
                content=message.content
        )
        self.client_handler.broadcast_message(broadcast_message, handlers)
        if absent_users:
            self.client_handler.send_message(
                self.form_error_server_msg(content=f'These users are absent: {", ".join(absent_users)}')
            )

    def handle_server_time_message(self):
        uptime_ms = time.time() - self.client_handler.server_info['socket_start_time']
        formatted_time = time.strftime("%Hh %Mm %Ss", time.gmtime(uptime_ms))
        response = self.form_success_server_msg(content=f'Server uptime: {formatted_time}')
        self.client_handler.send_message(response)

    def validate_message(self, message):
        super().validate_message(message, ['command'], [('command', Commands.list())])
        if not self.client_handler.user:
            raise InvalidMessage("You need to authenticate first")
        validators = {
            Commands.ROCK_PAPER_SCISSORS: self.validate_rock_paper_scissors,
            Commands.GAME_STEP: lambda: self.validate_game_step(message),
            Commands.PRIVATE_MESSAGE: lambda: self.validate_private_message(message)
        }
        validator = validators.get(message.command, None)
        if validator:
            validator()

    def validate_rock_paper_scissors(self):
        if self.client_handler.active_game:
            raise InvalidMessage("Please finish last game before starting a new")

    def validate_game_step(self, message):
        if not self.client_handler.active_game:
            raise InvalidMessage("You don't have an active game")
        if not message.content:
            raise InvalidMessage("You need to pass an action inside of content")
        available_steps = GameSteps.list()
        if message.content not in available_steps:
            raise InvalidMessage(f"step must be one of {', '.join(available_steps)}")

    def validate_private_message(self, message):
        if not message.selected_users:
            raise InvalidMessage(f"You need to choose users")
        if not message.content:
            raise InvalidMessage(f"Content can't be empty")
        if len(message.selected_users) == 1 and message.selected_users[0] == self.client_handler.user.name:
            raise InvalidMessage("You can't send message just for yourself")