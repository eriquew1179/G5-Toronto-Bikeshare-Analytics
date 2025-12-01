time_analysis.py
import pandas as pd

def get_peak_hours(df):
    """
    US-08: Returns hourly trip counts for 0–23 hours.
    """
    df["hour"] = pd.to_datetime(df["start_time"]).dt.hour
    hourly_counts = (
        df.groupby("hour").size().reset_index(name="trip_count").sort_values("hour")
    )
    return hourly_counts


def get_daily_trend(df):
    """
    US-09: Returns daily trip counts sorted chronologically,
    with helper columns for day_of_week and highlight (max day).
    """
    df["date"] = pd.to_datetime(df["start_time"]).dt.date
    daily_counts = (
        df.groupby("date").size().reset_index(name="trip_count").sort_values("date")
    )
    daily_counts["day_of_week"] = pd.to_datetime(daily_counts["date"]).dt.day_name()
    daily_counts["highlight"] = (
        daily_counts["trip_count"] == daily_counts["trip_count"].max()
    )
    return daily_counts


def refactor_get_peak_hours(df):
    """
    US-10: Refactored version of get_peak_hours() for faster execution.
    """
    start = pd.to_datetime(df["start_time"], errors="coerce")
    counts = start.dt.hour.value_counts(sort=False).sort_index()
    result = counts.reset_index()
    result.columns = ["hour", "trip_count"]
    return result
