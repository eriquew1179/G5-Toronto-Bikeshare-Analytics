"""
Sprint 2 Refactor (US-08, US-09, US-10)
Refactored by: [Your Name]
Date: [Today's Date]

Summary:
- Improved efficiency using vectorized pandas operations.
- Added datetime error handling and sorting for charts.
- Updated docstrings to show Sprint 2 refactor changes.
- Verified compatibility with Streamlit dashboard and tests.
"""
import pandas as pd

def get_peak_hours(df: pd.DataFrame) -> pd.DataFrame:
    """
    US-08: Returns hourly trip counts for 0–23 hours.

    Sprint 2 Refactor:
    - Accepts DataFrame after date/time cleaning.
    - Vectorized operations for performance.
    - Returns DataFrame with columns ['hour', 'trip_count'] sorted ascending.
    """
    if df.empty or "start_time" not in df.columns:
        return pd.DataFrame(columns=["hour", "trip_count"])

    # Convert and extract hour efficiently
    df["hour"] = pd.to_datetime(df["start_time"], errors="coerce").dt.hour.astype("Int8")

    hourly_counts = (
        df["hour"]
        .value_counts(sort=False)
        .sort_index()
        .rename_axis("hour")
        .reset_index(name="trip_count")
    )
    return hourly_counts


def get_daily_trend(df: pd.DataFrame) -> pd.DataFrame:
    """
    US-09: Returns daily trip counts sorted chronologically with helper columns.
    
    Sprint 2 Refactor:
    - Aggregates trips per day.
    - Adds weekday name and highlight column.
    - Optimized with categorical dtype and vectorized sort.
    """
    if df.empty or "start_time" not in df.columns:
        return pd.DataFrame(columns=["date", "trip_count", "day_of_week", "highlight"])

    # Extract and group by date
    df["date"] = pd.to_datetime(df["start_time"], errors="coerce").dt.date
    daily_counts = (
        df.groupby("date", observed=True)
        .size()
        .reset_index(name="trip_count")
        .sort_values("date")
    )

    # Add weekday and highlight max day
    daily_counts["day_of_week"] = pd.to_datetime(daily_counts["date"]).dt.day_name().astype("category")
    daily_counts["highlight"] = daily_counts["trip_count"] == daily_counts["trip_count"].max()
    return daily_counts


def refactor_get_peak_hours(df: pd.DataFrame) -> pd.DataFrame:
    """
    US-10: Refactored version of get_peak_hours() for faster execution.

    Sprint 2 Refactor:
    - Reduces computation by using value_counts.
    - Returns DataFrame with ['hour', 'trip_count'] sorted ascending.
    - Ensures Int8 dtype for hour to save memory.
    """
    if df.empty or "start_time" not in df.columns:
        return pd.DataFrame(columns=["hour", "trip_count"])

    start = pd.to_datetime(df["start_time"], errors="coerce")
    counts = start.dt.hour.value_counts(sort=False)
    result = counts.reset_index()
    result.columns = ["hour", "trip_count"]
    result = result.sort_values("hour").reset_index(drop=True)
    result["hour"] = result["hour"].astype("Int8")
    return result