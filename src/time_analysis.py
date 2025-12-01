import pandas as pd

def get_peak_hours(df: pd.DataFrame) -> pd.DataFrame:
    """
    US-08: Peak Hours Analysis
    Returns hourly trip counts for 0–23 hours.
    """
    if df.empty:
        return pd.DataFrame(columns=["hour", "trip_count"])

    # Create a copy to avoid SettingWithCopyWarning
    df = df.copy()
    
    # Extract hour
    df["hour"] = df["Start Time"].dt.hour
    
    # Group by hour
    hourly_counts = (
        df.groupby("hour")
        .size()
        .reset_index(name="trip_count")
        .sort_values("hour")
    )
    
    return hourly_counts


def get_daily_trend(df: pd.DataFrame) -> pd.DataFrame:
    """
    US-09: Daily Trends
    Returns daily trip counts sorted chronologically.
    """
    if df.empty:
        return pd.DataFrame(columns=["date", "trip_count"])

    # Create a copy
    df = df.copy()
    
    # Extract date
    df["date"] = df["Start Time"].dt.date
    
    # Group by date
    daily_counts = (
        df.groupby("date")
        .size()
        .reset_index(name="trip_count")
        .sort_values("date")
    )
    
    return daily_counts