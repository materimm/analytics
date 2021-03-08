import pandas as pd
from pathlib import Path
import os
import backend.helper as help


base_dir = str(Path(os.getcwd())) #.parents[0])

# @param team - 3 letter code for team. aka BUF for the Buffalo Sabres
def get_team_stats(team):
    data_5v5 = help.upload_data(base_dir + r'\NHLData\Natural-Stat-Trick\all_teams_5v5.csv')
    data_pp = help.upload_data(base_dir + r'\NHLData\Natural-Stat-Trick\all_teams_PP.csv')
    data_pk = help.upload_data(base_dir + r'\NHLData\Natural-Stat-Trick\all_teams_PK.csv')


def get_league_stats(start_season, end_season, filter='all'):
    # game_data = help.upload_data(base_dir + r'\NHLData\moneypuck\games\20-21-games.csv')
    # g5v5 = game_data.loc[game_data.situation=='5on5']
    teams = help.get_teams(filter)
    rolling_xgf = {}
    goal_share = get_goal_share(teams, start_season, end_season, False)
    xgoal_share = get_goal_share(teams, start_season, end_season, True)
    all_dates = []
    for team in teams:
        rolling_xgf[team] = get_rolling_xGF(team, start_season, end_season)
        all_dates = all_dates + rolling_xgf[team].get('dates')
    all_dates = list(set(all_dates))
    all_dates.sort()
    rolling_xgf['all_dates'] = all_dates

    return {
        'rolling_xgf': rolling_xgf,
        'goal_share': goal_share,
        'xgoal_share': xgoal_share,
        'colors': help.get_all_nhl_colors(),
        'logos': help.get_all_nhl_logos(),
        'teams': teams
    }


def get_rolling_xGF(team, start_season, end_season):
    game_data = help.upload_data(base_dir + '\\NHLData\\moneypuck\\games\\' + team + '.csv')
    game_data = game_data.loc[(game_data.season >= start_season)  & (game_data.season <= end_season)]
    game_data = game_data.loc[game_data.situation=='5on5']
    dates = []
    xGFs = []
    for index, row in game_data.iterrows():
        r = row.to_dict()
        date = str(r.get('gameDate'))
        dates.append(date[4:6] + "/" + date[-2:] + "/" + date[:4])
        xGFs.append(r.get('xGoalsPercentage') * 100)
    xGFs = help.get_5_game_rolling_average(xGFs)
    return {
        'xgf': xGFs,
        'dates': dates
    }


def get_goal_share(teams, start_season, end_season, is_expected):
    gf_label = 'xGoalsFor' if is_expected else 'goalsFor'
    ga_label = 'xGoalsAgainst' if is_expected else 'goalsAgainst'
    seasons = list(range(start_season, end_season + 1))
    data = pd.DataFrame()
    for season in seasons:
        data = data.append(help.upload_data(base_dir + r'\NHLData\moneypuck\overall\teams-' + str(season) + '.csv'))

    data = data.loc[(data.season >= start_season)  & (data.season <= end_season)]
    data = data.loc[data.situation=='5on5']
    data = data.groupby(['team'], as_index=False).agg({gf_label:'mean', ga_label:'mean', 'iceTime': 'sum'})
    goal_share = {}
    for team in teams:
        team_label = team
        team = team[:1] + "." + team[-1:] if len(team) == 2 else team
        df = data.loc[data.team==team]
        for index, row in df.iterrows():
            r = row.to_dict()
            gf = r.get(gf_label)
            ga = r.get(ga_label)
            toi = r.get('iceTime') / 60 # convert from seconds to minutes
            goal_share[team_label] = {
                'gf60': help.get_per_60(gf, toi),
                'ga60': help.get_per_60(ga, toi)
            }

    return goal_share


if __name__ == '__main__':
    r = get_league_stats(2019, 2020)
    print(str(r))
