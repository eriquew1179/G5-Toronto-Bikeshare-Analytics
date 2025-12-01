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

import pandas as pd
from src.station_analysis import get_top_routes


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
import pandas as pd
from src.station_analysis import get_station_flow_balance

# -------- US-07 STATION FLOW BALANCE TESTS --------

def test_station_flow_balance_basic():
    df = pd.DataFrame({
        "start_station_name": ["A", "A", "B"],
        "end_station_name": ["B", "A", "A"],
    })
    result = get_station_flow_balance(df, 1)

    # Debe existir la columna net_flow
    assert "net_flow" in result.columns
    # Y debe ser tipo entero
    assert result["net_flow"].dtype == "int64"


def test_station_flow_balance_empty():
    df = pd.DataFrame(columns=["start_station_name", "end_station_name"])
    result = get_station_flow_balance(df)
    assert result.empty
