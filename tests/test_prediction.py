import pytest
import pandas as pd
import numpy as np
from src.prediction import predict_hourly_demand

@pytest.fixture
def sample_mixed_data():
    """
    Creates a fake dataset spanning a Weekday and a Weekend to test segmentation.
    Aug 2, 2024 (Friday) - Weekday
    Aug 3, 2024 (Saturday) - Weekend
    """
    data = {
        "Start Time": [
            # Friday (Weekday) - 8:00 AM (High Commute) - 3 trips
            "2024-08-02 08:00:00", "2024-08-02 08:15:00", "2024-08-02 08:30:00",
            
            # Saturday (Weekend) - 8:00 AM (Low Commute) - 1 trip
            "2024-08-03 08:00:00"
        ]
    }
    df = pd.DataFrame(data)
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    return df

def test_prediction_schema(sample_mixed_data):
    """Test that the output contains the new advanced columns."""
    result = predict_hourly_demand(sample_mixed_data)
    
    expected_cols = ['hour', 'predicted_demand', 'std_dev', 'weekday_demand', 'weekend_demand']
    for col in expected_cols:
        assert col in result.columns

def test_weekday_vs_weekend_logic(sample_mixed_data):
    """
    Test logic:
    - Weekday Avg at 8am: 3 trips (from Friday)
    - Weekend Avg at 8am: 1 trip (from Saturday)
    - Overall Avg at 8am: (3+1)/2 = 2.0 trips
    """
    result = predict_hourly_demand(sample_mixed_data)
    
    # Check Hour 8
    row_8am = result[result['hour'] == 8].iloc[0]
    
    assert row_8am['weekday_demand'] == 3.0
    assert row_8am['weekend_demand'] == 1.0
    assert row_8am['predicted_demand'] == 2.0

def test_std_deviation(sample_mixed_data):
    """
    Test standard deviation calculation.
    Values at 8am: 3, 1. Mean: 2.
    Std Dev (Population): 1.0  (or Sample Std Dev: 1.414)
    """
    result = predict_hourly_demand(sample_mixed_data)
    row_8am = result[result['hour'] == 8].iloc[0]
    
    # Just check it's not NaN and is positive
    assert not pd.isna(row_8am['std_dev'])
    assert row_8am['std_dev'] > 0