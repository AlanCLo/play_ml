#!/usr/bin/env python

import os
import json
import uuid

FILENAME = 'tictactoe.json'

DRAW = -1
EMPTY = 0
PLAYER1 = 1
PLAYER2 = 2

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


class Board:
    PRINT_CHARS = {
        EMPTY: '_',
        PLAYER1: 'X',
        PLAYER2: 'O',
    }

    def __init__(self, N=3):
        self.id = uuid.uuid1()
        self.N = N
        self.state = [[EMPTY for j in range(self.N)] for i in range(self.N)]
        self.bitStates = {
            EMPTY: 0,
            PLAYER1: 0,
            PLAYER2: 0,
        }
        self.outcome = EMPTY
        self.turns = []

    def print(self):
        i = 1
        for r in self.state:
            row = ""
            for c in r:
                if c == 0:
                    row += str(i)
                else:
                    row += self.PRINT_CHARS[c]
                i += 1
            print(f"{row}")

        for p, s in self.bitStates.items():
            if p == 0:
                print(f"Board state   : {s:>032b}")
            else:
                print(f"Player {p} state: {s:>032b}")
        print("\n")

    def humanToIndicies(self, humanIndex):
        humanIndex -= 1
        i = int(humanIndex / self.N)
        j = humanIndex % self.N
        return i, j

    def isValidMove(self, humanIndex):
        i, j = self.humanToIndicies(humanIndex)
        return self.state[i][j] == EMPTY

    def makeMove(self, player, humanIndex):
        i, j = self.humanToIndicies(humanIndex)
        if self.state[i][j] != EMPTY:
            raise Exception("Not Empty!")

        self.turns.append(self.bitStates.copy())

        self.state[i][j] = player

        arrayIndex = humanIndex - 1
        self.bitStates[player] = self.bitStates[player] | (1 << arrayIndex)
        self.bitStates[EMPTY] = self.bitStates[EMPTY] | (1 << arrayIndex)

    def isGameFinished(self):
        outcome = EMPTY
        for p, s in self.bitStates.items():
            if p != EMPTY:
                for w in WIN_STATES:
                    if s & w == w:
                        outcome = p
                        break
            if outcome != EMPTY:
                break
        if outcome != EMPTY:
            self.outcome = outcome
            return True

        if self.bitStates[EMPTY] & GAMEOVER == GAMEOVER:
            self.outcome = DRAW
            return True

        return False

    def validMoves(self):
        moves = []
        for m in range(self.N * self.N):
            if self.bitStates[EMPTY] >> m & 1 == 0:
                moves.append(m+1)
        return moves

    def saveJson(self):
        if os.path.isfile(FILENAME):
            with open(FILENAME, 'r') as f:
                gameTurns = json.load(f)
        else:
            gameTurns = []

        for t in self.turns:
            gameTurns.append({
                'uuid': str(self.id),
                'Board': t[EMPTY],
                'P1': t[PLAYER1],
                'P2': t[PLAYER2],
                'Result': self.outcome
            })

        with open(FILENAME, 'w') as outfile:
            json.dump(gameTurns, outfile)


def getPlayerInput(current, board):
    valid = False
    while not valid:
        try:
            print(f"Valid Moves: {board.validMoves()}")
            print(f"Player {current} move: ")
            move = int(input())
            valid = board.isValidMove(move)

            if not valid:
                print("That is not a valid move")
        except Exception as e:
            print(f"Invalid input {e}")
            print("Enter an integer")
    return move


def main():
    print("Tic Tac Toe")
    b = Board()
    b.print()

    current = PLAYER1
    while not b.isGameFinished():
        move = getPlayerInput(current, b)
        b.makeMove(current, move)
        b.print()
        if current == PLAYER1:
            current = PLAYER2
        else:
            current = PLAYER1

    print("Game finished - ")
    if b.outcome == DRAW:
        print("Draw game")
    else:
        print(f"Player {b.outcome} wins!")

    b.saveJson()


if __name__ == '__main__':
    main()
