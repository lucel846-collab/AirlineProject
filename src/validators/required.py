import pandas as pd
from src.validators.validator_result import ValidationResult

# 必須列
REQUIRED_COLUMNS1 = [
    "運航区分",
    "運航日",
    "航空会社",
    "便名",
    "出発空港",
    "到着空港",
    "機材",
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

REQUIRED_COLUMNS4 = [
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

REQUIRED_COLUMNS5 = [
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

REQUIRED_COLUMNS6 = [
    "運航区分",
    "運航日",
    "航空会社",
    "国内国際",
    "運航種別1",
    "運航種別2",
    "便名",
    "出発空港",
    "到着空港",
    "機材",
    "座席数",
    "旅客数",
    "INF数",
    "貨物重量",
    "メール重量",
    "ハンドリング会社",
    "事業所",
]
def validate_required_base(df: pd.DataFrame, result: ValidationResult, required_columns: list[str]) -> None:
    #必須項目の存在チェックを行う共通ロジック"""
    filename = df.attrs.get("filename")
    for col in required_columns:
         for index, value in df[col].items():
            if pd.isna(value) or str(value).strip() == "":
                result.add_error(
                    filenm=filename,
                    index=index,
                    column=col,
                    value=value,
                    message="必須項目です"
            )
def validate_required_daily(df: pd.DataFrame,_master, result: ValidationResult) -> None:
    validate_required_base(df, result, REQUIRED_COLUMNS1)

def validate_required_monthly(df: pd.DataFrame,_master, result: ValidationResult) -> None:
    validate_required_base(df, result, REQUIRED_COLUMNS2)
    
def validate_required_daily_route(df: pd.DataFrame,_master, result: ValidationResult) -> None:
    validate_required_base(df, result, REQUIRED_COLUMNS3)
    
def validate_required_monthly_cargo(df: pd.DataFrame,_master, result: ValidationResult) -> None:
    validate_required_base(df, result, REQUIRED_COLUMNS4)

def validate_required_foreign_cargo(df: pd.DataFrame,_master, result: ValidationResult) -> None:
    validate_required_base(df, result, REQUIRED_COLUMNS5)

def validate_required_irregular(df: pd.DataFrame,_master, result: ValidationResult) -> None:
    validate_required_base(df, result, REQUIRED_COLUMNS6)
