import pytest
import pandas as pd
from src.prediction import predict_hourly_demand

# --- Fixtures ---
@pytest.fixture
def sample_hourly_data():
    """
    Creates a fake dataset for testing the prediction integration.
    """
    data = {
        "Start Time": [
            "2024-08-01 08:00:00", "2024-08-01 08:30:00",
            "2024-08-02 08:00:00", "2024-08-02 08:30:00"
        ]
    }
    df = pd.DataFrame(data)
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    return df

# --- Tests ---
def test_prediction_integration(sample_hourly_data):
    """
    Test that the prediction function returns the expected structure
    for the dashboard to consume.
    """
    # 1. Run the prediction logic (just like the app would)
    forecast = predict_hourly_demand(sample_hourly_data)
    
    # 2. Assert the structure matches what the UI expects
    assert isinstance(forecast, pd.DataFrame)
    assert "hour" in forecast.columns
    assert "predicted_demand" in forecast.columns
    
    # 3. Check that it covers 24 hours (0-23)
    assert len(forecast) == 24
    
    # 4. Check a specific value (Hour 8 should have 2 trips avg)
    # Hour 8: 2 trips on Day 1, 2 trips on Day 2 -> Avg = 2
    val_8am = forecast.loc[forecast['hour'] == 8, 'predicted_demand'].iloc[0]
    assert val_8am == 2.0