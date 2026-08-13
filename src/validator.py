from src.logger import logger
from src.validator_result import ValidationResult
from src.validators.airline import validate_airline_code
from src.validators.airport import (
    validate_airport_alias,
    validate_airport_office,
)
from src.validators.colums import (
    validate_columns_daily,
    validate_columns_daily_route,
    validate_columns_monthly,
)
from src.validators.date import (
    validate_previous_date_check_daytype,
    validate_previous_date_check_monthtype,
)
from src.validators.flight import (
    validate_cancelled_flights,
    validate_operation_attributes,
    validate_operation_type,
    validate_seat_count,
)
from src.validators.numeric import (
    validate_numeric_daily,
    validate_numeric_daily_route,
    validate_numeric_monthly,
)
from src.validators.required import (
    validate_required_daily,
    validate_required_daily_route,
    validate_required_monthly,
)
from src.validators.route import (
    validate_route_alias_routecode,
    validate_route_alias_routename,
)


class BaseValidator:
    required_checks = ()
    master_checks = ()
    business_rule_checks = ()
    log_name = "検証"

    def __init__(self, master ):
        self.master = master

    def validate(self, df):
        result = ValidationResult()

        logger.info(f"{self.log_name}開始")

        self._run_checks(self.required_checks, df, result)
        self._run_checks(self.master_checks, df, result)
        self._run_checks(self.business_rule_checks, df, result)

        logger.info(f"{self.log_name}完了")

        return result

    def _run_checks(self, checks, df, result):
        for check in checks:
            check(df, self.master, result)

class CommonValidator(BaseValidator):
    log_name ="共通ファイルチェック"
    master_checks = (
        validate_airline_code,
        validate_airport_office,
    )
    business_rule_checks = (
        validate_operation_type,
        validate_seat_count,
    )

class DailyValidator(BaseValidator):
    log_name ="DAILYファイルチェック"
    required_checks = (
        validate_columns_daily,
        validate_required_daily,
        validate_numeric_daily,
    )
    master_checks = (
        validate_airport_alias,
        validate_route_alias_routecode,
    )
    business_rule_checks = (
        validate_previous_date_check_daytype,
        validate_cancelled_flights,
        validate_operation_attributes,
    )


class MonthlyValidator(BaseValidator):
    log_name ="Monthlyファイルチェック"
    required_checks = (
        validate_columns_monthly,
        validate_required_monthly,
        validate_numeric_monthly,
    )
    master_checks = (
        validate_route_alias_routename,
    )
    business_rule_checks = (
        validate_previous_date_check_monthtype,
    )

class DailyRouteValidator(BaseValidator):
    log_name ="Daily_routeファイルチェック"
    required_checks = (
        validate_columns_daily_route,
        validate_required_daily_route,
        validate_numeric_daily_route,
    )
    master_checks = (
        validate_route_alias_routename,
    )
    business_rule_checks = (
        validate_previous_date_check_daytype,
    )

