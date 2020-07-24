
from math import inf

import numpy as np

from board import TI, Board
from player import AbstractPlayer


def _playerWin(states, player):
    for w in Board.WIN_STATES:
        if states[player] == w:
            return True
    return False


def _checkOutcome(states):
    if _playerWin(states, TI.PLAYER1):
        return TI.PLAYER1
    elif _playerWin(states, TI.PLAYER2):
        return TI.PLAYER2
    elif states[TI.EMPTY] & Board.GAMEOVER == Board.GAMEOVER:
        return TI.DRAW
    return TI.EMPTY


def _isGameOver(outcome: TI):
    return outcome != TI.EMPTY


def _validMoves(states):
    moves = []
    for i in range(0, 9):
        if not Board._testBit(states[TI.EMPTY], i):
            moves.append(i+1)
    return moves


def _move(states, player, humanIndex):
    newStates = states.copy()
    arrayIndex = humanIndex - 1
    bit = (1 << arrayIndex)
    newStates[player] = newStates[player] | bit
    newStates[TI.EMPTY] = newStates[TI.EMPTY] | bit
    return newStates


def _minmax(whoAmI, otherPlayer, states, depth, isMax):
    result = _checkOutcome(states)
    if depth == 0 or _isGameOver(result):
        # Heuristic value of node
        if result == TI.DRAW:
            return 0, None
        elif result == whoAmI:
            return 1, None
        else:
            return -1, None

    moves = _validMoves(states)
    if isMax:
        value = -inf
        best = -1
        scores = []
        for m in moves:
            child = _move(states, whoAmI, m)
            s, mv = _minmax(whoAmI, otherPlayer, child, depth - 1, False)
            scores.append(s)
            if s > value:
                best = m
                value = s
        np_scores = np.array(scores)
        value = np_scores.sum()
        m_i = np_scores.argmax()
        best = moves[m_i]
        return value, best
    if not isMax:
        value = inf
        best = -1
        for m in moves:
            child = _move(states, otherPlayer, m)
            s, mv = _minmax(whoAmI, otherPlayer, child, depth - 1, True)
            if s < value:
                best = m
                value = s
        return value, best


class MinMaxPlayer(AbstractPlayer):
    def getPlayerInput(self, board: Board):
        if self.whoAmI == TI.PLAYER1:
            otherPlayer = TI.PLAYER2
        else:
            otherPlayer = TI.PLAYER1

        s, m = _minmax(self.whoAmI, otherPlayer, board.bitStates, 9, True)
        return m
