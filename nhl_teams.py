import pandas as pd
import json
import helper as help

TEAM_STATS_PATH = './NHLData/Natural-Stat-Trick/5v5/team-stats.csv'

def get_team_radar(team_names):
    data = help.upload_data(TEAM_STATS_PATH)
    radar_teams = []
    for index, row in data.iterrows():
        team_data = row.to_dict()
        name = team_data.get('Team')
        if name in team_names:
            obj = {
                'name' : name,
                'colors' : help.get_nhl_team_colors(name),
                'data' : [team_data.get('CF%'), team_data.get('xGF%'), team_data.get('GF%'), team_data.get('SF%'), team_data.get('SCF%'), team_data.get('SCGF%')] #, team_data.get('SV%'), team_data.get('SH%')]
            }
            radar_teams.append(obj)

    radar_obj = {
        'stats' : ['CF%', 'xGF%', 'GF%', 'SF%', 'SCF%', 'SCGF%'], #, 'SV%', 'SH%'],
        'teams' : radar_teams
    }
    return radar_obj

def get_rolling_xGF(teams):
    rolling_xGFs = []
    all_dates = []
    for team in teams:
        abbrev = help.get_nhl_team_abbreviation(team)
        file_path = './NHLData/Natural-Stat-Trick/5v5/' + abbrev + '-games.csv'
        data = help.upload_data(file_path)
        dates = []
        xGFs = []
        queue = []
        counter = 1
        for index, row in data.iterrows():
            game_data = row.to_dict()
            g = game_data.get('Game')
            g_split = g.split('-')
            dates.append(g_split[1].strip() + "/" + g_split[2].strip() + "/" + g_split[0].strip())
            queue.append(game_data.get('xGF%'))
            if counter > 5:
                queue.pop(0)
                xGFs.append(round(sum(queue)/5, 2))
            else:
                xGFs.append(round(sum(queue)/counter, 2))
                counter += 1

        all_dates = all_dates + dates
        obj = {
            'dates': dates,
            'xGFs': xGFs,
            'name' : team,
            'colors' : help.get_nhl_team_colors(team)
        }
        rolling_xGFs.append(obj)

    all_dates = list(set(all_dates))
    all_dates.sort()
    obj = {
        'teams': rolling_xGFs,
        'all_dates' : all_dates
    }
    return obj


def get_goal_share(teams):
    data = help.upload_data(TEAM_STATS_PATH)
    goal_shares = []
    for index, row in data.iterrows():
        team_data = row.to_dict()
        name = team_data.get('Team')
        if name in teams:
            toi = team_data.get('TOI')
            gf = team_data.get('GF')
            ga = team_data.get('GA')
            gf60 = round((gf*60)/toi, 2)
            ga60 = round((ga*60)/toi, 2)
            goal_shares.append({
                'gf60' : gf60,
                'ga60' : ga60,
                'name' : name,
                'colors' : help.get_nhl_team_colors(name)
            })
    return goal_shares

def get_expected_goal_share(teams):
    data = help.upload_data(TEAM_STATS_PATH)
    goal_shares = []
    for index, row in data.iterrows():
        team_data = row.to_dict()
        name = team_data.get('Team')
        if name in teams:
            toi = team_data.get('TOI')
            xgf = team_data.get('xGF')
            xga = team_data.get('xGA')
            xgf60 = round((xgf*60)/toi, 2)
            xga60 = round((xga*60)/toi, 2)
            goal_shares.append({
                'xgf60' : xgf60,
                'xga60' : xga60,
                'name' : name,
                'colors' : help.get_nhl_team_colors(name)
            })
    return goal_shares


#if __name__ == '__main__':
#    teams = ['Buffalo Sabres', 'Boston Bruins', 'New York Islanders', 'New York Rangers', 'Philadelphia Flyers', 'New Jersey Devils', 'Washington Capitals']
#    r = get_team_radar(teams)
#    teams = ['Buffalo Sabres', 'Philadelphia Flyers']
#    r = get_rolling_xGF(teams)
#    r = get_goal_share(teams)
#    r = get_expected_goal_share(teams)
#    print(str(r))
