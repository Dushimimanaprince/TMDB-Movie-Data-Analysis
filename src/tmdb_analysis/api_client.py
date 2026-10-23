"""Fetch movie data from the TMDB API and save it to a local file."""

import json
import os
import time

import pandas as pd
import requests
from dotenv import load_dotenv

from tmdb_analysis import config


def get_api_key():
    """Read the TMDB API key from the .env file."""
    load_dotenv(config.PROJECT_ROOT / ".env")
    api_key = os.getenv("TMDB_API_KEY")

    if not api_key:
        raise ValueError("TMDB_API_KEY is missing. Copy .env.example to .env and add your key.")

    return api_key


def fetch_movie(movie_id, api_key):
    """Fetch one movie and its credits. Return a dict, or None if it fails."""
    url = f"{config.API_BASE_URL}/movie/{movie_id}"
    params = {"api_key": api_key, "append_to_response": "credits"}

    for attempt in range(1, config.MAX_RETRIES + 1):
        try:
            response = requests.get(url, params=params, timeout=config.REQUEST_TIMEOUT_SECONDS)
        except requests.RequestException as error:
            print(f"Movie {movie_id}: network error, attempt {attempt} ({error})")
            time.sleep(attempt)  # wait 1s, then 2s, then 3s
            continue

        if response.status_code == 200:
            return response.json()

        if response.status_code == 404:
            print(f"Movie {movie_id}: not found, skipping")
            return None

        if response.status_code == 401:
            raise ValueError("TMDB rejected the API key (401). Check your .env file.")

        if response.status_code == 429 or response.status_code >= 500:
            print(f"Movie {movie_id}: status {response.status_code}, retrying...")
            time.sleep(attempt)
            continue

        print(f"Movie {movie_id}: unexpected status {response.status_code}, skipping")
        return None

    print(f"Movie {movie_id}: failed after {config.MAX_RETRIES} attempts")
    return None


def fetch_movies(movie_ids, api_key):
    """Fetch every movie in the list and keep only the successful ones."""
    movies = []

    for movie_id in movie_ids:
        movie = fetch_movie(movie_id, api_key)
        if movie is not None:
            movies.append(movie)

    print(f"Fetched {len(movies)} of {len(movie_ids)} movies")
    return movies


def load_movies(refresh=False):
    """Return the raw movie data as a DataFrame.

    The first run calls the API and saves the result to data/raw/.
    Later runs read that saved file. Use refresh=True to call the API again.
    """
    path = config.RAW_DATA_PATH

    if path.exists() and not refresh:
        print(f"Loading saved data from {path}")
        with open(path, encoding="utf-8") as file:
            movies = json.load(file)
    else:
        api_key = get_api_key()
        movies = fetch_movies(config.MOVIE_IDS, api_key)

        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as file:
            json.dump(movies, file, indent=2)

    return pd.DataFrame(movies)