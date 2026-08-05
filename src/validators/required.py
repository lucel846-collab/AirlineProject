import pandas as pd
from src.validators.adderror import add_error

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

def validate_columns(df: pd.DataFrame, errors: list[dict[str, any]]) -> None:

    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            errors.append({"行番号":"","項目名":col,"入力値":"","エラー内容":"列が存在しません"})
 
def validate_required(df: pd.DataFrame, errors: list[dict[str, any]]) -> None:

    for col in REQUIRED_COLUMNS:

        for index, value in df[col].items():

            if pd.isna(value) or str(value).strip() == "":

                add_error(
                    errors,
                    index,
                    col,
                    value,
                    "必須項目です"
                )

def validate_numeric(df: pd.DataFrame, errors: list[dict[str, any]]) -> None:

    for col in REQUIRED_NUMERIC:

        for index, value in df[col].items():

            if not pd.isna(value) and not isinstance(value, (int, float)):

                add_error(
                    errors,
                    index,
                    col,
                    value,
                    "数値である必要があります"
                )
def validate_airport_office(df: pd.DataFrame, errors: list[dict[str, any]]) -> None:

    for index, value in df["事業所"].items():

        if value not in REQUIRED_AIRPORT_OFFICE:

            add_error(
                errors,
                index,
                "事業所",
                value,
                "事業所コードが不正です"
            )
                            