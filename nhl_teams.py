import pandas as pd
import json

file_path = './NHLData/Natural-Stat-Trick/team-stats.csv'

def upload_data(file_path):
    data = pd.read_csv(file_path)
    return data;

def get_team_radar(team_names):
    data = upload_data(file_path)
    radar_teams = []
    for index, row in data.iterrows():
        team_data = row.to_dict()
        name = team_data.get('Team')
        if name in team_names:
            obj = {
                'name' : name,
                'colors' : get_team_colors(name),
                'data' : [team_data.get('CF%'), team_data.get('xGF%'), team_data.get('GF%'), team_data.get('SF%'), team_data.get('SCF%'), team_data.get('SCGF%')] #, team_data.get('SV%'), team_data.get('SH%')]
            }
            radar_teams.append(obj)

    radar_obj = {
        'stats' : ['CF%', 'xGF%', 'GF%', 'SF%', 'SCF%', 'SCGF%'], #, 'SV%', 'SH%'],
        'teams' : radar_teams
    }
    return radar_obj

def get_team_colors(team_name):
    with open('./static/json/team_abbrevs.json') as teams_file:
        teams = json.load(teams_file)
    with open('./static/json/nhl_team_colors.json') as colors_file:
        colors = json.load(colors_file)
    abbrev = teams[team_name]
    colors = colors[abbrev]

    return colors

#if __name__ == '__main__':
#    teams = ['Buffalo Sabres', 'Boston Bruins', 'New York Islanders', 'New York Rangers', 'Philadelphia Flyers', 'New Jersey Devils', 'Washington Capitals']
#    print(str(get_team_radar(teams)))
