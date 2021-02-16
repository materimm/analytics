import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
import json

def get_shots(url):
    home_shots = 0
    away_shots = 0
    home_roster, home_team_name, away_roster, away_team_name = get_roster(url)

    driver = webdriver.Chrome("./chromedriver")
    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    play_by_play_section = soup.find(class_="Card--PlayByPlay")
    buttons = play_by_play_section.find_all("button")
    num_periods = len(buttons)
    num_periods = 1

    #1st period
    if num_periods >= 1:
        h, a, shot_flow, shot_flow_time, shots_per_60 = get_shots_web_reader(soup, home_roster, away_roster)
        home_shots += h
        away_shots += a
        #print("========================================")

    #2nd period
    if num_periods >= 2:
        button = driver.find_element_by_xpath('//button[text()="2nd"]')
        button.click()
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        #TODO add new returns
        h, a = get_shots_web_reader(soup, home_roster, away_roster)
        home_shots += h
        away_shots += a
        #print("========================================")

    #3rd period
    if num_periods >= 3:
        button = driver.find_element_by_xpath('//button[text()="3rd"]')
        button.click()
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        h, a = get_shots_web_reader(soup, home_roster, away_roster)
        home_shots += h
        away_shots += a
        #print("========================================")

    #OT if needed
    if num_periods >= 4:
        button = driver.find_element_by_xpath('//button[text()="OT"]')
        button.click()
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        h, a = get_shots_web_reader(soup, home_roster, away_roster)
        home_shots += h
        away_shots += a
        #print("========================================")

    driver.quit()

    home_colors, away_colors = get_team_colors(home_team_name, away_team_name)

    obj = {
        "home": {
            "name": home_team_name,
            "shots": home_shots,
            "colors": home_colors
        },
        "away": {
            "name": away_team_name,
            "shots": away_shots,
            "colors": away_colors
        },
        "shot_flow": shot_flow,
        "shot_flow_time": shot_flow_time,
        "shots_per_60" : shots_per_60
    }

    #print(str(obj))
    return obj


def get_shots_web_reader(soup, home_roster, away_roster):
    home_shots = 0
    away_shots = 0
    shot_flow = 0
    shot_flow_list = [0]
    shot_flow_time = [0]
    home_shots_per_60 =[0]
    away_shots_per_60 =[0]
    home_shots_per_60_time =[0]
    away_shots_per_60_time =[0]

    all_plays = soup.find_all(class_="playByPlay__tableRow")
    for play in all_plays:
        play_txt = play.find(class_="playByPlay__text").text
        play_time = play.find(class_="playByPlay__time").text
        time_split = play_time.split(":")
        time_in_seconds = 60 * int(time_split[0]) + int(time_split[1])

        shooter = ""
        if play_txt.startswith('Shot on goal'):
            s = re.search('Shot on goal by (.*) saved by*', play_txt)
            shooter = s.group(1)
        elif play_txt.startswith('Goal scored'):
            s = re.search('Goal scored by (.*) assisted by*', play_txt)
            if s == None: #unassisted
                s = re.search('Goal scored by (.*)$', play_txt)
                shooter = s.group(1)
            else:
                shooter = s.group(1)
        elif play_txt.startswith('Power Play Goal'):
            s = re.search('Power Play Goal Scored  by (.*) assisted by*', play_txt)
            if s == None: #unassisted
                s = re.search('Goal scored by (.*)$', play_txt)
                shooter = s.group(1)
            else:
                shooter = s.group(1)

        if shooter != "":
            if shooter in home_roster:
                home_shots += 1
                shot_flow += 1
                home_shots_per_60.append(round((home_shots*60*60) / time_in_seconds))
                home_shots_per_60_time.append(time_in_seconds)
            elif shooter in away_roster:
                away_shots += 1
                shot_flow -=1
                away_shots_per_60.append(round((away_shots*60*60) / time_in_seconds))
                away_shots_per_60_time.append(time_in_seconds)
            else:
                print("ERROR -- shooter not in either roster----------------------------------")

            shot_flow_list.append(shot_flow)
            shot_flow_time.append(time_in_seconds)

    #get shots per 60 at end of period
    home_shots_per_60.append(round((home_shots*60*60) / (20*60)))
    home_shots_per_60_time.append(20*60)
    away_shots_per_60.append(round((away_shots*60*60) / (20*60)))
    away_shots_per_60_time.append(20*60)

    shots_per_60 = {
        "home_shots_per_60" : home_shots_per_60,
        "home_shots_per_60_time" : home_shots_per_60_time,
        "away_shots_per_60" : away_shots_per_60,
        "away_shots_per_60_time" : away_shots_per_60_time
    }

    return home_shots, away_shots, shot_flow_list, shot_flow_time, shots_per_60


def get_team_colors(home_team_name, away_team_name):
    with open('./static/json/team_abbrevs.json') as teams_file:
        teams = json.load(teams_file)
    with open('./static/json/nhl_team_colors.json') as colors_file:
        colors = json.load(colors_file)
    home_abbrev = teams[home_team_name]
    away_abbrev = teams[away_team_name]
    home_colors = colors[home_abbrev]
    away_colors = colors[away_abbrev]

    return home_colors, away_colors


def get_roster(url):
    home_players, home_team_name = get_players(url, "ShotChartControls__team--home")
    away_players, away_team_name = get_players(url, "ShotChartControls__team--away")

    return home_players, home_team_name, away_players, away_team_name


def get_players(url, class_to_find):
    players = []
    #url = "https://www.espn.com/nhl/playbyplay/_/gameId/401272098"
    #url = "https://www.espn.com/nhl/playbyplay/_/gameId/401272216"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    shots = soup.find(class_=class_to_find)

    #get player roster
    player_select = shots.find(class_="dropdown__select")
    options = player_select.find_all("option")
    for opt in options:
        text = opt.text
        if text == "All Players":
            continue;
        #names are double spaced so we set spacing to only 1
        text = ' '.join(text.split())
        players.append(text)

    #get team name
    img = shots.find("img")
    team_name = img["alt"]

    return players, team_name


#if __name__ == '__main__':
#    url = "https://www.espn.com/nhl/playbyplay/_/gameId/401272216"
#    print(str(get_shots(url)))
