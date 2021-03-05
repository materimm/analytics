import pandas as pd
from pathlib import Path
import os
import helper as help


base_dir = str(Path(os.getcwd()).parents[0])

# @param team - 3 letter code for team. aka BUF for the Buffalo Sabres
def get_team_stats(team):
    data_5v5 = help.upload_data(base_dir + r'\NHLData\Natural-Stat-Trick\all_teams_5v5.csv')
    data_pp = help.upload_data(base_dir + r'\NHLData\Natural-Stat-Trick\all_teams_PP.csv')
    data_pk = help.upload_data(base_dir + r'\NHLData\Natural-Stat-Trick\all_teams_PK.csv')


def get_league_stats():
    game_data = help.upload_data(base_dir + r'\NHLData\moneypuck\games\20-21-games.csv')
    g5v5 = game_data.loc[game_data.situation=='5on5']
