from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedKFold, RepeatedStratifiedKFold, GridSearchCV
from numpy import mean, std, arange
import pandas as pd
from matplotlib import pyplot

def setup_data():
    df = pd.read_csv('../NHLData/moneypuck/shots/shots_2019.csv')

    #5v5 only
    df = df[(df.awaySkatersOnIce == 5) & (df.homeSkatersOnIce == 5)]
    #only shots on net
    df = df[df.shotWasOnGoal == 1]

    columns_to_use = ['time', 'goal', 'shotAngleAdjusted', 'shotDistance', 'shotType', 'offWing']
    columns_to_drop = ['shotID', 'arenaAdjustedShotDistance', 'arenaAdjustedXCord', 'arenaAdjustedXCordABS', 'arenaAdjustedYCord', 'arenaAdjustedYCordAbs', 'averageRestDifference',
    'awayEmptyNet', 'awayPenalty1Length', 'awayPenalty1TimeLeft', 'awaySkatersOnIce', 'awayTeamCode', 'awayTeamGoals', 'defendingTeamAverageTimeOnIce', 'defendingTeamAverageTimeOnIceOfDefencemen',
    'defendingTeamAverageTimeOnIceOfDefencemenSinceFaceoff', 'defendingTeamAverageTimeOnIceOfForwards', 'defendingTeamAverageTimeOnIceOfForwardsSinceFaceoff',
    'defendingTeamAverageTimeOnIceSinceFaceoff', 'defendingTeamDefencemenOnIce', 'defendingTeamForwardsOnIce', 'defendingTeamMaxTimeOnIce', 'defendingTeamMaxTimeOnIceOfDefencemen',
    'defendingTeamMaxTimeOnIceOfDefencemenSinceFaceoff', 'defendingTeamMaxTimeOnIceOfForwards',	'defendingTeamMaxTimeOnIceOfForwardsSinceFaceoff', 'defendingTeamMaxTimeOnIceSinceFaceoff',
    'defendingTeamMinTimeOnIce', 'defendingTeamMinTimeOnIceOfDefencemen', 'defendingTeamMinTimeOnIceOfDefencemenSinceFaceoff', 'defendingTeamMinTimeOnIceOfForwards',
    'defendingTeamMinTimeOnIceOfForwardsSinceFaceoff', 'defendingTeamMinTimeOnIceSinceFaceoff',	'distanceFromLastEvent', 'event', 'game_id',
    #'goal',
    'goalieIdForShot', 'goalieNameForShot',
    'homeEmptyNet', 'homePenalty1Length', 'homePenalty1TimeLeft', 'homeSkatersOnIce', 'homeTeamCode', 'homeTeamGoals', 'homeTeamWon', 'id', 'isHomeTeam', 'isPlayoffGame',
    'lastEventCategory', 'lastEventShotAngle', 'lastEventShotDistance', 'lastEventTeam', 'lastEventxCord', 'lastEventxCord_adjusted', 'lastEventyCord', 'lastEventyCord_adjusted', 'location',
    #'offWing',
    'period', 'playerNumThatDidEvent', 'playerNumThatDidLastEvent', 'playerPositionThatDidEvent', 'season', 'shooterLeftRight', 'shooterName', 'shooterPlayerId',
    'shooterTimeOnIce', 'shooterTimeOnIceSinceFaceoff', 'shootingTeamAverageTimeOnIce', 'shootingTeamAverageTimeOnIceOfDefencemen', 'shootingTeamAverageTimeOnIceOfDefencemenSinceFaceoff',
    'shootingTeamAverageTimeOnIceOfForwards', 'shootingTeamAverageTimeOnIceOfForwardsSinceFaceoff', 'shootingTeamAverageTimeOnIceSinceFaceoff', 'shootingTeamDefencemenOnIce',
    'shootingTeamForwardsOnIce', 'shootingTeamMaxTimeOnIce', 'shootingTeamMaxTimeOnIceOfDefencemen', 'shootingTeamMaxTimeOnIceOfDefencemenSinceFaceoff', 'shootingTeamMaxTimeOnIceOfForwards',
    'shootingTeamMaxTimeOnIceOfForwardsSinceFaceoff', 'shootingTeamMaxTimeOnIceSinceFaceoff', 'shootingTeamMinTimeOnIce', 'shootingTeamMinTimeOnIceOfDefencemen',
    'shootingTeamMinTimeOnIceOfDefencemenSinceFaceoff', 'shootingTeamMinTimeOnIceOfForwards', 'shootingTeamMinTimeOnIceOfForwardsSinceFaceoff', 'shootingTeamMinTimeOnIceSinceFaceoff', 'shotAngle',
    #'shotAngleAdjusted',
    'shotAnglePlusRebound', 'shotAnglePlusReboundSpeed', 'shotAngleReboundRoyalRoad',
    #'shotDistance',
    'shotGeneratedRebound', 'shotGoalieFroze', 'shotOnEmptyNet', 'shotPlayContinuedInZone', 'shotPlayContinuedOutsideZone', 'shotPlayStopped', 'shotRebound', 'shotRush',
    #'shotType',
    'shotWasOnGoal', 'speedFromLastEvent', 'team', 'teamCode',
    #'time',
    'timeDifferenceSinceChange', 'timeSinceFaceoff', 'timeSinceLastEvent', 'timeUntilNextEvent', 'xCord', 'xCordAdjusted', 'xFroze', 'xGoal', 'xPlayContinuedInZone',
    'xPlayContinuedOutsideZone', 'xPlayStopped', 'xRebound', 'xShotWasOnGoal', 'yCord', 'yCordAdjusted']


    df = df.drop(columns_to_drop, axis=1)
    df.reset_index(drop=True, inplace=True)

    output = df.goal
    input = df.drop(['goal'], axis=1)
    input = pd.get_dummies(input, columns=['shotType'])

    max_time = 3600
    max_angle = 360
    max_distance = 194
    input['time'] = input['time'].map(lambda t: t/max_time)
    input['shotAngleAdjusted'] = input['shotAngleAdjusted'].map(lambda a: a/max_angle)
    input['shotDistance'] = input['shotDistance'].map(lambda sd: sd/max_distance)

    return input, output


def get_models_trees():
    models = dict()
    n_trees = [10, 50, 100, 500, 1000]
    for t in n_trees:
        models[str(t)] = GradientBoostingClassifier(n_estimators=t)
    return models


def get_models_samples():
    models = dict()
    for i in arange(0.1, 1.1, 0.1):
        key = '%.1f' % i
        models[key] = GradientBoostingClassifier(subsample=i)
    return models


def get_models_features():
    models = dict()
    for i in range(1, 12):
        models[str(i)] = GradientBoostingClassifier(max_features=i)
    return models


def get_models_learning_rate():
    models = dict()
    for i in [0.0001, 0.001, 0.01, 0.1, 1.0]:
        key = '%.4f' % i
        models[key] = GradientBoostingClassifier(learning_rate=i)
    return models


def get_models_tree_depth():
    models = dict()
    for i in range(1,11):
        models[str(i)] = GradientBoostingClassifier(max_depth=i)
    return models


def grid_search():
    input, output = setup_data()
    model = GradientBoostingRegressor()
    grid = dict()
    grid['n_estimators'] = [10, 50, 100, 500]
    grid['learning_rate'] = [0.0001, 0.001, 0.01, 0.1, 1.0]
    grid['subsample'] = [0.3, 0.5, 0.7, 1.0]
    grid['max_depth'] = [2, 3, 4, 7, 9]
    cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
    grid_search = GridSearchCV(estimator=model, param_grid=grid, n_jobs=-1, cv=cv, scoring='neg_mean_absolute_error')
    grid_result = grid_search.fit(input, output)
    print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
    means = grid_result.cv_results_['mean_test_score']
    stds = grid_result.cv_results_['std_test_score']
    params = grid_result.cv_results_['params']
    for mean, stdev, param in zip(means, stds, params):
        print("%f (%f) with: %r" % (mean, stdev, param))



def evaluate_model(model, input, output):
    cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
    scores = cross_val_score(model, input, output, scoring='accuracy', cv=cv, n_jobs=1)
    return scores


def xgoal():
    input, output = setup_data()
    print(str(input))
    models = get_models_tree_depth()
    results, names = list(), list()
    for name, model in models.items():
        scores = evaluate_model(model, input, output)
        results.append(scores)
        names.append(name)
        print('>%s %.3f (%.3f)' % (name, mean(scores), std(scores)))

    pyplot.boxplot(results, labels=names, showmeans=True)
    pyplot.show()


if __name__ == '__main__':
    xgoal()
    #grid_search()







# model = GradientBoostingRegressor()
# print('model created')
# cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
# print('folds completed')
# n_scores = cross_val_score(model, input, output, scoring='neg_mean_absolute_error', cv=cv, n_jobs=-1)
# print('MAE: %.3f (%.3f)' % (mean(n_scores), std(n_scores)))

# model.fit(input, output)
# row=[1, 0.038990, 0.021253, 0.006944, 0, 0, 0, 0, 1, 0, 0]
# p = model.predict([row])
# print('prediction: %d' % p[0])
