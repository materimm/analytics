import json
import pandas as pd

#############
#### NHL ####
#############
def get_nhl_team_colors(team_name):
    with open('./static/json/nhl_team_colors.json') as colors_file:
        colors = json.load(colors_file)
    abbrev = get_nhl_team_abbreviation(team_name)
    colors = colors[abbrev]

    return colors

def get_nhl_team_abbreviation(team_name):
    with open('./static/json/team_abbrevs.json') as teams_file:
        teams = json.load(teams_file)
    return teams[team_name]


#############
#### NFL ####
#############
def get_nfl_data(season):
    if season in list(range(1999, 2021)):
        filepath = r"C:\Users\MoreyMATERISE\Documents\analytics_dev\analytics\NFLData\play_by_play_" + str(season) + ".csv.gz"
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
