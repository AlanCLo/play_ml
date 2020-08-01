import random
from abc import ABC, abstractmethod


class AbstractPlayer(ABC):
    """Abstract class for all implementations of players"""
    def __init__(self, is_player1, **kwargs):
        self.is_player1 = is_player1

    @abstractmethod
    def get_player_input(self, board):
        pass


class PlayerFactory:
    """Register player types and makes instances"""
    class __PlayerFactory:
        def __init__(self):
            self.player_types = dict()

        def register(self, cls):
            self.player_types[cls.__name__] = cls

        def player_type_list(self):
            return [k for k in self.player_types.keys()]

        def CreatePlayer(self, type_name, is_player1, **kwargs):
            player_class = self.player_types.get(type_name)
            if player_class is not None:
                return player_class(is_player1, *kwargs)
            raise Exception(f"No Player of type {type_name} exists")

    __instance = None

    def __init__(self):
        if not PlayerFactory.__instance:
            PlayerFactory.__instance = PlayerFactory.__PlayerFactory()

    def __getattr__(self, name):
        return getattr(self.__instance, name)


def player_type(cls):
    """
    Decorator for new player implementations that will be automatically
    added to the factory
    """
    PlayerFactory().register(cls)
    return cls


@player_type
class ConsolePlayer(AbstractPlayer):
    def get_player_input(self, board):
        valid = False
        label = 'X' if self.is_player1 else 'O'
        while not valid:
            try:
                print(f"Valid Moves: {board.get_valid_moves_list()}")
                print(f"Player '{label}' move:")
                move = int(input())
                valid = board.is_valid_move(move)
                if not valid:
                    print(f"{move} is already taken.")
            except Exception as e:
                print(f"Invalid input {e}")
                print("Please enter an integer.")
        return move


@player_type
class RandomPlayer(AbstractPlayer):
    def get_player_input(self, board):
        return random.choice(board.get_valid_moves_list())
