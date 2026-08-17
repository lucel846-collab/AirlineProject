from src.logger import logger
from src.validators.validator_result import ValidationResult


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