import pandas as pd
from src.logger import logger
from src.master_data import MasterData


class DailyNormalizer:

    def __init__(self, master: MasterData):
        self.master = master
    def normalize_airport(self, df: pd.DataFrame) -> None:
        logger.info("運航日・空港コードの正規化開始")
        df["運航日"] = pd.to_datetime(df["運航日"])
        # 空港コードをエイリアスから正規の空港コードに変換
        df["出発空港"] = df["出発空港"].map(self.master.get_airport_cd).fillna(df["出発空港"])
        df["到着空港"] = df["到着空港"].map(self.master.get_airport_cd).fillna(df["到着空港"])
        df["到着予定空港"] = df["到着予定空港"].map(self.master.get_airport_cd).fillna(df["到着予定空港"])
        logger.info("運航日・空港コードの正規化完了")

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

        df["到着予定空港"] = df["到着予定空港"].map(self.master.airport_name_dict)
            
        logger.info("路線コード・路線名追加完了")

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
        logger.info("路線コード・路線名追加完了")

class DailyRouteNormalizer:

    def __init__(self, master: MasterData):
        self.master = master
    def normalize_airport(self, df: pd.DataFrame) -> None:
        logger.info("運航日の正規化開始")
        df["運航日"] = pd.to_datetime(df["運航日"])
        logger.info("運航日の正規化完了")

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


class MonthlyCargoNormalizer:

    def __init__(self, master: MasterData):
        self.master = master
    def normalize_airport(self, df: pd.DataFrame) -> None:
        logger.info("運航日の正規化開始")
        df["年月"] = pd.to_datetime(df["年月"])
        logger.info("運航日の正規化完了")

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
        df["座席数"] = 0
        df["旅客数"] = 0
        df["INF数"] = 0

        logger.info("路線コード・路線名追加完了")


class ForeignCargoNormalizer:

    def __init__(self, master: MasterData):
        self.master = master
    def normalize_airport(self, df: pd.DataFrame) -> None:
        logger.info("運航日の正規化開始")
        df["年月"] = pd.to_datetime(df["年月"])
        logger.info("運航日の正規化完了")

    def add_airline_name(self, df: pd.DataFrame) -> None:
        logger.info("航空会社名追加開始")
        df["航空会社名"] = df["航空会社"].map(self.master.get_airline_name)
        logger.info("航空会社名追加完了")

    def add_route(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("路線コード・路線名追加開始")

        df_proc =df.copy()

        df_proc["便数"] = df_proc["フレーター便数"]
        #出発（積荷）データの作成
        df_divide1 = df_proc[["運航区分",
                                "年月",
                                "航空会社",
                                "航空会社名",
                                "相手先空港",
                                "便数",
                                "積荷重量",
                                "郵便積荷重量",
                                "事業所"
                                ]].rename(columns={"積荷重量":"貨物重量",
                                                   "郵便積荷重量":"メール重量"})
        df_divide1["発着区分"] = "出発"

        df_divide2 = df_proc[["運航区分",
                                "年月",
                                "航空会社",
                                "航空会社名",
                                "相手先空港",
                                "便数",
                                "卸荷重量",
                                "郵便卸荷重量",
                                "事業所"
                                ]].rename(columns={"卸荷重量":"貨物重量",
                                                   "郵便卸荷重量":"メール重量"})
        df_divide2["発着区分"] = "到着"
        df_divide2["便数"] = 0      #便数は変更ないので、到着分を0にして、合計では変更ないようにする
        df_combined = pd.concat([df_divide1, df_divide2], ignore_index=True)
        # データ拡張後のデータに対して実施
        df_combined["路線CD"] = df_combined.apply(
            lambda row: self.master.get_route_counter(
                row["航空会社"],
                row["事業所"],
                f"{row['相手先空港']}{row['事業所']}",
                row["発着区分"]
            ),
            axis=1
        )

        df_combined["路線名"] = df_combined.apply(
            lambda row:self.master.get_route_name(
                row["路線CD"], 
                row["事業所"]
            ),
            axis=1
        )

        # 元のdfのすべての行・列を完全に消去（クリア）
        df.drop(df.index, inplace=True)
        df.drop(df.columns, axis=1, inplace=True)

        for col in df_combined.columns:
            df[col] = df_combined[col] # データを上書き

        logger.info("路線コード・路線名追加完了")
        return df