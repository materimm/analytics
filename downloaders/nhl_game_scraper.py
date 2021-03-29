#####################################################################################
#####           Evolving-Hockey Scraper but in Python by @moman939             ######
# https://github.com/evolvingwild/evolving-hockey/blob/master/EH_scrape_functions.R #
#####################################################################################


## --------------- ##
##   Source URLs   ##
## --------------- ##

#####################

## NHL HTLM Reports:
# events source:        http://www.nhl.com/scores/htmlreports/20182019/PL020001.HTM
# rosters source:       http://www.nhl.com/scores/htmlreports/20182019/RO020001.HTM
# shifts source (home): http://www.nhl.com/scores/htmlreports/20182019/TH020001.HTM
# shifts source (away): http://www.nhl.com/scores/htmlreports/20182019/TV020001.HTM
# game summary:         http://www.nhl.com/scores/htmlreports/20182019/GS020001.HTM
# event summary:        http://www.nhl.com/scores/htmlreports/20182019/ES020001.HTM

## NHL API:
# events source:   https://statsapi.web.nhl.com/api/v1/game/2018020001/feed/live?site=en_nhl
# shifts source:   http://www.nhl.com/stats/rest/shiftcharts?cayenneExp=gameId=2018020001       *** OLD ***
# shifts source:   https://api.nhle.com/stats/rest/en/shiftcharts?cayenneExp=gameId=2018020001  *** NEW, not implemented yet ***
# shifts charts:   http://www.nhl.com/stats/shiftcharts?id=2018020001  *** (for viewing)
# schedule source: https://statsapi.web.nhl.com/api/v1/schedule?startDate=2018-10-03&endDate=2018-10-03
# roster source:   https://statsapi.web.nhl.com/api/v1/game/2018020001/boxscore
# player bios:     https://api.nhle.com/stats/rest/en/skater/bios?isAggregate=false&isGame=false&start=0&limit=50&factCayenneExp=gamesPlayed%3E=1
#                  &cayenneExp=gameTypeId=2%20and%20seasonId%3C=20182019%20and%20seasonId%3E=20182019

## ESPN links:
# ESPN game IDs source: http://www.espn.com/nhl/scoreboard?date=20181003
# ESPN XML source:      http://www.espn.com/nhl/gamecast/data/masterFeed?lang=en&isAll=true&rand=0&gameId=401044320
# ESPN events check:    http://www.espn.com/nhl/playbyplay/_/gameId/401044320


## ------------------ ##
##      Imports       ##
## ------------------ ##

import pandas as pd
from datetime import date, datetime
import urllib.request
import json
from bs4 import BeautifulSoup
import re

## ------------------ ##
##   Create Objects   ##
## ------------------ ##

## Dead NHL games (html source)
dead_games = ["2007020011", "2007021178", "2008020259", "2008020409", "2008021077",
    "2008030311", "2009020081", "2009020658", "2009020885", "2010020124", "2019030016"]    ## too many shift errors to fix

## Create Team IDs (to use for API team triCodes)
team_ids = list(range(1,31))
team_ids.append(52)
team_ids.append(53)
team_ids.append(54)
Team_ID = pd.DataFrame()
Team_ID['Team'] = ["N.J", "NYI", "NYR", "PHI", "PIT", "BOS", "BUF", "MTL",
    "OTT", "TOR", "ATL", "CAR", "FLA", "T.B", "WSH", "CHI", "DET", "NSH", "STL",
    "CGY", "COL", "EDM", "VAN", "ANA", "DAL", "L.A", "ARI", "S.J", "CBJ", "MIN",
    "WPG", "ARI", "VGK"]
Team_ID['ID'] = team_ids

## For identifying event_team in HTM events
Team_ID_vec = ["ANA", "ARI", "BOS", "BUF", "CAR", "CBJ", "CGY", "CHI", "COL", "DAL", "DET", "EDM", "FLA", "L.A", "MIN",
  "MTL", "N.J", "NSH", "NYI", "NYR", "OTT", "PHI", "PIT", "S.J", "STL", "T.B", "TOR", "VAN", "WPG", "WSH",
  "PHX", "ATL", "VGK", "L.V"]

full_team_names = pd.DataFrame()
full_team_names['fullTeam'] = ["ANAHEIM DUCKS", "ARIZONA COYOTES",
    "ATLANTA THRASHERS", "BOSTON BRUINS", "BUFFALO SABRES", "CALGARY FLAMES",
    "CAROLINA HURRICANES", "CHICAGO BLACKHAWKS", "COLORADO AVALANCHE",
    "COLUMBUS BLUE JACKETS", "DALLAS STARS", "DETROIT RED WINGS",
    "EDMONTON OILERS", "FLORIDA PANTHERS", "LOS ANGELES KINGS",
    "MINNESOTA WILD", "MONTREAL CANADIENS", "CANADIENS MONTREAL",
    "NASHVILLE PREDATORS", "NEW JERSEY DEVILS", "NEW YORK ISLANDERS",
    "NEW YORK RANGERS", "OTTAWA SENATORS", "PHILADELPHIA FLYERS",
    "PHOENIX COYOTES", "PITTSBURGH PENGUINS", "SAN JOSE SHARKS",
    "ST. LOUIS BLUES", "TAMPA BAY LIGHTNING", "TORONTO MAPLE LEAFS",
    "VANCOUVER CANUCKS", "VEGAS GOLDEN KNIGHTS", "WASHINGTON CAPITALS",
    "WINNIPEG JETS"]
full_team_names['Team'] = ["ANA", "ARI", "ATL", "BOS", "BUF", "CGY", "CAR",
            "CHI", "COL", "CBJ", "DAL", "DET", "EDM", "FLA", "L.A", "MIN",
            "MTL", "MTL", "NSH", "N.J", "NYI", "NYR", "OTT", "PHI", "ARI",
            "PIT", "S.J", "STL", "T.B", "TOR", "VAN", "VGK", "WSH", "WPG"]
full_team_names['partTeam'] = ["DUCKS", "COYOTES", "THRASHERS", "BRUINS",
            "SABRES", "FLAMES", "HURRICANES", "BLACKHAWKS", "AVALANCHE",
            "BLUE JACKETS", "STARS", "RED WINGS", "OILERS", "PANTHERS", "KINGS",
            "WILD", "CANADIENS", "MONTREAL", "PREDATORS", "DEVILS", "ISLANDERS",
            "RANGERS", "SENATORS", "FLYERS", "COYOTES", "PENGUINS", "SHARKS",
            "BLUES", "LIGHTNING", "MAPLE LEAFS", "CANUCKS", "GOLDEN KNIGHTS",
            "CAPITALS", "JETS"]

## ESPN's team IDs & event type codes
ESPN_team_IDs = pd.DataFrame()
ESPN_team_IDs['team_ID'] = [25, 24, 1, 2, 7, 29, 3, 4, 17, 9, 5, 6, 26, 8, 30,
                10, 11, 27, 12, 13, 14, 15, 16, 18, 19, 20, 21, 22, 37, 28, 23]
ESPN_team_IDs['Team'] = ["ANA", "ARI", "BOS", "BUF", "CAR", "CBJ", "CGY", "CHI",
                "COL", "DAL", "DET", "EDM", "FLA", "L.A", "MIN", "MTL", "N.J",
                "NSH", "NYI", "NYR", "OTT", "PHI", "PIT", "S.J", "STL", "T.B",
                "TOR", "VAN", "VGK", "WPG", "WSH"]

ESPN_codes = pd.DataFrame()
ESPN_codes['event'] = ["FAC", "HIT", "GvTk", "GOAL", "SHOT", "MISS", "BLOCK",
                "PENL","STOP", "PRDY", "PSTR", "PEND", "PERD", "SOC", "GEND",
                "SOut","error", "TAKE", "GIVE", "early intermission", "nothing",
                "nothing"]
ESPN_codes['code'] = ['502', '503', '504', '505', '506', '507', '508', '509',
                '516', '517', '518', '519', '520', '521', '522', '0', '9999',
                '1401', '1402', '-2147483648', '1', '5']

## Other objects
shot_events = ["SHOT", "GOAL"]
fenwick_events = ["SHOT", "GOAL", "MISS"]
corsi_events = ["SHOT", "GOAL", "MISS", "BLOCK"]
strength_states = ["3v3", "5v5", "4v4", "5v4", "4v5", "5v3", "3v5", "4v3",
    "3v4", "5vE", "Ev5", "4vE", "Ev4", "3vE", "Ev3"]
even_strength = ["5v5", "4v4", "3v3"]
pp_strength = ["5v4", "4v5", "5v3", "3v5", "4v3", "3v4"]
empty_net = ["5vE", "Ev5", "4vE", "Ev4", "3vE", "Ev3"]


## Functions
def na_if_null(x): #?????
    return None if x is None else x


## --------------------- ##
##   Scraper Functions   ##
## --------------------- ##

## --------------- ##
##   Scrape Data   ##
## --------------- ##

def scrape_schedule(start_date=date.today().strftime('%Y-%m-%d'), end_date=date.today().strftime('%Y-%m-%d'), print_sched=True):
    ## getURL for schedule data
    url_schedule = None
    try_count = 3

    while (not isinstance(url_schedule, str)) and try_count > 0:
        try:
            try_count = try_count - 1
            url = "https://statsapi.web.nhl.com/api/v1/schedule?startDate={}&endDate={}"
            url = url.format(start_date, end_date)
            url_schedule = urllib.request.urlopen(url).read()

            # Decode UTF-8 bytes to Unicode, and convert single quotes
            # to double quotes to make it valid JSON
            my_json = url_schedule.decode('utf8').replace("'", '"')
            try_count = try_count - 1
        except Exception as e:
            print(e)
            print("ERROR: Schedule download for " + url + " failed.")



    ## Parse JSON
    if isinstance(my_json, str):
        schedule_list = json.loads(url_schedule)

    ## Return from function if scrape returned no data
    if len(schedule_list.get('dates')) == 0:
        print("ERROR: NHL schedule API returned no data.")

        ## Return empty data frame in same format if error occurred
        return pd.DataFrame(columns=['game_id', 'game_date', 'season',
            'session', 'game_status', 'away_team', 'home_team',
            'game_venue', 'game_datetime', 'EST_time_convert', 'EST_date'])

    #print(str(schedule_list.get('dates')))
    ## Bind games from schedule list
    bind_schedule = pd.DataFrame()
    for date in schedule_list.get('dates'):
        for game in date.get('games'):
            game_df = pd.DataFrame(columns=['game_id', 'game_date',
                'season', 'session', 'game_status', 'away_team_id',
                'home_team_id', 'game_venue', 'game_datetime'])

            row = [game.get('gamePk'), game.get('gameDate'),
                game.get('season'), game.get('gameType'),
                game.get('game_status'),
                game.get('teams').get('away').get('team').get('id'),
                game.get('teams').get('home').get('team').get('id'),
                game.get('venue').get('name'), game.get('gameDate')]
            series_row = pd.Series(row, index=game_df.columns)
            game_df = game_df.append(series_row, ignore_index=True)
            bind_schedule = bind_schedule.append(game_df)

    ## Modify bound schedule data
    schedule_current = bind_schedule.loc[(bind_schedule.session == "R") | (bind_schedule.session == "P")] #only include regular seasons and playoff games
    #get team abbrevs from ids
    schedule_current['home_team_id'] = schedule_current['home_team_id'].apply(lambda x: Team_ID.at[Team_ID[Team_ID['ID'] == x].index[0], 'Team'])
    schedule_current['away_team_id'] = schedule_current['away_team_id'].apply(lambda x: Team_ID.at[Team_ID[Team_ID['ID'] == x].index[0], 'Team'])
    schedule_current = schedule_current.rename(columns={'away_team_id': 'away_team', 'home_team_id': 'home_team'})
    #TODO
    #make col for EST_time_convert, EST_date, game_date
    schedule_current = schedule_current.sort_values('game_id')

    if print_sched == True:
        print(schedule_current.head(20))


## Scrape Events (HTM)
def scrape_events_HTM(game_id_fun, season_id_fun, attempts=3):
    url_events_HTM = None
    try_count = attempts

    while (not isinstance(url_events_HTM, str)) and try_count > 0:
        try:
            try_count = try_count - 1
            url = "http://www.nhl.com/scores/htmlreports/{}/PL0{}.HTM"
            url = url.format(season_id_fun, game_id_fun) #TODO substr game_id_fun 6-10
            url_events_HTM = urllib.request.urlopen(url).read()
            # Decode UTF-8 bytes to Unicode, and convert single quotes
            # to double quotes to make it valid JSON
            url_events_HTM = url_events_HTM.decode('utf8').replace("'", '"')
        except Exception as e:
            print(e)
            print("ERROR: HTM event download for " + url + " failed.")

    soup = BeautifulSoup(url_events_HTM, 'html.parser')
    events_body_text = soup.find_all(class_ ='bborder') ##evolvingwild return this
    ## TODO ----------
    # add in home and away teams names
    # add in score at time of event
    events_df = pd.DataFrame(columns=['id', 'period', 'strength', 'time_elapsed', 'game_time', 'event', 'description',
        'a_p1_number', 'a_p1_name', 'a_p1_position', 'a_p2_number', 'a_p2_name', 'a_p2_position',
        'a_p3_number', 'a_p3_name', 'a_p3_position', 'a_p4_number', 'a_p4_name', 'a_p4_position',
        'a_p5_number', 'a_p5_name', 'a_p5_position', 'a_p6_number', 'a_p6_name', 'a_p6_position',
        'h_p1_number', 'h_p1_name', 'h_p1_position', 'h_p2_number', 'h_p2_name', 'h_p2_position',
        'h_p3_number', 'h_p3_name', 'h_p3_position', 'h_p4_number', 'h_p4_name', 'h_p4_position',
        'h_p5_number', 'h_p5_name', 'h_p5_position', 'h_p6_number', 'h_p6_name', 'h_p6_position'])

    skip = False
    skip_count = 0
    skip_amount = 8
    col_num = 1
    x=0
    row = []
    for event in events_body_text:
        x = x+1
        if event.text == '#':
            skip = True
            skip_amount = 8

        if skip:
            skip_count = skip_count + 1
            if skip_count == skip_amount:
                row = []
                skip_count = 0
                skip = False
            continue

        if col_num == 1:
            #play number
            row.append(event.text)
        elif col_num == 2:
            #period
            row.append(event.text)
        elif col_num == 3:
            #strength
            row.append(event.text)
        elif col_num == 4:
            #time
            #TODO split the elapsed and game time
            row.append(event.text)
            row.append(event.text)
            #print(str(time))
            #time_elapsed, game_time = time.split('</br>')
        elif col_num == 5:
            event_type = event.text
            row.append(event_type)
            if (event_type == 'PGSTR') | (event_type == 'PGEND') | (event_type == 'ANTHEM') | (event_type == 'PSTR'):
                skip = True
                skip_amount = 3
                col_num = 1
                continue
        elif col_num == 6:
            #event description
            #TODO split description into more details
            row.append(event.text)
        elif col_num == 7:
            #away_team_on_ice
            fonts = event.find_all('font')
            away_players = []
            for f in fonts:
                title = f.get('title', None)
                position, name = title.split('-')
                number = f.text
                row.append(number)
                row.append(name)
                row.append(position)
            if len(fonts) < 6:
                for n in list(range(0, 6-len(fonts))):
                    row.append('NA')
                    row.append('NA')
                    row.append('NA')
        elif col_num == 8:
            #home_team_on_ice
            fonts = event.find_all('font')
            home_players = []
            for f in fonts:
                title = f.get('title', None)
                position, name = None, None
                if title is not None:
                    position, name = title.split('-')
                player_number = f.text
                row.append(number)
                row.append(name)
                row.append(position)
            if len(fonts) < 6:
                for n in list(range(0, 6-len(fonts))):
                    row.append('NA')
                    row.append('NA')
                    row.append('NA')
            series_row = pd.Series(row, index=events_df.columns)
            events_df = events_df.append(series_row, ignore_index=True)
            row = []
            col_num = 0

        col_num = col_num + 1

    return events_df


## Scrape Events (API)
def scrape_events_API(game_id_fun, attempts=3):
    url_events_api = None
    try_count = attempts

    while (not isinstance(url_events_api, str)) and try_count > 0:
        try:
            try_count = try_count - 1
            url = "https://statsapi.web.nhl.com/api/v1/game/{}/feed/live?site=en_nhl"
            url = url.format(game_id_fun)
            url_events_api = urllib.request.urlopen(url).read()
            # Decode UTF-8 bytes to Unicode, and convert single quotes
            # to double quotes to make it valid JSON
            url_events_api = url_events_api.decode('utf8')
        except Exception as e:
            print(e)
            print("ERROR: API event download for " + url + " failed.")

    events_json = json.loads(url_events_api)
    #TODO format
    return events_json


## Scrape Events (ESPN)
def scrape_events_ESPN(date, attempts=3):#game_id_fun, season_id_fun, game_info_data, attempts=3):
    url_espn_page = None
    try_count = attempts

    while (not isinstance(url_espn_page, str)) and try_count > 0:
        try:
            try_count = try_count - 1
            url = "http://www.espn.com/nhl/scoreboard?date={}"
            url = url.format(date)
            url_espn_page = urllib.request.urlopen(url).read()
            # Decode UTF-8 bytes to Unicode, and convert single quotes
            # to double quotes to make it valid JSON
            url_espn_page = url_espn_page.decode('utf8')
        except Exception as e:
            print(e)
            print("ERROR: ESPN event download for " + url + " failed.")

    ## Get game ids
    espn_game_ids = list(map(lambda x: x.removeprefix('boxscore/_/gameId/'), re.findall("boxscore/_/gameId/[0-9]+", url_espn_page)))

    ## Get team ids
    soup = BeautifulSoup(url_espn_page, 'html.parser')
    espn_container = soup.find("div", {"id": "fittPageContainer"})
    f = open("test.txt", "w")
    f.write(str(espn_container))
    f.close()
    espn_teams = list(map(lambda x: x.removeprefix('/nhl/team/_/name/').split('/')[1].replace('-', ' ').upper(), list(set(re.findall("/nhl/team/_/name/[a-z]+/[a-z-]+", str(espn_container))))))

    #part_team_names TODO


    if len(espn_game_ids) > 0:
        espn_games_df = pd.DataFrame()

        #### TODO ###

## Scrape Shifts (HTM)
def scrape_shifts(game_id_fun, season_id_fun, attempts=3):
    url_home_shifts = None
    try_count = attempts

    while (not isinstance(url_home_shifts, str)) and try_count > 0:
        try:
            try_count = try_count - 1
            url = "http://www.nhl.com/scores/htmlreports/{}/TH0{}.HTM"
            url = url.format(season_id_fun, game_id_fun[6:10])
            url_home_shifts = urllib.request.urlopen(url).read()
            # Decode UTF-8 bytes to Unicode
            url_home_shifts = url_home_shifts.decode('utf8')
        except Exception as e:
            print(e)
            print("ERROR: Home shift download for " + url + " failed.")

    url_away_shifts = None
    try_count = attempts

    while (not isinstance(url_away_shifts, str)) and try_count > 0:
        try:
            try_count = try_count - 1
            url = "http://www.nhl.com/scores/htmlreports/{}/TV0{}.HTM"
            url = url.format(season_id_fun, game_id_fun)
            url_away_shifts = urllib.request.urlopen(url).read()
            # Decode UTF-8 bytes to Unicode
            url_away_shifts = url_home_shifts.decode('utf8')
        except Exception as e:
            print(e)
            print("ERROR: Away shift download for " + url + " failed.")

    ## Pull out scraped shifts data
    home_soup = BeautifulSoup(url_home_shifts, 'html.parser')
    away_soup = BeautifulSoup(url_away_shifts, 'html.parser')
    home_shifts_titles = home_soup.find( class_ = '.border')
    away_shifts_titles = away_soup.find( class_ = '.border')
    home_shifts_text = soup.find( class_ = '.bborder')
    away_shifts_text = soup.find( class_ = '.bborder')

    return {
        'home_shifts_titles': home_shifts_titles,
        'away_shifts_titles': away_shifts_titles,
        'home_shifts_text': home_shifts_text,
        'away_shifts_text': away_shifts_text
    }


## Scrape Shifts (API)
def scrape_shifts_API(game_id_fun, attempts=3):
    url_shifts = None
    try_count = attempts

    while (not isinstance(url_shifts, str)) and try_count > 0:
        try:
            try_count = try_count - 1
            url = "http://www.nhl.com/stats/rest/shiftcharts?cayenneExp=gameId={}"
            url = url.format(game_id_fun)
            url_shifts = urllib.request.urlopen(url).read()
            # Decode UTF-8 bytes to Unicode
            url_shifts = url_shifts.decode('utf8')
        except Exception as e:
            print(e)
            print("ERROR: Shift download for " + url + " failed.")

    if isinstance(url_shifts, str):
        shifts_list = json.loads(url_shifts)
    else:
        shifts_list = {}

    return shifts_list


## Scrape Rosters
def scrape_rosters(game_id_fun, season_id_fun, attempts=3):
    url_rosters = None
    try_count = attempts

    while (not isinstance(url_rosters, str)) and try_count > 0:
        try:
            try_count = try_count - 1
            url = "http://www.nhl.com/scores/htmlreports/{}/RO0{}.HTM"
            url = url.format(season_id_fun, game_id_fun)
            url_rosters = urllib.request.urlopen(url).read()
            # Decode UTF-8 bytes to Unicode
            url_rosters = url_rosters.decode('utf8')
        except Exception as e:
            print(e)
            print("ERROR: Roster download for " + url + " failed.")

    ## Pull out roster data
    soup = BeautifulSoup(url_rosters, 'html.parser')
    rosters_text = [x.text for x in soup.find_all('td')]
    #TODO maybe return as json?
    return rosters_text



## Scrape Rosters API
#def scrape_rosters_API(games_data, cores):
    #TODO


## Scrape Event Summary
def scrape_event_summary(game_id_fun, season_id_fun, attempts=3):
    url_event_summary = None
    try_count = attempts

    while (not isinstance(url_event_summary, str)) and try_count > 0:
        try:
            try_count = try_count - 1
            url = "http://www.nhl.com/scores/htmlreports/{}/ES0{}.HTM"
            url = url.format(season_id_fun, game_id_fun[6:10])
            url_rosters = urllib.request.urlopen(url).read()
            # Decode UTF-8 bytes to Unicode
            url_event_summary = url_event_summary.decode('utf8')
        except Exception as e:
            print(e)
            print("ERROR: Event download for " + url + " failed.")

    ## Pull out roster data
    soup = BeautifulSoup(url_event_summary, 'html.parser')
    event_summary_text = [x.text for x in soup.find_all('td')]
    return event_summary_text



## ---------------------------- ##
##   Create Basic Data Frames   ##
## ---------------------------- ##

## Create Game Information data.frame
def game_info(game_id_fun, season_id_fun, events_data, roster_data):

    ## Find coaches
    coach_index = 1 #Todo

#scrape_schedule('2018-10-03', '2018-10-03')
#scrape_events_HTM(20001, 20182019)
#scrape_events_api(2018020001)
#scrape_events_ESPN(20181003)
scrape_rosters(20001,20182019)


## --------------------- ##
##   Compile Functions   ##
## --------------------- ##

## Run All Functions to Scrape Game Data
def scrape_game(game_id, season_id, scrape_type_, live_scrape_):
    ## --------------- ##
    ##   Scrape Data   ##
    ## --------------- ##

    ## Scrape events - HTM
    events_HTM = scrape_events_HTM(game_id_fun=game_id, season_id_fun=season_id, attempts=3)

    ## Scrape shifts - HTM
    shifts_data_scrape = scrape_shifts(game_id_fun=game_id, season_id_fun=season_id, attempts=3)

    ## Scrape events - API
    if scrape_type_ == "full":
        events_api = scrape_events_API(game_id_fun=game_id, attempts=3)

    ## Scrape rosters
    rosters_HTM = scrape_rosters(game_id_fun=game_id, season_id_fun=season_id, attempts=3)

    ## Scrape Event Summary
    if scrape_type_ in ['full', 'event_summary']:
        event_summary_HTM = scrape_event_summary(game_id_fun=game_id, season_id_fun=season_id, attempts=3)

    ## ---------------------------- ##
    ##   Create Basic Data Frames   ##
    ## ---------------------------- ##

    ## Create game information data frame
    game_info_df = game_info(game_id_fun=game_id, season_id_fun=season_id, events_data=events_HTM, roster_data=rosters_HTM)

    ## Scrape API for shits data if HTM source fails
    if (len(shifts_data_scrape['home_shifts_text']) == 0) or (len(shifts_data_scrape['away_shifts_text']) == 0):
        shifts_data_scrape = shifts_process_API(game_id_fun=game_id, game_info_data=game_info_df)
        HTM_shifts_okay = False
    else:
        HTM_shifts_okay = True

    ## Create rosters data frame
    rosters_list = roster_info(game_id_fun=game_id, season_id_fun=season_id, roster_data=rosters_HTM, game_info_data=game_info_df, shifts_list=shifts_data_scrape)

    ## Create event summary data frame
    if scrape_type_ in ['full', 'event_summary']:
        event_summary_df = event_summary(game_id_fun=game_id, season_id_fun=season_id, event_summary_data=event_summary_HTM,
                                         roster_data=rosters_list['roster_df'], game_info_data=game_info_df)

    if scrape_type_ == 'full':
        ## ----------------------- ##
        ##   Prepare Events Data   ##
        ## ----------------------- ##

        ## Prepare Events Data (HTM)
        prepare_events_HTM_df = prepare_events_HTM(game_id_fun=game_id, season_id_fun=season_id, events_data=events_HTM, game_info_data=game_info_df)

        ## Prepare Events Data (API)
        if not (events_api.get('liveData').get('plays').get('all').get('allPlays').get('coordinates') == None):
            if len(events_api.get('liveData').get('plays').get('all').get('allPlays').get('coordinates') > 0): #maybe dataframe get len(df.columns)
                prepare_events_api_df = prepare_events_API(game_id_fun=game_id, events_data=events_HTM, game_info_data=game_info_df)
                coord_type = "NHL_API"
            else:
                prepare_events_api_df = None
        else:
            prepare_events_api_df = None

        ## ----------------------- ##
        ##   Prepare Shifts Data   ##
        ## ----------------------- ##

        ## Parse Shifts & Period Sums Data
        if HTM_shifts_okay:
            shifts_parsed_list = shifts_parse(game_id_fun=game_id, season_id_fun=season_id, shifts_list=shifts_data_scrape,
                                            roster_data=rosters_list.get('roster_df'), game_info_data=game_info_df, fix_shifts=(not live_scrape_))
        else:
            shifts_parsed_list = shifts_parse_API(game_id_fun=game_id, shifts_list=shifts_data_scrape,
                                            roster_data=rosters_list.get('roster_df'), game_info_data=game_info_df)

        ## Fix Goalie Shifts & Finalize
        shifts_final_df = shifts_finalize(game_id_fun=game_id, shifts_parse_data=shifts_parsed_list.get('shifts_parse'),
                                        events_data_HTM=prepare_events_HTM_df, game_info_data=game_info_df, fix_shifts=(not live_scrape_))

        ## Create ON/OFF Event Types
        shifts_event_types_df = shifts_create_events(shifts_final_data=shifts_final_df)

        ## -------------------- ##
        ##   Join Coordinates   ##
        ## -------------------- ##

        if not (prepare_events_api_df == None): ## NHL API Source
            events_full_df = join_coordinates_API(events_data_API=prepare_events_API_df, events_data_HTM=prepare_events_HTM_df)
        else: ##ESPN XML Source
            prepare_events_ESPN_df = scrape_events_ESPN(game_id_fun=game_id, season_id_fun=season_id, game_info_data=game_info_df, attempts=3)

        if isinstance(prepare_events_ESPN_df, pd.DataFrame):
            if len(prepare_events_ESPN_df.index) > 0:
                events_full_df = join_coordinates_ESPN(season_id_fun=season_id, events_data_ESPN=prepare_events_ESPN_df,
                                                    events_data_HTM=prepare_events_HTM_df, roster_data=rosters_list['roster_df'],
                                                    game_info_data = game_info_df)
                coord_type = "ESPN"
            else: ## COORDINATES NOT AVAILABLE
                events_full_df = prepare_events_HTM_df
                events_full_df['coords_x'] = events_full_df['coords_x'].apply(lambda x: "NA")
                events_full_df['coords_y'] = events_full_df['coords_y'].apply(lambda x: "NA")
                events_full_df['event_description_alt'] = events_full_df['event_description_alt'].apply(lambda x: "NA")
                coord_type = "NO COORDS"
        else: ## COORDINATES NOT AVAILABLE
            events_full_df = prepare_events_HTM_df
            events_full_df['coords_x'] = events_full_df['coords_x'].apply(lambda x: "NA")
            events_full_df['coords_y'] = events_full_df['coords_y'].apply(lambda x: "NA")
            events_full_df['event_description_alt'] = events_full_df['event_description_alt'].apply(lambda x: "NA")
            coord_type = "NO COORDS"

        ## -------------------- ##
        ##   Combine All Data   ##
        ## -------------------- ##

        ## Combine / Process Shifts and Events Data
        pbp_combine_list = pbp_combine(events_data=events_full_df, shifts_data=shifts_event_types_df,
                                    roster_data=rosters_list['roster_df'], game_info_data = game_info_df)

        ## Finalize PBP Data
        pbp_finalize_list = pbp_finalize(pbp_data=pbp_combine_list['pbp_final'], on_data_home=pbp_combine_list['is_on_df_home'],
                                        on_data_away=pbp_combine_list['is_on_df_away'], roster_data=rosters_list['roster_df'],
                                        game_info_data=game_info_df, live_scrape=live_scrape_)

        ## Modify game_info_df to return
        game_info_df_return = game_info_df
        #TODO match mutate for coord_source, period count, etc. (line 3580)

        ## Ensure database friendly column names
        #TODO

        ## Return all data as a list
        #TODO

        #...

        ## Return data
        return return_list
