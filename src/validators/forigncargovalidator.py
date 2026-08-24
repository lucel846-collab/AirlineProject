from src.validators.airport import validate_airport_alias3
from src.validators.basevalidator import BaseValidator
from src.validators.colums import validate_columns_foreign_cargo
from src.validators.date import (
    validate_date_attr_check_monthtype,
    validate_previous_date_check_monthtype,
)
from src.validators.flight import validate_operation_foreign_cargo_type
from src.validators.numeric import validate_numeric_foreign_cargo
from src.validators.required import validate_required_foreign_cargo
from src.validators.route import validate_route_alias_routecode2


class ForeignCargoValidator(BaseValidator):
    log_name ="monthly_cargoファイルチェック"
    required_checks = (
        validate_columns_foreign_cargo,
        validate_required_foreign_cargo,
        validate_numeric_foreign_cargo,
    )
    master_checks = (
        validate_airport_alias3,
        validate_route_alias_routecode2,
    )
    business_rule_checks = (
        validate_date_attr_check_monthtype,
        validate_operation_foreign_cargo_type,
        validate_previous_date_check_monthtype,
    )
