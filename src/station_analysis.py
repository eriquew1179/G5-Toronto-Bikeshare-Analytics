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
        raise KeyError("'start_station_name' column missing")

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
    Returns the Top N most common routes sorted descending by usage.
    """
    if df is None or df.empty:
        return pd.DataFrame(columns=["route", "trip_count"])
def get_station_flow_balance(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    US-07 Station Flow Balance (Sprint 1)

    Calculates net flow per station:
        net_flow = (Arrivals) - (Departures)
    Returns Top N stations sorted by imbalance (descending).
    """
    if df is None or df.empty:
        return pd.DataFrame(columns=["station_name", "net_flow"])

    required_cols = ["start_station_name", "end_station_name"]
    for col in required_cols:
        if col not in df.columns:
            return pd.DataFrame(columns=["route", "trip_count"])

    df = df.copy()
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
            return pd.DataFrame(columns=["station_name", "net_flow"])

    # Count departures (trips leaving the station)
    departures = (
        df.groupby("start_station_name")
        .size()
        .reset_index(name="departures")
        .rename(columns={"start_station_name": "station_name"})
    )

    # Count arrivals (trips arriving at the station)
    arrivals = (
        df.groupby("end_station_name")
        .size()
        .reset_index(name="arrivals")
        .rename(columns={"end_station_name": "station_name"})
    )

    # Combine departures and arrivals
    flow = pd.merge(arrivals, departures, on="station_name", how="outer").fillna(0)

    # Calculate net flow
    flow["net_flow"] = flow["arrivals"].astype(int) - flow["departures"].astype(int)

    # Sort by highest net imbalance
    flow = flow.sort_values(by="net_flow", ascending=False).head(n).reset_index(drop=True)

    return flow[["station_name", "net_flow"]]
