import pandas as pd

from src.paths import (
    AIRPORT_MASTER_FILE,
    AIRLINE_MASTER_FILE,
    ROUTE_MASTER_FILE,
)

def read_airport_master() -> pd.DataFrame:
    return pd.read_csv(AIRPORT_MASTER_FILE)

def read_airline_master() -> pd.DataFrame:
    return pd.read_csv(AIRLINE_MASTER_FILE)

def read_route_master() -> pd.DataFrame:
    return pd.read_csv(ROUTE_MASTER_FILE)