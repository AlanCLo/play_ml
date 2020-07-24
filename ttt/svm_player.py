# Using Support Vector Machine to make a moves
# The main problem here is that there isn't a linear relationship between
# inputs and result...

# Problem with SVM Player
# 1. The early moves of the game don't really have a "classificaiton"
# it is possible for someone to win after turn 1 or 2 even though tic-tac-toe
# can be a sure-win for player 1. So its quite hard for the player to find
# an alternative move in the early game.
# i.e. All the moves look like they are win moves in the long run, lose moves
# I guess it could be tweaked to take a random move of the choices when equal
# but that isn't productive

import numpy as np
import pandas as pd
from sklearn import svm

from board import TI, Board
from player import AbstractPlayer


class SvmPlayer(AbstractPlayer):
    def __init__(self, whoAmI: TI, datafile: str):
        self.datafile = datafile
        super().__init__(whoAmI)

        print(f"SVM Player: reading {self.datafile}")
        df = pd.read_csv(self.datafile)
        print(f"Found {len(df['uuid'].unique())} unique games")
        print(df['Result'].value_counts())
        df['outcome'] = df.apply(
            lambda r:
                10 if r['Result'] == int(self.whoAmI) else
                5 if r['Result'] == int(TI.DRAW) else
                0, axis=1)
        na = df.values
        X = na[:, 1:4]
        Y = na[:, 5].astype('int')
        self.clf = svm.SVR()
        self.clf.fit(X, Y)

    def getPlayerInput(self, board: Board):
        moves, states = board.validMovesAsStates()
        predictions = self.clf.predict(states)
        mp = np.vstack((moves, predictions)).T
        mp = mp[mp[:, 1].argsort()]
        print("SVM analysis:")
        print(mp)
        select_move = int(mp[-1, 0])
        print(f"SVM picks: {select_move}")
        return select_move
