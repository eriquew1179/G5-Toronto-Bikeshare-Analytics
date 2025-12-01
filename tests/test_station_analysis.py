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
