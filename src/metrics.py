def get_total_trips(df):
    """
    US-01 Sprint 1:
    Return total number of trips (row count).
    """
    if df is None:
        raise ValueError("df must not be None")

    return int(len(df))