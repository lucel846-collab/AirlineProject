import os
from collections.abc import Callable
from pathlib import Path
from typing import Optional

import pandas as pd

from src.layout_conv import (
    layout_arrival_cargo,
    layout_arrival_mail,
    layout_conv_domestic,
    layout_conv_inter,
    layout_departure_cargo,
    layout_departure_mail,
    layout_reservation_flight,
)


def _determine_layout(df: pd.DataFrame, sheet_name: str) -> Optional[Callable]:
    """シートの内容と名前から、適用すべきレイアウト変換関数を判定する"""
    LAYOUT1_COLUMNS = [
        "運航日",
        "便名",
        "出発空港",
        "到着空港",
        "到着予定空港",
        "機材名",
        "貨物重量",
        "メール重量",
        ]
    # DAILY2用の列定義
    LAYOUT2_COLUMNS = [
        "運航日",
        "便名",
        "出発空港",
        "到着空港",
        "到着予定空港",
        "機材名",
        "日本人数",
        "貨物重量",
        "メール重量",
        ]
    # DAILY3用の列定義
    LAYOUT3_COLUMNS = [
        "運航日",
        "便名",
        "出発空港",
        "到着空港",
        "到着予定空港",
        "機材名",
        ]
    # MONTHLY_ROUTE用の列定義
    LAYOUT4_COLUMNS = [
        "年月",
        "路線名",
        "発着区分",
        "計画便数",
        "貨物重量",
        "メール重量",
        "有償貨物件数",
        ]
    # DAILY_ROUTE用の列定義
    LAYOUT5_COLUMNS = [
        "運航日",
        "路線名",
        "便数",
        "貨物重量",
        "メール重量",
        ]
    # IRREGULAR用の列定義
    LAYOUT6_COLUMNS = [
        "運航種別1",
        "運航種別2",
        "発着区分",
        "機体記号",
        "手荷物数",
        "ハンドリング会社",
        ]
    # MONTHLY_CARGO用の列定義
    LAYOUT7_COLUMNS = [
        "年月",
        "航空会社",
        "便名",
        "出発空港",
        "到着空港",
        "便数",
        "貨物重量",
        "メール重量",
        ]
    # FOREIGN_CARGO用の列定義
    LAYOUT8_COLUMNS = [
        "年月",
        "相手先空港",                
        "積荷重量",
        "卸荷重量",
        "郵便積荷重量",
        "郵便卸荷重量",
        "フレーター便数",
        ]
 
    # MONTHLY_CARGO2用の列定義
    LAYOUT9_COLUMNS = [
        "航空会社2Lコード",
        "便名",
        "出発空港",
        "到着空港",
        "便数",
        "貨物重量",
        "メール重量",
        ]
    # RESERVATION用の列定義
    LAYOUT10_COLUMNS = [
        "運航日",
        "航空会社2Lコード",
        "便名",
        "出発空港",
        "到着空港",
        "機材名",
        "出発時刻",
        "到着時刻",
        "リードタイム"
        ]

    # セル内の全文字列を結合した1つの大きなテキストを作る（検索を高速化）
    all_text = " ".join(df.fillna("").astype(str).to_numpy().flatten())
    # ここで、各レイアウトの列定義と照合して、どのレイアウトに該当するかを判定する
    if any(
        all(col in all_text for col in columns)
        for columns in (
            LAYOUT1_COLUMNS,
            LAYOUT2_COLUMNS,
            LAYOUT3_COLUMNS,
            LAYOUT4_COLUMNS,
            LAYOUT5_COLUMNS,
            LAYOUT6_COLUMNS,
            LAYOUT7_COLUMNS,
            LAYOUT8_COLUMNS,
            LAYOUT9_COLUMNS,
            LAYOUT10_COLUMNS,
        )
    ):
        return "list_format"

    # 1. キーワードだけで一発判定できるもの
    if "航空旅客輸送実績" in all_text:
        return layout_conv_domestic
    if "Air Transport Statistics" in all_text:
        return layout_conv_inter
    if "Passenger Reservations" in all_text:
        return layout_reservation_flight

    # 2. キーワード + シート名で複合判定するもの
    if "到着AIRPORT" in all_text:
        if sheet_name.startswith("Ｈ０１３"):
            return layout_arrival_cargo
        if sheet_name.startswith("H16"):
            return layout_arrival_mail

    if "発送AIRPORT" in all_text:
        if sheet_name.startswith("Ｈ００５"):
            return layout_departure_cargo
        if sheet_name.startswith("Ｈ００８"):
            return layout_departure_mail


        # 必要に応じてMail_Departure用のシート名条件をここに追加
        # if sheet_name.startswith("XXX"):
        #     return layout_departure_mail

    return None

def read_excel(path: Path) -> pd.DataFrame:
    # 1. 全シート名を取得するため ExcelFile オブジェクトを作成
    excel_file = pd.ExcelFile(path)

    for sheet in excel_file.sheet_names:
        # 一旦 header=None で読み込んで判定に回す
        df_tmp = pd.read_excel(excel_file, sheet_name=sheet, header=None)
        result_type = _determine_layout(df_tmp, sheet)
        # レイアウト判定と同時に、対応する関数を取得
        if result_type == "list_format":
            # 一覧形式だと判定された場合、1行目をヘッダーとして正しく読み直す
            # (または df_tmp の1行目を columns に設定する処理でも可)
            df_actual = pd.read_excel(excel_file, sheet_name=sheet) 
            df_actual.attrs["filename"] = os.path.basename(path)
            return df_actual
            
        elif callable(result_type):
            # 帳票形式の変換関数が返ってきた場合
            converted_df = result_type(df_tmp)
            converted_df.attrs["filename"] = os.path.basename(path)
            return converted_df
        
    raise ValueError(f"対応するレイアウトが見つかりませんでした: {path.name}")