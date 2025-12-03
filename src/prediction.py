import pandas as pd
import numpy as np

def predict_hourly_demand(df: pd.DataFrame) -> pd.DataFrame:
    """
    Forecasts hourly bike demand with advanced segmentation.
    
    Metrics Calculated:
    1. predicted_demand: Overall average trips per hour.
    2. std_dev: Volatility/Risk (Standard Deviation) of demand.
    3. weekday_demand: Average demand on Mon-Fri.
    4. weekend_demand: Average demand on Sat-Sun.
    
    Args:
        df: The transaction dataframe with 'Start Time'.
        
    Returns:
        DataFrame with 24 rows (Hours 0-23) and the metric columns.
    """
    if df.empty:
        return pd.DataFrame(columns=['hour', 'predicted_demand', 'std_dev', 'weekday_demand', 'weekend_demand'])

    df = df.copy()
    
    # 1. Feature Engineering
    # We need to know which specific date and hour each trip happened
    df['date'] = df['Start Time'].dt.date
    df['hour'] = df['Start Time'].dt.hour
    
    # Identify Weekends (Day of week 5=Saturday, 6=Sunday)
    df['is_weekend'] = df['Start Time'].dt.dayofweek >= 5 
    
    # 2. Calculate Daily-Hourly Counts (The "Raw" Data for stats)
    # This gives us: "How many trips happened on Aug 1 at 8am?", "On Aug 2 at 8am?", etc.
    # We keep 'is_weekend' in the group to use it later for segmentation
    hourly_counts = df.groupby(['date', 'hour', 'is_weekend']).size().reset_index(name='trips')
    
    # 3. Initialize the 24-hour template (ensures we always have 0-23 hours)
    all_hours = pd.DataFrame({'hour': range(24)})
    
    # --- A. Overall Average & Risk (Std Dev) ---
    # We group by hour across ALL days to get the general expectation
    overall_stats = hourly_counts.groupby('hour')['trips'].agg(['mean', 'std']).reset_index()
    overall_stats.rename(columns={'mean': 'predicted_demand', 'std': 'std_dev'}, inplace=True)# Merge Everything Together    

    # --- B. Weekday Average ---
    # Filter for weekdays only, then calculate mean per hour
    weekday_data = hourly_counts[hourly_counts['is_weekend'] == False]
    weekday_stats = weekday_data.groupby('hour')['trips'].mean().reset_index(name='weekday_demand')
    
    # --- C. Weekend Average ---
    # Filter for weekends only, then calculate mean per hour
    weekend_data = hourly_counts[hourly_counts['is_weekend'] == True]
    weekend_stats = weekend_data.groupby('hour')['trips'].mean().reset_index(name='weekend_demand')
    
    # 4. Merge Everything Together
    # We merge onto the 'all_hours' template to ensure no hours are missing
    final_df = all_hours.merge(overall_stats, on='hour', how='left')
    final_df = final_df.merge(weekday_stats, on='hour', how='left')
    final_df = final_df.merge(weekend_stats, on='hour', how='left')
    
    # 5. Clean up NaNs (hours with no trips imply 0 demand)
    final_df = final_df.fillna(0)
    
    # 6. Formatting (Round for readability)
    cols_to_round = ['predicted_demand', 'std_dev', 'weekday_demand', 'weekend_demand']
    final_df[cols_to_round] = final_df[cols_to_round].round(0)
    
    return final_df

    # 3. Calculate AVERAGE demand per hour across all available days
    # Group by [hour] and take the mean of 'trips'
    #prediction = hourly_counts.groupby('hour')['trips'].mean().reset_index()
    #prediction.columns = ['hour', 'predicted_demand']

    
    # 4. Ensure all 24 hours are represented (fill missing with 0)
    #prediction = pd.merge(all_hours, prediction, on='hour', how='left').fillna(0)
    
    # Round to 1 decimal place for readability
    #prediction['predicted_demand'] = prediction['predicted_demand'].round(1)
    
    #return prediction