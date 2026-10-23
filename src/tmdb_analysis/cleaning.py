"""Functions that clean the raw movie data (Step 2 of the brief)."""

import numpy as np
import pandas as pd

# Columns the brief says to remove
COLUMNS_TO_DROP = ["adult", "imdb_id", "original_title", "video", "homepage"]

# Text that means "no information" in overview and tagline
TEXT_PLACEHOLDERS = ["", "No Data", "No overview found.", "N/A"]

# The final column order required by the brief
FINAL_COLUMNS = [
    "id", "title", "tagline", "release_date", "genres", "belongs_to_collection",
    "original_language", "budget_musd", "revenue_musd", "production_companies",
    "production_countries", "vote_count", "vote_average", "popularity", "runtime",
    "overview", "spoken_languages", "poster_path", "cast", "cast_size", "director",
    "crew_size",
]

# Columns that hold a list like [{"name": "Action"}, {"name": "Drama"}]
LIST_COLUMNS = ["genres", "spoken_languages", "production_countries", "production_companies"]


def drop_irrelevant_columns(df):
    """Remove the columns we don't need."""
    return df.drop(columns=COLUMNS_TO_DROP, errors="ignore")


def extract_names(items):
    """Turn [{'name': 'Action'}, {'name': 'Drama'}] into 'Action|Drama'.

    Return NaN when there is nothing to extract.
    """
    if not isinstance(items, list) or len(items) == 0:
        return np.nan

    names = [item["name"] for item in items]
    return "|".join(names)


def get_collection_name(collection):
    """Return the name from {'id': 10, 'name': 'Avatar Collection'}, or NaN."""
    if isinstance(collection, dict):
        return collection["name"]
    return np.nan


def get_cast(credits):
    """Return all actor names as 'Actor A|Actor B', or NaN."""
    if not isinstance(credits, dict):
        return np.nan
    return extract_names(credits["cast"])


def get_cast_size(credits):
    """Return the number of actors, or NaN."""
    if not isinstance(credits, dict):
        return np.nan
    return len(credits["cast"])


def get_director(credits):
    """Return the director name(s) as 'Director A|Director B', or NaN."""
    if not isinstance(credits, dict):
        return np.nan

    directors = []
    for person in credits["crew"]:
        if person["job"] == "Director":
            directors.append(person["name"])

    if len(directors) == 0:
        return np.nan
    return "|".join(directors)


def get_crew_size(credits):
    """Return the number of crew members, or NaN."""
    if not isinstance(credits, dict):
        return np.nan
    return len(credits["crew"])


def flatten_json_columns(df):
    """Turn the nested JSON columns into simple text and numbers."""
    df = df.copy()

    df["belongs_to_collection"] = df["belongs_to_collection"].apply(get_collection_name)

    for column in LIST_COLUMNS:
        df[column] = df[column].apply(extract_names)

    df["cast"] = df["credits"].apply(get_cast)
    df["cast_size"] = df["credits"].apply(get_cast_size)
    df["director"] = df["credits"].apply(get_director)
    df["crew_size"] = df["credits"].apply(get_crew_size)

    df = df.drop(columns=["credits"])
    return df

def convert_dtypes(df):
    """Make number columns numeric and release_date a real date.

    Values that can't be converted become NaN (errors="coerce").
    """
    df = df.copy()

    for column in ["id", "budget", "revenue", "popularity", "runtime", "vote_count", "vote_average"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    return df


def replace_zeros_with_nan(df):
    """A budget, revenue or runtime of 0 means "unknown", so replace it with NaN."""
    df = df.copy()

    for column in ["budget", "revenue", "runtime"]:
        df[column] = df[column].replace(0, np.nan)

    return df


def convert_to_musd(df):
    """Add budget_musd and revenue_musd (millions of USD) and remove the raw columns.

    Run this AFTER replace_zeros_with_nan, otherwise an unknown budget
    becomes 0.0 instead of NaN.
    """
    df = df.copy()

    df["budget_musd"] = df["budget"] / 1_000_000
    df["revenue_musd"] = df["revenue"] / 1_000_000

    df = df.drop(columns=["budget", "revenue"])
    return df   

def fix_zero_votes(df):
    """If nobody voted, the vote_average means nothing, so make it NaN."""
    df = df.copy()
    df.loc[df["vote_count"] == 0, "vote_average"] = np.nan
    return df


def replace_text_placeholders(df):
    """Replace placeholder text like "No Data" in overview and tagline with NaN."""
    df = df.copy()

    for column in ["overview", "tagline"]:
        df[column] = df[column].str.strip()  # "   " becomes "", which is a placeholder
        df[column] = df[column].replace(TEXT_PLACEHOLDERS, np.nan)

    return df

def remove_bad_rows(df):
    """Remove duplicates, rows without id or title, rows with too little data,
    and movies that are not released yet."""
    df = df.drop_duplicates(subset="id")
    df = df.dropna(subset=["id", "title"])
    df = df.dropna(thresh=10)                # keep rows with at least 10 non-NaN values
    df = df[df["status"] == "Released"]
    df = df.drop(columns=["status"])
    return df


def finalize_columns(df):
    """Put the columns in the order the brief asks for and reset the index."""
    df = df[FINAL_COLUMNS]                   # raises an error if a column is missing
    df = df.reset_index(drop=True)
    return df