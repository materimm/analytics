import json
import pandas as pd
import os
from pathlib import Path
from PIL import Image
from urllib.request import urlopen

base_dir = str(Path(os.getcwd()))
#base_dir = str(Path(os.getcwd()).parents[0])

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
    return (stat*60)/toi


#############
#### NFL ####
#############
def get_nfl_data(season):
    if season in list(range(1999, 2021)):
        filepath = base_dir + r"\NFLData\play_by_play_" + str(season) + ".csv.gz"
        return pd.read_csv(filepath, compression='gzip', low_memory=False)
    else:
        print(str(season) + " not in data")


def get_nfl_colors():
    with open(base_dir + '/static/json/nfl_team_colors.json') as colors_file:
        colors = json.load(colors_file)
    return colors

def get_full_nfl_team_name(abbrev):
    with open(base_dir + '/static/json/nfl_abbrev_to_full.json') as teams_file:
        teams = json.load(teams_file)
    return teams[abbrev]

def get_all_nfl_logos():
    with open(base_dir + '/static/json/nfl_logos.json') as logos_file:
        logos = json.load(logos_file)
    return logos

def get_nfl_team_logo(team_code):
    data = get_nfl_logos()
    data = data.loc[data.team_code==team_code]
    return data['url'].tolist()[0]
##############
#### Both ####
##############
def get_percentile(arr, x, r=False):
    arr.sort(reverse=r)
    index = arr.index(x)
    return round((index/len(arr)) * 100)

def get_image_resizes(src, max_width, max_height):
    img = Image.open(urlopen(src))
    w, h = img.size
    ratio = min(max_width/w, max_height/h)
    return w*ratio, h*ratio

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


def hex_to_RGB(hex):
    ''' "#FFFFFF" -> [255,255,255] '''
    # Pass 16 to the integer function for change of base
    return [int(hex[i:i+2], 16) for i in range(1,6,2)]

def RGB_to_hex(RGB):
      ''' [255,255,255] -> "#FFFFFF" '''
      # Components need to be integers for hex to make sense
      RGB = [int(x) for x in RGB]
      return "#"+"".join(["0{0:x}".format(v) if v < 16 else
                "{0:x}".format(v) for v in RGB])


def get_color_gradient(start_hex="#F52933", finish_hex="#4075B5", n=32):
    # Starting, middle and ending colors in RGB form
    s = hex_to_RGB(start_hex)
    m = hex_to_RGB("#ffffff")
    f = hex_to_RGB(finish_hex)
    # Initilize a list of the output colors with the starting color
    RGB_list = [s]
    half = round(n/2)
    # Calcuate a color at each evenly spaced value of t from 1 to half
    for t in range(1, n):
        # Interpolate RGB vector for color at the current value of t
        curr_vector = [
            int(s[j] + (float(t)/(n-1))*(f[j]-s[j]))
            for j in range(3)
        ]
        # Add it to our list of output colors
        RGB_list.append(curr_vector)

    return [RGB_to_hex(RGB) for RGB in RGB_list]
