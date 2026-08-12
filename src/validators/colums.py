import pandas as pd
from src.validator_result import ValidationResult

# 必須列
LAYOUT_COLUMNS1 = [
    "運航区分",
    "運航日",
    "航空会社",
    "便名",
    "出発空港",
    "到着空港",
    "到着予定空港",
    "機材",
    "座席数",
    "旅客数",
    "INF数",
    "貨物重量",
    "メール重量",
    "備考",
    "事業所",
]

LAYOUT_COLUMNS2 = [
    "運航区分",
    "年月",
    "航空会社",
    "路線名",
    "発着区分",
    "便数", 
    "座席数",
    "旅客数",
    "INF数",
    "有償貨物件数",
    "貨物重量",
    "メール重量",
    "備考",
    "事業所",
]

LAYOUT_COLUMNS3 = [
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
    "備考",
    "事業所",
]

def validate_columns_daily(df: pd.DataFrame,_master,result: ValidationResult) -> None:

    required_columns = LAYOUT_COLUMNS1
    for col in required_columns:
        if col not in df.columns:
            result.add_error(
                index=None,
                column=col,
                value="",
                message="列が存在しません"
            )

def validate_columns_monthly(df: pd.DataFrame,_master,result: ValidationResult) -> None:
    required_columns = LAYOUT_COLUMNS2
    for col in required_columns:
        if col not in df.columns:
            result.add_error(
                index=None,
                column=col,
                value="",
                message="列が存在しません"
            )

def validate_columns_daily_route(df: pd.DataFrame,_master,result: ValidationResult) -> None:
    required_columns = LAYOUT_COLUMNS3
    for col in required_columns:
        if col not in df.columns:
            result.add_error(
                index=None,
                column=col,
                value="",
                message="列が存在しません"
            )
 