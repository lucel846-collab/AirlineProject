import pandas as pd
from src.validators.validator_result import ValidationResult

# 必須列
LAYOUT_COLUMNS1 = [
    "運航区分",
    "運航日",
    "航空会社",
    "便名",
    "出発空港",
    "到着空港",
    "到着予定空港",
    "機材名",
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
    "運航日",
    "航空会社",
    "便名",
    "出発空港",
    "到着空港",
    "到着予定空港",
    "機材名",
    "座席数",
    "日本人数",
    "旅客数",
    "INF数",
    "貨物重量",
    "メール重量",
    "備考",
    "事業所",
]

LAYOUT_COLUMNS3 = [
    "運航区分",
    "運航日",
    "航空会社",
    "便名",
    "出発空港",
    "到着空港",
    "到着予定空港",
    "機材名",
    "座席数",
    "旅客数",
    "INF数",
    "備考",
    "事業所",
]


LAYOUT_COLUMNS4 = [
    "運航区分",
    "年月",
    "航空会社",
    "路線名",
    "発着区分",
    "計画便数", 
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

LAYOUT_COLUMNS7 = [
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

LAYOUT_COLUMNS5 = [
    "運航区分",
    "年月",
    "航空会社",
    "便名",
    "出発空港",
    "到着空港",
    "便数", 
    "貨物重量",
    "メール重量",
    "事業所",
]

LAYOUT_COLUMNS8 = [
    "運航区分",
    "年月",
    "航空会社",
    "相手先空港",
    "フレーター便数",
    "積荷重量",
    "卸荷重量",
    "郵便積荷重量",
    "郵便卸荷重量",
    "事業所",
]

LAYOUT_COLUMNS6 = [
    "運航区分",
    "運航日",
    "航空会社",
    "国内国際",
    "運航種別1",
    "運航種別2",
    "便名",
    "出発空港",
    "到着空港",
    "到着予定空港",
    "発着区分",
    "機体記号",
    "機材名",
    "座席数",
    "旅客数",
    "手荷物数",
    "INF数",
    "貨物重量",
    "メール重量",
    "ハンドリング会社",
    "事業所",
]

# --- 共通ロジック関数 ---
def validate_columns_base(df: pd.DataFrame, result: ValidationResult, required_columns: list[str]) -> None:
    #列の存在チェックを行う共通ロジック
    filename = df.attrs.get("filename")
    for col in required_columns:
        if col not in df.columns:
            result.add_error(
                filenm=filename,
                index=0,
                column=col,
                value="",
                message="列が存在しません"
            )

def validate_columns_daily(df: pd.DataFrame,_master,result: ValidationResult) -> None:
    validate_columns_base(df, result, LAYOUT_COLUMNS1)

def validate_columns_daily2(df: pd.DataFrame,_master,result: ValidationResult) -> None:
    validate_columns_base(df, result, LAYOUT_COLUMNS2)

def validate_columns_daily3(df: pd.DataFrame,_master,result: ValidationResult) -> None:
    validate_columns_base(df, result, LAYOUT_COLUMNS3)

def validate_columns_monthly(df: pd.DataFrame,_master,result: ValidationResult) -> None:
    validate_columns_base(df, result, LAYOUT_COLUMNS4)

def validate_columns_monthly_cargo(df: pd.DataFrame,_master,result: ValidationResult) -> None:
    validate_columns_base(df, result, LAYOUT_COLUMNS5)

def validate_columns_irregular(df: pd.DataFrame,_master,result: ValidationResult) -> None:
    validate_columns_base(df, result, LAYOUT_COLUMNS6)

def validate_columns_daily_route(df: pd.DataFrame,_master,result: ValidationResult) -> None:
    validate_columns_base(df, result, LAYOUT_COLUMNS7)

def validate_columns_foreign_cargo(df: pd.DataFrame,_master,result: ValidationResult) -> None:
    validate_columns_base(df, result, LAYOUT_COLUMNS8)

