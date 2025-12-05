import pytest
import pandas as pd
import os
from src.loader import DataLoader

# --- Fixtures ---
@pytest.fixture
def sample_csv(tmp_path):
    # Create dummy data using the ORIGINAL column names (mimicking the raw CSV)
    data = {
        "Trip Id": [101, 102, 103, 104],
        "Start Time": ["01/01/2018 00:00", "01/01/2018 00:15", "01/01/2018 00:30", None],
        "End Time":   ["01/01/2018 00:20", "01/01/2018 00:45", "01/01/2018 01:00", "01/01/2018 01:00"],
        "Trip Duration": [1200, 1800, 1800, 0],
        "Start Station Name": ["Station A", "Station B", "Station C", "Station A"],
        "End Station Name":   ["Station B", "Station C", "Station A", "Station B"],
        "User Type": ["Member", "Casual", "Member", "Casual"]
    }
    df = pd.DataFrame(data)
    
    # Save to a temp file
    file_path = tmp_path / "test_bikes.csv"
    df.to_csv(file_path, index=False)
    return str(file_path)

# --- Tests ---

def test_load_data_successfully(sample_csv):
    """Test AC 1: Loads CSV without errors and returns a DataFrame."""
    loader = DataLoader(sample_csv)
    df = loader.load()
    
    assert isinstance(df, pd.DataFrame)
    # Should be 3 because the 4th row has None in 'Start Time' and should be dropped
    assert len(df) == 3  
    
    # UPDATED ASSERTION: Check for the NEW standardized column name
    assert "trip_id" in df.columns 

def test_date_conversion(sample_csv):
    """Test AC 2: Converts date columns to datetime objects."""
    loader = DataLoader(sample_csv)
    df = loader.load()
    
    # Check if the column is actually a datetime type
    assert pd.api.types.is_datetime64_any_dtype(df['Start Time'])
    assert pd.api.types.is_datetime64_any_dtype(df['End Time'])

def test_clean_data_nulls(sample_csv):
    """Test AC 3: Returns a clean DataFrame (no nulls in key cols)."""
    loader = DataLoader(sample_csv)
    df = loader.load()
    
    # The 4th row in fixture has None in 'Start Time', it should be dropped
    assert df['Start Time'].isna().sum() == 0

def test_file_not_found():
    """Test edge case: Handles FileNotFoundError gracefully."""
    loader = DataLoader("path/to/ghost/file.csv")
    with pytest.raises(FileNotFoundError):
        loader.load()