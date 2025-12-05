import pandas as pd

def get_top_stations(df: pd.DataFrame, n: int = 10, station_type: str = "start") -> pd.DataFrame:
    """
    US-05 Refactor (Sprint 2)
    Returns the top N stations with highest trip counts.

    Enhancements:
    - Filters out null/blank/test stations (e.g., containing "test", "temp")
    - Toggle between "start" vs "end" stations via station_type parameter
    - Alphabetical tie-breaker when trip counts are equal
    - Maintains backward compatibility with app.py

    Args:
        df: DataFrame with trip data
        n: Number of top stations to return
        station_type: "start" or "end" to analyze departure vs arrival stations

    Output Columns:
        ['station_name', 'trip_count']
    """
    if df is None or df.empty:
        return pd.DataFrame(columns=["station_name", "trip_count"])

    # Determine which column to use
    col_name = "start_station_name" if station_type == "start" else "end_station_name"
    
    if col_name not in df.columns:
        return pd.DataFrame(columns=["station_name", "trip_count"])

    # Filter out invalid entries
    clean_df = df[
        df[col_name].notna() & 
        (df[col_name] != "") &
        (~df[col_name].astype(str).str.lower().str.contains("test|temp|invalid", na=False))
    ].copy()

    if clean_df.empty:
        return pd.DataFrame(columns=["station_name", "trip_count"])

    # Count occurrences with observed=True to avoid FutureWarning
    station_counts = (
        clean_df.groupby(col_name, observed=True)
        .size()
        .reset_index(name="trip_count")
        .rename(columns={col_name: "station_name"})
    )

    # Sort: Primary by trip_count (desc), Secondary by station_name (asc)
    station_counts = station_counts.sort_values(
        by=["trip_count", "station_name"],
        ascending=[False, True]
    ).reset_index(drop=True)

    return station_counts.head(n)


def get_top_routes(df: pd.DataFrame, n: int = 10, include_circular: bool = True) -> pd.DataFrame:
    """
    US-06 Refactor (Sprint 2)
    Returns the top N most frequently used routes.

    Enhancements:
    - Filters out null/blank/test stations
    - Option to exclude circular routes (Start == End)
    - Optimized for large datasets using categorical types
    - Alphabetical tie-breaker for consistent sorting
    - Maintains backward compatibility with app.py format

    Args:
        df: DataFrame with trip data
        n: Number of top routes to return
        include_circular: If False, excludes routes where start == end

    Output Columns:
        ['route', 'trip_count']
    """
    if df is None or df.empty:
        return pd.DataFrame(columns=["route", "trip_count"])

    required_cols = ["start_station_name", "end_station_name"]
    if any(col not in df.columns for col in required_cols):
        return pd.DataFrame(columns=["route", "trip_count"])

    # Filter out invalid entries
    clean_df = df[
        df["start_station_name"].notna() &
        df["end_station_name"].notna() &
        (df["start_station_name"] != "") &
        (df["end_station_name"] != "") &
        (~df["start_station_name"].astype(str).str.lower().str.contains("test|temp|invalid", na=False)) &
        (~df["end_station_name"].astype(str).str.lower().str.contains("test|temp|invalid", na=False))
    ].copy()

    if clean_df.empty:
        return pd.DataFrame(columns=["route", "trip_count"])

    # Exclude circular routes if requested
    if not include_circular:
        clean_df = clean_df[clean_df["start_station_name"] != clean_df["end_station_name"]]

    # Optimize for large datasets: convert to categorical
    if len(clean_df) > 10000:
        clean_df["start_station_name"] = clean_df["start_station_name"].astype("category")
        clean_df["end_station_name"] = clean_df["end_station_name"].astype("category")

    # Create route string (maintains app.py format with arrow)
    clean_df["route"] = clean_df["start_station_name"].astype(str) + " → " + clean_df["end_station_name"].astype(str)

    # Count route frequency with observed=True
    route_counts = (
        clean_df.groupby("route", observed=True)
        .size()
        .reset_index(name="trip_count")
    )

    # Sort: Primary by trip_count (desc), Secondary by route (asc)
    route_counts = route_counts.sort_values(
        by=["trip_count", "route"],
        ascending=[False, True]
    ).reset_index(drop=True)

    return route_counts.head(n)


def get_station_flow_balance(df: pd.DataFrame, n: int = 20, priority_threshold: int = 50) -> pd.DataFrame:
    """
    US-07 Refactor (Sprint 2)
    Calculates the net flow for each station: net_flow = arrivals - departures

    Enhancements:
    - Filters out null/blank/test stations
    - Adds "Rebalancing Priority" flag for stations with abs(net_flow) > threshold
    - Returns data optimized for diverging bar charts
    - Consistent sorting with alphabetical tie-breaker
    - Maintains backward compatibility with app.py

    Args:
        df: DataFrame with trip data
        n: Number of top stations to return (default 20 for better visibility)
        priority_threshold: Net flow threshold for rebalancing flag (default 50)

    Output Columns:
        ['Station', 'Net Flow', 'Priority'] or ['station_name', 'net_flow', 'priority']
        Note: Returns 'Station' and 'Net Flow' for app.py compatibility
    """
    if df is None or df.empty:
        return pd.DataFrame(columns=["Station", "Net Flow", "Priority"])

    required_cols = ["start_station_name", "end_station_name"]
    if any(col not in df.columns for col in required_cols):
        return pd.DataFrame(columns=["Station", "Net Flow", "Priority"])

    # Filter out invalid entries
    clean_df = df[
        df["start_station_name"].notna() &
        df["end_station_name"].notna() &
        (df["start_station_name"] != "") &
        (df["end_station_name"] != "") &
        (~df["start_station_name"].astype(str).str.lower().str.contains("test|temp|invalid", na=False)) &
        (~df["end_station_name"].astype(str).str.lower().str.contains("test|temp|invalid", na=False))
    ].copy()

    if clean_df.empty:
        return pd.DataFrame(columns=["Station", "Net Flow", "Priority"])

    # Count departures with observed=True
    departures = (
        clean_df.groupby("start_station_name", observed=True)
        .size()
        .reset_index(name="departures")
        .rename(columns={"start_station_name": "Station"})
    )

    # Count arrivals with observed=True
    arrivals = (
        clean_df.groupby("end_station_name", observed=True)
        .size()
        .reset_index(name="arrivals")
        .rename(columns={"end_station_name": "Station"})
    )

    # Merge and calculate net flow
    flow = pd.merge(arrivals, departures, on="Station", how="outer").fillna(0)
    flow["Net Flow"] = (flow["arrivals"] - flow["departures"]).astype(int)

    # Add rebalancing priority flag
    flow["Priority"] = flow["Net Flow"].abs() > priority_threshold
    flow["Priority"] = flow["Priority"].map({True: "🚨 High", False: "✓ Normal"})

    # Sort by absolute net flow (biggest imbalances first), then alphabetically
    flow["abs_flow"] = flow["Net Flow"].abs()
    flow = flow.sort_values(
        by=["abs_flow", "Station"],
        ascending=[False, True]
    ).drop(columns=["abs_flow", "arrivals", "departures"]).reset_index(drop=True)

    # Return top N stations
    return flow[["Station", "Net Flow", "Priority"]].head(n)


# Backward Compatibility Aliases
# These ensure existing app.py code continues to work without modification
def get_top_stations_legacy(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Legacy wrapper for backward compatibility"""
    result = get_top_stations(df, n, station_type="start")
    return result[["station_name", "trip_count"]]


def get_top_routes_legacy(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Legacy wrapper for backward compatibility"""
    return get_top_routes(df, n, include_circular=True)


def get_station_flow_balance_legacy(df: pd.DataFrame) -> pd.DataFrame:
    """Legacy wrapper for backward compatibility"""
    result = get_station_flow_balance(df, n=20, priority_threshold=50)
    return result[["Station", "Net Flow"]]  # Remove Priority column for legacy compatibility