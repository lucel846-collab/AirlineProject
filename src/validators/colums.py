import pandas as pd

from src.validators.validator_result import ValidationResult

# カラムの存在列
# 日次データ用の列定義
DAILY_COLUMNS  = [
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
# 日次データ2用の列定義
DAILY2_COLUMNS = [
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
# 日次データ3用の列定義
DAILY3_COLUMNS = [
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
# 月次データ用の列定義
MONTHLYR_COLUMNS = [
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
# 日次ルートデータ用の列定義
DAILYR_COLUMNS = [
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

# 不定期便データ用の列定義
IRREGULAR_COLUMNS = [
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
# 月次貨物専用データ用の列定義
MONTHLYC_COLUMNS = [
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

# 海外貨物データ用の列定義
FOREIGNC_COLUMNS = [
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
# 月次貨物データ2用の列定義
MONTHLYC2_COLUMNS = [
    "運航区分",
    "航空会社2Lコード",
    "便名",
    "出発空港",
    "到着空港",
    "便数",
    "貨物重量",
    "メール重量",
    "事業所",
]
# 予約データ用の列定義
RESERVATION_COLUMNS = [
    "運航日",
    "航空会社2Lコード",
    "便名",
    "出発空港",
    "到着空港",
    "機材名",
    "座席数",
    "旅客数",
    "出発時刻",
    "到着時刻",
    "事業所",
    "リードタイム",
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
    validate_columns_base(df, result, DAILY_COLUMNS)  

def validate_columns_daily2(df: pd.DataFrame,_master,result: ValidationResult) -> None:
    validate_columns_base(df, result, DAILY2_COLUMNS)

def validate_columns_daily3(df: pd.DataFrame,_master,result: ValidationResult) -> None:
    validate_columns_base(df, result, DAILY3_COLUMNS)

def validate_columns_monthly(df: pd.DataFrame,_master,result: ValidationResult) -> None:
    validate_columns_base(df, result, MONTHLYR_COLUMNS)

def validate_columns_daily_route(df: pd.DataFrame,_master,result: ValidationResult) -> None:
    validate_columns_base(df, result, DAILYR_COLUMNS)

def validate_columns_irregular(df: pd.DataFrame,_master,result: ValidationResult) -> None:
    validate_columns_base(df, result, IRREGULAR_COLUMNS)

def validate_columns_monthly_cargo(df: pd.DataFrame,_master,result: ValidationResult) -> None:
    validate_columns_base(df, result, MONTHLYC_COLUMNS)

def validate_columns_foreign_cargo(df: pd.DataFrame,_master,result: ValidationResult) -> None:
    validate_columns_base(df, result, FOREIGNC_COLUMNS)

def validate_columns_monthly_cargo2(df: pd.DataFrame,_master,result: ValidationResult) -> None:
    validate_columns_base(df, result, MONTHLYC2_COLUMNS)

def validate_columns_reservation(df: pd.DataFrame,_master,result: ValidationResult) -> None:
    validate_columns_base(df, result, RESERVATION_COLUMNS)
