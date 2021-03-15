import pandas as pd
import backend.helper as help


def get_league_stats(season):
    data = help.get_nfl_data(season)
    data = filter_df(data)
    data = data.groupby(['posteam'], as_index=False).agg({'epa': 'mean', 'cpoe': 'mean'})
    data = data.sort_values('epa', ascending=False)
    epa = {
        'teams': data['posteam'].tolist(),
        'epa': data['epa'].tolist()
    }
    data = data.sort_values('cpoe', ascending=False)
    cpoe = {
        'teams': data['posteam'].tolist(),
        'cpoe': data['cpoe'].tolist()
    }

    return {
        'season': season,
        'epa': epa,
        'cpoe': cpoe,
        'colors': help.get_nfl_colors()
    }




#return rgular season data only and remove non important plays
def filter_df(df):
    #regular season data only
    df = df.loc[df.season_type=='REG']
    #remove plays like kickoffs, fgs, kneel downs
    df = df.loc[(df.play_type.isin(['no_play','pass','run'])) & (df.epa.isna()==False)]
    #reset index
    df.reset_index(drop=True, inplace=True)
    return df


# if __name__ == '__main__':
#     r = get_league_stats(2020)
#     print(str(r))
