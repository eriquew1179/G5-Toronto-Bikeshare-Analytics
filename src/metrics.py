import pytest
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

def get_bike_usage(df):
    """
    US-03 Sprint 1:
    Group trips by bike_id and sum total duration per bike.
    (Implementation to be added in Green phase.)
    """
    raise NotImplementedError("stub for US-03 TDD")

def get_user_type_breakdown(df):
    """
    US-04 Sprint 1:
    Return counts of Member vs Casual users.
    """

    if df is None or "user_type" not in df:
        raise ValueError("df must contain 'user_type' column")

    if df.empty:
        return {"Member": 0, "Casual": 0}

    # Count occurrences
    counts = df["user_type"].value_counts()

    return {
        "Member": int(counts.get("Member", 0)),
        "Casual": int(counts.get("Casual", 0)),
    }

