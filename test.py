from unittest import TestCase
from app import app
# start_game, game_page, words, track_score
from flask import Flask, session, request
from boggle import Boggle

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['TESTING'] = True

boggle_game = Boggle()

class FlaskTests(TestCase):
    def test_start_game(self):
        """Verify menu HTML elements are being properly generated"""
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 id="welcome">Welcome to Boggle!</h1>', html)

    def test_game_page(self):
            """Verify board HTML elements are being properly generated"""
            """Verify session data is stored properly"""
            with app.test_client() as client:
                    with client.session_transaction() as change_session:
                        change_session['highscore'] = 10
                        change_session['games_played'] = 1
                        change_session['board'] = [
                            ['G', 'U', 'E', 'S', 'S'],
                            ['W', 'S', 'D', 'F', 'G'],
                            ['O', 'S', 'D', 'F', 'G'],
                            ['R', 'S', 'D', 'F', 'G'],
                            ['D', 'S', 'D', 'F', 'G']
                        ]
                    resp = client.get('/game')
                    html = resp.get_data(as_text=True)

                    self.assertEqual(resp.status_code, 200)
                    self.assertIn('<td></td>', html)

    def test_words(self):
        """Verify that word validation is functioning"""
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [
                    ['G', 'U', 'E', 'S', 'S'],
                    ['W', 'S', 'D', 'F', 'G'],
                    ['O', 'S', 'D', 'F', 'G'],
                    ['R', 'S', 'D', 'F', 'G'],
                    ['D', 'S', 'D', 'F', 'G']
                ]

            resp = client.get('/word_list', query_string={'word': 'guess'})

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(boggle_game.check_valid_word(session['board'], 'guess'), 'ok')
            self.assertEqual(boggle_game.check_valid_word(session['board'], 'check'), 'not-on-board')
            self.assertEqual(boggle_game.check_valid_word(session['board'], 'asdf'), 'not-word')

    def test_track_score(self):
        """Verify json data is being received"""
        """Verify highscore value is updated when score is higher than previous highscore value"""
        """Verify games_played is updated """
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['highscore'] = 5
                change_session['games_played'] = 9

            client.post('/score', json={'score': 10})

            self.assertEqual(session['highscore'], 10)
            self.assertEqual(session['games_played'], 10)
            self.assertEqual(request.json, {'score': 10})
