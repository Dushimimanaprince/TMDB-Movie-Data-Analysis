"""Search queries (Step 3.2) and franchise / director analysis (Steps 3.3-3.5)."""
import numpy as np

def contains_all(text, items):
    """Return True if every item is one of the values in a pipe-separated text.

    Example: contains_all("Action|Science Fiction", ["Action"]) -> True
    It compares whole values, so "Bruce Willis" does not match "Bruce Willis Jr.".
    """
    if not isinstance(text, str):   # NaN (missing) never matches
        return False

    values = text.split("|")
    for item in items:
        if item not in values:
            return False
    return True


def search_bruce_willis_scifi_action(df):
    """Search 1: Science Fiction Action movies starring Bruce Willis, best rated first."""
    is_scifi_action = df["genres"].apply(lambda genres: contains_all(genres, ["Science Fiction", "Action"]))
    has_bruce_willis = df["cast"].apply(lambda cast: contains_all(cast, ["Bruce Willis"]))

    result = df[is_scifi_action & has_bruce_willis]
    result = result.sort_values("vote_average", ascending=False)
    return result[["title", "vote_average", "genres"]]


def search_uma_thurman_tarantino(df):
    """Search 2: movies starring Uma Thurman directed by Quentin Tarantino, shortest first."""
    has_uma_thurman = df["cast"].apply(lambda cast: contains_all(cast, ["Uma Thurman"]))
    by_tarantino = df["director"].apply(lambda director: contains_all(director, ["Quentin Tarantino"]))

    result = df[has_uma_thurman & by_tarantino]
    result = result.sort_values("runtime", ascending=True)
    return result[["title", "runtime", "director"]]

def add_franchise_status(df):
    """Add a column: "Franchise" if the movie belongs to a collection, otherwise "Standalone"."""
    df = df.copy()
    df["franchise_status"] = np.where(df["belongs_to_collection"].isna(), "Standalone", "Franchise")
    return df


def compare_franchise_vs_standalone(df):
    """Compare franchise and standalone movies on the 5 metrics from the brief.

    ROI uses the median because one very successful movie can pull the mean up a lot.
    """
    result = df.groupby("franchise_status").agg(
        movies=("id", "count"),
        mean_revenue_musd=("revenue_musd", "mean"),
        median_roi=("roi", "median"),
        mean_budget_musd=("budget_musd", "mean"),
        mean_popularity=("popularity", "mean"),
        mean_rating=("vote_average", "mean"),
    )
    return result.round(2)

def get_top_franchises(df):
    """Most successful franchises, ranked by total revenue."""
    franchises = df[df["belongs_to_collection"].notna()]

    result = franchises.groupby("belongs_to_collection").agg(
        movies=("id", "count"),
        total_budget_musd=("budget_musd", "sum"),
        mean_budget_musd=("budget_musd", "mean"),
        total_revenue_musd=("revenue_musd", "sum"),
        mean_revenue_musd=("revenue_musd", "mean"),
        mean_rating=("vote_average", "mean"),
    )
    result = result.sort_values("total_revenue_musd", ascending=False)
    return result.round(2)


def get_top_directors(df):
    """Most successful directors, ranked by total revenue.

    A movie with two directors ("Anthony Russo|Joe Russo") counts for both of them.
    """
    directors = df.copy()
    directors["director"] = directors["director"].str.split("|")   # text -> list of names
    directors = directors.explode("director")                       # one row per director
    directors = directors[directors["director"].notna()]

    result = directors.groupby("director").agg(
        movies=("id", "count"),
        total_revenue_musd=("revenue_musd", "sum"),
        mean_rating=("vote_average", "mean"),
    )
    result = result.sort_values("total_revenue_musd", ascending=False)
    return result.round(2)