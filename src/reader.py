from collections.abc import Callable
from pathlib import Path

import pandas as pd

from src.constants import LAYOUT_CHECK_MAP
from src.converters.layout_cargo import (
    layout_arrival_cargo,
    layout_arrival_mail,
    layout_departure_cargo,
    layout_departure_mail,
)
from src.converters.layout_mixed import (
    layout_passenger_report,
    layout_passenger_report2,
    layout_passenger_report3,
)
from src.converters.layout_passenger import (
    layout_conv_domestic,
    layout_conv_domestic2,
    layout_conv_inter,
)
from src.converters.layout_resavation import layout_reservation_flight
from src.resultform import ReadResult


def _determine_layout(
    df: pd.DataFrame, sheet_name: str) -> tuple[str, str] | Callable | None:
    # セル内の全文字列を結合した1つの大きなテキストを作る（検索を高速化）
    all_text = " ".join(df.head(6).fillna("").astype(str).to_numpy().flatten())
    sorted_layouts = sorted(LAYOUT_CHECK_MAP.items(), key=lambda x: len(x[1]), reverse=True)

    # 1. キーワードだけで一発判定できるもの
    if "航空旅客輸送実績" in all_text:
        if "日本人" in all_text:
            return layout_conv_domestic2
        else:
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

    if "旅客輸送実績" in all_text and sheet_name.startswith("入力シート"):
        
        if "計画便数" in all_text :
            return layout_passenger_report2

        elif "有償貨物件数" in all_text :
            return layout_passenger_report3

        else:
            return layout_passenger_report


        # 必要に応じてMail_Departure用のシート名条件をここに追加
        # if sheet_name.startswith("XXX"):
        #     return layout_departure_mail

    # 3. 一覧形式の自動一括判定（エクセル定義ベース）
    for layout_name, check_cols in sorted_layouts:
        if all(col in all_text for col in check_cols):
            # 状態とレイアウト名をタプルで綺麗に返す
            return "list_format", layout_name

    return None

def read_excel(path: Path) -> list[ReadResult]:
    # 1. 全シート名を取得するため ExcelFile オブジェクトを作成
    excel_file = pd.ExcelFile(path)
    results = []
    for sheet in excel_file.sheet_names:
        # 一旦 header=None で読み込んで判定に回す
        df_tmp = pd.read_excel(excel_file, sheet_name=sheet, header=None)
        result = _determine_layout(df_tmp, sheet)
        if isinstance(result, tuple) :
            status, layout_name = result
            if status == "list_format":
                # 一覧形式のレイアウトが判定された場合、1行目をヘッダーとして正しく読み直す
                df_actual = pd.read_excel(excel_file, sheet_name=sheet)
                df_actual.attrs["layout_name"] = layout_name

                results.append(ReadResult(df=df_actual,layout=layout_name))  
                return results
                
        elif callable(result):
            # 帳票形式の変換関数が返ってきた場合
            results = result(df_tmp)
            return results
        #else:
        #    print(os.path.basename(path))
        #    print(sheet)
        #    print(result)

    #raise ValueError(f"対応するレイアウトが見つかりませんでした: {path.name}")