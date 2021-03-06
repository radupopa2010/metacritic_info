# metacritic_scraper

Scrape top 10 PlayStation games found at 
http://www.metacritic.com/game/playstation-4 and expose result as a REST API.

## Install
After cloning the repo, use [virtualenvwrapper:](https://virtualenvwrapper.readthedocs.io/en/latest/)

```bash
cd metacritic_info
mkvirtualenv metacritic_scraper
pip install -r requirements.txt
```

### Run the testcases, from the main directory, metacritic_info
```bash
python -m unittest 

```
### Run the application
```bash
python metacritic/scraper.py
```


Open the browser at http://127.0.0.1:5000/games/ and you should see the
results.

And go to http://127.0.0.1:5000/games/<game> to see details about a game.
