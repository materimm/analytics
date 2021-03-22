from elopy.elo import Elo
import helper as help
import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def save_nfl_data_for_elo():
    base_dir = str(Path(os.getcwd()).parents[0])
    #games = help.get_nfl_data(1999)
    for season in list(range(1999, 2021)):
        data = pd.read_csv(base_dir + '/NFLData/play_by_play_' + str(season) + '.csv.gz', compression='gzip', low_memory=False)
        data = data.loc[data.season_type=='REG']
        data = data.loc[data.desc=='END GAME']
        data = data[['home_team', 'away_team', 'game_id', 'game_date', 'total_home_score', 'total_away_score']]
        data.to_csv('nfl_results_' + str(season) + '.csv', index=False)


def get_nfl_elo(team=None):
    nfl_elos = {
        'ARI' : Elo(start_elo=1500, k=20, hca=100),
        'ATL' : Elo(start_elo=1500, k=20, hca=100),
        'BAL' : Elo(start_elo=1500, k=20, hca=100),
        'BUF' : Elo(start_elo=1500, k=20, hca=100),
        'CAR' : Elo(start_elo=1500, k=20, hca=100),
        'CHI' : Elo(start_elo=1500, k=20, hca=100),
        'CIN' : Elo(start_elo=1500, k=20, hca=100),
        'CLE' : Elo(start_elo=1500, k=20, hca=100),
        'DAL' : Elo(start_elo=1500, k=20, hca=100),
        'DEN' : Elo(start_elo=1500, k=20, hca=100),
        'DET' : Elo(start_elo=1500, k=20, hca=100),
        'GB' :  Elo(start_elo=1500, k=20, hca=100),
        'HOU' : Elo(start_elo=1500, k=20, hca=100),
        'IND' : Elo(start_elo=1500, k=20, hca=100),
        'JAX' : Elo(start_elo=1500, k=20, hca=100),
        'KC' :  Elo(start_elo=1500, k=20, hca=100),
        'LAC' : Elo(start_elo=1500, k=20, hca=100),
        'LA' :  Elo(start_elo=1500, k=20, hca=100),
        'LV' :  Elo(start_elo=1500, k=20, hca=100),
        'MIA' : Elo(start_elo=1500, k=20, hca=100),
        'MIN' : Elo(start_elo=1500, k=20, hca=100),
        'NE' :  Elo(start_elo=1500, k=20, hca=100),
        'NO' :  Elo(start_elo=1500, k=20, hca=100),
        'NYG' : Elo(start_elo=1500, k=20, hca=100),
        'NYJ' : Elo(start_elo=1500, k=20, hca=100),
        'OAK' : Elo(start_elo=1500, k=20, hca=100),
        'PHI' : Elo(start_elo=1500, k=20, hca=100),
        'PIT' : Elo(start_elo=1500, k=20, hca=100),
        'SD' :  Elo(start_elo=1500, k=20, hca=100),
        'SF' :  Elo(start_elo=1500, k=20, hca=100),
        'SEA' : Elo(start_elo=1500, k=20, hca=100),
        'TB' :  Elo(start_elo=1500, k=20, hca=100),
        'TEN' : Elo(start_elo=1500, k=20, hca=100),
        'WAS' : Elo(start_elo=1500, k=20, hca=100)
    }

    nfl_elos_over_time = {
        'ARI' : [1500],
        'ATL' : [1500],
        'BAL' : [1500],
        'BUF' : [1500],
        'CAR' : [1500],
        'CHI' : [1500],
        'CIN' : [1500],
        'CLE' : [1500],
        'DAL' : [1500],
        'DEN' : [1500],
        'DET' : [1500],
        'GB' :  [1500],
        'HOU' : [1500],
        'IND' : [1500],
        'JAX' : [1500],
        'KC' :  [1500],
        'LAC' : [1500],
        'LA' :  [1500],
        'LV' :  [1500],
        'MIA' : [1500],
        'MIN' : [1500],
        'NE' :  [1500],
        'NO' :  [1500],
        'NYG' : [1500],
        'NYJ' : [1500],
        'OAK' : [1500],
        'PHI' : [1500],
        'PIT' : [1500],
        'SD' :  [1500],
        'SF' :  [1500],
        'SEA' : [1500],
        'TB' :  [1500],
        'TEN' : [1500],
        'WAS' : [1500]
    }

    base_dir = str(Path(os.getcwd()).parents[0])
    #games = help.get_nfl_data(1999)
    games = pd.DataFrame()
    for season in list(range(1999, 2021)):
        data = help.upload_data(base_dir + '/NFLData/results/nfl_results_' + str(season) + '.csv')
        games = games.append(data)

    games.sort_values(['game_date'], inplace=True)

    for index, row in games.iterrows():
        r = row.to_dict()
        #print(str(r))
        team1 = r.get('home_team')
        team2 = r.get('away_team')
        score_diff = r.get('total_home_score') - r.get('total_away_score')
        t1_elo = nfl_elos.get(team1)
        t2_elo = nfl_elos.get(team2)
        t1_elo.play_game(t2_elo, score_diff, is_home=True)
        nfl_elos_over_time.get(team1).append(t1_elo.elo)
        nfl_elos_over_time.get(team2).append(t2_elo.elo)

    for key, value in nfl_elos.items():
         print(key + ' = ' + str(value.elo))

    x_arr = [list(range(0, len(nfl_elos_over_time.get('BUF')))), list(range(0, len(nfl_elos_over_time.get('PHI'))))]
    y_arr = [nfl_elos_over_time.get('BUF'), nfl_elos_over_time.get('PHI')]
    colors = ["#00338D", "#004C54"]
    plot_elos(x_arr, y_arr, colors)



def get_nhl_elo(team=None):
    nhl_elos = {
        'ANA' : Elo(start_elo=1500, k=5, hca=100),
        'ARI' : Elo(start_elo=1500, k=5, hca=100),
        'ATL' : Elo(start_elo=1500, k=5, hca=100),
        'BOS' : Elo(start_elo=1500, k=5, hca=100),
        'BUF' : Elo(start_elo=1500, k=5, hca=100),
        'CGY' : Elo(start_elo=1500, k=5, hca=100),
        'CAR' : Elo(start_elo=1500, k=5, hca=100),
        'COL' : Elo(start_elo=1500, k=5, hca=100),
        'CBJ' : Elo(start_elo=1500, k=5, hca=100),
        'CHI' : Elo(start_elo=1500, k=5, hca=100),
        'DAL' : Elo(start_elo=1500, k=5, hca=100),
        'DET' : Elo(start_elo=1500, k=5, hca=100),
        'EDM' : Elo(start_elo=1500, k=5, hca=100),
        'FLA' : Elo(start_elo=1500, k=5, hca=100),
        'L.A' : Elo(start_elo=1500, k=5, hca=100),
        'MIN' : Elo(start_elo=1500, k=5, hca=100),
        'MTL' : Elo(start_elo=1500, k=5, hca=100),
        'NSH' : Elo(start_elo=1500, k=5, hca=100),
        'N.J' : Elo(start_elo=1500, k=5, hca=100),
        'NYI' : Elo(start_elo=1500, k=5, hca=100),
        'NYR' : Elo(start_elo=1500, k=5, hca=100),
        'OTT' : Elo(start_elo=1500, k=5, hca=100),
        'PHI' : Elo(start_elo=1500, k=5, hca=100),
        'PIT' : Elo(start_elo=1500, k=5, hca=100),
        'STL' : Elo(start_elo=1500, k=5, hca=100),
        'S.J' : Elo(start_elo=1500, k=5, hca=100),
        'T.B' : Elo(start_elo=1500, k=5, hca=100),
        'TOR' : Elo(start_elo=1500, k=5, hca=100),
        'VAN' : Elo(start_elo=1500, k=5, hca=100),
        'VGK' : Elo(start_elo=1500, k=5, hca=100),
        'WSH' : Elo(start_elo=1500, k=5, hca=100),
        'WPG' : Elo(start_elo=1500, k=5, hca=100),
    }

    nhl_elos_over_time = {
        'ANA' : [1500],
        'ARI' : [1500],
        'ATL' : [1500],
        'BOS' : [1500],
        'BUF' : [1500],
        'CGY' : [1500],
        'CAR' : [1500],
        'COL' : [1500],
        'CBJ' : [1500],
        'CHI' : [1500],
        'DAL' : [1500],
        'DET' : [1500],
        'EDM' : [1500],
        'FLA' : [1500],
        'L.A' : [1500],
        'MIN' : [1500],
        'MTL' : [1500],
        'NSH' : [1500],
        'N.J' : [1500],
        'NYI' : [1500],
        'NYR' : [1500],
        'OTT' : [1500],
        'PHI' : [1500],
        'PIT' : [1500],
        'STL' : [1500],
        'S.J' : [1500],
        'T.B' : [1500],
        'TOR' : [1500],
        'VAN' : [1500],
        'VGK' : [1500],
        'WSH' : [1500],
        'WPG' : [1500],
    }

    base_dir = str(Path(os.getcwd()).parents[0])
    games = help.upload_data(base_dir + '/NHLData/moneypuck/games/all_games.csv')
    games = games.loc[games.situation=='all']
    games = games[['gameId', 'team', 'opposingTeam', 'home_or_away', 'gameDate', 'goalsFor', 'goalsAgainst']]
    games.sort_values(['gameId'], inplace=True)

    x = 0
    for index, row in games.iterrows():
        x = x+1
        if x%2 == 0:
            #skip duplicate games
            continue

        r = row.to_dict()
        team1 = r.get('team')
        team2 = r.get('opposingTeam')
        is_team1_home = True if r.get('home_or_away') == 'HOME' else False
        score_diff = r.get('goalsFor') - r.get('goalsAgainst')
        t1_elo = nhl_elos.get(team1)
        t2_elo = nhl_elos.get(team2)
        t1_elo.play_game(t2_elo, score_diff, is_home=is_team1_home)
        nhl_elos_over_time.get(team1).append(t1_elo.elo)
        nhl_elos_over_time.get(team2).append(t2_elo.elo)

    x_arr = [list(range(0, len(nhl_elos_over_time.get('BUF')))), list(range(0, len(nhl_elos_over_time.get('PHI'))))]
    y_arr = [nhl_elos_over_time.get('BUF'), nhl_elos_over_time.get('PHI')]
    colors = ["#002D80", "#F74902"]
    plot_elos(x_arr, y_arr, colors)

    # if team != None:
    #     return {
    #         'elo_over_time': nhl_elos_over_time.get(team),
    #         'current_elo' : nhl_elos.get(team).elo
    #     }
    # else:
    #     return {
    #     'elo_over_time': nhl_elos_over_time
    # }


    # for key, value in nhl_elos.items():
    #     print(key + ' = ' + str(value.elo))
    #
    # nyr = nhl_elos.get('NYR')
    # buf = nhl_elos.get('BUF')
    #
    # win_prob = nyr.win_probs(buf, is_home=True)
    # spread = nyr.point_spread(buf, is_home=True)
    # print('win prob = ' + str(win_prob))
    # print('spread  = ' + str(spread))


def plot_elos(x_obj, y_obj, colors):
    for x, y, c in zip(x_obj, y_obj, colors):
        plt.plot(x, y, color=c)

    x = list(range(0,len(x_obj[0])))
    y = [1500] * len(x_obj[0])
    plt.plot(x, y, label='threshold', color="black")

    plt.xlabel('Game Number')
    plt.ylabel('Elo Rating')
    plt.title('Elo Over Time')
    plt.show()


if __name__ == '__main__':
    #save_nfl_data_for_elo()
    r = get_nhl_elo('BUF')
    print(str(r))
