from math import inf

from .player import AbstractPlayer, player_type
from .board import Outcome


def _minmax(is_player1, board, depth, is_max):
    if depth == 0 or board.is_finished():
        result = board.check_outcome()
        if result == Outcome.DRAW:
            return 0, None
        elif is_player1 == (result == Outcome.PLAYER1):
            return 1, None
        else:
            return -1, None

    current_move = None
    moves = board.get_valid_moves_list()
    if is_max:
        value = -inf
        for m in moves:
            board.move(is_player1, m)
            score, _ = _minmax(is_player1, board, depth - 1, False)
            board.undo_move(m)
            if score > value:
                value = score
                current_move = m
    else:
        value = inf
        for m in moves:
            board.move(not is_player1, m)
            score, _ = _minmax(is_player1, board, depth - 1, True)
            board.undo_move(m)
            if score < value:
                value = score
                current_move = m
    return value, current_move


@player_type
class MinMaxPlayer(AbstractPlayer):
    def get_player_input(self, board):
        b = board.copy()
        score, move = _minmax(self.is_player1, b, 9, True)
        return move
