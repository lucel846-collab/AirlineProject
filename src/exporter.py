from pathlib import Path

import pandas as pd
from src.detect_layout import Layout_type
from src.logger import logger

REINDEXED_COLUMNS1 = [
    "運航区分",
    "運航日",
    "航空会社",
    "航空会社名",
    "便名",
    "路線名",
    "出発空港",
    "到着空港",
    "到着予定空港",
    "路線CD",
    "座席数",
    "旅客数",
    "INF数",
    "貨物重量",
    "メール重量",
    "事業所",
]

REINDEXED_COLUMNS2 = [
    "運航区分",
    "年月",
    "航空会社",
    "航空会社名",
    "路線CD",
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

REINDEXED_COLUMNS3 = [
    "運航区分",
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



def export_csv(df, path: Path,layout:str) -> pd.DataFrame:
    logger.info("CSV出力開始")
    selectors = {
        Layout_type.DAILY_FLIGHT.value: REINDEXED_COLUMNS1,
        Layout_type.MONTHLY_ROUTE.value: REINDEXED_COLUMNS2,
        Layout_type.DAILY_ROUTE.value: REINDEXED_COLUMNS3,
        }
    selector = selectors.get(layout)
    df_reindexed =df.reindex(columns=selector)
    df_reindexed.to_csv(path, index=False, encoding="utf-8-sig")
    logger.info("CSV出力完了")