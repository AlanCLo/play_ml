from enum import Enum


class Cell(Enum):
    """Possible states of a single cell on the board"""
    EMPTY = 0,
    PLAYER1 = 1
    PLAYER2 = 2


class Outcome(Enum):
    """Possible outcomes of a single game"""
    DRAW = -1,
    NOT_FINISHED = 0
    PLAYER1 = 1
    PLAYER2 = 2

    def is_finished(self):
        return self != Outcome.NOT_FINISHED


class Board:
    """A Tic Tac Toe game state"""
    D = 3
    LENGTH = 9
    WIN_STATES = [
        # Horizontal
        0B000000111,
        0B000111000,
        0B111000000,
        # Vertical
        0B001001001,
        0B010010010,
        0B100100100,
        # Diagonal
        0B100010001,
        0B001010100,
    ]
    GAMEOVER = 0B111111111

    def test_bit(state, array_index):
        return (state >> array_index) & 1 == 1

    def __init__(self, bit_board=0, bit_p1=0, bit_p2=0):
        self.bit_board = bit_board
        self.bit_p1 = bit_p1
        self.bit_p2 = bit_p2

    def copy(self):
        return Board(self.bit_board, self.bit_p1, self.bit_p2)

    def value_at(self, human_index):
        array_index = human_index - 1
        if not Board.test_bit(self.bit_board, array_index):
            return Cell.EMPTY
        elif Board.test_bit(self.bit_p1, array_index):
            return Cell.PLAYER1
        else:
            return Cell.PLAYER2

    def check_win(self, is_player1):
        s = self.bit_p1 if is_player1 else self.bit_p2
        for w in Board.WIN_STATES:
            if s & w == w:
                return True
        return False

    def check_outcome(self):
        if self.check_win(True):
            return Outcome.PLAYER1
        elif self.check_win(False):
            return Outcome.PLAYER2
        elif self.bit_board & Board.GAMEOVER == Board.GAMEOVER:
            return Outcome.DRAW
        return Outcome.NOT_FINISHED

    def is_finished(self):
        return self.check_outcome().is_finished()

    def get_valid_moves(self):
        for i in range(0, Board.LENGTH):
            if not Board.test_bit(self.bit_board, i):
                yield i + 1

    def get_valid_moves_list(self):
        return [m for m in self.get_valid_moves()]

    def is_valid_move(self, human_index):
        return not Board.test_bit(self.bit_board, human_index - 1)

    def move(self, is_player1, human_index):
        array_index = human_index - 1
        mask = 1 << array_index
        self.bit_board |= mask
        if is_player1:
            self.bit_p1 |= mask
        else:
            self.bit_p2 |= mask

    def undo_move(self, human_index):
        array_index = human_index - 1
        mask = ~(1 << array_index)
        self.bit_board &= mask
        self.bit_p1 &= mask
        self.bit_p2 &= mask
