
def add_error(errors: list[dict[str, any]], row: int, column: str, value: str, message: str) -> None:
    errors.append({""
        "行番号":row+2,
        "項目名":column,
        "入力値":value,
        "エラー内容":message,
        })
