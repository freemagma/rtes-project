from requests_html import HTMLSession
import requests
import os
from urllib.parse import urlparse

CROSSWORDFIEND_URL = "https://crosswordfiend.com/download/"
PUZZLE_DIR = "src/resources/"


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


def get_url_filename(url):
    return os.path.basename(urlparse(url).path)


if __name__ == "__main__":
    scrape_crosswordfiend()
