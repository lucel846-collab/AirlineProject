import os
from collections.abc import Callable
from pathlib import Path

import pandas as pd

from src.constants import LAYOUT_CHECK_MAP
from src.layout_conv import (
    layout_arrival_cargo,
    layout_arrival_mail,
    layout_conv_domestic,
    layout_conv_inter,
    layout_departure_cargo,
    layout_departure_mail,
    layout_reservation_flight,
)


def _determine_layout(
    df: pd.DataFrame, sheet_name: str
) -> tuple[str, str] | Callable | None:
    # セル内の全文字列を結合した1つの大きなテキストを作る（検索を高速化）
    all_text = " ".join(df.fillna("").astype(str).to_numpy().flatten())
    """ ここで、各レイアウト """   
    """シートの内容と名前から、適用すべきレイアウトを判定する。
    
    戻り値:
        - 一覧形式の場合: ("list_format", "DAILY") のようなタプル
        - 帳票形式の場合: 変換関数 (Callable)
        - 該当なしの場合: None
    """
      # セル内の全文字列を結合した1つの大きなテキストを作る（検索を高速化）
    all_text = " ".join(df.fillna("").astype(str).to_numpy().flatten())
    sorted_layouts = sorted(LAYOUT_CHECK_MAP.items(), key=lambda x: len(x[1]), reverse=True)
    # 1. 一覧形式の自動一括判定（エクセル定義ベース）
    for layout_name, check_cols in sorted_layouts:
        if all(col in all_text for col in check_cols):
            # 状態とレイアウト名をタプルで綺麗に返す
            return "list_format", layout_name

    # 2. キーワードだけで一発判定できるもの
    if "航空旅客輸送実績" in all_text:
        return layout_conv_domestic
    if "Air Transport Statistics" in all_text:
        return layout_conv_inter
    if "Passenger Reservations" in all_text:
        return layout_reservation_flight

    # 3. キーワード + シート名で複合判定するもの
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
        result = _determine_layout(df_tmp, sheet)
        if isinstance(result, tuple) :
            status, layout_name = result
            if status == "list_format":
                # 一覧形式のレイアウトが判定された場合、1行目をヘッダーとして正しく読み直す
                df_actual = pd.read_excel(excel_file, sheet_name=sheet)
                df_actual.attrs["filename"] = os.path.basename(path)
                df_actual.attrs["layout_name"] = layout_name

                return df_actual  
            
        elif callable(result):
            # 帳票形式の変換関数が返ってきた場合
            converted_df = result(df_tmp)
            converted_df.attrs["filename"] = os.path.basename(path)
            return converted_df
        #else:
        #    print(os.path.basename(path))
        #    print(sheet)
        #    print(result)

    #raise ValueError(f"対応するレイアウトが見つかりませんでした: {path.name}")