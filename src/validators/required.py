import pandas as pd
from src.detect_layout import detect_layout
from src.validator_result import ValidationResult

# 必須列
REQUIRED_COLUMNS1 = [
    "運航日",
    "航空会社",
    "便名",
    "出発空港",
    "到着空港",
    "運航区分",
    "座席数",
    "旅客数",
    "INF数",
    "貨物重量",
    "メール重量",
    "事業所",
]

REQUIRED_COLUMNS2 = [
    "年月",
    "航空会社",
    "路線名",
    "運航区分",
    "発着区分",
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


REQUIRED_AIRPORT_OFFICE = [
    "AKJ","CTS","MMB","OBO","WKJ","HKD","KUH"  
]

def validate_columns(df: pd.DataFrame,result: ValidationResult) -> None:

    layout = detect_layout(df)
    if layout == "DAILY_FLIGHT":
        required_columns = REQUIRED_COLUMNS1
        for col in required_columns:
            if col not in df.columns:
                result.add_error(
                    index=None,
                    column=col,
                    value="",
                    message="列が存在しません"
                )

    elif layout == "MONTHLY_ROUTE":
        required_columns = REQUIRED_COLUMNS2
        for col in required_columns:
            if col not in df.columns:
                result.add_error(
                    index=None,
                    column=col,
                    value="",
                    message="列が存在しません"
                )

 
def validate_required(df: pd.DataFrame, result: ValidationResult) -> None:
    layout = detect_layout(df)
    if layout == "DAILY_FLIGHT":
        for col in REQUIRED_COLUMNS1:
          for index, value in df[col].items():
                if pd.isna(value) or str(value).strip() == "":
                    result.add_error(
                        index=index,
                        column=col,
                        value=value,
                        message="必須項目です"
                    )
    elif layout == "MONTHLY_ROUTE":
        for col in REQUIRED_COLUMNS2:
              for index, value in df[col].items():
  
                  if pd.isna(value) or str(value).strip() == "":
  
                      result.add_error(
                          index=index,
                          column=col,
                          value=value,
                          message="必須項目です"
                      )
    
def validate_numeric(df: pd.DataFrame, result: ValidationResult) -> None:
    layout = detect_layout(df)
    if layout == "DAILY_FLIGHT":
        for col in REQUIRED_NUMERIC1:
            for index, value in df[col].items():
                if not pd.isna(value) and not isinstance(value, (int, float)):
                    result.add_error(
                        index=index,
                        column=col,
                        value=value,
                        message="数値である必要があります"
                    )
    elif layout == "MONTHLY_ROUTE":
        for col in REQUIRED_NUMERIC2:
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
                            