from requests_html import HTMLSession
import requests
import os
import puz
from urllib.parse import urlparse

from src import crud, models, schemas
from src.api import deps

CROSSWORDFIEND_URL = "https://crosswordfiend.com/download/"
BACKEND_URL = "http://localhost:5001"
PUZZLE_DIR = "../resources/"


def scrape_crosswordfiend():
    current_puzzles = set(os.listdir(PUZZLE_DIR))

    session = HTMLSession()
    response = session.get(CROSSWORDFIEND_URL)
    response.html.render()

    for link in response.html.links:
        filename = get_url_filename(link)
        if not str(filename).endswith(".puz") or filename in current_puzzles:
            continue
        print(f"Downloading {filename}")
        with open(f"{PUZZLE_DIR}/{filename}", "wb") as f:
            f.write(requests.get(link).content)
        blank_crossword = {
            'title': get_title_from_filename(filename),
            'puzfilename': filename 
        }
        requests.post(BACKEND_URL + "/crosswords", data=blankcrossword)


def get_url_filename(url):
    return os.path.basename(urlparse(url).path)


def get_title_from_filename(filename):
        puzzle = puz.read(f"app/src/resources/{filename}")
        title = f"{puzzle.title}  {puzzle.copyright}"
        return title


if __name__ == "__main__":
    scrape_crosswordfiend()
