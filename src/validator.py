import pandas as pd
from src.logger import logger
from src.validators.airline import validate_airline_code
from src.validators.airport import validate_airport_alias
from src.validators.date import validate_previous_date_check
from src.validators.flight import validate_cancelled_flights
from src.validators.required import validate_columns, validate_required
from src.validators.route import validate_route_alias


def validate(df: pd.DataFrame,
             airline_master_df: pd.DataFrame, 
             route_alias_dict: dict[tuple[str, str, str], str],
             airport_alias_dict: dict[tuple[str, str], str] 
             ) -> list[dict[str, any]]: 
    logger.info("ファイルチェック開始")
    errors: list[dict[str, any]] = []
    validate_required(df, errors)
    validate_columns(df, errors)
    validate_previous_date_check(df, errors)
    validate_cancelled_flights(df, errors)  
    validate_airline_code(df, airline_master_df, errors)
    validate_airport_alias(df,airport_alias_dict, errors)
    validate_route_alias(df, route_alias_dict, errors)
    logger.info("ファイルチェック完了")
    return errors   

