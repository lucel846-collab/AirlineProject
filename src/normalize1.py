import pandas as pd
from src.logger import logger
from src.master_data import MasterData


def normalize1(df: pd.DataFrame,master: MasterData) -> None:
    logger.info("ファイル正規化開始")
   # 空港コードをエイリアスから正規の空港コードに変換
    df["出発空港"] = df["出発空港"].map(master.get_airport_cd).fillna(df["出発空港"])
    df["到着空港"] = df["到着空港"].map(master.get_airport_cd).fillna(df["到着空港"])  
    logger.info("ファイル正規化完了")