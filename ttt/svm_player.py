# Using Support Vector Machine to make a moves
# The main problem here is that there isn't a linear relationship between
# inputs and result...


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
        self.clf = svm.SVC()
        self.clf.fit(X, Y)

    def getPlayerInput(self, board: Board):
        moves, states = board.validMovesAsStates()
        predictions = self.clf.predict(states)
        mp = np.vstack((moves, predictions)).T
        mp = mp[mp[:, 1].argsort()]
        print("SVM analysis:")
        print(mp)
        select_move = mp[-1, 0]
        print(f"SVM picks: {select_move}")
        return select_move
