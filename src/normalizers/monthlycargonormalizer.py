import pandas as pd

from src.logger import logger
from src.master_data import MasterData
from src.validators.date import privious_month_first_day


class MonthlyCargoNormalizer:

    def __init__(self, master: MasterData):
        self.master = master

    def normalize_prevalidate(self, df: pd.DataFrame) -> None:
        logger.info("チェック前の正規化開始")
        # 年月を日付型で作成する。
        if "年月" not in df.columns :
            df["年月"] = privious_month_first_day(df)
        else:    
            df["年月"] = pd.to_datetime(df["年月"])
        # 空港コードをエイリアスから正規の空港コードに変換
        df["出発空港"] = df["出発空港"].map(self.master.get_airport_cd).fillna(df["出発空港"])
        df["到着空港"] = df["到着空港"].map(self.master.get_airport_cd).fillna(df["到着空港"])
        # 航空会社コード2Lから正規の航空会社コードに変換
        if "航空会社2Lコード" in df.columns:
            df["航空会社"] = df["航空会社2Lコード"].map(self.master.get_airline_code).fillna(df["航空会社2Lコード"])
        logger.info("チェック前の正規化終了")

    def add_airline_name(self, df: pd.DataFrame) -> None:
        logger.info("航空会社名追加開始")
        df["航空会社名"] = df["航空会社"].map(self.master.get_airline_name)
        logger.info("航空会社名追加完了")

    def add_route(self, df: pd.DataFrame) -> None:
        logger.info("路線コード・路線名追加開始")
        df["路線CD"] = df.apply(
            lambda row: self.master.get_route_code(
                row["航空会社"],
                row["事業所"],
                f"{row['出発空港']}{row['到着空港']}"
            ),
            axis=1
        )

        df["路線名"] = df.apply(
            lambda row:self.master.get_route_name(
                row["路線CD"], 
                row["事業所"]
            ),
            axis=1
        )

        logger.info("路線コード・路線名追加完了")
        
    def add_others(self, df: pd.DataFrame) -> None:
        logger.info("その他変換処理開始")

        df["座席数"] = 0
        df["旅客数"] = 0
        df["INF数"] = 0

        logger.info("その他変換処理終了")

