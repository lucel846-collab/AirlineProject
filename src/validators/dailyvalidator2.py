from src.validators.airport import (
    validate_airport_alias,
    validate_airport_alias2,
)
from src.validators.basevalidator import BaseValidator
from src.validators.colums import validate_columns_daily2
from src.validators.date import validate_previous_date_check_daytype
from src.validators.flight import (
    validate_cancelled_flights,
    validate_operation_attributes,
    validate_seat_count,
)
from src.validators.numeric import validate_numeric_daily2
from src.validators.required import validate_required_daily2
from src.validators.route import validate_route_alias_routecode


class DailyValidator2(BaseValidator):
    log_name ="DAILY2ファイルチェック"
    required_checks = (
        validate_columns_daily2,
        validate_required_daily2,
        validate_numeric_daily2,
    )
    master_checks = (
        validate_airport_alias,
        validate_airport_alias2,
        validate_route_alias_routecode,
    )
    business_rule_checks = (
        validate_previous_date_check_daytype,
        validate_cancelled_flights,
        validate_operation_attributes,
        validate_seat_count,
    )
