
from .board import Board
from .player import PlayerFactory
from .console import Console
from .minmaxplayer import MinMaxPlayer


class Game:
    """Controller class for Tic Tac Toe games"""

    def player_types():
        return PlayerFactory().player_type_list()

    def get_default_ai_player():
        return MinMaxPlayer.__name__

    def __init__(self, p1, p2, save, save_file):
        self.p1 = PlayerFactory().CreatePlayer(p1, True)
        self.p2 = PlayerFactory().CreatePlayer(p2, False)
        self.save = save
        self.save_file = save_file
        self.turns = []

    def play(self):
        print("NEW GAME")

        board = Board()
        view = Console()
        is_player1 = True
        view.display_board(board)
        while not board.is_finished():
            if is_player1:
                move = self.p1.get_player_input(board)
            else:
                move = self.p2.get_player_input(board)
            board.move(is_player1, move)
            is_player1 = not is_player1
            view.display_board(board)

        view.display_result(board)

        # TODO: save game moves
