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

# -------- US-06 REFACTOR TESTS (SPRINT 2) --------

def test_top_routes_ignore_invalid_stations():
    df = pd.DataFrame({
        "start_station_name": ["A", None, "A", "", "B"],
        "end_station_name": ["B", "B", None, "C", ""],
    })
    result = get_top_routes(df, 2)

    # Should not include blank or null station names
    assert not result["start_station"].isin(["", None]).any()
    assert not result["end_station"].isin(["", None]).any()
    assert len(result) <= 2


def test_top_routes_tie_breaker_sort():
    df = pd.DataFrame({
        "start_station_name": ["A", "B"],
        "end_station_name": ["C", "C"],
    })
    # Both A→C and B→C appear once → tie
    result = get_top_routes(df, 2)

    assert len(result) == 2
    # Alphabetical tie-breaker for consistency
    assert result.loc[0, "start_station"] == "A"
    assert result.loc[1, "start_station"] == "B"

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

# -------- US-07 REFACTOR TESTS (SPRINT 2) --------

def test_station_flow_balance_ignore_invalid_entries():
    df = pd.DataFrame({
        "start_station_name": ["A", None, "B", ""],
        "end_station_name":   ["B", "A", "", None],
    })
    result = get_station_flow_balance(df, 5)

    # Invalid entries removed
    assert not result["station_name"].isin(["", None]).any()


def test_station_flow_balance_tie_breaker_sorting():
    df = pd.DataFrame({
        "start_station_name": ["A", "B"],
        "end_station_name":   ["B", "A"],
    })
    # Both have net_flow = 0
    result = get_station_flow_balance(df, 2)

    assert len(result) == 2
    # Alphabetical tie-breaker for consistent ordering
    assert result.loc[0, "station_name"] == "A"
    assert result.loc[1, "station_name"] == "B"
