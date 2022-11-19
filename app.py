from flask import Flask, request, render_template, redirect, flash, jsonify, url_for, session
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.debug = True
debug = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route('/', methods=['GET'])
def start_game():
    """Creates the board for '/game' to display"""
    session['board'] = boggle_game.make_board()

    return render_template('home.html')

@app.route('/game', methods=['GET', 'POST'])
def game_page():
    """Displays high score, games played and board to the user"""
    highscore = session.get('highscore', 0)
    games_played = session.get('games_played', 0)

    return render_template('game.html', board=session['board'], highscore=highscore, games_played=games_played)

@app.route('/word_list')
def words():
    """Verifies users' guess is both a word and is on the board"""
    word = request.args['word']
    board = session['board']
    res = boggle_game.check_valid_word(board, word)

    return jsonify({'result': res})

@app.route('/score', methods=['POST'])
def track_score():
    """Check if user achieved a high score and updates the number of games played"""
    score = request.json['score']
    highscore = session.get('highscore', 0)
    games_played = session.get('games_played', 0)
    session['highscore'] = max(score, highscore)
    session['games_played'] = games_played + 1

    return jsonify(score)
