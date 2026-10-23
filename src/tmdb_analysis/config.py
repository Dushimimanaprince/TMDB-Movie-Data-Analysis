"""Central configuration: paths, movie IDs and API settings.

Every fixed value the pipeline depends on lives here, so the notebook and
any script read from one place. More settings are added in later phases.
"""

from __future__ import annotations

from pathlib import Path

# --------------------------------------------------------------------------- #
# Paths (built from this file's location, so they work from any folder)
# --------------------------------------------------------------------------- #
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_PATH = DATA_DIR / "raw" / "movies_raw.json"
CLEAN_DATA_PATH = DATA_DIR / "processed" / "tmdb_movies_clean.csv"

# --------------------------------------------------------------------------- #
# Movie IDs
# --------------------------------------------------------------------------- #
# The exact list required by the lab brief. ID 0 is deliberately invalid and
# tests the API client's 404 handling.
LAB_MOVIE_IDS: list[int] = [
    0, 299534, 19995, 140607, 299536, 597, 135397,
    420818, 24428, 168259, 99861, 284054, 12445,
    181808, 330457, 351286, 109445, 321612, 260513,
]

# None of the lab IDs star Bruce Willis or are directed by Quentin Tarantino,
# so the two required searches (Step 3.2) would always return empty tables.
# These IDs are added only so the searches can be demonstrated.
SEARCH_SUPPLEMENT_IDS: list[int] = [
    18,     # The Fifth Element (Bruce Willis, Sci-Fi/Action)
    95,     # Armageddon (Bruce Willis, Sci-Fi/Action)
    59967,  # Looper (Bruce Willis, Sci-Fi/Action)
    680,    # Pulp Fiction (Uma Thurman, Tarantino)
    24,     # Kill Bill: Vol. 1 (Uma Thurman, Tarantino)
    393,    # Kill Bill: Vol. 2 (Uma Thurman, Tarantino)
]
INCLUDE_SEARCH_SUPPLEMENT = True


def get_movie_ids() -> list[int]:
    """Return the IDs to fetch: the lab list, plus the search supplement if enabled.

    Order is kept and duplicates are removed.
    """
    ids = LAB_MOVIE_IDS + (SEARCH_SUPPLEMENT_IDS if INCLUDE_SEARCH_SUPPLEMENT else [])
    return list(dict.fromkeys(ids))


# --------------------------------------------------------------------------- #
# API
# --------------------------------------------------------------------------- #
API_BASE_URL = "https://api.themoviedb.org/3"
API_KEY_ENV_VAR = "TMDB_API_KEY"
REQUEST_TIMEOUT_SECONDS = 10
MAX_RETRIES = 3
RETRY_BACKOFF_FACTOR = 0.5            # waits 0.5s, 1s, 2s between retries
RETRY_STATUS_CODES = (429, 500, 502, 503, 504)