# from nanoid import generate

from .board import Outcome, Board
from .player import PlayerFactory


class Game:
    def player_types():
        return PlayerFactory().player_type_list()

    def __init__(self, p1_type, p2_type, save_file):
        self.p1 = PlayerFactory().CreatePlayer(p1_type, True)
        self.p2 = PlayerFactory().CreatePlayer(p2_type, False)
        self.save_file = save_file
        self.turns = []

    def display_board(self, board):
        i = 1
        for r in range(Board.D):
            row = ""
            for c in range(Board.D):
                value = board.value_at((r * Board.D) + c + 1)
                if value == 0:
                    row += str(i)
                elif value == 1:
                    row += 'X'
                else:
                    row += 'O'
                i += 1
            print(row)
        print("\n")

    def print_board_state(self, board):
        print(f"Board state   : 0B{board.bit_board:>09b}")
        print(f"Player 1 state: 0B{board.bit_p1:>09b}")
        print(f"Player 2 state: 0B{board.bit_p2:>09b}")

    def play(self):
        print("NEW GAME")

        board = Board()
        is_player1 = True
        self.display_board(board)
        while not board.is_finished():
            if is_player1:
                move = self.p1.get_player_input(board)
            else:
                move = self.p2.get_player_input(board)
            board.move(is_player1, move)
            is_player1 = not is_player1
            self.display_board(board)

        print("Game finished - ")
        result = board.check_outcome()
        if result == Outcome.DRAW:
            print("Draw game")
        elif result == Outcome.PLAYER1:
            print("Player 1 'X' WINS!")
        else:
            print("Player 2 'O' WINS!")

        # TODO: Save
