import pandas as pd
from src.metrics import get_total_trips


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
