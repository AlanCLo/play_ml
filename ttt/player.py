# Represents a players

import random
from abc import ABC, abstractmethod

from board import TI, Board


class AbstractPlayer(ABC):

    def __init__(self, whoAmI: TI):
        self.whoAmI = whoAmI

    @abstractmethod
    def getPlayerInput(self, board: Board):
        pass


class ConsolePlayer(AbstractPlayer):
    def getPlayerInput(self, board: Board):
        valid = False
        while not valid:
            try:
                print(f"Valid Moves: {board.validMoves()}")
                print(f"Player '{self.whoAmI}' move: ")
                move = int(input())
                valid = board.isValidMove(move)
                if not valid:
                    print(f"{move} is already taken.")
            except Exception as e:
                print(f"Invalid input {e}")
                print("Please enter an integer.")
        return move


class RandomPlayer(AbstractPlayer):
    def getPlayerInput(self, board: Board):
        return random.choice(board.validMoves())
