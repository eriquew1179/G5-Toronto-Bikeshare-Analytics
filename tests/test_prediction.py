import pytest
import pandas as pd
from src.prediction import predict_hourly_demand

@pytest.fixture
def sample_week_data():
    """
    Creates a fake dataset spanning 2 days (for simplicity) to test averaging.
    Day 1: 8:00 AM (2 trips), 9:00 AM (1 trip)
    Day 2: 8:00 AM (4 trips), 9:00 AM (3 trips)
    
    Expected Prediction:
    8:00 AM -> (2 + 4) / 2 = 3.0 avg
    9:00 AM -> (1 + 3) / 2 = 2.0 avg
    """
    data = {
        "Start Time": [
            # Day 1
            "2024-08-01 08:00:00", "2024-08-01 08:30:00", # 2 trips at 8am
            "2024-08-01 09:15:00",                        # 1 trip at 9am
            
            # Day 2
            "2024-08-02 08:10:00", "2024-08-02 08:15:00", "2024-08-02 08:45:00", "2024-08-02 08:50:00", # 4 trips at 8am
            "2024-08-02 09:05:00", "2024-08-02 09:30:00", "2024-08-02 09:55:00"                         # 3 trips at 9am
        ]
    }
    df = pd.DataFrame(data)
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    return df

def test_predict_hourly_structure(sample_week_data):
    """Test that the output has the correct columns and shape."""
    result = predict_hourly_demand(sample_week_data)
    
    assert "hour" in result.columns
    assert "predicted_demand" in result.columns
    # We expect rows for hours 8 and 9 at least. 
    # Ideally, a robust function returns 0 for missing hours, but let's start simple.
    assert len(result) >= 2 

def test_predict_hourly_calculation(sample_week_data):
    """Test that the math (Average per hour) is correct."""
    result = predict_hourly_demand(sample_week_data)
    
    # Filter for specific hours
    pred_8am = result.loc[result['hour'] == 8, 'predicted_demand'].values[0]
    pred_9am = result.loc[result['hour'] == 9, 'predicted_demand'].values[0]
    
    # Assert expected averages
    assert pred_8am == 3.0  # (2 + 4) / 2
    assert pred_9am == 2.0  # (1 + 3) / 2