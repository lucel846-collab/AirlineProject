import pandas as pd
from src.logger import logger
from src.master_data import MasterData


class MonthlyNormalizer:

    def __init__(self, master: MasterData):
        self.master = master
    def normalize_airport(self, df: pd.DataFrame) -> None:
        logger.info("年月の正規化開始")
        df["年月"] = pd.to_datetime(df["年月"])
        logger.info("年月の正規化完了")

    def add_airline_name(self, df: pd.DataFrame) -> None:
        logger.info("航空会社名追加開始")
        df["航空会社名"] = df["航空会社"].map(self.master.get_airline_name)
        logger.info("航空会社名追加完了")

    def add_route(self, df: pd.DataFrame) -> None:
        logger.info("路線コード・路線名追加開始")

        #　項目初期化0セット
        if "計画便数" not in df.columns :
            df["計画便数"] = df["計画便数"].astype("Int64")
            df["計画便数"] = 0
        if "有償貨物件数" not in df.columns :
            df["有償貨物件数"] = df["有償貨物件数"].astype("Int64")
            df["有償貨物件数"] = 0

        df["路線CD"] = df.apply(
            lambda row: self.master.get_route_counter(
                row["航空会社"],
                row["事業所"],
                row["路線名"],
                row["発着区分"]
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
        #　入力項目のあるにも関わらず、数値なければ0セット
        df["計画便数"] = df["計画便数"].astype("Int64")
        df["計画便数"] = df["計画便数"].fillna(0)
        df["有償貨物件数"] = df["有償貨物件数"].astype("Int64")
        df["有償貨物件数"] = df["有償貨物件数"].fillna(0)


        df["貨物重量"] = df["貨物重量"].fillna(0)
        df["メール重量"] = df["メール重量"].fillna(0)

        logger.info("路線コード・路線名追加完了")
