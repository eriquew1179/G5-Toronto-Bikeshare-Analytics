import pandas as pd


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
