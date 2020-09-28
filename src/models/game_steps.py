from .enumerator import Enumerator


class GameSteps(Enumerator):

    ROCK = 'rock',
    PAPER = 'paper',
    SCISSORS = 'scissors'

    @staticmethod
    def list():
        return Enumerator.list(GameSteps)