import os
from pathlib import Path

import pandas as pd
from src.layout_conv import layout_conv


def read_excel(path: Path) -> pd.DataFrame:
    # 1. 全シート名を取得するため ExcelFile オブジェクトを作成
    excel_file = pd.ExcelFile(path)

    target_sheet = None
    raw_df = None

    # 2. シートを1つずつ確認し「航空旅客輸送実績」があるシートを探す
    for sheet in excel_file.sheet_names:
        df_tmp = pd.read_excel(excel_file, sheet_name=sheet, header=None)

        # シート内に「航空旅客輸送実績」が含まれているか判定
        if any(
            "航空旅客輸送実績" in str(cell)
            for cell in df_tmp.to_numpy().flatten()
        ):
            target_sheet = sheet
            raw_df = df_tmp
            break

    # 3. 該当シートが見つかった場合はレイアウト変換を実施
    if raw_df is not None:
        df = layout_conv(raw_df)
        df.attrs["sheet_name"] = target_sheet  # 読み込んだシート名も記録しておく
    else:
        # 見つからなかった場合はデフォルト（先頭シート）を通常読み込み
        df = pd.read_excel(path)

    df.attrs["filename"] = os.path.basename(path)
    return df