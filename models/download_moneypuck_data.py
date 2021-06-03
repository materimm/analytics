import requests
from pathlib import Path
import os

teams = ["ANA", "ARI", "BOS", "BUF", "CGY", "CAR", "CHI", "COL", "CBJ", "DAL",
 "DET", "EDM", "FLA", "LA", "MIN", "MTL", "NSH", "NJ", "NYI", "NYR", "OTT",
 "PHI", "PIT", "STL", "SJ", "TB", "TOR", "VAN", "VGK", "WSH", "WPG"]

base_dir = str(Path(os.getcwd()).parents[0])

for team in teams:
    url = 'http://moneypuck.com/moneypuck/playerData/careers/gameByGame/regular/teams/'
    team_url = team
    if len(team) == 2:
        team_url = team[0] + '.' + team[1]
    url = url + team_url + '.csv'
    r = requests.get(url, allow_redirects=True)
    open(base_dir + '/NHLData/moneypuck/games/' + team + '.csv', 'wb').write(r.content)


seasons = list(range(2020, 2021))
data_type = ['skaters', 'goalies', 'lines', 'teams']
url = 'http://moneypuck.com/moneypuck/playerData/seasonSummary/{}/regular/{}.csv'
path = base_dir + '/NHLData/moneypuck/{}/{}-{}-{}.csv'
for data in data_type:
    for s in seasons:
        formatted_url = url.format(s, data)
        r = requests.get(formatted_url, allow_redirects=True)
        formatted_path = path.format(data, s, s+1, data)
        open(formatted_path, 'wb').write(r.content)
