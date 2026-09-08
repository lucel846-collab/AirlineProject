import pandas as pd

from src.constants import LAYOUT_COLUMNS_MAP
from src.detect_layout import Layout_type
from src.validators.validator_result import ValidationResult


def validate_columns_base(df: pd.DataFrame, result: ValidationResult, required_columns: list[str]) -> None:
    """列の存在チェックを行う共通ロジック"""
    filename = df.attrs.get("filename")
    for col in required_columns:
        if col not in df.columns:
            result.add_error(
                filenm=filename,
                index=0,
                column=col,
                value="",
                message="列が存在しません",
            )

def _validate_by_key(df: pd.DataFrame, result: ValidationResult, layout_key: str) -> None:
    """個別のラッパー関数から呼び出すための内部補助関数"""
    expected_columns = LAYOUT_COLUMNS_MAP.get(layout_key)
    if expected_columns is None:
        raise ValueError(f"定義書に存在しないレイアウト名です: {layout_key}")
    validate_columns_base(df, result, expected_columns)

def validate_columns_daily(df: pd.DataFrame, _master, result: ValidationResult) -> None:
    _validate_by_key(df, result, Layout_type.DAILY.value)  

def validate_columns_daily2(df: pd.DataFrame, _master, result: ValidationResult) -> None:
    _validate_by_key(df, result, Layout_type.DAILY2.value)

def validate_columns_daily3(df: pd.DataFrame, _master, result: ValidationResult) -> None:
    _validate_by_key(df, result, Layout_type.DAILY3.value)

def validate_columns_monthly(df: pd.DataFrame, _master, result: ValidationResult) -> None:
    _validate_by_key(df, result, Layout_type.MONTHLY_ROUTE.value)  

def validate_columns_daily_route(df: pd.DataFrame, _master, result: ValidationResult) -> None:
    _validate_by_key(df, result, Layout_type.DAILY_ROUTE.value)

def validate_columns_irregular(df: pd.DataFrame, _master, result: ValidationResult) -> None:
    _validate_by_key(df, result, Layout_type.IRREGULAR.value)

def validate_columns_monthly_cargo(df: pd.DataFrame, _master, result: ValidationResult) -> None:
    _validate_by_key(df, result, Layout_type.MONTHLY_CARGO.value)

def validate_columns_foreign_cargo(df: pd.DataFrame, _master, result: ValidationResult) -> None:
    _validate_by_key(df, result, Layout_type.FOREIGN_CARGO.value)

def validate_columns_monthly_cargo2(df: pd.DataFrame, _master, result: ValidationResult) -> None:
    _validate_by_key(df, result, Layout_type.MONTHLY_CARGO2.value)

def validate_columns_reservation(df: pd.DataFrame, _master, result: ValidationResult) -> None:
    _validate_by_key(df, result, Layout_type.RESERVATION.value)