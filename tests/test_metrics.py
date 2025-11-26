import pandas as pd
import pytest
from src.metrics import get_total_trips
from src.metrics import get_total_trips, get_avg_duration


def test_get_total_trips_returns_row_count():
    df = pd.DataFrame(
        {
            "trip_id": [1, 2, 3],
            "start_time": ["2024-01-01", "2024-01-02", "2024-01-03"],
        }
    )

    result = get_total_trips(df)

    assert result == 3


def test_get_total_trips_returns_zero_for_empty_df():
    df = pd.DataFrame(columns=["trip_id", "start_time"])

    result = get_total_trips(df)

    assert result == 0
def test_get_avg_duration_returns_mean_in_minutes():
    df = pd.DataFrame({
        "trip_duration_seconds": [60, 120, 180]  # 1, 2, 3 minutes
    })

    result = get_avg_duration(df)

    # average = (60 + 120 + 180)/3 = 120 sec = 2 minutes
    assert result == pytest.approx(2.0)


def test_get_avg_duration_returns_zero_for_empty_df():
    df = pd.DataFrame(columns=["trip_duration_seconds"])

    result = get_avg_duration(df)

    assert result == 0


def test_get_avg_duration_excludes_outliers_over_24h():
    df = pd.DataFrame({
        "trip_duration_seconds": [60, 120, 90000]  # 90000 seconds > 24 hours
    })

    result = get_avg_duration(df)

    # Only 60 and 120 included → avg = 90 sec = 1.5 min
    assert result == pytest.approx(1.5)
