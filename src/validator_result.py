from src.error_report import export_validation_errors
from src.paths import ERROR_FILE


class ValidationResult:
    def __init__(self):
        self.errors = []

    @property
    def has_errors(self):
        return bool(self.errors) 

    def export(self):
        export_validation_errors(self.errors, ERROR_FILE)

    def add_error(self, index, column, value, message):
        self.errors.append({
            "行番号": index + 2,
            "項目名": column,
            "入力値": value,
            "エラー内容": message
        })