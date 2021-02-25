import pandas as pd
import json
import helper as help

SHOTS_PATH = './NHLData/moneypuck/shots/shots_'

def get_scoring_locations(player, seasons):
    df = pd.DataFrame()
    for s in seasons:
        print(str(s))
        df = df.append(help.upload_data(SHOTS_PATH + str(s) + '.csv'))

    df = df.loc[(df.shooterName == player) & (df.goal==1)]

    neutral_zone = df.loc[(df.xCordAdjusted<25)]
    behind_net = df.loc[(df.xCordAdjusted>89)]
    high_slot = df.loc[(df.xCordAdjusted>=25) & (df.xCordAdjusted<46) & (df.yCordAdjusted>=-4) & (df.yCordAdjusted<=4)]
    slot = df.loc[(df.xCordAdjusted>=46) & (df.xCordAdjusted<67) & (df.yCordAdjusted>=-4) & (df.yCordAdjusted<=4)]
    net_front = df.loc[(df.xCordAdjusted>=67) & (df.xCordAdjusted<=89) & (df.yCordAdjusted>=-4) & (df.yCordAdjusted<=4)]
    left_point = df.loc[(df.xCordAdjusted>=25) & (df.xCordAdjusted<57) & (df.yCordAdjusted>4)]
    low_left = df.loc[(df.xCordAdjusted>=57) & (df.xCordAdjusted<=89) & (df.yCordAdjusted>4)]
    right_point = df.loc[(df.xCordAdjusted>=25) & (df.xCordAdjusted<57) & (df.yCordAdjusted<-4)]
    low_right = df.loc[(df.xCordAdjusted>=57) & (df.xCordAdjusted<=89) & (df.yCordAdjusted<-4)]

    wrist = []
    backhand = []
    snap = []
    slap = []
    tip = []
    deflection = []
    wrap = []
    shot_locations = [neutral_zone, behind_net, high_slot, slot, net_front, left_point, low_left, right_point, low_right]
    for sl in shot_locations:
        w, b, sn, slp, t, d, wr = get_shot_type_count(sl)
        wrist.append(w)
        backhand.append(b)
        snap.append(sn)
        slap.append(slp)
        tip.append(t)
        deflection.append(d)
        wrap.append(wr)

    return {
        'name' : player,
        'seasons': str(seasons[0]) if len(seasons) == 1 else str(seasons[0]) + ' - ' + str(seasons[len(seasons)-1]),
        'labels': ['Neutral Zone', 'Behind the Net', 'High Slot', 'Slot', 'Net Front', 'Left Point', 'Right Point', 'Low Left Side', 'Low Right Side'],
        'data_labels': ['Wrist shot', 'Backhanded', 'Snap shot', 'Slap shot', 'Tip', 'Deflection', 'Wrap Around'],
        'data': [wrist, backhand, snap, slap, tip, deflection, wrap],
        'colors': ['#7BE0AD', '#E0B0D5', '#F93943', '#7EB2DD', '#445E93', '#0B5563', '#947BD3']
    }



    # return {
    #     'neutral_zone': get_shot_type_count(neutral_zone),
    #     'behind_net': get_shot_type_count(behind_net),
    #     'high_slot': get_shot_type_count(high_slot),
    #     'slot': get_shot_type_count(slot),
    #     'net_front': get_shot_type_count(net_front),
    #     'left_point': get_shot_type_count(left_point),
    #     'right_point': get_shot_type_count(right_point),
    #     'low_left': get_shot_type_count(low_left),
    #     'low_right': get_shot_type_count(low_right),
    #     'labels': ['Neutral Zone', 'Behind the Net', 'High Slot', 'Slot', 'Net Front', 'Left Point', 'Right Point', 'Low Left Side', 'Low Right Side'],
    #     'shot_type': ['Wrist shot', 'Backhanded', 'Snap shot', 'Slap shot', 'Tip', 'Deflection', 'Wrap Around']
    # }


def get_shot_type_count(df):
    wrist = 0 #WRIST
    backhand = 0 #BACK
    snap = 0 #SNAP
    slap = 0 #SLAP
    tip = 0 #TIP
    deflection = 0 #DEFL
    wrap = 0 #WRAP
    for index, row in df.iterrows():
        r = row.to_dict()
        shot_type = r.get('shotType')
        if shot_type == 'WRIST':
            wrist += 1
        elif shot_type == 'BACK':
            backhand += 1
        elif shot_type == 'SNAP':
            snap += 1
        elif shot_type == 'SLAP':
            slap += 1
        elif shot_type == 'TIP':
            tip += 1
        elif shot_type == 'DEFL':
            deflection += 1
        elif shot_type == 'WRAP':
            wrap += 1
        else:
            print('shot type-------------------------------->' + r.get('shotType'))

    return [wrist, backhand, snap, slap, tip, deflection, wrap]

# if __name__ == '__main__':
#     player = 'Jeff Skinner'
#     seasons =list(range(2010, 2021))
#     r = get_scoring_locations(player, seasons)
#     print(str(r))
