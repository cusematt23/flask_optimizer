import pydfs_lineup_optimizer as dfs
import pandas as pd
import numpy as np


if __name__ == '__main__':
    optimizer = dfs.get_optimizer(site='DRAFTKINGS', sport='FOOTBALL')
    optimizer.load_players_from_csv('slates/DK_Proj_Week7.csv')
    N=10
    lineups = optimizer.optimize(n=N)
    for lineup in lineups:
        print(lineup)





