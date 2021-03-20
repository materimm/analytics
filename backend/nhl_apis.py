import pandas as pd
from pathlib import Path
import os
import backend.helper as help

######################
##  API End Points  ##
##------------------##
## get_team_stats   ##
## get_league_stats ##
## get_player_card  ##
######################

base_dir = str(Path(os.getcwd()))
#base_dir = str(Path(os.getcwd()).parents[0])

# @param team - 3 letter code for team. aka BUF for the Buffalo Sabres
def get_team_stats(team, season):
    team_filter = team
    #for moneypuck teams that are 2 chars use a . in the middle aka NJ = N.J
    if len(team) == 2:
        team_filter = team[0] + '.' + team[1]
    data = help.upload_data(base_dir + '\\NHLData\\moneypuck\\teams\\' + str(season) + '-' + str(season+1) + '-teams.csv')
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
        'gf_percent': '%.2f' % (gf_percent),
        'gf_percent_rank': gf_percent_rank,
        'xgf': xgf,
        'xgf_rank': xgf_rank,
        'xga': xga,
        'xga_rank': xga_rank,
        'xgf_percent': '%.2f' % (xgf_percent * 100),
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
        'shooting_percent': '%.2f' % (shooting_percent * 100),
        'shooting_percent_rank': shooting_percent_rank,
        'save_percent': '%.2f' % (save_percent * 100),
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

    seasons = start_season if start_season == end_season else str(start_season) + ' - ' + str(end_season)

    return {
        'rolling_xgf': rolling_xgf,
        'goal_share': goal_share,
        'xgoal_share': xgoal_share,
        'colors': help.get_all_nhl_colors(),
        'logos': help.get_all_nhl_logos(),
        'teams': teams,
        'season': seasons
    }


def get_player_card(player, season):
    colors = help.get_color_gradient(finish_hex="#ffffff", n=50) + help.get_color_gradient(start_hex="#ffffff", n=50)
    cap_data = help.upload_data(base_dir + '\\NHLData\\nhl_cap.csv')
    name_split = player.split(' ')
    cap_data = cap_data.loc[cap_data.name==name_split[1] + ', ' + name_split[0]]
    for index, row in cap_data.iterrows():
        r = row.to_dict()
        position = r.get('position')
        age = r.get('age')
        cap_hit = r.get('cap_hit')
        term_remaining = r.get('term_remaining')
        team_code = r.get('team_code')
    player_obj = {
        'name': player,
        'season': str(season) + ' - ' + str(season+1),
        'team': help.get_full_nhl_team_name(team_code),
        'logo': help.get_all_nhl_logos()[team_code],
        'age': age,
        'position': position,
        'cap_hit': cap_hit,
        'term': term_remaining,
    }

    path = base_dir + '\\NHLData\\moneypuck\\skaters\\{}-{}-skaters.csv'
    path = path.format(season, season+1)
    data = help.upload_data(path)

    #------all situations ---------------
    all_situtions = data.copy()
    all_situtions = all_situtions.loc[(all_situtions.name==player) & (all_situtions.situation=='all')]
    for index, row in all_situtions.iterrows():
        r = row.to_dict()
        #rounding to remove decimal
        player_obj['points'] = round(r.get('I_F_points'))
        player_obj['goals'] = round(r.get('I_F_goals'))
        player_obj['assists'] = round(r.get('I_F_primaryAssists') + r.get('I_F_secondaryAssists'))
        player_obj['a1'] = round(r.get('I_F_primaryAssists'))
        player_obj['a2'] = round(r.get('I_F_secondaryAssists'))
        player_obj['gp'] = round(r.get('games_played'))

    #------ 5v5 ---------------
    five_v_five_data = data.copy()
    five_v_five_data = data.loc[data.situation=='5on5']

    # l prefix means whole league
    l_toi = five_v_five_data['icetime'].tolist()
    l_on_ice_gf = five_v_five_data['OnIce_F_goals'].tolist()
    l_on_ice_xgf = five_v_five_data['OnIce_F_xGoals'].tolist()
    l_xgf_percent = five_v_five_data['onIce_xGoalsPercentage'].tolist()
    l_on_ice_ga = five_v_five_data['OnIce_A_goals']
    l_on_ice_xga = five_v_five_data['OnIce_A_xGoals'].tolist()
    l_ixgf = five_v_five_data['I_F_xGoals'].tolist()
    l_shots = five_v_five_data['I_F_shotsOnGoal'].tolist()
    l_corsi = five_v_five_data['onIce_corsiPercentage'].tolist()
    l_blocks = five_v_five_data['shotsBlockedByPlayer'].tolist()
    l_hits = five_v_five_data['I_F_hits'].tolist()
    l_goals = five_v_five_data['I_F_goals'].tolist()
    l_a1 = five_v_five_data['I_F_primaryAssists'].tolist()
    l_a2 = five_v_five_data['I_F_secondaryAssists'].tolist()

    l_gf_60, l_xgf_60, l_ga_60, l_xga_60, l_ixgf_60 = [], [], [], [], []
    l_blocks_60, l_hits_60, l_goals_60, l_a1_60, l_a2_60 = [], [], [], [], []
    l_shooting_percent = []
    for toi, gf, xgf, ga, xga, ixgf, b, h, g, a1, a2, sh in zip(l_toi, l_on_ice_gf,
      l_on_ice_xgf, l_on_ice_ga, l_on_ice_xga, l_ixgf, l_blocks, l_hits,
      l_goals, l_a1, l_a2, l_shots):
        l_gf_60.append(help.get_per_60(gf, toi))
        l_xgf_60.append(help.get_per_60(xgf, toi))
        l_ga_60.append(help.get_per_60(ga, toi))
        l_xga_60.append(help.get_per_60(xga, toi))
        l_ixgf_60.append(help.get_per_60(ixgf, toi))
        l_blocks_60.append(help.get_per_60(b, toi))
        l_hits_60.append(help.get_per_60(h, toi))
        l_goals_60.append(help.get_per_60(g, toi))
        l_a1_60.append(help.get_per_60(a1, toi))
        l_a2_60.append(help.get_per_60(a2, toi))
        l_shooting_percent.append(0 if sh==0 else round((g/sh)*100, 2))

    five_v_five_data = five_v_five_data.loc[five_v_five_data.name==player]
    for index, row in five_v_five_data.iterrows():
        r = row.to_dict()
        toi = r.get('icetime')
        gf_60 = help.get_per_60(r.get('OnIce_F_goals'), toi)
        xgf_60 = help.get_per_60(r.get('OnIce_F_xGoals'), toi)
        xgf_percent = r.get('onIce_xGoalsPercentage')
        ga_60 = help.get_per_60(r.get('OnIce_A_goals'), toi)
        xga_60 = help.get_per_60(r.get('OnIce_A_xGoals'), toi)
        ixgf_60 = help.get_per_60(r.get('I_F_xGoals'), toi)
        shots = r.get('I_F_shotsOnGoal')
        corsi = r.get('onIce_corsiPercentage')
        blocks_60 = help.get_per_60(r.get('shotsBlockedByPlayer'), toi)
        hits_60 = help.get_per_60(r.get('I_F_hits'), toi)
        goals = r.get('I_F_goals')
        a1_60 = help.get_per_60(r.get('I_F_primaryAssists'), toi)
        a2_60 = help.get_per_60(r.get('I_F_secondaryAssists'), toi)
        shooting_percent = 0 if shots==0 else round((goals/shots)*100, 2)
        goals_60 = help.get_per_60(goals, toi)

    gf_percentile = help.get_percentile(l_gf_60, gf_60)
    xgf_percentile = help.get_percentile(l_xgf_60, xgf_60)
    xgf_percent_percentile = help.get_percentile(l_xgf_percent, xgf_percent)
    ga_percentile = help.get_percentile(l_ga_60, ga_60, True)
    xga_percentile = help.get_percentile(l_xga_60, xga_60, True)
    ixgf_percentile = help.get_percentile(l_ixgf_60, ixgf_60)
    shooting_percent_percentile = help.get_percentile(l_shooting_percent, shooting_percent)
    corsi_percentile = help.get_percentile(l_corsi, corsi)
    blocks_percentile = help.get_percentile(l_blocks_60, blocks_60)
    hits_percentile = help.get_percentile(l_hits_60, hits_60)
    goals_percentile = help.get_percentile(l_goals_60, goals_60)
    a1_percentile = help.get_percentile(l_a1_60, a1_60)
    a2_percentile = help.get_percentile(l_a2_60, a2_60)

    even_obj = {
        'gf_percentile': gf_percentile,
        'gf_color': _get_percentile_color(colors, gf_percentile),
        'xgf_percentile': xgf_percentile,
        'xgf_color': _get_percentile_color(colors, xgf_percentile),
        'xgf_percent_percentile': xgf_percent_percentile,
        'xgf_percent_color': _get_percentile_color(colors, xgf_percent_percentile),
        'ga_percentile': ga_percentile,
        'ga_color': _get_percentile_color(colors, ga_percentile),
        'xga_percentile': xga_percentile,
        'xga_color': _get_percentile_color(colors, xga_percentile),
        'ixgf_percentile': ixgf_percentile,
        'ixgf_color': _get_percentile_color(colors, ixgf_percentile),
        'shooting_percent_percentile': shooting_percent_percentile,
        'shooting_percent_color': _get_percentile_color(colors, shooting_percent_percentile),
        'corsi_percentile': corsi_percentile,
        'corsi_color': _get_percentile_color(colors, corsi_percentile),
        'blocks_percentile': blocks_percentile,
        'blocks_color': _get_percentile_color(colors, blocks_percentile),
        'hits_percentile': hits_percentile,
        'hits_color': _get_percentile_color(colors, hits_percentile),
        'goals_percentile': goals_percentile,
        'goals_color': _get_percentile_color(colors, goals_percentile),
        'a1_percentile': a1_percentile,
        'a1_color': _get_percentile_color(colors, a1_percentile),
        'a2_percentile': a2_percentile,
        'a2_color': _get_percentile_color(colors, a2_percentile)
    }

    pp_data = data.copy()
    pp_data = data.loc[data.situation=='5on4']
    l_toi = pp_data['icetime'].tolist()
    l_on_ice_gf = pp_data['OnIce_F_goals'].tolist()
    l_on_ice_xgf = pp_data['OnIce_F_xGoals'].tolist()
    l_ixgf = pp_data['I_F_xGoals'].tolist()
    l_goals = pp_data['I_F_goals'].tolist()
    l_a1 = pp_data['I_F_primaryAssists']
    l_a2 = pp_data['I_F_secondaryAssists']

    l_gf_60, l_xgf_60, l_ixgf_60, l_goals_60, l_assists_60 = [], [], [], [], []
    for toi, gf, xgf, ixgf, g, a1, a2 in zip(l_toi, l_on_ice_gf, l_on_ice_xgf, l_ixgf, l_goals, l_a1, l_a2):
        if toi==0:
            l_gf_60.append(0)
            l_xgf_60.append(0)
            l_ixgf_60.append(0)
            l_goals_60.append(0)
            l_assists_60.append(0)
        else:
            l_gf_60.append(help.get_per_60(gf, toi))
            l_xgf_60.append(help.get_per_60(xgf, toi))
            l_ixgf_60.append(help.get_per_60(ixgf, toi))
            l_goals_60.append(help.get_per_60(g, toi))
            l_assists_60.append(help.get_per_60(a1 + a2, toi))

    pp_data = pp_data.loc[pp_data.name==player]
    for index, row in pp_data.iterrows():
        r = row.to_dict()
        toi = r.get('icetime')
        if toi != 0:
            gf_60 = help.get_per_60(r.get('OnIce_F_goals'), toi)
            xgf_60 = help.get_per_60(r.get('OnIce_F_xGoals'), toi)
            ixgf_60 = help.get_per_60(r.get('I_F_xGoals'), toi)
            goals_60 = help.get_per_60(r.get('I_F_goals'), toi)
            a1 = r.get('I_F_primaryAssists')
            a2 = r.get('I_F_secondaryAssists')
            assists_60 = help.get_per_60(a1 + a2, toi)

    if toi != 0:
        gf_percentile = help.get_percentile(l_gf_60, gf_60)
        xgf_percentile = help.get_percentile(l_xgf_60, xgf_60)
        ixgf_percentile = help.get_percentile(l_ixgf_60, ixgf_60)
        goals_percentile = help.get_percentile(l_goals_60, goals_60)
        assists_percentile = help.get_percentile(l_assists_60, assists_60)

        pp_obj = {
            'gf_percentile': gf_percentile,
            'gf_color': _get_percentile_color(colors, gf_percentile),
            'xgf_percentile': xgf_percentile,
            'xgf_color': _get_percentile_color(colors, xgf_percentile),
            'ixgf_percentile': ixgf_percentile,
            'ixgf_color': _get_percentile_color(colors, ixgf_percentile),
            'goals_percentile': goals_percentile,
            'goals_color': _get_percentile_color(colors, goals_percentile),
            'assists_percentile': assists_percentile,
            'assists_color': _get_percentile_color(colors, assists_percentile),
        }
    else:
        pp_obj = {
            'gf_percentile': 'N/A',
            'gf_color': "#ffffff",
            'xgf_percentile': 'N/A',
            'xgf_color': "#ffffff",
            'ixgf_percentile': 'N/A',
            'ixgf_color': "#ffffff",
            'goals_percentile': 'N/A',
            'goals_color': "#ffffff",
            'assists_percentile': 'N/A',
            'assists_color': "#ffffff",
        }

    pk_data = data.copy()
    pk_data = data.loc[data.situation=='4on5']
    l_toi = pk_data['icetime'].tolist()
    l_on_ice_ga = pk_data['OnIce_A_goals'].tolist()
    l_on_ice_xga = pk_data['OnIce_A_xGoals'].tolist()
    l_blocks = pk_data['shotsBlockedByPlayer'].tolist()

    l_ga_60, l_xga_60, l_blocks_60 = [], [], []
    for toi, ga, xga, b in zip(l_toi, l_on_ice_ga, l_on_ice_xga, l_blocks):
        if toi==0:
            l_ga_60.append(0)
            l_xga_60.append(0)
            l_blocks_60.append(0)
        else:
            l_ga_60.append(help.get_per_60(ga, toi))
            l_xga_60.append(help.get_per_60(xga, toi))
            l_blocks_60.append(help.get_per_60(b, toi))

    pk_data = pk_data.loc[pk_data.name==player]
    for index, row in pk_data.iterrows():
        r = row.to_dict()
        toi = r.get('icetime')
        if toi != 0:
            ga_60 = help.get_per_60(r.get('OnIce_A_goals'), toi)
            xga_60 = help.get_per_60(r.get('OnIce_A_xGoals'), toi)
            blocks_60 = help.get_per_60(r.get('shotsBlockedByPlayer'), toi)

    if toi != 0:
        ga_percentile = help.get_percentile(l_ga_60, ga_60, True)
        xga_percentile = help.get_percentile(l_xga_60, xga_60, True)
        blocks_percentile = help.get_percentile(l_blocks_60, blocks_60)

        pk_obj = {
            'ga_percentile': ga_percentile,
            'ga_color': _get_percentile_color(colors, ga_percentile),
            'xga_percentile': xga_percentile,
            'xga_color': _get_percentile_color(colors, xga_percentile),
            'blocks_percentile': blocks_percentile,
            'blocks_color': _get_percentile_color(colors, blocks_percentile),
        }
    else:
        pk_obj = {
            'ga_percentile': 'N/A',
            'ga_color': "#ffffff",
            'xga_percentile': 'N/A',
            'xga_color': "#ffffff",
            'blocks_percentile': 'N/A',
            'blocks_color': "#ffffff",
        }

    return {
        'player_info': player_obj,
        'even': even_obj,
        'pp': pp_obj,
        'pk': pk_obj,
    }

def _get_percentile_color(colors, percentile):
    if percentile != 0:
        percentile = percentile - 1
    return colors[percentile]

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
        data = data.append(help.upload_data(base_dir + '\\NHLData\\moneypuck\\teams\\' + str(season) + '-' + str(season+1) + '-teams.csv'))
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
    # r = get_player_card('Connor McDavid', 2020)
    # print(str(r))
