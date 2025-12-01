import pandas as pd


def get_top_stations(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    US-05 Top Stations (Sprint 1)
    - Groups by 'start_station_name'
    - Returns Top N stations sorted descending by usage (count of trips)
    - Drops rows with null station names

    Output Columns:
        ['station_name', 'trip_count']
    """
    if df is None or df.empty:
        return pd.DataFrame(columns=["station_name", "trip_count"])

    if "start_station_name" not in df.columns:
        # Fallback or raise error depending on strictness
        return pd.DataFrame(columns=["station_name", "trip_count"])

    top = (
        df.dropna(subset=["start_station_name"])
        .groupby("start_station_name")
        .size()
        .reset_index(name="trip_count")
        .sort_values(by="trip_count", ascending=False)
        .head(n)
        .reset_index(drop=True)
    )
    
    top = top.rename(columns={"start_station_name": "station_name"})
    return top


def get_top_routes(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    US-06 Top Routes (Sprint 1)
    
    Groups by route:
        route = "Start → End"
    Returns Top N routes by frequency.
    """
    if df is None or df.empty:
        return pd.DataFrame(columns=["route", "trip_count"])

    required_cols = ["start_station_name", "end_station_name"]
    for col in required_cols:
        if col not in df.columns:
            return pd.DataFrame(columns=["route", "trip_count"])

    df = df.copy()
    # Create the route string
    df["route"] = df["start_station_name"].astype(str) + " → " + df["end_station_name"].astype(str)

    top_routes = (
        df.groupby("route")
        .size()
        .reset_index(name="trip_count")
        .sort_values(by="trip_count", ascending=False)
        .head(n)
        .reset_index(drop=True)
    )

    return top_routes


def get_station_flow_balance(df: pd.DataFrame) -> pd.DataFrame:
    """
    US-07 Station Flow Balance (Sprint 1)
    
    Calculates Net Flow = Arrivals (Ends) - Departures (Starts)
    Returns DataFrame with columns: ['Station', 'Net Flow']
    Sorted by absolute magnitude of flow (highest surplus/deficit first).
    """
    if df is None or df.empty:
        return pd.DataFrame(columns=["Station", "Net Flow"])
        
    required_cols = ["start_station_name", "end_station_name"]
    for col in required_cols:
        if col not in df.columns:
            return pd.DataFrame(columns=["Station", "Net Flow"])

    # Count departures (trips leaving the station)
    departures = (
        df.groupby("start_station_name")
        .size()
        .reset_index(name="departures")
        .rename(columns={"start_station_name": "Station"})
    )

    # Count arrivals (trips arriving at the station)
    arrivals = (
        df.groupby("end_station_name")
        .size()
        .reset_index(name="arrivals")
        .rename(columns={"end_station_name": "Station"})
    )

    # Combine departures and arrivals
    # Outer join ensures we capture stations that might only have starts or only ends
    flow = pd.merge(arrivals, departures, on="Station", how="outer").fillna(0)

    # Calculate Net Flow: Positive = Surplus (More arrivals), Negative = Deficit (More departures)
    flow["Net Flow"] = flow["arrivals"] - flow["departures"]

    # Sort by absolute impact (biggest movers first)
    flow["abs_flow"] = flow["Net Flow"].abs()
    flow = flow.sort_values("abs_flow", ascending=False).drop(columns=["abs_flow"])

    return flow[["Station", "Net Flow"]]