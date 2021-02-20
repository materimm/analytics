import json

def get_team_colors(team_name):
    with open('./static/json/nhl_team_colors.json') as colors_file:
        colors = json.load(colors_file)
    abbrev = get_team_abbreviation(team_name)
    colors = colors[abbrev]

    return colors

def get_team_abbreviation(team_name):
    with open('./static/json/team_abbrevs.json') as teams_file:
        teams = json.load(teams_file)
    return teams[team_name]
