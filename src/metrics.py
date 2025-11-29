import pytest
import pandas as pd

def get_avg_duration(df):
    """
    US-02: Calculate average trip duration in minutes.
    - Excludes outliers > 24 hours.
    - Returns 0 for empty or invalid input.
    """

    if df is None or "trip_duration_seconds" not in df:
        raise ValueError("df must contain 'trip_duration_seconds' column")

    if df.empty:
        return 0

    # 24 hours in seconds
    MAX_DURATION = 24 * 60 * 60  

    # Filter outliers
    valid = df[df["trip_duration_seconds"] <= MAX_DURATION]

    if valid.empty:
        return 0

    avg_seconds = valid["trip_duration_seconds"].mean()

    # convert to minutes
    return avg_seconds / 60

def get_total_trips(df):
    """
    US-01 Sprint 1:
    Return total number of trips (row count).
    """
    if df is None:
        raise ValueError("df must not be None")

    return int(len(df))

def get_bike_usage(df: pd.DataFrame) -> pd.DataFrame:
    """
    US-03: Bike Usage

    Group trips by bike_id and sum total trip_duration_seconds per bike.

    Returns
    -------
    DataFrame
        Columns:
            - bike_id
            - total_duration_seconds
        One row per bike, sorted by total_duration_seconds (descending).

    Sprint 1 scope:
        - Sum duration per bike.
        - Handle empty DataFrame gracefully.
    """

    if df is None:
        raise ValueError("df must not be None")

    required_cols = {"bike_id", "trip_duration_seconds"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"df is missing required columns: {missing}")

    # If no rows, return an empty DataFrame with the expected columns
    if df.empty:
        return pd.DataFrame(columns=["bike_id", "total_duration_seconds"])

    # Group by bike_id and sum duration
    grouped = (
        df.groupby("bike_id", as_index=False)["trip_duration_seconds"]
        .sum()
        .rename(columns={"trip_duration_seconds": "total_duration_seconds"})
        .sort_values("total_duration_seconds", ascending=False)
    )

    return grouped
