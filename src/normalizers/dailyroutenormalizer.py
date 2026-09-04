import pandas as pd

from src.logger import logger
from src.master_data import MasterData
from src.validators.date import privious_month_first_day


class DailyRouteNormalizer:

    def __init__(self, master: MasterData):
        self.master = master

    def normalize_prevalidate(self, df: pd.DataFrame) -> None:
        logger.info("チェック前の正規化開始")
        df["運航日"] = pd.to_datetime(df["運航日"])
        # 年月を作成する。
        df["年月"] = privious_month_first_day(df)
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
                row["路線名"]
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

        df["貨物重量"] = df["貨物重量"].fillna(0)
        df["メール重量"] = df["メール重量"].fillna(0)

        logger.info("その他変換処理終了")

