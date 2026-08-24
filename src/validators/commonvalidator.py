from src.validators.airline import validate_airline_code
from src.validators.airport import validate_airport_office
from src.validators.basevalidator import BaseValidator


class CommonValidator(BaseValidator):
    log_name ="共通ファイルチェック"
    master_checks = (
        validate_airline_code,
        validate_airport_office,
    )
