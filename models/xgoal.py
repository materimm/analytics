from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedKFold, RepeatedStratifiedKFold, GridSearchCV, train_test_split
from sklearn.metrics import mean_squared_error
from numpy import mean, std, arange
import pandas as pd
from matplotlib import pyplot as plt
import pickle


def setup_data():
    df = pd.read_csv('../NHLData/moneypuck/shots/shots_2019.csv')

    #5v5 only
    df = df[(df.awaySkatersOnIce == 5) & (df.homeSkatersOnIce == 5)]
    #only shots on net
    df = df[df.shotWasOnGoal == 1]

    columns_to_use = ['time', 'goal', 'shotAngleAdjusted', 'shotDistance', 'shotType', 'offWing']
    df = df[columns_to_use]
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

# Best: -0.085554 using {'learning_rate': 0.01, 'max_depth': 4, 'n_estimators': 100, 'subsample': 0.3}
## n_splits=3 test_size=0.95 n_repeats=3
def grid_search():
    features, labels = setup_data()
    print(str(features))
    print(str(labels))
    xtrain, xtest, ytrain, ytest=train_test_split(features, labels, random_state=12, test_size=0.95)
    print(str(xtrain))
    model = GradientBoostingClassifier()
    grid = dict()
    grid['n_estimators'] = [10, 50, 100, 500]
    grid['learning_rate'] = [0.0001, 0.001, 0.01, 0.1, 1.0]
    grid['subsample'] = [0.3, 0.5, 0.7, 1.0]
    grid['max_depth'] = [2, 3, 4, 7, 9]

    cv = RepeatedStratifiedKFold(n_splits=3, n_repeats=3, random_state=1)
    print('folded')
    grid_search = GridSearchCV(estimator=model, param_grid=grid, n_jobs=-1, cv=cv, scoring='neg_mean_absolute_error')
    print('grid search cv created')
    grid_result = grid_search.fit(xtrain, ytrain)
    print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
    f = open("gridsearch.txt", "w")
    f.write("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
    f.close()
    means = grid_result.cv_results_['mean_test_score']
    stds = grid_result.cv_results_['std_test_score']
    params = grid_result.cv_results_['params']
    for mean, stdev, param in zip(means, stds, params):
        print("%f (%f) with: %r" % (mean, stdev, param))



def evaluate_model(model, input, output):
    cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
    scores = cross_val_score(model, input, output, scoring='accuracy', cv=cv, n_jobs=1)
    return scores


def eval_all_models():
    input, output = setup_data()
    print(str(input))
    models = get_models_learning_rate()
    results, names = list(), list()
    for name, model in models.items():
        scores = evaluate_model(model, input, output)
        results.append(scores)
        names.append(name)
        print('>%s %.7f (%.7f)' % (name, mean(scores), std(scores)))

    pyplot.boxplot(results, labels=names, showmeans=True)
    pyplot.show()


def xgoal_model():
    features, labels = setup_data()
    xtrain, xtest, ytrain, ytest=train_test_split(features, labels, random_state=12, test_size=0.25)
    # with new parameters
    gbc = GradientBoostingClassifier(n_estimators=100,
        max_depth=4,
        learning_rate=0.01,
        subsample=0.3)

    gbc.fit(xtrain, ytrain)
    save_model(gbc, 'xgoal_gbc.sav')

    ypred = gbc.predict(xtest)
    mse = mean_squared_error(ytest, ypred)
    print("MSE: %.5f" % mse)

    ## for sorted graph
    Z = [x for _,x in sorted(zip(ytest,ypred))]
    V = ytest.tolist()
    V.sort()
    x_ax = range(len(V))
    plt.scatter(x_ax, V, s=5, color="blue", label="original")
    plt.plot(x_ax, Z, lw=0.8, color="red", label="predicted")

    # x_ax = range(len(ytest))
    # plt.scatter(x_ax, ytest, s=5, color="blue", label="original")
    # plt.plot(x_ax, ypred, lw=0.8, color="red", label="predicted")

    plt.legend()
    plt.show()


def save_model(model, filename):
    # save the model to disk
    pickle.dump(model, open(filename, 'wb'))


def load_model(filename):
    # load the model from disk
    return pickle.load(open(filename, 'rb'))


xgoal_model()
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
