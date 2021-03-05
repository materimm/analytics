import pandas as pd
import json
import helper as help

GOALIE_PATH = './NHLData/moneypuck/20-21-goalies.csv'
LINES_PATH = './NHLData/moneypuck/20-21-lines.csv'
SKATERS_PATH = './NHLData/moneypuck/skaters/20-21-skaters.csv'

def get_skater_stats(team):
    team_abbrev = help.get_nhl_team_abbreviation(team)
    df = help.upload_data(SKATERS_PATH)
    df = df.loc[df.team==team_abbrev]

    fiveVfive = df.loc[df.situation=='5on5']
    fiveVfive.sort_values('onIce_xGoalsPercentage', ascending=False, inplace=True)
    gf_diff_5v5 = []
    cf_diff_5v5 = []
    skaters = []

    for index, row in fiveVfive.iterrows():
        r = row.to_dict()
        #print(str(r.get('name') + ' = ' + str(r.get('onIce_xGoalsPercentage')) + ' - ' + str(r.get('onIce_corsiPercentage'))))
        skaters.append({
            'name': r.get('name'),
            'xgf_diff': r.get('onIce_xGoalsPercentage'),
            'cf_diff': r.get('onIce_corsiPercentage')
        })

    return {
        'team': team,
        'colors': help.get_nhl_team_colors(team),
        'skaters': skaters
    }

#if __name__ == '__main__':
#    team = 'Buffalo Sabres'
#    r=get_skater_stats(team)
#    print(str(r))
