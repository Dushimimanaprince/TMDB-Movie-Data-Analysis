"""Settings used by the whole project: file paths, movie IDs and API settings."""

from pathlib import Path

# ---------------- Paths ----------------
# This file is at: TMDB-Movie-Data-Analysis/src/tmdb_analysis/config.py
# Going up 3 folders (.parent three times) gives the project folder.
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "movies_raw.json"
CLEAN_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "tmdb_movies_clean.csv"

# ---------------- Movie IDs ----------------
# The IDs required by the lab brief.
# ID 0 does not exist on purpose: it tests that we handle "not found" (404).
LAB_MOVIE_IDS = [
    0, 299534, 19995, 140607, 299536, 597, 135397,
    420818, 24428, 168259, 99861, 284054, 12445,
    181808, 330457, 351286, 109445, 321612, 260513,
]

# None of the lab movies star Bruce Willis or are directed by Quentin Tarantino,
# so the two search questions would return nothing. These extra movies fix that.
SEARCH_MOVIE_IDS = [
    18,     # The Fifth Element (Bruce Willis)
    95,     # Armageddon (Bruce Willis)
    59967,  # Looper (Bruce Willis)
    680,    # Pulp Fiction (Uma Thurman, Tarantino)
    24,     # Kill Bill: Vol. 1 (Uma Thurman, Tarantino)
    393,    # Kill Bill: Vol. 2 (Uma Thurman, Tarantino)
]

# All the movies we fetch
MOVIE_IDS = LAB_MOVIE_IDS + SEARCH_MOVIE_IDS

# ---------------- API ----------------
API_BASE_URL = "https://api.themoviedb.org/3"
REQUEST_TIMEOUT_SECONDS = 10   # give up on a request after 10 seconds
MAX_RETRIES = 3                # try a failed request up to 3 times