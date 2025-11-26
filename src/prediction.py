import pandas as pd

def predict_hourly_demand(df: pd.DataFrame) -> pd.DataFrame:
    """
    Forecasts the expected number of bikes needed per hour (0-23)
    based on the average demand from the provided historical data.
    
    Logic:
    1. Count trips per hour for each specific date.
    2. Average those counts across all dates.
    
    Args:
        df: The transaction dataframe with 'Start Time'.
        
    Returns:
        DataFrame with columns ['hour', 'predicted_demand'].
    """
    df = df.copy()
    
    # 1. Extract Date and Hour features
    df['date'] = df['Start Time'].dt.date
    df['hour'] = df['Start Time'].dt.hour
    
    # 2. Calculate ACTUAL demand for every hour of every day
    # Group by [date, hour] to get counts like: 
    # Aug 1, 8am: 2 trips
    # Aug 2, 8am: 4 trips
    hourly_counts = df.groupby(['date', 'hour']).size().reset_index(name='trips')
    
    # 3. Calculate AVERAGE demand per hour across all available days
    # Group by [hour] and take the mean of 'trips'
    prediction = hourly_counts.groupby('hour')['trips'].mean().reset_index()
    prediction.columns = ['hour', 'predicted_demand']
    
    # 4. Ensure all 24 hours are represented (fill missing with 0)
    all_hours = pd.DataFrame({'hour': range(24)})
    prediction = pd.merge(all_hours, prediction, on='hour', how='left').fillna(0)
    
    # Round to 1 decimal place for readability
    prediction['predicted_demand'] = prediction['predicted_demand'].round(1)
    
    return prediction