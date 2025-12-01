import pandas as pd

def get_total_trips(df: pd.DataFrame) -> int:
    """
    US-01: Total Volume KPI
    Returns total number of trips (rows) in the dataframe.
    """
    if df is None:
        return 0
    return len(df)

def get_avg_duration(df: pd.DataFrame) -> float:
    """
    US-02: Average Trip Duration
    Calculates the average of 'trip_duration_seconds' and returns it in minutes.
    """
    if df is None or df.empty:
        return 0.0
    
    # Try standard name first, then fallbacks
    col_name = 'trip_duration_seconds'
    if col_name not in df.columns:
        # Fallback to 'amount' or original name if mapping failed
        for fallback in ['Trip Duration', 'amount']:
            if fallback in df.columns:
                col_name = fallback
                break
    
    if col_name not in df.columns:
        return 0.0

    # Calculate mean (handling potential string issues)
    avg_val = pd.to_numeric(df[col_name], errors='coerce').mean()
    
    # Return in minutes (assuming data is in seconds)
    return avg_val / 60 if avg_val else 0.0

def get_bike_usage(df: pd.DataFrame) -> pd.DataFrame:
    """
    US-03: Bike Usage
    Groups by bike_id and sums the duration.
    """
    if df is None or df.empty:
        return pd.DataFrame(columns=["bike_id", "total_usage"])

    # 1. Identify ID Column (Smart Search)
    id_cols = ['bike_id', 'Bike Id', 'Bike ID', 'customer_id']
    id_col = next((c for c in id_cols if c in df.columns), None)

    # 2. Identify Value Column (Smart Search)
    val_cols = ['trip_duration_seconds', 'Trip Duration', 'amount']
    val_col = next((c for c in val_cols if c in df.columns), None)

    if not id_col or not val_col:
        print("ERROR: Could not find required columns for Bike Usage.")
        return pd.DataFrame(columns=["bike_id", "total_usage"])

    # 3. Group and Sum
    # Ensure value column is numeric before summing
    df = df.copy()
    df[val_col] = pd.to_numeric(df[val_col], errors='coerce')
    
    usage = (
        df.groupby(id_col)[val_col]
        .sum()
        .reset_index()
        .sort_values(val_col, ascending=False)
    )
    
    # Standardize output names for the UI
    usage.columns = ["bike_id", "total_usage"]
    
    return usage

def get_user_type_breakdown(df: pd.DataFrame) -> dict:
    """
    US-04: User Type Split
    Returns counts of each user type.
    """
    if df is None or df.empty:
        return {}

    # Identify User Column
    user_cols = ['user_type', 'User Type', 'type']
    col_name = next((c for c in user_cols if c in df.columns), None)
    
    if not col_name:
        return {}

    # Get value counts
    counts = df[col_name].value_counts().to_dict()
    return counts