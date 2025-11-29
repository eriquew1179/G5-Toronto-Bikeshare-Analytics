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