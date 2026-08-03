import pandas as pd
from src.logger import logger


def normalize2(df: pd.DataFrame, route_alias_dict: dict, route_code_dict: dict)   -> None:
    logger.info("ルートコード追加開始")
    # 航空会社コード、事業所、路線コードを結合してルートCDに変換
    df["路線CD"] = df.apply(
        lambda row: route_alias_dict.get(
            (
                row["航空会社"], 
                row["事業所"], 
                f"{row['出発空港']}{row['到着空港']}"
            ),
    None),
    axis=1
    )
    logger.info("ルートコード追加完了")
    logger.info("ルート名追加開始")
    df["路線名"] = df["路線CD"].map(route_code_dict)
    logger.info("ルート名追加完了")
 