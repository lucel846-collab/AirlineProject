from src.validators.airport import validate_airport_alias
from src.validators.colums import validate_columns_monthly_cargo
from src.validators.date import (
    validate_date_attr_check_monthtype,
    validate_previous_date_check_monthtype,
)
from src.validators.flight import validate_operation_monthly_type
from src.validators.numeric import validate_numeric_monthly_cargo
from src.validators.required import validate_required_monthly_cargo
from src.validators.route import validate_route_alias_routecode
from src.validators.validator_flame import BaseValidator


class MonthlyCargoValidator(BaseValidator):
    log_name ="monthly_cargoファイルチェック"
    required_checks = (
        validate_columns_monthly_cargo,
        validate_required_monthly_cargo,
        validate_numeric_monthly_cargo,
    )
    master_checks = (
        validate_airport_alias,
        validate_route_alias_routecode,
    )
    business_rule_checks = (
        validate_date_attr_check_monthtype,
        validate_previous_date_check_monthtype,
        validate_operation_monthly_type,
    )
