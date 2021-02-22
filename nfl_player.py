import pandas as pd
import json
import helper as help

def get_rolling_epa_and_cpoe(player, seasons):
    df = pd.DataFrame()
    for s in seasons:
        df = df.append(help.get_nfl_data(s))

    #regular season data only
    df = df.loc[df.season_type=='REG']

    qbs = df.copy()
    qbs = qbs.groupby(['passer', 'posteam', 'game_id'], as_index=False).agg({'epa':'mean',
                                                              'cpoe':'mean',
                                                              'play_id':'count'})
    #Filter to players with 10 or more dropbacks in a game
    qbs = qbs.loc[qbs.play_id>9]
    #get league average epa and cpoe per game
    qbs = qbs.agg({'epa':'mean', 'cpoe':'mean'})

    
    df = df.loc[df.passer==player]
    df = df.groupby(['posteam', 'passer', 'game_id'], as_index=False).agg({'epa':'mean',
                                                              'cpoe':'mean'})

    games = []
    epa = []
    cpoe = []
    for index, row in df.iterrows():
        r = row.to_dict()
        game_data = r.get('game_id').split('_')
        games.append(game_data[0] + ' Week ' + game_data[1] + ': ' + game_data[2] + ' @ ' + game_data[3])
        epa.append(r.get('epa'))
        cpoe.append(r.get('cpoe'))
        team = r.get('posteam')

    return {
        'name': player,
        'games': games,
        'epa': help.get_5_game_rolling_average(epa),
        'cpoe': help.get_5_game_rolling_average(cpoe),
        'colors': help.get_nfl_team_colors(team),
        'league_avg_epa' : qbs.get(key='epa'),
        'league_avg_cpoe' : qbs.get(key='cpoe')
    }

#if __name__ == '__main__':
#    player = 'C.Wentz'
#    seasons = list(range(2016, 2021)) #note end is not inclusive
#    r = get_rolling_epa_and_cpoe(player, seasons)
#    print(str(r))
