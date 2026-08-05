import pandas as pd
from src.logger import logger
from src.master_data import MasterData
from src.validator_result import ValidationResult
from src.validators.airline import validate_airline_code
from src.validators.airport import validate_airport_alias
from src.validators.date import validate_previous_date_check
from src.validators.flight import validate_cancelled_flights, validate_seat_count
from src.validators.required import (
    validate_airport_office,
    validate_columns,
    validate_numeric,
    validate_required,
)
from src.validators.route import validate_route_alias


def validate(df: pd.DataFrame,
             master: MasterData
             ) -> ValidationResult:
    result = ValidationResult() 
    logger.info("ファイルチェック開始")
    validate_required(df, result)
    validate_columns(df, result)
    validate_previous_date_check(df, result)
    validate_cancelled_flights(df, result)  
    validate_airline_code(df, master, result)
    validate_airport_alias(df, master, result)
    validate_route_alias(df, master, result)
    validate_numeric(df, result)
    validate_airport_office(df, result)
    validate_seat_count(df, result)
    logger.info("ファイルチェック完了")
    return result   

