import pandas as pd
import backend.helper as help

def get_league_stats(season):
    data = help.get_nfl_data(season)
    data = _filter_df(data)
    epa_obj = _get_stat_mean_by_team(data, 'epa')
    cpoe_obj = _get_stat_mean_by_team(data, 'cpoe')
    return {
        'season': season,
        'epa': epa_obj,
        'cpoe': cpoe_obj,
        'colors': help.get_nfl_colors()
    }

def _get_stat_mean_by_team(data, label):
    data = data.groupby(['posteam'], as_index=False).agg({label: 'mean'})
    data = data.sort_values(label, ascending=False)
    return {
        'teams': data['posteam'].tolist(),
        label: data[label].tolist()
    }


def get_team_stats(team, season):
    data = help.get_nfl_data(season)
    data = _filter_df(data)

    game_data = _get_data_per_game(data.copy(), team)

    epa, epa_rank = _get_stat_and_rank(_get_stat_mean_by_team(data, 'epa'), 'epa', team)
    cpoe, cpoe_rank = _get_stat_and_rank(_get_stat_mean_by_team(data, 'cpoe'), 'cpoe', team)

    pass_data = data.copy()
    pass_data = pass_data.loc[pass_data.play_type=='pass']
    pass_epa, pass_epa_rank = _get_stat_and_rank(_get_stat_mean_by_team(pass_data, 'epa'), 'epa', team)

    rush_data = data.copy()
    rush_data = rush_data.loc[rush_data.play_type=='run']
    rush_epa, rush_epa_rank = _get_stat_and_rank(_get_stat_mean_by_team(rush_data, 'epa'), 'epa', team)



    return {
        'name': help.get_full_nhl_team_name(team),
        'logo': help.get_nfl_team_logo(team),
        'season': season,
        'colors': help.get_nfl_colors()[team],
        'game_data': game_data,
        'epa': '%.3f' % epa,
        'epa_rank': epa_rank,
        'cpoe': '%.3f' % cpoe,
        'cpoe_rank': cpoe_rank,
        'pass_epa': '%.3f' % pass_epa,
        'pass_epa_rank': pass_epa_rank,
        'rush_epa': '%.3f' % rush_epa,
        'rush_epa_rank': rush_epa_rank,
    }


def _get_data_per_game(data, team):
    data = data.loc[data.posteam==team]
    pass_data = data.copy()
    pass_data = pass_data.loc[pass_data.play_type=='pass']
    rush_data = data.copy()
    rush_data = rush_data.loc[rush_data.play_type=='run']

    data = data.groupby(['game_date'], as_index=False).agg({'epa': 'mean'})
    pass_data = pass_data.groupby(['game_date'], as_index=False).agg({'epa': 'mean'})
    rush_data = rush_data.groupby(['game_date'], as_index=False).agg({'epa': 'mean'})

    return {
        'dates' : data['game_date'].tolist(),
        'epa': data['epa'].tolist(),
        'pass_epa': pass_data['epa'].tolist(),
        'rush_epa': rush_data['epa'].tolist(),
    }


def _get_stat_and_rank(obj, label, team):
    rank = obj.get('teams').index(team)
    stat = obj.get(label)[rank]
    return stat, rank+1


#return rgular season data only and remove non important plays
def _filter_df(df):
    #regular season data only
    df = df.loc[df.season_type=='REG']
    #remove plays like kickoffs, fgs, kneel downs
    df = df.loc[(df.play_type.isin(['no_play','pass','run'])) & (df.epa.isna()==False)]
    #reset index
    df.reset_index(drop=True, inplace=True)
    return df


# if __name__ == '__main__':
#     r = get_league_stats(2020)
#     r = get_team_stats('BUF', 2020)
#     print(str(r.get('game_data')))
