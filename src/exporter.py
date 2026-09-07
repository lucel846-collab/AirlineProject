from pathlib import Path

import pandas as pd

from src.detect_layout import Layout_type
from src.logger import logger

# Define the reindexed columns for each layout type
# Daily l,Daily2,Daily3 ,Irregal layout reindexed columns
REINDEXED_COLUMNS1 = [
    "運航区分",
    "年月",
    "運航日",
    "航空会社",
    "航空会社名",
    "便名",
    "機材名",
    "路線CD",
    "路線名",
    "到着予定空港",
    "便数", 
    "座席数",
    "旅客数",
    "日本人数",
    "INF数",
    "貨物重量",
    "メール重量",
    "備考",
    "事業所",
]
# Monthly route layout
REINDEXED_COLUMNS2 = [
    "運航区分",
    "年月",
    "航空会社",
    "航空会社名",
    "路線CD",
    "路線名",
    "計画便数",
    "有償貨物件数",
    "便数", 
    "座席数",
    "旅客数",
    "INF数",
    "貨物重量",
    "メール重量",
    "事業所",
]
# Daily route layout 
REINDEXED_COLUMNS3 = [
    "運航区分",
    "年月",
    "運航日",
    "航空会社",
    "航空会社名",
    "路線CD",
    "路線名",
    "便数", 
    "座席数",
    "旅客数",
    "INF数",
    "貨物重量",
    "メール重量",
    "事業所",
]
# Monthly cargo layout reindexed columns
REINDEXED_COLUMNS4 = [
    "運航区分",
    "年月",
    "航空会社",
    "航空会社名",
    "路線CD",
    "路線名",
    "便名",
    "便数", 
    "座席数",
    "旅客数",
    "INF数",
    "貨物重量",
    "メール重量",
    "事業所",
]
# foreign Cargo layout reindexed columns
REINDEXED_COLUMNS5 = [
    "運航区分",
    "年月",
    "航空会社",
    "航空会社名",
    "路線CD",
    "路線名",
    "便数", 
    "座席数",
    "旅客数",
    "INF数",
    "貨物重量",
    "メール重量",
    "事業所",
]
# Reservation layout reindexed columns
REINDEXED_COLUMNS6 = [
    "年月",
    "運航日",
    "航空会社",
    "航空会社名",
    "便名",
    "機材名",
    "路線CD",
    "路線名",
    "座席数",
    "旅客数",
    "出発時刻",
    "到着時刻",
    "リードタイム",
    "搭乗手続開始時刻",
    "事業所",
]


def export_csv(df, path: Path,layout:str) -> pd.DataFrame:
    logger.info("CSV出力開始")
    selectors = {
        Layout_type.DAILY.value: REINDEXED_COLUMNS1,
        Layout_type.DAILY2.value: REINDEXED_COLUMNS1,
        Layout_type.DAILY3.value: REINDEXED_COLUMNS1,
        Layout_type.MONTHLY_ROUTE.value: REINDEXED_COLUMNS2,
        Layout_type.DAILY_ROUTE.value: REINDEXED_COLUMNS3,
        Layout_type.MONTHLY_CARGO.value: REINDEXED_COLUMNS4,
        Layout_type.MONTHLY_CARGO2.value: REINDEXED_COLUMNS4,
        Layout_type.FOREIGN_CARGO.value: REINDEXED_COLUMNS5,
        Layout_type.IRREGULAR.value: REINDEXED_COLUMNS1,
        Layout_type.RESERVATION.value: REINDEXED_COLUMNS6,
        }        
    selector = selectors.get(layout)
    df_reindexed =df.reindex(columns=selector)
    df_reindexed.to_csv(path, index=False, encoding="utf-8-sig")
    logger.info("CSV出力完了")