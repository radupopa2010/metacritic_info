import json
import	unittest
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from metacritic.scraper import game_get_ts, get_games, URL, app, TOP_PS_GAMES


class TestScraper(unittest.TestCase):
    """Test the scraper."""
    games_container = None
    # Using setUpClass instead of setUp saves unnecessary page loads;
    def setUpClass():
        global games_container
        url = URL
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req)
        bs_obj = BeautifulSoup(html.read(), "html.parser")
        games_container = bs_obj.findAll("div", {"class": "product_basics stats"})

    def test_games_container_has_ten_elements(self):
        global games_container
        self.assertEqual(10, len(games_container))

    def test_first_game_is_shadow_of_the_colossus(self):
        global games_container
        self.assertEqual(
            {'title': 'Shadow of the Colossus', 'score': 92},
            game_get_ts(games_container[0]))

    def test_last_game_is_iconoclasts(self):
        global games_container
        self.assertEqual(
            {'title': 'Iconoclasts', 'score': 83},
            game_get_ts(games_container[-1]))

    def test_get_games_saves_list_of_ten_objects(self):
        with open(TOP_PS_GAMES, 'r') as fh:
            top_g = json.load(fh)
        self.assertEqual(10, len(top_g))


class TestApp(unittest.TestCase):
    """Test the Flask app"""
    get_games(URL)

    def setUp(self):
        # fix a bug in the flask
        app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False
        # test client can use to send requests to and then test the responses.
        self.app = app.test_client()

    def test_get_games_api_returns_valid_json(self):
        response = self.app.get('/games/')
        self.assertTrue(json.loads(response.get_data(as_text=True)))

    def test_get_games_api_returns_ten_games(self):
        response = self.app.get('/games/')
        self.assertEqual(10, len(json.loads(response.get_data(as_text=True))))

    def test_get_games_api_returns_valid_data(self):
        response = self.app.get('/games/')
        self.assertTrue(
            'Shadow of the Colossus' in response.get_data(as_text=True))
        self.assertTrue(
            'Street Fighter V: Arcade Edition' in response.get_data(as_text=True))
        self.assertTrue(
            'Iconoclasts' in response.get_data(as_text=True))

    def test_get_game_api_returns_valid_json(self):
        top_resp = self.app.get('/games/')
        top_games = json.loads(top_resp.get_data(as_text=True))
        response = self.app.get('/games/' + top_games[0])
        self.assertTrue(json.loads(response.get_data(as_text=True)))

    def test_get_game_api_returns_valid_data(self):
        top_resp = self.app.get('/games/')
        top_games = json.loads(top_resp.get_data(as_text=True))
        response = self.app.get('/games/' + top_games[0])
        self.assertEqual(
            {'title': 'Shadow of the Colossus', 'score': 92},
            json.loads(response.get_data(as_text=True)))
