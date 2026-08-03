import pandas as pd

from src.paths import (
    AIRLINE_MASTER_FILE,
    AIRPORT_ALIAS_FILE,
    AIRPORT_MASTER_FILE,
    ROUTE_ALIAS_FILE,
    ROUTE_MASTER_FILE,
)


def read_airport_master() -> pd.DataFrame:
    return pd.read_csv(AIRPORT_MASTER_FILE)

def read_airline_master() -> pd.DataFrame:
    return pd.read_csv(AIRLINE_MASTER_FILE)

def read_route_master() -> pd.DataFrame:
    return pd.read_csv(ROUTE_MASTER_FILE)

def read_route_alias_master() -> pd.DataFrame:
    return pd.read_csv(ROUTE_ALIAS_FILE)

def read_airport_alias_master() -> pd.DataFrame:
    return pd.read_csv(AIRPORT_ALIAS_FILE)

def create_route_alias_dict(route_alias_df: pd.DataFrame) -> dict[tuple[str, str, str], str]:
    return {
        (
            row["AirlineCD"],
            row["AirportOffice"],
            row["RouteAlias"]
        ): row["RouteCD"]
        for _, row in route_alias_df.iterrows()
    }

def create_route_code_dict(route_code_df: pd.DataFrame) -> dict[tuple[str, str, str], str]:
    return {
        (
            row["RouteCD"] ): row["RouteName"]
        for _, row in route_code_df.iterrows()
    }

def create_airport_alias_dict(airport_alias_df: pd.DataFrame) -> dict[str, str]:
    return {
        row["AirportAlias"]: row["AirportCD"]
        for _, row in airport_alias_df.iterrows()
    } 


def load_route_alias_dict() -> dict[tuple[str, str, str], str]:
    route_alias_df = read_route_alias_master()
    return create_route_alias_dict(route_alias_df)

def load_route_code_dict() -> dict[tuple[str, str, str], str]:
    route_code_df = read_route_master()
    return create_route_code_dict(route_code_df)

def load_airport_alias_dict() -> dict[str, str]:
    airport_alias_df = read_airport_alias_master()
    return create_airport_alias_dict(airport_alias_df)
