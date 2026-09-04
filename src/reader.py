import os
from pathlib import Path

import pandas as pd

from src.layout_conv import (
    layout_arrival_cargo,
    layout_arrival_mail,
    layout_conv_domestic,
    layout_conv_inter,
    layout_departure_cargo,
    layout_departure_mail,
)


def read_excel(path: Path) -> pd.DataFrame:
    # 1. 全シート名を取得するため ExcelFile オブジェクトを作成
    excel_file = pd.ExcelFile(path)

    raw_df = None

    # 2. シートを1つずつ確認し「航空旅客輸送実績」があるシートを探す
    for sheet in excel_file.sheet_names:
        df_tmp = pd.read_excel(excel_file, sheet_name=sheet, header=None)
        # レイアウト判定用のフラグを初期化
        domein_flight_layout = False
        Cargo_Arrival_layout = False
        Cargo_Departure_layout = False
        Mail_Arrival_layout = False
        Mail_Departure_layout = False
        international_flight_layout = False

        # シート内に「航空旅客輸送実績」が含まれているか判定
        if any(
            "航空旅客輸送実績" in str(cell)
            for cell in df_tmp.to_numpy().flatten()
            ):
            domein_flight_layout = True
            raw_df = df_tmp
            break
        elif any(
            "Air Transport Statistics" in str(cell)
            for cell in df_tmp.to_numpy().flatten()
            ):
            international_flight_layout = True
            raw_df = df_tmp
            break

        elif any(
            "到着AIRPORT" in str(cell)
            for cell in df_tmp.to_numpy().flatten()
            ):
            raw_df = df_tmp
            if sheet.startswith("Ｈ０１３"):
                Cargo_Arrival_layout = True
                break
            elif sheet.startswith("H16"):   
                Mail_Arrival_layout = True
            break

        elif any(
            "発送AIRPORT" in str(cell)
            for cell in df_tmp.to_numpy().flatten()
            ):
            raw_df = df_tmp
            if sheet.startswith("Ｈ００５"):
                Cargo_Departure_layout = True
                break
            elif sheet.startswith("Ｈ００８"):
                Mail_Departure_layout = True
            break


    # 3. 該当シートが見つかった場合はレイアウト変換を実施
    if raw_df is not None:
        if  domein_flight_layout == True :
            df = layout_conv_domestic(raw_df)
        elif international_flight_layout == True:
            df = layout_conv_inter(raw_df)
        elif Cargo_Arrival_layout == True:
            df = layout_arrival_cargo(raw_df)
        elif Cargo_Departure_layout == True:
            df = layout_departure_cargo(raw_df)
        elif Mail_Arrival_layout == True:
            df = layout_arrival_mail(raw_df)
        elif Mail_Departure_layout == True:
            df = layout_departure_mail(raw_df)
    else:
        # 見つからなかった場合はデフォルト（先頭シート）を通常読み込み
        df = pd.read_excel(path)

    df.attrs["filename"] = os.path.basename(path)
    return df