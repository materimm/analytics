import pandas as pd

def upload_data(file_path):
    print("uploading data...")
    data = pd.read_csv(file_path)

    #for index, row in data.iterrows():
        #print(str(row.to_dict()))
        #break

    print("done")

    return data;

def get_team_pdos(data):
    team_pdos = {}
    pdo_sum = 0
    for index, row in data.iterrows():
        r = row.to_dict()
        if r.get("situation") == "5on5":
            team = r.get("team")
            goals_for = r.get("goalsFor")
            shots_on_goal_for = r.get("shotsOnGoalFor")
            shots_on_goal_against = r.get("shotsOnGoalAgainst")
            saves = r.get("savedShotsOnGoalAgainst")

            pdo = (goals_for/shots_on_goal_for) + (saves/shots_on_goal_against)
            team_pdos[team] = pdo
            pdo_sum += pdo

    print("pdo sum: " + str(pdo_sum))
    print("----------------------")
    print(str(team_pdos))
    return team_pdos


if __name__ == '__main__':
    print("in main")
    #file_path = r'C:\Users\MoreyMATERISE\Documents\NHL\moneypuck\20-21-skaters.csv'
    file_path = r'C:\Users\MoreyMATERISE\Documents\NHL\moneypuck\20-21-teams.csv'
    data = upload_data(file_path)
    pdo_dict = get_team_pdos(data)
