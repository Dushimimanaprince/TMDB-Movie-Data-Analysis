"""KPI calculations: profit, ROI and the 10 best/worst movie rankings (Step 3.1)."""

# Filters from the brief
MIN_BUDGET_FOR_ROI = 10   # million USD
MIN_VOTES_FOR_RATING = 10


def add_profit_and_roi(df):
    """Add profit_musd (revenue - budget) and roi (revenue / budget).

    If budget or revenue is NaN, the result is NaN too, so unknown
    values never turn into a fake profit or an infinite ROI.
    """
    df = df.copy()
    df["profit_musd"] = df["revenue_musd"] - df["budget_musd"]
    df["roi"] = df["revenue_musd"] / df["budget_musd"]
    return df


def rank_movies(df, column, ascending=False, min_budget=None, min_votes=None, top_n=5):
    """Return the top_n movies ranked by one column.

    ascending=True gives the lowest values first.
    min_budget / min_votes keep only movies that meet that minimum.
    """
    result = df[df[column].notna()]

    if min_budget is not None:
        result = result[result["budget_musd"] >= min_budget]

    if min_votes is not None:
        result = result[result["vote_count"] >= min_votes]

    result = result.sort_values(column, ascending=ascending).head(top_n)

    # Show the title, the ranked column, and budget/votes for context
    columns = ["title", column]
    for extra in ["budget_musd", "vote_count"]:
        if extra != column:
            columns.append(extra)

    result = result[columns]
    result.index = range(1, len(result) + 1)   # rank 1, 2, 3...
    return result


def get_all_kpis(df):
    """Run all 10 rankings from the brief and return them in a dictionary."""
    return {
        "Highest Revenue": rank_movies(df, "revenue_musd"),
        "Highest Budget": rank_movies(df, "budget_musd"),
        "Highest Profit": rank_movies(df, "profit_musd"),
        "Lowest Profit": rank_movies(df, "profit_musd", ascending=True),
        "Highest ROI (budget >= $10M)": rank_movies(df, "roi", min_budget=MIN_BUDGET_FOR_ROI),
        "Lowest ROI (budget >= $10M)": rank_movies(df, "roi", ascending=True, min_budget=MIN_BUDGET_FOR_ROI),
        "Most Voted": rank_movies(df, "vote_count"),
        "Highest Rated (>= 10 votes)": rank_movies(df, "vote_average", min_votes=MIN_VOTES_FOR_RATING),
        "Lowest Rated (>= 10 votes)": rank_movies(df, "vote_average", ascending=True, min_votes=MIN_VOTES_FOR_RATING),
        "Most Popular": rank_movies(df, "popularity"),
    }