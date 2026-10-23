"""Search queries (Step 3.2) and franchise / director analysis (Steps 3.3-3.5)."""


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