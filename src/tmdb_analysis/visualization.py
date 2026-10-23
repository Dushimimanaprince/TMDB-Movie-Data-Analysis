"""The five charts required by the brief (Step 4), made with Matplotlib.

Each function returns the figure, so the notebook can show it and save it.
"""

import matplotlib.pyplot as plt

from tmdb_analysis.analysis import compare_franchise_vs_standalone
from tmdb_analysis.kpis import MIN_BUDGET_FOR_ROI


def plot_revenue_vs_budget(df):
    """Scatter plot of revenue against budget, with a break-even line."""
    fig, ax = plt.subplots(figsize=(9, 6))

    franchise = df[df["franchise_status"] == "Franchise"]
    standalone = df[df["franchise_status"] == "Standalone"]
    ax.scatter(franchise["budget_musd"], franchise["revenue_musd"], alpha=0.7, label="Franchise")
    ax.scatter(standalone["budget_musd"], standalone["revenue_musd"], alpha=0.7, label="Standalone")

    # Points above this line earned more than they cost
    max_budget = df["budget_musd"].max()
    ax.plot([0, max_budget], [0, max_budget], "k--", label="Break-even (revenue = budget)")

    ax.set_title("Revenue vs. Budget")
    ax.set_xlabel("Budget (million USD)")
    ax.set_ylabel("Revenue (million USD)")
    ax.legend()
    return fig


def plot_roi_by_genre(df):
    """Box plot of ROI for each genre (movies with budget >= $10M, genres with 2+ movies)."""
    data = df[df["budget_musd"] >= MIN_BUDGET_FOR_ROI].copy()
    data["genre"] = data["genres"].str.split("|")
    data = data.explode("genre")

    genre_counts = data["genre"].value_counts()
    genres = genre_counts[genre_counts >= 2].index

    roi_per_genre = []
    for genre in genres:
        roi_per_genre.append(data[data["genre"] == genre]["roi"].dropna())

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.boxplot(roi_per_genre)
    ax.set_xticklabels(genres, rotation=45)
    ax.axhline(1, color="grey", linestyle="--", label="ROI = 1 (break-even)")

    ax.set_title("ROI Distribution by Genre (budget >= $10M)")
    ax.set_xlabel("Genre")
    ax.set_ylabel("ROI (revenue / budget)")
    ax.legend()
    fig.tight_layout()
    return fig


def plot_popularity_vs_rating(df):
    """Scatter plot of popularity against rating, with the correlation in the title."""
    correlation = df["vote_average"].corr(df["popularity"])

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.scatter(df["vote_average"], df["popularity"], alpha=0.7)

    ax.set_title(f"Popularity vs. Rating (correlation = {correlation:.2f})")
    ax.set_xlabel("Average rating")
    ax.set_ylabel("Popularity score")
    return fig


def plot_yearly_box_office(df):
    """Total revenue per release year (bars) and mean revenue per movie (line)."""
    years = df["release_date"].dt.year
    yearly = df.groupby(years)["revenue_musd"].agg(["sum", "mean"])

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.bar(yearly.index, yearly["sum"], alpha=0.7, label="Total revenue")
    ax.plot(yearly.index, yearly["mean"], "o--", color="orange", label="Mean revenue per movie")

    ax.set_title("Yearly Box Office Performance")
    ax.set_xlabel("Release year")
    ax.set_ylabel("Revenue (million USD)")
    ax.legend()
    return fig


def plot_franchise_vs_standalone(df):
    """One small bar chart per metric, because the metrics use very different scales."""
    summary = compare_franchise_vs_standalone(df)
    metrics = ["mean_revenue_musd", "mean_budget_musd", "median_roi", "mean_popularity", "mean_rating"]

    fig, axes = plt.subplots(1, len(metrics), figsize=(16, 4))
    for ax, metric in zip(axes, metrics):
        ax.bar(summary.index, summary[metric], color=["tab:blue", "tab:orange"])
        ax.set_title(metric)

    fig.suptitle("Franchise vs. Standalone Movies")
    fig.tight_layout()
    return fig