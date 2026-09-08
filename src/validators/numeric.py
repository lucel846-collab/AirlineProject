import pandas as pd

from src.constants import NUMERIC_CHECK_MAP
from src.detect_layout import Layout_type
from src.validators.validator_result import ValidationResult


def validate_numeric_base(df: pd.DataFrame, result: ValidationResult, required_columns: list[str]) -> None:
    #必須項目の数値チェックを行う共通ロジック"""
    filename = df.attrs.get("filename")
    for col in required_columns:
         for index, value in df[col].items():
            if not pd.isna(value) and str(value).strip() != "" and not isinstance(value, (int, float)):
                result.add_error(
                    filenm=filename,
                    index=index,
                    column=col,
                    value=value,
                    message="数値である必要があります"
                )
            elif not pd.isna(value) and isinstance(value, (int, float)) and value < 0:
                result.add_error(
                    filenm=filename,
                    index=index,
                    column=col,
                    value=value,
                    message="正数値の必要があります"
                )
def _validate_by_key(df: pd.DataFrame, result: ValidationResult, layout_key: str) -> None:
    """個別のラッパー関数から呼び出すための内部補助関数"""
    expected_columns = NUMERIC_CHECK_MAP.get(layout_key)
    if expected_columns is None:
        raise ValueError(f"定義書に存在しないレイアウト名です: {layout_key}")
    validate_numeric_base(df, result, expected_columns)

def validate_numeric_daily(df: pd.DataFrame,_master, result: ValidationResult) -> None:
    _validate_by_key(df, result,  Layout_type.DAILY.value)

def validate_numeric_daily2(df: pd.DataFrame,_master, result: ValidationResult) -> None:
    _validate_by_key(df, result,  Layout_type.DAILY2.value)

def validate_numeric_daily3(df: pd.DataFrame,_master, result: ValidationResult) -> None:
    _validate_by_key(df, result,  Layout_type.DAILY3.value)

def validate_numeric_monthly(df: pd.DataFrame,_master, result: ValidationResult) -> None:
    _validate_by_key(df, result, Layout_type.MONTHLY_ROUTE.value)

def validate_numeric_daily_route(df: pd.DataFrame,_master, result: ValidationResult) -> None:
    _validate_by_key(df, result, Layout_type.DAILY_ROUTE.value)

def validate_numeric_irreguler(df: pd.DataFrame,_master, result: ValidationResult) -> None:
    _validate_by_key(df, result, Layout_type.IRREGULAR.value)

def validate_numeric_monthly_cargo(df: pd.DataFrame,_master, result: ValidationResult) -> None:
    _validate_by_key(df, result, Layout_type.MONTHLY_CARGO.value)

def validate_numeric_foreign_cargo(df: pd.DataFrame,_master, result: ValidationResult) -> None:
    _validate_by_key(df, result, Layout_type.FOREIGN_CARGO.value)

def validate_numeric_monthly_cargo2(df: pd.DataFrame,_master, result: ValidationResult) -> None:
    _validate_by_key(df, result, Layout_type.MONTHLY_CARGO2.value)

def validate_numeric_reservation(df: pd.DataFrame,_master, result: ValidationResult) -> None:
    _validate_by_key(df, result, Layout_type.RESERVATION.value)
