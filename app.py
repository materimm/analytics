from flask import Flask, jsonify, request, render_template
import api_controller as api
import nhl_game_scraper as ngs
import nhl_teams as nhlt

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html', **locals())


@app.route('/pdo', methods=['GET'])
def pdo():
    pdos = api.get_team_pdos()
    return render_template('pdo.html', **locals())


@app.route('/radar', methods=['GET'])
def radar():
    return render_template('radar.html')

@app.route('/player_score', methods=['GET'])
def player_score():
    player_stats = api.get_player_stats()
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

    rolling_xGF_obj = nhlt.get_rolling_xGF('Buffalo Sabres')

    return render_template('nhl_team.html', **locals())
