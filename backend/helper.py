import json
import pandas as pd
import os
from pathlib import Path

base_dir = str(Path(os.getcwd())) #str(Path(os.getcwd()).parents[0]) #

#############
#### NHL ####
#############
def get_all_nhl_colors():
    with open(base_dir + '/static/json/nhl_team_colors.json') as colors_file:
        colors = json.load(colors_file)
    return colors


def get_all_nhl_logos():
    with open(base_dir + '/static/json/nhl_logos.json') as logos_file:
        logos = json.load(logos_file)
    return logos


def get_nhl_team_abbreviation(team_name):
    with open(base_dir + '/static/json/nhl_full_to_abbrev.json') as teams_file:
        teams = json.load(teams_file)
    return teams[team_name]


def get_full_nhl_team_name(abbrev):
    with open(base_dir + '/static/json/nhl_abbrev_to_full.json') as teams_file:
        teams = json.load(teams_file)
    return teams[abbrev]

def get_teams(key):
    with open(base_dir + '/static/json/nhl_teams.json') as teams_file:
        t = json.load(teams_file)
    return t[key]


def get_per_60(stat, toi):
    return round((stat*60)/toi, 2)


#############
#### NFL ####
#############
def get_nfl_data(season):
    cwd = os.getcwd()
    if season in list(range(1999, 2021)):
        filepath = cwd + r"\NFLData\play_by_play_" + str(season) + ".csv.gz"
        return pd.read_csv(filepath, compression='gzip', low_memory=False)
    else:
        print(str(season) + " not in data")


def get_nfl_team_colors(team_name):
    with open('./static/json/nfl_team_colors.json') as colors_file:
        colors = json.load(colors_file)
    colors = colors[team_name]
    return colors

##############
#### Both ####
##############
def upload_data(file_path):
    data = pd.read_csv(file_path)
    return data;


def get_5_game_rolling_average(arr):
    rolling_avg = []
    queue = []
    i = 0
    for val in arr:
        queue.append(arr[i])
        if i >= 5:
            queue.pop(0)
            rolling_avg.append(round(sum(queue)/5, 2))
        else:
            rolling_avg.append(round(sum(queue)/(i+1), 2))
        i += 1
    return rolling_avg
