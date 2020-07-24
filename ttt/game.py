#!/usr/bin/env python

import argparse

from board import TI, Board
from player import AbstractPlayer, ConsolePlayer, RandomPlayer
from svm_player import SvmPlayer
from minmax_player import MinMaxPlayer

DEFAULT_OUT = 'ttt_default_data.csv'


class Game:
    def __init__(
            self,
            player1: AbstractPlayer,
            player2: AbstractPlayer,
            saveFile):
        self.board = Board()
        self.players = {
            TI.PLAYER1: player1,
            TI.PLAYER2: player2
        }
        self.saveFile = saveFile

    def play(self):
        b = self.board

        print("New Game: Tic Tac Toe")
        print(f"Results will be saved in {self.saveFile}")
        print("=====================")
        b.print()
        while not b.isGameFinished():
            current = b.currentPlayer
            move = self.players[current].getPlayerInput(b)
            b.makeMove(current, move)
            b.print()

        print("Game finished - ")
        if b.outcome == TI.DRAW:
            print("Draw game")
        else:
            print(f"Player '{b.outcome}' wins!")

        b.saveGameResults(self.saveFile)


def instantiatePlayer(typeString, player, args):
    print(f"Creating Player: {player} is {typeString}")
    if typeString == "CP":
        return ConsolePlayer(player)
    elif typeString == "RP":
        return RandomPlayer(player)
    elif typeString == "SP":
        return SvmPlayer(player, args.inputdata)
    elif typeString == "MM":
        return MinMaxPlayer(player)
    raise Exception(f"{typeString} player not found!")


def main(args):
    N = int(args.N)
    if N < 1:
        print("Why are you like this?")
        return
    else:
        print(f"Playing {N} games")
        print(">>>>>>>>>>>>>>>>>>>>>>>")

    for i in range(N):
        print(f"Starting Game {i} of {N}...")
        player1 = instantiatePlayer(args.p1, TI.PLAYER1, args)
        player2 = instantiatePlayer(args.p2, TI.PLAYER2, args)
        g = Game(player1, player2, args.outputdata)
        g.play()


if __name__ == '__main__':
    player_choices = ("CP", "RP", "SP", "MM")
    parser = argparse.ArgumentParser(description="Tic Tac Toe game!")
    parser.add_argument(
        "-p1", choices=player_choices, dest="p1", default="CP")
    parser.add_argument(
        "-p2", choices=player_choices, dest="p2", default="CP")
    parser.add_argument(
        "--input", action="store", dest="inputdata", default=DEFAULT_OUT)
    parser.add_argument(
        "--output", action="store", dest="outputdata", default=DEFAULT_OUT)
    parser.add_argument(
        "-N", action="store", dest="N", default=1)
    parser.add_argument("-hh", action="store_true")
    parser.add_argument("-hr", action="store_true")
    parser.add_argument("-rh", action="store_true")
    parser.add_argument("-rr", action="store_true")
    args = parser.parse_args()
    if args.hh:
        args.p1 = "CP"
        args.p2 = ""
    if args.hr:
        args.p1 = "CP"
        args.p2 = "RP"
    if args.rh:
        args.p1 = "RP"
        args.p2 = "CP"
    if args.rr:
        args.p1 = "RP"
        args.p2 = "RP"
        args.outputdata = "ttt_rr_data.csv"

    main(args)
