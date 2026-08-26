import numpy as np
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
        logger.info("路線コード・路線名・その他変換処理開始")
        #　項目の有無により初期化する
        if "便数" not in df.columns :
            df["便数"] = 1

        if "日本人数" not in df.columns :
            df["日本人数"] = 0

        if "貨物重量" not in df.columns :
            df["貨物重量"] = 0
            df["メール重量"] = 0

        if "備考" not in df.columns :
            df["備考"] = ""    

        # 備考があってもNULLの場合はブランクで初期化しておく
        df["備考"] = np.where(df["備考"].isnull,"",df["備考"])

        # 対策：存在しないカラムを、あらかじめ空の文字列（str）の列として新規作成
        df["路線CD"] = ""
        df["路線名"] = ""
        # 明示的にオブジェクト型（何でも入る型）に
        df["路線CD"] = df["路線CD"].astype(object)
        df["路線名"] = df["路線名"].astype(object)
        # 運航区分をグループに分ける
        is_target1 = df["運航区分"].isin(["SD(定期)", "SI(定期)", "XD(臨時)", "XI(臨時)"])
        is_target2 = df["運航区分"].isin(["ND(CHRT)","NI(CHRT)","ND(周遊)"])
        is_target3 = df["運航区分"].isin(["XD(DVT)","XI(DVT)"])
        is_target4 = df["機材名"].isin(["CNL","CXL"])
        # 運航区分定期および臨時増便の対応
        df.loc[is_target1, "路線CD"] = df[is_target1].apply(
            lambda row: self.master.get_route_code(
                row["航空会社"],
                row["事業所"],
                f"{row['出発空港']}{row['到着空港']}"
            ),
            axis=1
        )
        df.loc[is_target1,"路線名"] = df.apply(
            lambda row:self.master.get_route_name(
                row["路線CD"], 
                row["事業所"]
            ),
            axis=1
        )
        # 運航区分チャーター増便の対応
        df.loc[is_target2, "路線CD"] = df.loc[is_target2].apply(
            lambda row: f"{row['出発空港']}{row['到着空港']}",
            axis=1,
        )
        df.loc[is_target2,"路線名"] = "チャーター"

        # 運航区分ダイバート便の対応
        df.loc[is_target3,"路線CD"] = df.loc[is_target3].apply(
            lambda row: f"{row['出発空港']}{row['到着予定空港']}",
            axis=1,
        )
        df.loc[is_target3,"路線名"] = "その他"

        # 欠航便の備考設定対応
        df.loc[is_target4,"備考"] = "欠航"

        #　到着予定空港の名称取得
        df["到着予定空港"] = df["到着予定空港"].map(self.master.airport_name_dict)
        #　入力項目のあるにも関わらず、項目あれば値セットなければ0セット
        df["日本人数"] = df["日本人数"].fillna(0)
        df["貨物重量"] = df["貨物重量"].fillna(0)
        df["メール重量"] = df["メール重量"].fillna(0)

        logger.info("路線コード・路線名・その他変換処理完了")
