import pandas as pd
from src.validator_result import ValidationResult

# 必須列
REQUIRED_COLUMNS = [
    "運航日",
    "航空会社",
    "便名",
    "出発空港",
    "運航区分",
    "座席数",
    "旅客数",
    "INF数",
    "貨物重量",
    "メール重量",
    "事業所",
]

REQUIRED_NUMERIC = [
    "座席数",
    "旅客数",
    "INF数",
    "貨物重量",
    "メール重量"
]

REQUIRED_AIRPORT_OFFICE = [
    "AKJ","CTS","MMB","OBO","WKJ","HKD","KUH"  
]

def validate_columns(df: pd.DataFrame,result: ValidationResult) -> None:

    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            result.add_error(
                index=None,
                column=col,
                value="",
                message="列が存在しません"
            )
 
def validate_required(df: pd.DataFrame, result: ValidationResult) -> None:

    for col in REQUIRED_COLUMNS:

        for index, value in df[col].items():

            if pd.isna(value) or str(value).strip() == "":

                result.add_error(
                    index=index,
                    column=col,
                    value=value,
                    message="必須項目です"
                )

def validate_numeric(df: pd.DataFrame, result: ValidationResult) -> None:

    for col in REQUIRED_NUMERIC:

        for index, value in df[col].items():

            if not pd.isna(value) and not isinstance(value, (int, float)):

                result.add_error(
                    index=index,
                    column=col,
                    value=value,
                    message="数値である必要があります"
                )
def validate_airport_office(df: pd.DataFrame, result: ValidationResult) -> None:

    for index, value in df["事業所"].items():

        if value not in REQUIRED_AIRPORT_OFFICE:

            result.add_error(
                index=index,
                column="事業所",
                value=value,
                message="事業所コードが不正です"
            )
                            