"""Exploratory data analysis: missing values, summary statistics and outliers."""

import pandas as pd


def missing_values(df):
    """Count missing values per column, showing only columns that have some."""
    missing = df.isna().sum()
    percent = (missing / len(df) * 100).round(1)

    result = pd.DataFrame({"missing": missing, "percent": percent})
    result = result[result["missing"] > 0]
    return result.sort_values("missing", ascending=False)


def summary_statistics(df):
    """describe() for the number columns (id is left out because it is just a label)."""
    numbers = df.select_dtypes("number").drop(columns=["id"])
    return numbers.describe().T.round(2)


def find_outliers(df, column):
    """Return movies with an unusually low or high value, using the IQR rule.

    IQR = Q3 - Q1. A value is an outlier if it is below Q1 - 1.5*IQR
    or above Q3 + 1.5*IQR.
    """
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    outliers = df[(df[column] < lower) | (df[column] > upper)]
    return outliers[["title", column]].sort_values(column, ascending=False)