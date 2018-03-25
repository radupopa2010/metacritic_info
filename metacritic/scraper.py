#!/usr/bin/env python

import json
from urllib.error import HTTPError
from urllib.request import Request
from urllib.request import urlopen

from bs4 import BeautifulSoup
from flask import Flask, jsonify

URL = "http://www.metacritic.com/game/playstation-4"
# Save the results in a file
TOP_PS_GAMES = 'metacritic_results.json'

def game_get_ts(game_container):
    """Helper func to extract values for a game
    Args:
        game_container: BeautifulSoupObject
    Returns:
        Dict
    """
    title = game_container.find("",{"class": "product_title"}).get_text()
    score = game_container.find("",{"class": "metascore_w"}).get_text()
    return {"title": title, "score": int(score)}


def get_games(url):
    """Scrape all games found at 'url'
    Args:
        url: String
    Return:
        Side effect: save result in TOP_PS_GAMES
    """
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urlopen(req)
    except HTTPError as e:
        print("Could not open url", url)
        raise ValueError(e)
    try:
        bs_obj = BeautifulSoup(html.read(), "html.parser")
        games_container = bs_obj.findAll("div", {"class": "product_basics stats"})
    except AttributeError as e:
        raise ValueError("Could not read html")
    with open(TOP_PS_GAMES, 'w') as fh:
        json.dump([game_get_ts(c) for c in games_container], fh)


# create the application object
app = Flask(__name__)

@app.route("/games/", methods=["GET"])
def get_games_api():
    with open(TOP_PS_GAMES, 'r') as fh:
        top_games = json.load(fh)
    return jsonify([g["title"] for g in top_games])


@app.route("/games/<title>", methods=["GET"])
def get_game_api(title):
    with open(TOP_PS_GAMES, 'r') as fh:
        top_games = json.load(fh)
    for game in top_games:
        if game["title"] == title:
            return jsonify(game)


if __name__ == "__main__":
    try:
        # Scrape the web page and save results to TOP_PS_GAMES
        get_games(URL)
    except ValueError:
        print("Could not scrape", URL)
    app.run()

