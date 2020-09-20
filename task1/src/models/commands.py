import enum


class Commands(str, enum.Enum):
    ROCK_PAPER_SCISSORS = 'rock-paper-scissors',
    PARTICIPANTS_COUNT = 'participants-count',
    PARTICIPANTS = 'participants',
    PRIVATE_MESSAGE = 'private-message',
    GAME_STEP = 'game-step'

