import pandas as pd
from pathlib import Path
import os
import backend.helper as help


base_dir = str(Path(os.getcwd())) #.parents[0])

# @param team - 3 letter code for team. aka BUF for the Buffalo Sabres
def get_team_stats(team, season):
    team_filter = team
    #for moneypuck teams that are 2 chars use a . in the middle aka NJ = N.J
    if len(team) == 2:
        team_filter = team[0] + '.' + team[1]
    data = help.upload_data(base_dir + '\\NHLData\\moneypuck\\overall\\teams-' + str(season) + '.csv')
    team_data = data.loc[data.team==team_filter]
    for index, row in team_data.iterrows():
        r = row.to_dict()
        if r.get('situation')=='5on5':
            gf = r.get('goalsFor')
            ga = r.get('goalsAgainst')
            gf_percent = round((gf / (gf + ga))*100, 2)
            xgf = r.get('xGoalsFor')
            xga = r.get('xGoalsAgainst')
            xgf_percent = r.get('xGoalsPercentage')
            corsi_percent = r.get('corsiPercentage')
            penalites_for = r.get('penaltiesFor')
            penalites_against = r.get('penaltiesAgainst')
            gax = gf - xgf
            gsax = xga - ga
            sf = r.get('shotsOnGoalFor')
            sa = r.get('shotsOnGoalAgainst')
            shooting_percent = round(gf/sf, 2)
            save_percent = round(1 - (ga/sa), 2)
        elif r.get('situation')=='5on4':
            #power play
            pp_goals = r.get('goalsFor')

        elif r.get('situation')=='4on5':
            #penalty kill
            pk_goals = r.get('goalsAgainst')

    pp_percent = round(pp_goals/penalites_for, 2)
    pk_percent = round(1 - (pk_goals/penalites_against), 2)

    five_v_five_data = data.loc[data.situation=='5on5']

    all_xgfs = five_v_five_data['xGoalsFor'].tolist()
    all_goals_for = five_v_five_data['goalsFor'].tolist()

    #goals above expected ranking
    all_gax = []
    for axgf, agf in zip(all_xgfs, all_goals_for):
        all_gax.append(agf - axgf)
    all_gax.sort(reverse=True)
    gax_rank = all_gax.index(gax) + 1

    all_xgas = five_v_five_data['xGoalsAgainst'].tolist()
    all_goals_against = five_v_five_data['goalsAgainst'].tolist()

    #goals saved above expected ranking
    all_gsax = []
    for axga, aga in zip(all_xgas, all_goals_against):
        all_gsax.append(axga - aga)
    all_gsax.sort(reverse=True)
    gsax_rank = all_gsax.index(gsax) + 1

    #corsi rank
    corsis = five_v_five_data['corsiPercentage'].tolist()
    corsis.sort(reverse=True)
    corsi_rank = corsis.index(corsi_percent) + 1

    #shooting percent rank
    all_shots_for = five_v_five_data['shotsOnGoalFor'].tolist()
    all_shooting_percent = []
    for shots, agf in zip(all_shots_for, all_goals_for):
        all_shooting_percent.append(round((agf/shots), 2))
    all_shooting_percent.sort(reverse=True)
    shooting_percent_rank = all_shooting_percent.index(shooting_percent) + 1

    #save percent rank
    all_shots_against = five_v_five_data['shotsOnGoalAgainst'].tolist()
    all_save_percent = []
    for shots, agf in zip(all_shots_for, all_goals_for):
        all_save_percent.append(round(1 - (agf/shots), 2))
    all_save_percent.sort(reverse=True)
    save_percent_rank = all_save_percent.index(save_percent) + 1

    #shots for rank
    all_shots_for.sort(reverse=True)
    sf_rank = all_shots_for.index(sf) + 1

    #shots against rank
    all_shots_against.sort()
    sa_rank = all_shots_against.index(sa) + 1

    #expected goals for % rank
    xgf_percents = five_v_five_data['xGoalsPercentage'].tolist()
    xgf_percents.sort(reverse=True)
    xgf_percent_rank = xgf_percents.index(xgf_percent) + 1

    #expected goals for and against ranks
    all_xgfs.sort(reverse=True)
    xgf_rank = all_xgfs.index(xgf) + 1
    all_xgas.sort()
    xga_rank = all_xgas.index(xga) + 1

    #goals for and against ranks
    all_gf_percents = []
    for agf, aga in zip(all_goals_for, all_goals_against):
        all_gf_percents.append(round((agf / (agf + aga))*100, 2))
    all_gf_percents.sort(reverse=True)
    gf_percent_rank = all_gf_percents.index(gf_percent) + 1
    all_goals_for.sort(reverse=True)
    gf_rank = all_goals_for.index(gf) + 1
    all_goals_against.sort()
    ga_rank = all_goals_against.index(ga) + 1

    penalties_for = five_v_five_data['penaltiesFor'].tolist()
    penalties_against = five_v_five_data['penaltiesAgainst'].tolist()
    pp_data = data.loc[data.situation=='5on4']
    pp_goals = pp_data['goalsFor'].tolist()
    pk_data = data.loc[data.situation=='4on5']
    pk_goals = pk_data['goalsAgainst'].tolist()

    #PP and PK ranks
    pp_percentages = []
    for goals, pens in zip(pp_goals, penalties_for):
        pp_percentages.append(round(goals/pens, 2))
    pk_percentages = []
    for goals, pens in zip(pk_goals, penalties_against):
        pk_percentages.append(round(1- (goals/pens), 2))
    pp_percentages.sort(reverse=True)
    pk_percentages.sort(reverse=True)
    pp_percent_rank = pp_percentages.index(pp_percent) + 1
    pk_percent_rank = pk_percentages.index(pk_percent) + 1

    return {
        'name': help.get_full_nhl_team_name(team),
        'season': str(season) + " - "  + str(season + 1),
        'logo': help.get_all_nhl_logos()[team],
        'colors': help.get_all_nhl_colors()[team],
        'rolling_xgf' : get_rolling_xGF(team, season, season),
        #team card stats
        'gf': gf,
        'gf_rank': gf_rank,
        'ga': ga,
        'ga_rank': ga_rank,
        'gf_percent': gf_percent,
        'gf_percent_rank': gf_percent_rank,
        'xgf': xgf,
        'xgf_rank': xgf_rank,
        'xga': xga,
        'xga_rank': xga_rank,
        'xgf_percent': xgf_percent,
        'xgf_percent_rank': xgf_percent_rank,
        'corsi_percent': '%.2f' % (corsi_percent * 100),
        'corsi_rank': corsi_rank,
        'pp_percent': '%.2f' % (pp_percent * 100),
        'pp_percent_rank': pp_percent_rank,
        'pk_percent': '%.2f' % (pk_percent * 100),
        'pk_percent_rank': pk_percent_rank,
        'gax': '%.2f' % (gax),
        'gax_rank': gax_rank,
        'gsax': '%.2f' % (gsax),
        'gsax_rank': gsax_rank,
        'sf': sf,
        'sf_rank': sf_rank,
        'sa': sa,
        'sa_rank': sa_rank,
        'shooting_percent': shooting_percent * 100,
        'shooting_percent_rank': shooting_percent_rank,
        'save_percent': save_percent * 100,
        'save_percent_rank': save_percent_rank
    }


def get_league_stats(start_season, end_season, filter='all'):
    # game_data = help.upload_data(base_dir + r'\NHLData\moneypuck\games\20-21-games.csv')
    # g5v5 = game_data.loc[game_data.situation=='5on5']
    teams = help.get_teams(filter)
    rolling_xgf = {}
    goal_share = get_goal_share(teams, start_season, end_season, False)
    xgoal_share = get_goal_share(teams, start_season, end_season, True)
    all_dates = []
    for team in teams:
        rolling_xgf[team] = get_rolling_xGF(team, start_season, end_season)
        all_dates = all_dates + rolling_xgf[team].get('dates')
    all_dates = list(set(all_dates))
    all_dates.sort()
    rolling_xgf['all_dates'] = all_dates

    return {
        'rolling_xgf': rolling_xgf,
        'goal_share': goal_share,
        'xgoal_share': xgoal_share,
        'colors': help.get_all_nhl_colors(),
        'logos': help.get_all_nhl_logos(),
        'teams': teams
    }


def get_rolling_xGF(team, start_season, end_season):
    game_data = help.upload_data(base_dir + '\\NHLData\\moneypuck\\games\\' + team + '.csv')
    game_data = game_data.loc[(game_data.season >= start_season)  & (game_data.season <= end_season)]
    game_data = game_data.loc[game_data.situation=='5on5']
    dates = []
    xGFs = []
    for index, row in game_data.iterrows():
        r = row.to_dict()
        date = str(r.get('gameDate'))
        dates.append(date[4:6] + "/" + date[-2:] + "/" + date[:4])
        xGFs.append(r.get('xGoalsPercentage') * 100)
    xGFs = help.get_5_game_rolling_average(xGFs)
    return {
        'xgf': xGFs,
        'dates': dates
    }


def get_goal_share(teams, start_season, end_season, is_expected):
    gf_label = 'xGoalsFor' if is_expected else 'goalsFor'
    ga_label = 'xGoalsAgainst' if is_expected else 'goalsAgainst'
    seasons = list(range(start_season, end_season + 1))
    data = pd.DataFrame()
    for season in seasons:
        data = data.append(help.upload_data(base_dir + r'\NHLData\moneypuck\overall\teams-' + str(season) + '.csv'))

    data = data.loc[(data.season >= start_season)  & (data.season <= end_season)]
    data = data.loc[data.situation=='5on5']
    data = data.groupby(['team'], as_index=False).agg({gf_label:'mean', ga_label:'mean', 'iceTime': 'sum'})
    goal_share = {}
    all_gf = []
    all_ga = []
    for team in teams:
        team_label = team
        team = team[:1] + "." + team[-1:] if len(team) == 2 else team
        df = data.loc[data.team==team]
        for index, row in df.iterrows():
            r = row.to_dict()
            gf = r.get(gf_label)
            ga = r.get(ga_label)
            toi = r.get('iceTime') / 60 # convert from seconds to minutes
            gf60 = help.get_per_60(gf, toi)
            ga60 = help.get_per_60(ga, toi)
            goal_share[team_label] = {
                'gf60': gf60,
                'ga60': ga60
            }
            all_gf.append(gf60)
            all_ga.append(ga60)
    goal_share['avg'] = {
        'gf60' : sum(all_gf) / len(all_gf),
        'ga60' : sum(all_ga) / len(all_ga)
    }

    return goal_share


#if __name__ == '__main__':
    #r = get_league_stats(2019, 2020)
    #r = get_team_stats('BUF', 2020)
    #print(str(r))
