
def normalize(df: pd.DataFrame, route_alias_dict, airport_alias_dict) -> None:
    # 航空会社コード、事業所、路線コードを結合してルートCDに変換
    df["路線CD"] = df.apply(lambda row: route_alias_dict.get((row["航空会社"], row["事業所"], f"{row['出発空港']}{row['到着空港']}"), None), axis=1)
    
    # 空港コードをエイリアスから正規の空港コードに変換
    df["出発空港"] = df["出発空港"].map(airport_alias_dict).fillna(df["出発空港"])
    df["到着空港"] = df["到着空港"].map(airport_alias_dict).fillna(df["到着空港"])    

