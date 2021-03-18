from flask import Flask, jsonify, request, render_template, redirect, url_for

# API controllers
import backend.nhl_apis as nhl
import backend.nfl_apis as nfla

# NHL imports
import nhl_game_scraper as ngs
import nhl_single_game as nhlsg
import nhl_skater as nhlsk

#NFL imports
import nfl_qbs as qbs




app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('home.html', **locals())

############
# API Plan #
############
# /team/<league>/<team>

# /league/<league> (maybe make conference and division on page filters)

# /players/<league>
# /players/<league>/<player>
# /players/<league>/<team>
# /players/<league>/<position>

# /matchup/<league>/<game> (figure some idea for the game param to identify specific games)



@app.route('/league/<league>', methods=['GET'], defaults={'team': None})
@app.route('/league/<league>/<team>', methods=['GET'])
def league(league=None, team=None):
    if league is None:
        return redirect(url_for('home'))
    if league=='NHL':
        if team==None:
            league_stats = nhl.get_league_stats(2020, 2020)
            return render_template('nhl_league.html', **locals())
        else:
            team_stats = nhl.get_team_stats(team, 2020)
            return render_template('nhl_team.html', **locals())
    elif league=='NFL':
        if team==None:
            league_stats = nfla.get_league_stats(2020)
            return render_template('nfl_league.html', **locals())
        else:
            team_stats = nfla.get_team_stats(team, 2020)
            return render_template('nfl_team.html', **locals())
    else:
        return redirect(url_for('home'))




@app.route('/pdo', methods=['GET'])
def pdo():
    pdos = api.get_team_pdos()
    return render_template('pdo.html', **locals())


@app.route('/radar', methods=['GET'])
def radar():
    return render_template('radar.html')


@app.route('/player_score', methods=['GET'])
def player_score():
    player_stats = qbs.get_player_stats()
    return render_template('player_score.html', **locals())


@app.route('/nfl', methods=['GET'])
def nfl():
    qbs = api.get_epa(2020)
    return render_template('nfl.html', **locals())


@app.route('/nhl_game', methods=['GET'])
def nhl_game():
    url = "https://www.espn.com/nhl/playbyplay/_/gameId/401272216"
    #url="https://www.espn.com/nhl/playbyplay/_/gameId/401272337"
    #url = "https://www.espn.com/nhl/playbyplay/_/gameId/401272139"
    game_obj = ngs.get_shots(url)
    return render_template('nhl_game.html', **locals())


@app.route('/nhl_team', methods=['GET'])
def nhl_team():

    teams = ['Buffalo Sabres', 'Boston Bruins', 'New York Islanders', 'New York Rangers', 'Philadelphia Flyers', 'New Jersey Devils', 'Washington Capitals']
    team_obj = nhlt.get_team_radar(teams)
    rolling_xGF_obj = nhlt.get_rolling_xGF(['Washington Capitals', 'Buffalo Sabres'])
    goal_share_obj = nhlt.get_goal_share(teams)
    xgoal_share_obj = nhlt.get_expected_goal_share(teams)

    return render_template('nhl_team.html', **locals())


@app.route('/nhl_single_team', methods=['GET'])
def nhl_single_team():
    team = 'Buffalo Sabres'
    skater_stats = nhlst.get_skater_stats(team)
    return render_template('nhl_single_team.html', **locals())


@app.route('/nhl_single_game', methods=['GET'])
def nhl_single_game():
    game_stats = nhlsg.get_game_stats()
    return render_template('nhl_single_game.html', **locals())


@app.route('/nhl_skater', methods=['GET'])
def nhl_skater():
    player = 'Jeff Skinner'
    seasons = list(range(2010, 2021))
    skater_stats = nhlsk.get_scoring_locations(player, seasons)
    return render_template('nhl_skater.html', **locals())


@app.route('/nfl_qbs', methods=['GET'])
def nfl_qbs():
    qb = 'C.Newton'
    seasons = list(range(2020, 2021))

    qb_stats = qbs.get_rolling_epa_and_cpoe(qb, seasons)
    epa_per_dropback = qbs.get_qb_epa_ranked(seasons)
    return render_template('nfl_qbs.html', **locals())

#################
### Just APIs ###
#################
#@app.route('/team_radar', methods=['GET'])
#def team_radar():
#    print('here')
#    print(str(request))
#    print(str(request.form))
#    teams = request.form['teams']
#    print(str(teams))
#    return nhlt.get_team_radar(teams)
