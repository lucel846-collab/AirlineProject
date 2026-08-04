import pandas as pd

from src.logger import logger
from src.master_data import MasterData

from src.validators.airline import validate_airline_code
from src.validators.airport import validate_airport_alias
from src.validators.date import validate_previous_date_check
from src.validators.flight import validate_cancelled_flights
from src.validators.required import (
    validate_airport_office,
    validate_columns,
    validate_numeric,
    validate_required,
)
from src.validators.route import validate_route_alias


def validate(df: pd.DataFrame,
             master: MasterData
             ) -> list[dict[str, any]]: 
    logger.info("ファイルチェック開始")
    errors: list[dict[str, any]] = []
    validate_required(df, errors)
    validate_columns(df, errors)
    validate_previous_date_check(df, errors)
    validate_cancelled_flights(df, errors)  
    validate_airline_code(df, master, errors)
    validate_airport_alias(df, master, errors)
    validate_route_alias(df, master, errors)
    validate_numeric(df, errors)
    validate_airport_office(df, errors)
    logger.info("ファイルチェック完了")
    return errors   

