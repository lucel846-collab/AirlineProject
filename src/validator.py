import pandas as pd
from src.logger import logger
from src.master_data import MasterData
from src.validator_result import ValidationResult
from src.validators.airline import validate_airline_code
from src.validators.airport import validate_airport_alias
from src.validators.date import validate_previous_date_check
from src.validators.flight import (
    validate_cancelled_flights,
    validate_operation_attributes,
    validate_operation_type,
    validate_seat_count,
)
from src.validators.required import (
    validate_airport_office,
    validate_columns,
    validate_numeric,
    validate_required,
)
from src.validators.route import validate_route_alias


class Validator:
    def __init__(self, master: MasterData):
        self.master = master

    def validate(self, df: pd.DataFrame) -> ValidationResult:
        result = ValidationResult() 
        logger.info("ファイルチェック開始")

        self._validate_required(df, result)
        self._validate_master(df, result)
        self._validate_business_rules(df, result)

        logger.info("ファイルチェック完了")
        return result
    def _validate_required(self, df: pd.DataFrame, result: ValidationResult) -> None:
        validate_required(df, result)
        validate_numeric(df, result)
        validate_columns(df, result)

    def _validate_master(self, df: pd.DataFrame, result: ValidationResult) -> None:
        validate_airline_code(df, self.master, result)
        validate_airport_alias(df, self.master, result)
        validate_route_alias(df, self.master, result)
        validate_airport_office(df, result)

    def _validate_business_rules(self, df: pd.DataFrame, result: ValidationResult) -> None:
        validate_previous_date_check(df, result)
        validate_cancelled_flights(df, result)  
        validate_operation_attributes(df, result)
        validate_operation_type(df, result)
        validate_seat_count(df, result)
