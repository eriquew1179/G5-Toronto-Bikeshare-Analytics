import pytest
import pandas as pd
from datetime import date

# --- Logic Extraction (Updated for Sprint 2) ---
def filter_data(df: pd.DataFrame, start_date: date, end_date: date, selected_stations: list = None) -> pd.DataFrame:
    """
    Refactored Logic: Filters by Date AND Station.
    """
    # 1. Date Filter
    mask = (df['Start Time'].dt.date >= start_date) & (df['Start Time'].dt.date <= end_date)
    
    # 2. Station Filter (New)
    if selected_stations:
        mask = mask & (df['start_station_name'].isin(selected_stations))
        
    return df.loc[mask]

# --- Tests ---
def test_filter_by_station():
    # 1. Mock Data
    data = {
        'Start Time': pd.to_datetime(['2024-08-01', '2024-08-01', '2024-08-01']),
        'start_station_name': ['Station A', 'Station B', 'Station A'],
        'Trip Id': [1, 2, 3]
    }
    df = pd.DataFrame(data)
    
    # 2. Define Filters
    start = date(2024, 8, 1)
    end = date(2024, 8, 1)
    stations = ['Station B'] # We only want Station B
    
    # 3. Apply Logic
    result = filter_data(df, start, end, stations)
    
    # 4. Assert
    assert len(result) == 1
    assert result.iloc[0]['start_station_name'] == 'Station B'