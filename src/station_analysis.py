import pandas as pd


def get_top_stations(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    US-05 Refactor (Sprint 2)
    Returns the top N stations with highest departure counts.

    Enhancements:
    - Ignore null or blank station names
    - Alphabetical tie-breaker when trip counts are equal
    """

    if df is None or df.empty or "start_station_name" not in df.columns:
        return pd.DataFrame(columns=["station_name", "trip_count"])

    # Drop invalid/blank entries
    clean_df = df[df["start_station_name"].notna() & (df["start_station_name"] != "")]

    if clean_df.empty:
        return pd.DataFrame(columns=["station_name", "trip_count"])

    # Count occurrences
    station_counts = (
        clean_df.groupby("start_station_name")
        .size()
        .reset_index(name="trip_count")
        .rename(columns={"start_station_name": "station_name"})
    )

    # Primary sort: trip_count desc
    # Secondary sort: station_name alphabetical
    station_counts = station_counts.sort_values(
        by=["trip_count", "station_name"],
        ascending=[False, True]
    ).reset_index(drop=True)

    return station_counts.head(n)


def get_top_routes(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    US-06 Refactor (Sprint 2)
    Returns the top N most frequently used routes.

    Enhancements:
    - Ignore null or blank station names
    - Alphabetical tie-breaker for consistent sorting
    """

    required_cols = ["start_station_name", "end_station_name"]

    if df is None or df.empty or any(col not in df.columns for col in required_cols):
        return pd.DataFrame(columns=["start_station", "end_station", "trip_count"])

    # Drop invalid rows
    clean_df = df[
        df["start_station_name"].notna() &
        df["end_station_name"].notna() &
        (df["start_station_name"] != "") &
        (df["end_station_name"] != "")
    ]

    if clean_df.empty:
        return pd.DataFrame(columns=["start_station", "end_station", "trip_count"])

    # Count route frequency
    route_counts = (
        clean_df.groupby(["start_station_name", "end_station_name"])
        .size()
        .reset_index(name="trip_count")
        .rename(columns={
            "start_station_name": "start_station",
            "end_station_name": "end_station"
        })
    )

    # Sort:
    # 1️⃣ by trip_count descending
    # 2️⃣ by start_station (alphabetical) for tie-breaking
    route_counts = route_counts.sort_values(
        by=["trip_count", "start_station"],
        ascending=[False, True]
    ).reset_index(drop=True)

    return route_counts.head(n)


def get_station_flow_balance(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    US-07 Refactor (Sprint 2)
    Calculates the net flow for each station:
        net_flow = arrivals - departures

    Enhancements:
    - Ignore null or blank station names
    - Consistent sorting with alphabetical tie-breaker
    - Improved code clarity and maintainability
    """

    required_cols = ["start_station_name", "end_station_name"]

    if df is None or df.empty or any(col not in df.columns for col in required_cols):
        return pd.DataFrame(columns=["station_name", "net_flow"])

    # Filter out invalid entries
    clean_df = df[
        df["start_station_name"].notna() &
        df["end_station_name"].notna() &
        (df["start_station_name"] != "") &
        (df["end_station_name"] != "")
    ]

    if clean_df.empty:
        return pd.DataFrame(columns=["station_name", "net_flow"])

    # Count departures and arrivals
    departures = (
        clean_df.groupby("start_station_name")
        .size()
        .reset_index(name="departures")
        .rename(columns={"start_station_name": "station_name"})
    )

    arrivals = (
        clean_df.groupby("end_station_name")
        .size()
        .reset_index(name="arrivals")
        .rename(columns={"end_station_name": "station_name"})
    )

    # Merge into flow summary
    flow = pd.merge(arrivals, departures, on="station_name", how="outer").fillna(0)
    flow["net_flow"] = flow["arrivals"].astype(int) - flow["departures"].astype(int)

    # Sorting
    flow = flow.sort_values(
        by=["net_flow", "station_name"],
        ascending=[False, True]
    ).reset_index(drop=True)

    return flow[["station_name", "net_flow"]].head(n)