import pandas as pd
from src.station_analysis import get_top_stations

# -------- US-05 TOP STATIONS TESTS --------

def test_get_top_stations_basic():
    df = pd.DataFrame({
        "start_station_name": ["A", "A", "B"],
        "trip_duration_seconds": [100, 200, 150]  # sample values
    })
    result = get_top_stations(df, 1)
    assert len(result) == 1
    assert result.loc[0, "station_name"] == "A"
    assert result.loc[0, "trip_count"] == 2


def test_get_top_stations_empty():
    df = pd.DataFrame(columns=["start_station_name"])
    result = get_top_stations(df)
    assert result.empty
    
    # -------- US-06 TOP ROUTES TESTS --------

def test_get_top_routes_basic():
    df = pd.DataFrame({
        "start_station_name": ["A", "A", "B"],
        "end_station_name": ["B", "B", "C"],
    })
    result = get_top_routes(df, 1)
    assert len(result) == 1
    assert result.loc[0, "trip_count"] == 2


def test_get_top_routes_empty():
    df = pd.DataFrame(columns=["start_station_name", "end_station_name"])
    result = get_top_routes(df)
    assert result.empty
