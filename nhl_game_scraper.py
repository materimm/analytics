import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver

def get_shots():
    home_shots = 0
    away_shots = 0
    home_roster, home_team_name, away_roster, away_team_name = get_roster()

    driver = webdriver.Chrome("./chromedriver")
    #url = "https://www.espn.com/nhl/playbyplay/_/gameId/401272098"
    url = "https://www.espn.com/nhl/playbyplay/_/gameId/401272216"
    driver.get(url)


    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    play_by_play_section = soup.find(class_="Card--PlayByPlay")
    buttons = play_by_play_section.find_all("button")
    num_periods = len(buttons)
    #num_periods = 1

    #1st period
    if num_periods >= 1:
        h, a = get_shots_web_reader(soup, home_roster, away_roster)
        home_shots += h
        away_shots += a
        #print("========================================")

    #2nd period
    if num_periods >= 2:
        button = driver.find_element_by_xpath('//button[text()="2nd"]')
        button.click()
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
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

    obj = {
        "home": {
            "name": home_team_name,
            "shots": home_shots
        },
        "away": {
            "name": away_team_name,
            "shots": away_shots
        }
    }

    #print(str(obj))
    return obj


def get_shots_web_reader(soup, home_roster, away_roster):
    home_shots = 0
    away_shots = 0

    all_plays = soup.find_all(class_="playByPlay__tableRow")
    for play in all_plays:
        play_txt = play.find(class_="playByPlay__text").text
        #print(str(play_txt))
        if play_txt.startswith('Shot on goal'):
            s = re.search('Shot on goal by (.*) saved by*', play_txt)
            shooter = s.group(1)
            if shooter.strip() in home_roster:
                home_shots += 1
            elif shooter in away_roster:
                away_shots += 1
            else:
                print("ERROR -- shooter not in either roster----------------------------------")
        elif play_txt.startswith('Goal scored'):
            s = re.search('Goal scored by (.*) assisted by*', play_txt)
            if s == None: #unassisted
                s = re.search('Goal scored by (.*)$', play_txt)
                shooter = s.group(1)
            else:
                shooter = s.group(1)
            if shooter.strip() in home_roster:
                home_shots += 1
            elif shooter in away_roster:
                away_shots += 1
            else:
                print("ERROR -- shooter not in either roster----------------------------------")
        elif play_txt.startswith('Power Play Goal'):
            s = re.search('Power Play Goal Scored  by (.*) assisted by*', play_txt)
            if s == None: #unassisted
                s = re.search('Goal scored by (.*)$', play_txt)
                shooter = s.group(1)
            else:
                shooter = s.group(1)
            if shooter.strip() in home_roster:
                home_shots += 1
            elif shooter in away_roster:
                away_shots += 1
            else:
                print("ERROR -- shooter not in either roster----------------------------------")


    return home_shots, away_shots




def get_roster():
    home_players, home_team_name = get_players("ShotChartControls__team--home")
    away_players, away_team_name = get_players("ShotChartControls__team--away")

    return home_players, home_team_name, away_players, away_team_name


def get_players(class_to_find):
    players = []
    #url = "https://www.espn.com/nhl/playbyplay/_/gameId/401272098"
    url = "https://www.espn.com/nhl/playbyplay/_/gameId/401272216"
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
    #get_shots()
