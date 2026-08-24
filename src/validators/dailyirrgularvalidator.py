from src.validators.airport import (
    validate_airport_alias,
    validate_airport_alias2,
)
from src.validators.basevalidator import BaseValidator
from src.validators.colums import validate_columns_irregular
from src.validators.date import (
    validate_date_attr_check_daytype,
    validate_previous_date_check_daytype,
)
from src.validators.flight import (
    validate_operation_attributes,
    validate_operation_irregal_type,
    validate_seat_count,
)
from src.validators.numeric import validate_numeric_irreguler
from src.validators.required import validate_required_irregular
from src.validators.route import validate_route_alias_routecode


class DailyIrregularValidator(BaseValidator):
    log_name ="DAILY_IRRGULARファイルチェック"
    required_checks = (
        validate_columns_irregular,
        validate_required_irregular,
        validate_numeric_irreguler,
    )
    master_checks = (
        validate_airport_alias,
        validate_airport_alias2,
        validate_route_alias_routecode,
    )
    business_rule_checks = (
        validate_date_attr_check_daytype,
        validate_previous_date_check_daytype,
        validate_operation_attributes,
        validate_operation_irregal_type,
        validate_seat_count,
    )
