import pandas as pd

def download_play_by_play():
    YEARS = list(range(1999, 2021)) #note end is not inclusive

    data = pd.DataFrame()

    for i in YEARS:
        data = pd.read_csv('https://github.com/guga31bb/nflfastR-data/blob/master/data/' \
                             'play_by_play_' + str(i) + '.csv.gz?raw=True',
                             compression='gzip', low_memory=False)
        #redundant columns
        data.drop(['passer_player_name', 'passer_player_id',
                   'rusher_player_name', 'rusher_player_id',
                   'receiver_player_name', 'receiver_player_id'],
                  axis=1, inplace=True)

        #fix play types for scrambles
        data.play_type.loc[data['pass']==1] = 'pass'
        data.play_type.loc[data.rush==1] = 'run'

        data.reset_index(drop=True, inplace=True)

        filepath = r"C:\Users\MoreyMATERISE\Documents\analytics_dev\analytics\NFLData\play_by_play_" + str(i) + ".csv.gz"
        #save data
        data.to_csv(filepath, compression='gzip', index=False)

        print(str(i) + " saved")

def download_nfl_logos():
    urls = pd.read_csv('https://raw.githubusercontent.com/statsbylopez/BlogPosts/master/nfl_teamlogos.csv')

    filepath = r"C:\Users\MoreyMATERISE\Documents\analytics_dev\analytics\NFLData\team_logos.csv"
    #save data
    urls.to_csv(filepath)
    print("Logos saved")


if __name__ == '__main__':
    download_play_by_play()
    download_nfl_logos()
