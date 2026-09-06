from src.validators.airport import validate_airport_alias
from src.validators.colums import validate_columns_reservation
from src.validators.date import (
    validate_date_attr_check_daytype,
    validate_previous_date_check_daytype,
)
from src.validators.numeric import validate_numeric_reservation
from src.validators.required import validate_required_reservation
from src.validators.route import validate_route_alias_routecode3
from src.validators.time import validate_check_time_range
from src.validators.validator_flame import BaseValidator


class ReservationValidator(BaseValidator):
    log_name ="reservationファイルチェック"
    required_checks = (
        validate_columns_reservation,
        validate_required_reservation,
        validate_numeric_reservation,
    )
    master_checks = (
        validate_airport_alias,
        validate_route_alias_routecode3,
    )
    business_rule_checks = (
        validate_check_time_range,
        validate_date_attr_check_daytype,
        validate_previous_date_check_daytype,
    )
