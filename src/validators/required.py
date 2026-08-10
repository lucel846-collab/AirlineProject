import pandas as pd
from src.validator_result import ValidationResult

# 必須列
REQUIRED_COLUMNS1 = [
    "運航区分",
    "運航日",
    "航空会社",
    "便名",
    "出発空港",
    "到着空港",
    "座席数",
    "旅客数",
    "INF数",
    "貨物重量",
    "メール重量",
    "事業所",
]

REQUIRED_COLUMNS2 = [
    "運航区分",
    "年月",
    "航空会社",
    "路線名",
    "発着区分",
    "便数", 
    "座席数",
    "旅客数",
    "INF数",
    "貨物重量",
    "メール重量",
    "事業所",
]

REQUIRED_COLUMNS3 = [
    "運航区分",
    "運航日",
    "航空会社",
    "路線名",
    "便数", 
    "座席数",
    "旅客数",
    "INF数",
    "貨物重量",
    "メール重量",
    "事業所",
]


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

def validate_columns_daily(df: pd.DataFrame,result: ValidationResult) -> None:

    required_columns = REQUIRED_COLUMNS1
    for col in required_columns:
        if col not in df.columns:
            result.add_error(
                index=None,
                column=col,
                value="",
                message="列が存在しません"
            )

def validate_columns_monthly(df: pd.DataFrame,result: ValidationResult) -> None:
    required_columns = REQUIRED_COLUMNS2
    for col in required_columns:
        if col not in df.columns:
            result.add_error(
                index=None,
                column=col,
                value="",
                message="列が存在しません"
            )

def validate_columns_daily_route(df: pd.DataFrame,result: ValidationResult) -> None:
    required_columns = REQUIRED_COLUMNS3
    for col in required_columns:
        if col not in df.columns:
            result.add_error(
                index=None,
                column=col,
                value="",
                message="列が存在しません"
            )
 
def validate_required_daily(df: pd.DataFrame, result: ValidationResult) -> None:
    for col in REQUIRED_COLUMNS1:
        for index, value in df[col].items():
            if pd.isna(value) or str(value).strip() == "":
                result.add_error(
                    index=index,
                    column=col,
                    value=value,
                    message="必須項目です"
                )
def validate_required_monthly(df: pd.DataFrame, result: ValidationResult) -> None:
    for col in REQUIRED_COLUMNS2:
            for index, value in df[col].items():
                if pd.isna(value) or str(value).strip() == "":
                    result.add_error(
                        index=index,
                        column=col,
                        value=value,
                        message="必須項目です"
                    )
    
def validate_required_daily_route(df: pd.DataFrame, result: ValidationResult) -> None:
    for col in REQUIRED_COLUMNS3:
            for index, value in df[col].items():
                if pd.isna(value) or str(value).strip() == "":
                    result.add_error(
                        index=index,
                        column=col,
                        value=value,
                        message="必須項目です"
                    )
    
def validate_numeric_daily(df: pd.DataFrame, result: ValidationResult) -> None:
    for col in REQUIRED_NUMERIC1:
        for index, value in df[col].items():
            if not pd.isna(value) and not isinstance(value, (int, float)):
                result.add_error(
                    index=index,
                    column=col,
                    value=value,
                    message="数値である必要があります"
                )
    
def validate_numeric_monthly(df: pd.DataFrame, result: ValidationResult) -> None:
    for col in REQUIRED_NUMERIC2:
        for index, value in df[col].items():
            if not pd.isna(value) and not isinstance(value, (int, float)):
                result.add_error(
                    index=index,
                    column=col,
                    value=value,
                    message="数値である必要があります"
                )

def validate_numeric_daily_route(df: pd.DataFrame, result: ValidationResult) -> None:
    for col in REQUIRED_NUMERIC3:
        for index, value in df[col].items():
            if not pd.isna(value) and not isinstance(value, (int, float)):
                result.add_error(
                    index=index,
                    column=col,
                    value=value,
                    message="数値である必要があります"
                )
