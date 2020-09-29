from .board import Board, Cell, Outcome
from .player import AbstractPlayer, player_type


P1_CHAR = 'X'
P2_CHAR = 'O'


class Console(object):
    """A View class - the console implementation"""

    def __init__(self):
        super(Console, self).__init__()

    def display_board(self, board):
        i = 1
        for r in range(Board.D):
            row = ""
            for c in range(Board.D):
                value = board.value_at((r * Board.D) + c + 1)
                if value == Cell.EMPTY:
                    row += str(i)
                elif value == Cell.PLAYER1:
                    row += P1_CHAR
                else:
                    row += P2_CHAR
                i += 1
            print(row)
        print("\n")

    def display_board_state(self, board):
        print(f"Board state   : 0B{board.bit_board:>09b}")
        print(f"Player 1 state: 0B{board.bit_p1:>09b}")
        print(f"Player 2 state: 0B{board.bit_p2:>09b}")

    def display_result(self, board):
        print("Game finished - ")
        result = board.check_outcome()
        if result == Outcome.DRAW:
            print("Draw game")
        elif result == Outcome.PLAYER1:
            print(f"Player 1 '{P1_CHAR}' WINS!")
        else:
            print(f"Player 2 '{P2_CHAR}' WINS!")


@player_type
class ConsolePlayer(AbstractPlayer):
    def get_player_input(self, board):
        valid = False
        label = P1_CHAR if self.is_player1 else P2_CHAR
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
