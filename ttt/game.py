#!/usr/bin/env python

from board import TI, Board
from player import ConsolePlayer, RandomPlayer
from svm_player import SvmPlayer

FILENAME = 'tictactoe.csv'


def main():
    print("Tic Tac Toe")
    b = Board()
    players = {
        TI.PLAYER1: ConsolePlayer(TI.PLAYER1),
        # TI.PLAYER2: RandomPlayer(TI.PLAYER2)
        TI.PLAYER2: SvmPlayer(TI.PLAYER2, FILENAME)
    }

    b.print()
    while not b.isGameFinished():
        current = b.currentPlayer
        move = players[current].getPlayerInput(b)
        b.makeMove(current, move)
        b.print()

    print("Game finished - ")
    if b.outcome == TI.DRAW:
        print("Draw game")
    else:
        print(f"Player '{b.outcome}' wins!")

    b.saveGameResults(FILENAME)


if __name__ == '__main__':
    main()
