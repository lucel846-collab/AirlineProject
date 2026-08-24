from src.validators.basevalidator import BaseValidator
from src.validators.colums import validate_columns_daily_route
from src.validators.date import (
    validate_date_attr_check_daytype,
    validate_previous_date_check_daytype,
)
from src.validators.flight import validate_operation_daily_type, validate_seat_count
from src.validators.numeric import validate_numeric_daily_route
from src.validators.required import validate_required_daily_route
from src.validators.route import validate_route_alias_routename


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
        validate_operation_daily_type,
        validate_date_attr_check_daytype,
        validate_previous_date_check_daytype,
        validate_seat_count,
    )
