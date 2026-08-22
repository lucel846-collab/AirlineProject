from enum import Enum

import pandas as pd


class Layout_type(Enum):
    DAILY = "DAILY"
    DAILY2 = "DAILY2"
    DAILY3 = "DAILY3"
    DAILY_ROUTE = "DAILY_ROUTE"
    FOREIGN_CARGO = "FOREIGN_CARGO"
    MONTHLY_ROUTE = "MONTHLY_ROUTE"
    MONTHLY_CARGO = "MONTHLY_CARGO"
    IRREGULAR = "IRREGULAR"
    UNKNOWN = "UNKNOWN"


def detect_layout(df: pd.DataFrame) -> Layout_type:
    #データフレームのカラム名からレイアウトを判定する関数
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

    LAYOUT3_COLUMNS = [
        "運航日",
        "便名",
        "出発空港",
        "到着空港",
        "到着予定空港",
        "機材名",
        ]

    LAYOUT4_COLUMNS = [
        "年月",
        "路線名",
        "計画便数",
        "発着区分",
        "貨物重量",
        "メール重量",
        ]

    LAYOUT5_COLUMNS = [
        "運航日",
        "路線名",
        "便数",
        "貨物重量",
        "メール重量",
        ]

    LAYOUT6_COLUMNS = [
        "運航種別1",
        "運航種別2",
        "発着区分",
        "ハンドリング会社",
        ]

    LAYOUT7_COLUMNS = [
        "年月",
        "便名",
        "出発空港",
        "到着空港",
        "便数",
        "貨物重量",
        "メール重量",
        ]

    LAYOUT8_COLUMNS = [
        "フレーター便数",
        "積荷重量",
        "卸荷重量",
        "郵便積荷重量",
        "郵便卸荷重量"
        ]

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

    else:
        return Layout_type.UNKNOWN.value
        