from flask import Flask, jsonify, request, render_template
import api_controller as api
import nhl_game_scraper as ngs

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
    #qbs = api.get_epa(2020)
    shots = ngs.get_shots()
    return render_template('nhl_game.html', **locals())
