import pandas as pd
from src.validator_result import ValidationResult

REQUIRED_NUMERIC1 = [
    "座席数",
    "旅客数",
    "INF数",
    "貨物重量",
    "メール重量"
]

REQUIRED_NUMERIC2 = [
    "便数",
    "座席数",
    "旅客数",
    "INF数",
    "貨物重量",
    "メール重量"
]

REQUIRED_NUMERIC3 = [
    "便数",
    "座席数",
    "旅客数",
    "INF数",
    "貨物重量",
    "メール重量"
]
def validate_numeric_daily(df: pd.DataFrame,_master, result: ValidationResult) -> None:
    for col in REQUIRED_NUMERIC1:
        for index, value in df[col].items():
            if not pd.isna(value) and not isinstance(value, (int, float)):
                result.add_error(
                    filenm=df.attrs.get("filename"),
                    index=index,
                    column=col,
                    value=value,
                    message="数値である必要があります"
                )
            elif not pd.isna(value) and isinstance(value, (int, float)) and value < 0:
                result.add_error(
                    filenm=df.attrs.get("filename"),
                    index=index,
                    column=col,
                    value=value,
                    message="正数値の必要があります"
                )


def validate_numeric_monthly(df: pd.DataFrame,_master, result: ValidationResult) -> None:
    for col in REQUIRED_NUMERIC2:
        for index, value in df[col].items():
            if not pd.isna(value) and not isinstance(value, (int, float)):
                result.add_error(
                    filenm=df.attrs.get("filename"),
                    index=index,
                    column=col,
                    value=value,
                    message="数値である必要があります"
                )
            elif not pd.isna(value) and isinstance(value, (int, float)) and value < 0:
                result.add_error(
                    filenm=df.attrs.get("filename"),
                    index=index,
                    column=col,
                    value=value,
                    message="正数値の必要があります"
                )

def validate_numeric_daily_route(df: pd.DataFrame,_master, result: ValidationResult) -> None:
    for col in REQUIRED_NUMERIC3:
        for index, value in df[col].items():
            if not pd.isna(value) and not isinstance(value, (int, float)):
                result.add_error(
                    filenm=df.attrs.get("filename"),
                    index=index,
                    column=col,
                    value=value,
                    message="数値である必要があります"
                )
            elif not pd.isna(value) and isinstance(value, (int, float)) and value < 0:
                result.add_error(
                    filenm=df.attrs.get("filename"),
                    index=index,
                    column=col,
                    value=value,
                    message="正数値の必要があります"
                )
