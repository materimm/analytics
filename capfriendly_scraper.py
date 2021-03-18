from bs4 import BeautifulSoup
from selenium import webdriver
import csv

fields = ['name', 'team', 'team_code', 'position', 'age', 'contract_terms', 'cap_percentage', 'cap_hit', 'term_remaining', 'status_after_contract']
teams = ['flames', 'oilers', 'canadiens', 'senators',  'mapleleafs', 'canucks', 'jets',
        'ducks', 'coyotes', 'avalanche', 'kings', 'wild', 'sharks', 'blues', 'goldenknights',
        'hurricanes', 'blackhawks', 'bluejackets', 'stars', 'redwings', 'panthers', 'predators', 'lightning',
        'bruins', 'sabres', 'devils', 'islanders', 'rangers', 'flyers', 'penguins', 'capitals']
team_codes = {
    'flames': 'CGY',
    'oilers': 'EDM',
    'canadiens': 'MTL',
    'senators': 'OTT',
    'mapleleafs': 'TOR',
    'canucks': 'VAN',
    'jets': 'WPG',
    'ducks': 'ANA',
    'coyotes': 'ARI',
    'avalanche': 'COL',
    'kings': 'LA',
    'wild': 'MIN',
    'sharks': 'SJ',
    'blues': 'STL',
    'goldenknights': 'VGK',
    'hurricanes': 'CAR',
    'blackhawks': 'CHI',
    'bluejackets': 'CBJ',
    'stars': 'DAL',
    'redwings': 'DET',
    'panthers': 'FLA',
    'predators': 'NSH',
    'lightning': 'TB',
    'bruins': 'BOS',
    'sabres': 'BUF',
    'devils': 'NJ',
    'islanders': 'NYI',
    'rangers': 'NYR',
    'flyers': 'PHI',
    'penguins': 'PIT',
    'capitals': 'WSH'
}

#https://chromedriver.chromium.org/downloads
driver = webdriver.Chrome("./chromedriver")
team_caps = []
for team in teams:
    team_code = team_codes.get(team)
    url = 'https://www.capfriendly.com/teams/' + team
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    team_table = soup.find('table', id="team")
    rows = team_table.find_all('tr')
    total_count = 0
    for r in rows:
        if r.has_attr('class') and r['class'][0] == 'column_head':
            #header row
            continue
        elif r.has_attr('class') and r['class'][0] == 'total':
            total_count = total_count + 1
            #total row
            continue
        elif not r.has_attr('class'):
            #spacer row
            continue

        if total_count == 3:
            #we've hit the total row for forwards, d and goalies so we can break
            #dont really care about the taxi squad and buyouts rn
            break

        columns = r.find_all('td')
        col_counter = 1

        for col in columns:
            if col_counter == 1: #name
                name = col.find('a').text
            elif col_counter == 2: #term remaining and status after
                term_status = col.text.split(' ')
                term_remaining = term_status[0]
                status_after_contract = term_status[1]
            elif col_counter == 3: #contract terms
                spans = col.find_all('span')
                contract_terms = "none"
                if len(spans) > 1:
                    contract_terms = spans[1].text
            elif col_counter == 4: #position
                position = col.find('span').text
            #col 5 is status - dont really need
            elif col_counter == 6: #age
                age = col.find('span').text
            elif col_counter == 7: #cap %
                cap_percentage = col.text
            elif col_counter == 8: #cap hit
                span = col.find('span')
                if span == None:
                    #player is signed to a futures contract so skip
                    col_counter = col_counter + 1
                    continue
                cap_hit = span.text

            col_counter = col_counter + 1
            if col_counter > 8:
                break

        row_to_write = [name, team, team_code, position, age, contract_terms, cap_percentage, cap_hit, term_remaining, status_after_contract]
        team_caps.append(row_to_write)

    print(team + " done")
driver.quit()


# name of csv file
filename = "nhl_cap.csv"

# writing to csv file
with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(fields)

    # writing the data rows
    csvwriter.writerows(team_caps)
