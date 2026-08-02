import pandas as pd
def normalize2(df: pd.DataFrame, route_alias_dict: dict, route_code_dict: dict)   -> None:
    # 航空会社コード、事業所、路線コードを結合してルートCDに変換
    df["路線CD"] = df.apply(lambda row: route_alias_dict.get((row["航空会社"], row["事業所"], f"{row['出発空港']}{row['到着空港']}"), None), axis=1)
    df["路線名"] = df.apply(lambda row: route_code_dict.get(row["路線CD"]), axis=1)    