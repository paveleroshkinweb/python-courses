from .enumerator import Enumerator


class Commands(Enumerator):

    ROCK_PAPER_SCISSORS = 'rock-paper-scissors'
    PARTICIPANTS_COUNT = 'participants-count'
    PARTICIPANTS = 'participants'
    PRIVATE_MESSAGE = 'private-message'
    GAME_STEP = 'game-step'
    SERVER_TIME = 'server-time'

    @staticmethod
    def list():
        return Enumerator.list(Commands)


