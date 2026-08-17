from src.validators.basevalidator import BaseValidator
from src.validators.colums import validate_columns_monthly
from src.validators.date import validate_previous_date_check_monthtype
from src.validators.flight import validate_seat_count
from src.validators.numeric import validate_numeric_monthly
from src.validators.required import validate_required_monthly
from src.validators.route import validate_route_alias_routename


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
        validate_seat_count,
    )
