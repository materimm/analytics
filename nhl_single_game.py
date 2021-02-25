import pandas as pd
import json
import helper as help

OVERALL_PATH = './NHLData/Natural-Stat-Trick/single-game/5v5-overall.csv'
TEAM1_PATH = './NHLData/Natural-Stat-Trick/single-game/5v5-team1.csv'
TEAM2_PATH = './NHLData/Natural-Stat-Trick/single-game/5v5-team2.csv'
TEAM1_LINES_PATH = './NHLData/Natural-Stat-Trick/single-game/team1-lines.csv'
TEAM2_LINES_PATH = './NHLData/Natural-Stat-Trick/single-game/team2-lines.csv'

def upload_data(file_path):
    data = pd.read_csv(file_path)
    return data;

def get_game_stats():
    t1_name = ''
    t2_name = ''
    row_count = 1
    t1_periods = []
    t2_periods = []
    data = upload_data(OVERALL_PATH)
    for index, row in data.iterrows():
        r = row.to_dict()
        period = r.get('Period')
        if row_count < 5: #TODO find better switch
            if period == '1':
                t1_name = r.get('Team')
            t1_periods.append(get_team_values(r))
        else:
            if period == '1':
                t2_name = r.get('Team')
            t2_periods.append(get_team_values(r))
        row_count += 1


    data = upload_data(TEAM1_PATH)
    t1_skaters = []
    t1_toi = []
    t1_cf = []
    t1_xgf = []
    for index, row in data.iterrows():
        r = row.to_dict()
        t1_skaters.append(r.get('Player'))
        t1_toi.append(r.get('TOI'))
        t1_cf.append(r.get('CF%'))
        t1_xgf.append(r.get('xGF%'))

    data = upload_data(TEAM2_PATH)
    t2_skaters = []
    t2_toi = []
    t2_cf = []
    t2_xgf = []
    for index, row in data.iterrows():
        r = row.to_dict()
        t2_skaters.append(r.get('Player'))
        t2_toi.append(r.get('TOI'))
        t2_cf.append(r.get('CF%'))
        t2_xgf.append(r.get('xGF%'))

    data = upload_data(TEAM1_LINES_PATH)
    t1_lines = []
    t1_lines_toi = []
    t1_lines_cf = []
    t1_lines_xgf = []
    for index, row in data.iterrows():
        r = row.to_dict()
        t1_lines.append(r.get('Player 1') + ' & ' + r.get('Player 2') + ' & ' + r.get('Player 3'))
        t1_lines_toi.append(r.get('TOI'))
        t1_lines_cf.append(r.get('CF%'))
        t1_lines_xgf.append(r.get('xGF%'))

    data = upload_data(TEAM2_LINES_PATH)
    t2_lines = []
    t2_lines_toi = []
    t2_lines_cf = []
    t2_lines_xgf = []
    for index, row in data.iterrows():
        r = row.to_dict()
        t2_lines.append(r.get('Player 1') + ' & ' + r.get('Player 2') + ' & ' + r.get('Player 3'))
        t2_lines_toi.append(r.get('TOI'))
        t2_lines_cf.append(r.get('CF%'))
        t2_lines_xgf.append(r.get('xGF%'))

    obj1 = {
        'name' : t1_name,
        'colors': help.get_nhl_team_colors(t1_name),
        'skaters' : {
            'names': t1_skaters,
            'toi': t1_toi,
            'cf': t1_cf,
            'xgf': t1_xgf
        },
        'lines': {
            'names': t1_lines,
            'toi': t1_lines_toi,
            'cf': t1_lines_cf,
            'xgf': t1_lines_xgf
        },
        'periods': t1_periods
    }

    obj2 = {
        'name' : t2_name,
        'colors': help.get_nhl_team_colors(t2_name),
        'skaters' : {
            'names': t2_skaters,
            'toi': t2_toi,
            'cf': t2_cf,
            'xgf': t2_xgf
        },
        'lines': {
            'names': t2_lines,
            'toi': t2_lines_toi,
            'cf': t2_lines_cf,
            'xgf': t2_lines_xgf
        },
        'periods': t2_periods
    }

    return [obj1, obj2]

def get_team_values(data):
    return {
        'cf': data.get('CF%').strip('%'),
        'xgf': data.get('xGF%').strip('%'),
        'hdcf': data.get('HDCF%').strip('%')
    }


#if __name__ == '__main__':
#    r = get_game_stats()
#    print(str(r))
