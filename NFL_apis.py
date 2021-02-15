import pandas as pd



pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 300)


def get_nfl_data(season):
    if season in list(range(1999, 2021)):
        filepath = r"C:\Users\MoreyMATERISE\Documents\analytics_dev\analytics\NFLData\play_by_play_" + str(season) + ".csv.gz"
        return pd.read_csv(filepath, compression='gzip', low_memory=False)
    else:
        print(str(season) + " not in data")

def get_EPA(season):
    data = get_nfl_data(season)

    #regular season data only
    data = data.loc[data.season_type=='REG']

    qbs = data.groupby(['passer','posteam'], as_index=False).agg({'epa':'mean',
                                                              'cpoe':'mean',
                                                              'play_id':'count'})
    #Filter to players with 200 or more dropbacks
    qbs = qbs.loc[qbs.play_id>199]

    #Sort in descending order by EPA
    qbs.sort_values('epa', ascending=False, inplace=True)

    #Round to two decimal places where appropriate
    qbs = qbs.round(2)

    #Rename columns
    qbs.columns = ['Player','Team','EPA','CPOE','Dropbacks']
    qbs.reset_index(drop=True, inplace=True)

    qb_list = []
    for row in qbs.iterrows():
        index, player_obj = row
        qb_list.append(player_obj.to_dict())

    #print(str(qb_list))

    return qb_list



if __name__ == '__main__':
    season = 2020
    get_EPA(season)
