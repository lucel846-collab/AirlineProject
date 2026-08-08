import pandas as pd


def detect_layout(df: pd.DataFrame) -> str:
    #データフレームのカラム名からレイアウトを判定する関数
    LAYOUT1_COLUMNS = [
        "運航区分", 
        "運航日", 
        "航空会社", 
        "便名", 
        "出発空港", 
        "到着空港", 
        "到着予定空港", 
        "機材", 
        "座席数", 
        "旅客数", 
        "INF数", 
        "貨物重量", 
        "メール重量", 
        "備考", 
        "事業所"]
    LAYOUT2_COLUMNS = [
        "運航区分", 
        "年月", 
        "航空会社", 
        "路線名", 
        "発着区分", 
        "計画便数", 
        "便数", 
        "座席数", 
        "旅客数", 
        "INF数", 
        "有償貨物件数", 
        "貨物重量", 
        "メール重量", 
        "備考", 
        "事業所"]

    if all(col in df.columns for col in LAYOUT1_COLUMNS):
        return "DAILY_FLIGHT"
    elif all(col in df.columns for col in LAYOUT2_COLUMNS):
        return "MONTHLY_ROUTE"
    else:
        return "UNKNOWN"