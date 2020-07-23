# Board

import os
from enum import Enum

import pandas as pd
from nanoid import generate


class TI(Enum):
    DRAW = -1, "-"
    EMPTY = 0, "_"
    PLAYER1 = 1, "X"
    PLAYER2 = 2, "O"

    def __init__(self, value, displayName):
        self._value_ = value
        self.displayName = displayName
        super().__init__()

    def __int__(self):
        return self.value

    def __str__(self):
        return self.displayName


class Board:
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

    def __init__(self, N=3, id=generate(size=6)):
        self.N = N
        self.id = generate(size=6)
        self.bitStates = {
            TI.EMPTY: 0,
            TI.PLAYER1: 0,
            TI.PLAYER2: 0,
        }
        self.currentPlayer = TI.PLAYER1
        self.outcome = TI.EMPTY
        self.turns = []

    def print(self):
        i = 1
        for r in range(self.N):
            row = ""
            for c in range(self.N):
                value = self.valueAt((r * self.N) + c + 1)
                if value == TI.EMPTY:
                    row += str(i)
                else:
                    row += str(value)
                i += 1
            print(row)

        for p, s in self.bitStates.items():
            if p == 0:
                print(f"Board state   : {s:>032b}")
            else:
                print(f"Player {int(p)} state: {s:>032b}")
        print("\n")

    def humanToIndicies(self, humanIndex):
        humanIndex -= 1
        i = int(humanIndex / self.N)
        j = humanIndex % self.N
        return i, j

    def _testBit(state, arrayIndex):
        return (state >> arrayIndex) & 1 == 1

    def _moveState(states, player, arrayIndex):
        states[player] = states[player] | (1 << arrayIndex)
        states[TI.EMPTY] = states[TI.EMPTY] | (1 << arrayIndex)
        return states

    def valueAt(self, humanIndex):
        arrayIndex = humanIndex - 1
        # TODO: Validate arrayIndex is 0 to N*N-1
        if not Board._testBit(self.bitStates[TI.EMPTY], arrayIndex):
            return TI.EMPTY
        elif Board._testBit(self.bitStates[TI.PLAYER1], arrayIndex):
            return TI.PLAYER1
        else:
            return TI.PLAYER2

    def isValidMove(self, humanIndex):
        return self.valueAt(humanIndex) == TI.EMPTY

    def makeMove(self, player, humanIndex):
        if self.valueAt(humanIndex) != TI.EMPTY:
            raise Exception("Not Empty!")

        self.turns.append(self.bitStates.copy())

        arrayIndex = humanIndex - 1
        Board._moveState(self.bitStates, player, arrayIndex)
        # self.bitStates[player] = self.bitStates[player] | (1 << arrayIndex)
        # self.bitStates[TI.EMPTY] = self.bitStates[TI.EMPTY] | (1 << arrayIndex)

        if player == TI.PLAYER1:
            self.currentPlayer = TI.PLAYER2
        else:
            self.currentPlayer = TI.PLAYER1

    def isGameFinished(self):
        outcome = TI.EMPTY
        for p, s in self.bitStates.items():
            if p != TI.EMPTY:
                for w in Board.WIN_STATES:
                    if s & w == w:
                        outcome = p
                        break
            if outcome != TI.EMPTY:
                break
        if outcome != TI.EMPTY:
            self.outcome = outcome
            return True

        if self.bitStates[TI.EMPTY] & Board.GAMEOVER == Board.GAMEOVER:
            self.outcome = TI.DRAW
            return True

        return False

    def validMoves(self):
        moves = []
        for m in range(1, self.N * self.N + 1):
            if self.isValidMove(m):
                moves.append(m)
        return moves

    def validMovesAsStates(self):
        moves = self.validMoves()
        states = []
        for m in moves:
            newState = Board._moveState(
                self.bitStates.copy(),
                self.currentPlayer,
                m - 1)
            states.append([
                newState[TI.EMPTY],
                newState[TI.PLAYER1],
                newState[TI.PLAYER2]
            ])

        return moves, states

    def saveGameResults(self, filename):
        gameTurns = []
        for t in self.turns:
            gameTurns.append({
                'uuid': str(self.id),
                'Board': t[TI.EMPTY],
                'P1': t[TI.PLAYER1],
                'P2': t[TI.PLAYER2],
                'Result': int(self.outcome)
            })
        gameDF = pd.DataFrame(gameTurns)

        if os.path.isfile(filename):
            df = pd.read_csv(filename)
            df = pd.concat([df, gameDF])
        else:
            df = gameDF

        df.to_csv(filename, header=True, index=False)
