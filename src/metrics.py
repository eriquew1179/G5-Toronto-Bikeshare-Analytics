# src/metrics.py

from __future__ import annotations

from typing import Optional, Dict, List

import pandas as pd

# 24 hours in seconds – used for outlier detection
MAX_DURATION_SECONDS = 24 * 60 * 60


# -------------------------------------------------------------------
# Internal helper utilities (not part of the public API)
# -------------------------------------------------------------------
def _first_existing_column(df: pd.DataFrame, candidates: List[str]) -> Optional[str]:
    """Return the first column name from `candidates` that exists in `df`."""
    return next((c for c in candidates if c in df.columns), None)


def _is_empty(df: Optional[pd.DataFrame]) -> bool:
    """Small helper so we write the None/empty check only once."""
    return df is None or df.empty


# -------------------------------------------------------------------
# US-01 – Total Volume KPI
# -------------------------------------------------------------------
def get_total_trips(
    df: pd.DataFrame,
    start: Optional[pd.Timestamp] = None,
    end: Optional[pd.Timestamp] = None,
) -> int:
    """
    US-01: Total Volume KPI

    Returns the total number of trips (row count). Optionally accepts a
    date/time filter using the 'Start Time' column.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame where each row represents a trip.
    start : pd.Timestamp or datetime-like, optional
        Lower bound (inclusive) for Start Time filter.
    end : pd.Timestamp or datetime-like, optional
        Upper bound (inclusive) for Start Time filter.

    Returns
    -------
    int
        Number of trips after applying the optional date filter.
        Returns 0 if df is None or empty.
    """
    if _is_empty(df):
        return 0

    # If no filter requested, just return the row count
    if start is None and end is None:
        return int(len(df))

    # Only apply filter if we actually have a "Start Time" column
    if "Start Time" in df.columns:
        mask = pd.Series(True, index=df.index)

        if start is not None:
            mask &= df["Start Time"] >= pd.to_datetime(start)

        if end is not None:
            mask &= df["Start Time"] <= pd.to_datetime(end)

        df = df.loc[mask]

    return int(len(df))


# -------------------------------------------------------------------
# US-02 – Average Trip Duration
# -------------------------------------------------------------------
def get_avg_duration(df: pd.DataFrame) -> float:
    """
    US-02: Average Trip Duration

    Calculates the average trip duration in minutes, handling outliers and
    using vectorized operations for speed.

    Behaviour
    ---------
    - Uses 'trip_duration_seconds' as the primary column.
    - Falls back to 'Trip Duration' or 'amount' if needed.
    - Excludes outliers > 24 hours (86,400 seconds).
    - Returns 0.0 if the DataFrame is None/empty or no valid column exists.
    """
    if _is_empty(df):
        return 0.0

    duration_cols = ["trip_duration_seconds", "Trip Duration", "amount"]
    col_name = _first_existing_column(df, duration_cols)
    if col_name is None:
        return 0.0

    # Vectorized numeric conversion
    duration_sec = pd.to_numeric(df[col_name], errors="coerce")

    # Remove negative values and > 24-hour outliers
    duration_sec = duration_sec[
        (duration_sec >= 0) & (duration_sec <= MAX_DURATION_SECONDS)
    ]

    if duration_sec.empty:
        return 0.0

    avg_seconds = duration_sec.mean()
    return float(avg_seconds) / 60.0  # convert to minutes


# -------------------------------------------------------------------
# US-03 – Bike Usage
# -------------------------------------------------------------------
def get_bike_usage(
    df: pd.DataFrame,
    top_n: int = 10,
    extreme_threshold: float = 0.95,
) -> pd.DataFrame:
    """
    US-03: Bike Usage

    Groups trips by bike ID and sums total duration per bike, returning the
    bikes with the highest usage.

    Sprint 2 Enhancements
    ---------------------
    - Flags "extreme usage" bikes using a quantile threshold.
    - Returns the Top N most-used bikes (default: 10).

    Parameters
    ----------
    df : pd.DataFrame
        Input trip data.
    top_n : int, optional
        Number of bikes to return, ordered by total usage (desc).
    extreme_threshold : float, optional
        Quantile (0–1) used to flag extreme-usage bikes.
        Example: 0.95 = bikes in the top 5% by usage.

    Returns
    -------
    pd.DataFrame
        Columns:
        - 'bike_id': identifier of the bike
        - 'total_duration_seconds': summed duration per bike
        - 'is_extreme': True if bike is above the usage threshold

        Returns an empty DataFrame with these columns if df is None/empty
        or required columns are missing.
    """
    empty_result = pd.DataFrame(
        columns=["bike_id", "total_duration_seconds", "is_extreme"]
    )

    if _is_empty(df):
        return empty_result

    id_col = _first_existing_column(df, ["bike_id", "Bike Id", "Bike ID", "customer_id"])
    dur_col = _first_existing_column(df, ["trip_duration_seconds", "Trip Duration", "amount"])

    if id_col is None or dur_col is None:
        return empty_result

    df = df.copy()
    df[dur_col] = pd.to_numeric(df[dur_col], errors="coerce")

    grouped = (
        df.groupby(id_col)[dur_col]
        .sum()
        .reset_index()
        .rename(columns={id_col: "bike_id", dur_col: "total_duration_seconds"})
    )

    if grouped.empty:
        return empty_result

    # Sort by usage
    grouped = grouped.sort_values("total_duration_seconds", ascending=False)

    # Compute extreme-usage flag using quantile
    cutoff = grouped["total_duration_seconds"].quantile(extreme_threshold)
    grouped["is_extreme"] = grouped["total_duration_seconds"] >= cutoff

    # Return Top N bikes
    return grouped.head(top_n).reset_index(drop=True)


# -------------------------------------------------------------------
# US-04 – User Type Split
# -------------------------------------------------------------------
def get_user_type_breakdown(
    df: pd.DataFrame,
    return_percentages: bool = False,
) -> Dict[str, float]:
    """
    US-04: User Type Split

    Groups by user_type and returns either raw counts or percentage
    breakdown, ready for plotting.

    Sprint 1 Behaviour
    ------------------
    - When `return_percentages=False` (default), returns raw counts:
      {"Member": 1234, "Casual": 567, ...}

    Sprint 2 Enhancements
    ---------------------
    - When `return_percentages=True`, returns a 0–100 percentage breakdown:
      {"Member": 68.4, "Casual": 31.6}

    Parameters
    ----------
    df : pd.DataFrame
        Input data containing a user-type column.
    return_percentages : bool, optional
        False -> return counts (int).
        True  -> return percentages (float).

    Returns
    -------
    dict
        Mapping from user-type label to count or percentage.
        Returns {} if df is None/empty or no user-type column is found.
    """
    if _is_empty(df):
        return {}

    col_name = _first_existing_column(df, ["user_type", "User Type", "type"])
    if col_name is None:
        return {}

    counts = df[col_name].value_counts(dropna=True)

    if not return_percentages:
        # Sprint 1-style: raw counts
        return counts.to_dict()

    total = counts.sum()
    if total == 0:
        return {}

    percentages = (counts / total * 100).round(1)  # 1 decimal place
    return percentages.to_dict()
