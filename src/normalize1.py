import pandas as pd


def normalize1(df: pd.DataFrame, airport_alias_dict: dict) -> None:
   # 空港コードをエイリアスから正規の空港コードに変換
    df["出発空港"] = df["出発空港"].map(airport_alias_dict).fillna(df["出発空港"])
    df["到着空港"] = df["到着空港"].map(airport_alias_dict).fillna(df["到着空港"])    
   