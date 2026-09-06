from enum import Enum

import pandas as pd


class Layout_type(Enum):
    DAILY = "DAILY"
    DAILY2 = "DAILY2"
    DAILY3 = "DAILY3"
    MONTHLY_ROUTE = "MONTHLY_ROUTE"
    DAILY_ROUTE = "DAILY_ROUTE"
    IRREGULAR = "IRREGULAR"
    MONTHLY_CARGO = "MONTHLY_CARGO"
    FOREIGN_CARGO = "FOREIGN_CARGO"
    MONTHLY_CARGO2 = "MONTHLY_CARGO2"
    RESERVATION = "RESERVATION"
    UNKNOWN = "UNKNOWN"


def detect_layout(df: pd.DataFrame) -> Layout_type:
    #データフレームのカラム名からレイアウトを判定する関数
    # DAILY, DAILY2, DAILY3, DAILY_ROUTE, FOREIGN_CARGO, MONTHLY_ROUTE, MONTHLY_CARGO,
    #  IRREGULAR, RESERVATION, UNKNOWNのいずれかを返す
    LAYOUT1_COLUMNS = [
        "運航日",
        "便名",
        "出発空港",
        "到着空港",
        "到着予定空港",
        "機材名",
        "貨物重量",
        "メール重量",
        ]
    # DAILY2用の列定義
    LAYOUT2_COLUMNS = [
        "運航日",
        "便名",
        "出発空港",
        "到着空港",
        "到着予定空港",
        "機材名",
        "日本人数",
        "貨物重量",
        "メール重量",
        ]
    # DAILY3用の列定義
    LAYOUT3_COLUMNS = [
        "運航日",
        "便名",
        "出発空港",
        "到着空港",
        "到着予定空港",
        "機材名",
        ]
    # MONTHLY_ROUTE用の列定義
    LAYOUT4_COLUMNS = [
        "年月",
        "路線名",
        "発着区分",
        "計画便数",
        "貨物重量",
        "メール重量",
        ]
    # DAILY_ROUTE用の列定義
    LAYOUT5_COLUMNS = [
        "運航日",
        "路線名",
        "便数",
        "貨物重量",
        "メール重量",
        ]
    # IRREGULAR用の列定義
    LAYOUT6_COLUMNS = [
        "運航種別1",
        "運航種別2",
        "発着区分",
        "ハンドリング会社",
        ]
    # MONTHLY_CARGO用の列定義
    LAYOUT7_COLUMNS = [
        "年月",
        "航空会社",
        "便名",
        "出発空港",
        "到着空港",
        "便数",
        "貨物重量",
        "メール重量",
        ]
    # FOREIGN_CARGO用の列定義
    LAYOUT8_COLUMNS = [
        "年月",
        "相手先空港",                
        "積荷重量",
        "卸荷重量",
        "郵便積荷重量",
        "郵便卸荷重量",
        "フレーター便数",
        ]
 
    # MONTHLY_CARGO2用の列定義
    LAYOUT9_COLUMNS = [
        "航空会社2Lコード",
        "便名",
        "出発空港",
        "到着空港",
        "便数",
        "貨物重量",
        "メール重量",
        ]
    # RESERVATION用の列定義
    LAYOUT10_COLUMNS = [
        "運航日",
        "航空会社2Lコード",
        "便名",
        "出発空港",
        "到着空港",
        "機材名",
        "出発時刻",
        "到着時刻",
        "リードタイム"
        ]

    #レイアウトの判定には特徴のあるカラムを使用する。すべてのカラムが存在する場合にのみ判定する。
    if all(col in df.columns for col in LAYOUT6_COLUMNS):
        return Layout_type.IRREGULAR.value

    elif all(col in df.columns for col in LAYOUT2_COLUMNS):
        return Layout_type.DAILY2.value

    elif all(col in df.columns for col in LAYOUT1_COLUMNS):
        return Layout_type.DAILY.value

    elif all(col in df.columns for col in LAYOUT3_COLUMNS):
        return Layout_type.DAILY3.value

    elif all(col in df.columns for col in LAYOUT4_COLUMNS):
        return Layout_type.MONTHLY_ROUTE.value

    elif all(col in df.columns for col in LAYOUT5_COLUMNS):
        return Layout_type.DAILY_ROUTE.value

    elif all(col in df.columns for col in LAYOUT7_COLUMNS):
        return Layout_type.MONTHLY_CARGO.value

    elif all(col in df.columns for col in LAYOUT8_COLUMNS):
        return Layout_type.FOREIGN_CARGO.value

    elif all(col in df.columns for col in LAYOUT9_COLUMNS):
        return Layout_type.MONTHLY_CARGO2.value
   
    elif all(col in df.columns for col in LAYOUT10_COLUMNS):
        return Layout_type.RESERVATION.value
    
    else:
        return Layout_type.UNKNOWN.value
        