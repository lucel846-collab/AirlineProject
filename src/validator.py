import pandas as pd
from src.logger import logger
from src.master_data import MasterData
from src.validator_result import ValidationResult
from src.validators.airline import validate_airline_code
from src.validators.airport import validate_airport_alias
from src.validators.date import (
    validate_previous_date_check_daily,
    validate_previous_date_check_monthly,
)
from src.validators.flight import (
    validate_cancelled_flights,
    validate_operation_attributes,
    validate_operation_type,
    validate_seat_count,
)
from src.validators.required import (
    validate_airport_office,
    validate_columns_daily,
    validate_columns_daily_route,
    validate_columns_monthly,
    validate_numeric_daily,
    validate_numeric_daily_route,
    validate_numeric_monthly,
    validate_required_daily,
    validate_required_daily_route,
    validate_required_monthly,
)
from src.validators.route import (
    validate_route_alias_daily,
    validate_route_alias_monthly,
)


class Validator_Daily:
    def __init__(self, master: MasterData):
        self.master = master

    def validate(self, df: pd.DataFrame) -> ValidationResult:
        result = ValidationResult() 
        logger.info("DAILYファイルチェック開始")

        self._validate_required(df, result)
        self._validate_master(df, result)
        self._validate_business_rules(df, result)

        logger.info("DAILYファイルチェック完了")
        return result
    def _validate_required(self, df: pd.DataFrame, result: ValidationResult) -> None:
        validate_required_daily(df, result)                         #D
        validate_numeric_daily(df, result)                          #D
        validate_columns_daily(df, result)                          #D

    def _validate_master(self, df: pd.DataFrame, result: ValidationResult) -> None:
        validate_airline_code(df, self.master, result)              #C
        validate_airport_alias(df, self.master, result)             #D
        validate_route_alias_daily(df, self.master, result)         #D
        validate_airport_office(df, result)                         #C

    def _validate_business_rules(self, df: pd.DataFrame, result: ValidationResult) -> None:
        validate_previous_date_check_daily(df, result)              #D
        validate_cancelled_flights(df, result)                      #D 
        validate_operation_attributes(df, result)                   #D
        validate_operation_type(df, result)                         #C
        validate_seat_count(df, result)                             #C

class Validator_Monthly:
    def __init__(self, master: MasterData):
        self.master = master

    def validate(self, df: pd.DataFrame) -> ValidationResult:
        result = ValidationResult() 
        logger.info("Monthlyファイルチェック開始")

        self._validate_required(df, result)
        self._validate_master(df, result)
        self._validate_business_rules(df, result)

        logger.info("Monthlyファイルチェック完了")
        return result
    def _validate_required(self, df: pd.DataFrame, result: ValidationResult) -> None:
        validate_required_monthly(df, result)                       #M
        validate_numeric_monthly(df, result)                        #M
        validate_columns_monthly(df, result)                        #M

    def _validate_master(self, df: pd.DataFrame, result: ValidationResult) -> None:
        validate_airline_code(df, self.master, result)              #C
        validate_route_alias_monthly(df, self.master, result)       #M
        validate_airport_office(df, result)                         #C

    def _validate_business_rules(self, df: pd.DataFrame, result: ValidationResult) -> None:
        validate_previous_date_check_monthly(df, result)            #M
        validate_operation_type(df, result)                         #C
        validate_seat_count(df, result)                             #C

class Validator_Daily_Route:
    def __init__(self, master: MasterData):
        self.master = master

    def validate(self, df: pd.DataFrame) -> ValidationResult:
        result = ValidationResult() 
        logger.info("Daily_routeファイルチェック開始")

        self._validate_required(df, result)
        self._validate_master(df, result)
        self._validate_business_rules(df, result)

        logger.info("Daily_routeファイルチェック完了")
        return result
    def _validate_required(self, df: pd.DataFrame, result: ValidationResult) -> None:
        validate_required_daily_route(df, result)                   #R
        validate_numeric_daily_route(df, result)                    #R
        validate_columns_daily_route(df, result)                    #R

    def _validate_master(self, df: pd.DataFrame, result: ValidationResult) -> None:
        validate_airline_code(df, self.master, result)              #C
        validate_route_alias_monthly(df, self.master, result)       #M
        validate_airport_office(df, result)                         #C

    def _validate_business_rules(self, df: pd.DataFrame, result: ValidationResult) -> None:
        validate_previous_date_check_daily(df, result)              #D
        validate_operation_type(df, result)                         #C
        validate_seat_count(df, result)                             #C