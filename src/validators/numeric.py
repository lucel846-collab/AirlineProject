import pandas as pd
from src.validators.validator_result import ValidationResult

REQUIRED_NUMERIC1 = [
    "座席数",
    "旅客数",
    "INF数",
    "貨物重量",
    "メール重量"
]

REQUIRED_NUMERIC2 = [
    "座席数",
    "旅客数",
    "INF数",
    "日本人数",
    "貨物重量",
    "メール重量"
]

REQUIRED_NUMERIC3 = [
    "座席数",
    "旅客数",
    "INF数",
]


REQUIRED_NUMERIC4 = [
    "便数",
    "座席数",
    "旅客数",
    "INF数",
    "貨物重量",
    "メール重量"
]

REQUIRED_NUMERIC7 = [
    "便数",
    "座席数",
    "旅客数",
    "INF数",
    "貨物重量",
    "メール重量"
]

REQUIRED_NUMERIC5 = [
    "便数",
    "貨物重量",
    "メール重量"
]

#　foreign cargo layout8 
REQUIRED_NUMERIC8 = [
    "フレーター便数",
    "積荷重量",
    "卸荷重量",
    "郵便積荷重量",
    "郵便卸荷重量"
]

#　irregal layout6
REQUIRED_NUMERIC6 = [
    "座席数",
    "旅客数",
    "手荷物数",
    "INF数",
    "貨物重量",
    "メール重量"
]

def validate_numeric_base(df: pd.DataFrame, result: ValidationResult, required_columns: list[str]) -> None:
    #必須項目の数値チェックを行う共通ロジック"""
    filename = df.attrs.get("filename")
    for col in required_columns:
         for index, value in df[col].items():
            if not pd.isna(value) and not isinstance(value, (int, float)):
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

def validate_numeric_daily(df: pd.DataFrame,_master, result: ValidationResult) -> None:
    validate_numeric_base(df, result, REQUIRED_NUMERIC1)

def validate_numeric_daily2(df: pd.DataFrame,_master, result: ValidationResult) -> None:
    validate_numeric_base(df, result, REQUIRED_NUMERIC2)

def validate_numeric_daily3(df: pd.DataFrame,_master, result: ValidationResult) -> None:
    validate_numeric_base(df, result, REQUIRED_NUMERIC3)

def validate_numeric_monthly(df: pd.DataFrame,_master, result: ValidationResult) -> None:
    validate_numeric_base(df, result, REQUIRED_NUMERIC4)

def validate_numeric_monthly_cargo(df: pd.DataFrame,_master, result: ValidationResult) -> None:
    validate_numeric_base(df, result, REQUIRED_NUMERIC5)

def validate_numeric_irreguler(df: pd.DataFrame,_master, result: ValidationResult) -> None:
    validate_numeric_base(df, result, REQUIRED_NUMERIC6)

def validate_numeric_daily_route(df: pd.DataFrame,_master, result: ValidationResult) -> None:
    validate_numeric_base(df, result, REQUIRED_NUMERIC7)

def validate_numeric_foreign_cargo(df: pd.DataFrame,_master, result: ValidationResult) -> None:
    validate_numeric_base(df, result, REQUIRED_NUMERIC8)

