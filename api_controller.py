import pandas as pd
import bisect


def upload_data(file_path):
    data = pd.read_csv(file_path)
    return data;


def get_team_pdos():
    file_path = r'C:\Users\MoreyMATERISE\Documents\analytics_dev\moneypuck\20-21-teams.csv'
    data = upload_data(file_path)
    team_pdos = []

    for index, row in data.iterrows():
        r = row.to_dict()
        if r.get("situation") == "5on5":
            team = r.get("team")
            goals_for = r.get("goalsFor")
            shots_on_goal_for = r.get("shotsOnGoalFor")
            shots_on_goal_against = r.get("shotsOnGoalAgainst")
            saves = r.get("savedShotsOnGoalAgainst")

            pdo = (goals_for/shots_on_goal_for) + (saves/shots_on_goal_against)
            pdo_obj = {
                "team" : team,
                "pdo" : pdo
            }
            team_pdos.append(pdo_obj)

    print(str(team_pdos))
    return team_pdos


def get_player_stats():
    players = ["Jack Eichel", "Connor McDavid", "Auston Matthews"]
    file_path = r'C:\Users\MoreyMATERISE\Documents\analytics_dev\moneypuck\19-20-skaters.csv'
    data = upload_data(file_path)
    league_corsi = []
    league_faceoff_percent = []
    league_xGF = []
    league_xGA = []
    league_shooting_percent = []

    player_scores = []

    for index, row in data.iterrows():
        r = row.to_dict()
        if r.get("situation") == "5on5":
            corsi = r.get("onIce_corsiPercentage")
            xGA = r.get("OnIce_A_xGoals")
            xGF = r.get("I_F_xGoals")
            shot_attempts = r.get("I_F_shotAttempts")
            goals = r.get("I_F_goals")
            if shot_attempts == 0:
                shooting_percentage = 0
            else:
                shooting_percentage = goals / shot_attempts

            faceoffs_won = r.get("faceoffsWon")
            faceoffs_lost = r.get("faceoffsLost")
            total_faceoffs = faceoffs_won + faceoffs_lost
            if total_faceoffs == 0:
                faceoff_percentage = 0
            else:
                faceoff_percentage = faceoffs_won / total_faceoffs

            bisect.insort(league_corsi, corsi)
            bisect.insort(league_xGF, xGF)
            bisect.insort(league_xGA, xGA)
            bisect.insort(league_faceoff_percent, faceoff_percentage)
            bisect.insort(league_shooting_percent, shooting_percentage)

            player_stats = {}
            player_stats["name"] = r.get("name")
            player_stats["team"] = r.get("team")

            position = r.get("position").strip()
            if position == "L":
                position = "Left Wing"
            elif position == "R":
                position == "Right Wing"
            elif position == "C":
                position == "Center"
            elif position == "D":
                position == "Defenseman"

            player_stats["position"] = position
            player_stats["xGF"] = xGF
            player_stats["xGA"] = xGA
            player_stats["FO_percent"] = faceoff_percentage
            player_stats["corsi"] = corsi
            player_stats["shooting_percent"] = shooting_percentage

            player_scores.append(player_stats)

    for player_stats in player_scores:
        player_stats["xGF_rank"] = len(league_xGF) - league_xGF.index(player_stats.get("xGF"))
        player_stats["xGA_rank"] = league_xGA.index(player_stats.get("xGA")) + 1
        player_stats["FO_percent_rank"] = len(league_faceoff_percent) - league_faceoff_percent.index(player_stats.get("FO_percent"))
        player_stats["corsi_rank"] = len(league_corsi) - league_corsi.index(player_stats.get("corsi"))
        player_stats["shooting_percent_rank"] = len(league_shooting_percent) - league_shooting_percent.index(player_stats.get("shooting_percent"))

        player_stats["score"] = (player_stats.get("xGF_rank") + player_stats.get("xGA_rank") + player_stats.get("FO_percent_rank") +
                            player_stats.get("corsi_rank") + player_stats.get("shooting_percent_rank")) / 5

    player_scores = sorted(player_scores, key = lambda i: i["score"])
    #print(str(player_scores))
    return player_scores
