import pytest
import pandas as pd
from datetime import date

# --- Logic Extraction ---
# This mimics the logic inside app.py for testing purposes
def filter_data_by_date(df: pd.DataFrame, start_date: date, end_date: date) -> pd.DataFrame:
    """
    Filters the dataframe based on a date range (inclusive).
    Handles the comparison between pandas Timestamp and python date objects.
    """
    # Access the .dt.date accessor to compare with python date objects
    mask = (df['Start Time'].dt.date >= start_date) & (df['Start Time'].dt.date <= end_date)
    return df.loc[mask]

# --- The Test ---
def test_date_filtering_logic_august_data():
    # 1. Create mock data (Mimicking your Aug 1 - Aug 8 dataset)
    data = {
        'Trip Id': [101, 102, 103, 104],
        'Start Time': pd.to_datetime([
            '2024-08-01 08:00:00',  # Day 1
            '2024-08-04 12:30:00',  # Day 4 (Target)
            '2024-08-08 23:59:00',  # Day 8
            '2024-08-09 00:01:00'   # Day 9 (Out of range)
        ])
    }
    df = pd.DataFrame(data)
    
    # 2. Define filter range (e.g., Filter for the middle of the week)
    # We use datetime.date because that is what Streamlit returns
    start = date(2024, 8, 3)
    end = date(2024, 8, 5)
    
    # 3. Apply Logic
    filtered = filter_data_by_date(df, start, end)
    
    # 4. Assert
    # Should only keep the Aug 4th entry
    assert len(filtered) == 1
    assert filtered.iloc[0]['Trip Id'] == 102