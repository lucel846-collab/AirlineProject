import pandas as pd
from src.logger import logger
from src.master_data import MasterData


def normalize2(df: pd.DataFrame,master: MasterData)   -> None:
    logger.info("航空会社名追加開始")
    df["航空会社名"] = df["航空会社"].map(master.get_airline_name)
    logger.info("航空会社名追加完了")

    logger.info("ルートコード追加開始")
    # 航空会社コード、事業所、路線コードを結合してルートCDに変換
    df["路線CD"] = df.apply(
        lambda row: master.get_route_code(
            row["航空会社"],
            row["事業所"],
            f"{row['出発空港']}{row['到着空港']}"
        ),
        axis=1
    )

    logger.info("ルートコード追加完了")
    logger.info("ルート名追加開始")
    df["路線名"] = df["路線CD"].map(master.get_route_name)
    logger.info("ルート名追加完了")
    