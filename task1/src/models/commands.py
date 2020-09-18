import enum


class Command(str, enum.Enum):
    ROCK_PAPER_SCISSORS = 'rock_paper_scissors',
    PARTICIPANTS_COUNT = 'participants_count',
    PARTICIPANTS = 'participants',
    PRIVATE_MESSAGE = 'private_message',
    GAME_STEP = 'game_step'

