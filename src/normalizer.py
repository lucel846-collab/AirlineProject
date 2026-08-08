import pandas as pd
from src.detect_layout import detect_layout
from src.logger import logger
from src.master_data import MasterData


class Normalizer:

    def __init__(self, master: MasterData):
        self.master = master
    def normalize_airport(self, df: pd.DataFrame) -> None:
        if detect_layout(df) == "DAILY_FLIGHT":
            logger.info("運航日・空港コードの正規化開始")
            df["運航日"] = pd.to_datetime(df["運航日"])
            # 空港コードをエイリアスから正規の空港コードに変換
            df["出発空港"] = df["出発空港"].map(self.master.get_airport_cd).fillna(df["出発空港"])
            df["到着空港"] = df["到着空港"].map(self.master.get_airport_cd).fillna(df["到着空港"])
            df["到着予定空港"] = df["到着予定空港"].map(self.master.get_airport_cd).fillna(df["到着予定空港"])
            logger.info("運航日・空港コードの正規化完了")
        elif detect_layout(df) == "MONTHLY_ROUTE":
            logger.info("年月の正規化開始")
            df["年月"] = pd.to_datetime(df["年月"])
            logger.info("年月の正規化完了")

    def add_airline_name(self, df: pd.DataFrame) -> None:
        logger.info("航空会社名追加開始")
        df["航空会社名"] = df["航空会社"].map(self.master.get_airline_name)
        logger.info("航空会社名追加完了")

    def add_route(self, df: pd.DataFrame) -> None:
        if detect_layout(df) == "DAILY_FLIGHT":
            logger.info("路線コード・路線名追加開始")
            df["路線CD"] = df.apply(
                lambda row: self.master.get_route_code(
                    row["航空会社"],
                    row["事業所"],
                    f"{row['出発空港']}{row['到着空港']}"
                ),
                axis=1
            )


        elif detect_layout(df) == "MONTHLY_ROUTE":
            logger.info("路線コード・路線名追加開始")
            df["路線CD"] = df.apply(
                lambda row: self.master.get_route_code(
                    row["航空会社"],
                    row["事業所"],
                    row["路線名"]
                ),
                axis=1
            )

        df["路線名"] = df["路線CD"].map(self.master.get_route_name)
        logger.info("路線コード・路線名追加完了")


