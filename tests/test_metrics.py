import pandas as pd
import pytest
from src.metrics import get_total_trips, get_avg_duration, get_bike_usage, get_user_type_breakdown


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

def test_get_bike_usage_sums_duration_per_bike():
    # 3 trips: bike 1 has 60 + 120 = 180s, bike 2 has 30s
    df = pd.DataFrame({
        "bike_id": [1, 1, 2],
        "trip_duration_seconds": [60, 120, 30],
    })

    result = get_bike_usage(df)

    # Expect a DataFrame with one row per bike and total duration per bike
    # Sorted descending by total duration for determinism
    assert list(result["bike_id"]) == [1, 2]
    assert list(result["total_duration_seconds"]) == [180, 30]


def test_get_bike_usage_returns_empty_for_empty_df():
    df = pd.DataFrame(columns=["bike_id", "trip_duration_seconds"])

    result = get_bike_usage(df)

    # Should return an empty DataFrame with the same expected columns
    assert list(result.columns) == ["bike_id", "total_duration_seconds"]
    assert result.empty

def test_get_user_type_breakdown_counts_member_and_casual():
    # 5 users: 3 Members, 2 Casual
    df = pd.DataFrame({
        "user_type": ["Member", "Casual", "Member", "Member", "Casual"]
    })

    result = get_user_type_breakdown(df)

    # Expect counts for each type
    assert result["Member"] == 3
    assert result["Casual"] == 2
    # Only these two keys in Sprint 1
    assert set(result.keys()) == {"Member", "Casual"}


def test_get_user_type_breakdown_returns_zero_counts_for_empty_df():
    # No rows
    df = pd.DataFrame(columns=["user_type"])

    result = get_user_type_breakdown(df)

    # Should gracefully return zeros
    assert result["Member"] == 0
    assert result["Casual"] == 0
