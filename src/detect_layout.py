from enum import Enum

import pandas as pd

from src.constants import LAYOUT_CHECK_MAP


class Layout_type(Enum):
    DAILY = "DAILY"
    DAILY2 = "DAILY2"
    DAILY3 = "DAILY3"
    MONTHLY_ROUTE = "MONTHLY_ROUTE"
    DAILY_ROUTE = "DAILY_ROUTE"
    IRREGULAR = "IRREGULAR"
    MONTHLY_CARGO = "MONTHLY_CARGO"
    FOREIGN_CARGO = "FOREIGN_CARGO"
    MONTHLY_CARGO2 = "MONTHLY_CARGO2"
    RESERVATION = "RESERVATION"
    UNKNOWN = "UNKNOWN"


def detect_layout(df: pd.DataFrame) -> str:
    """
    データフレームからレイアウト名を判定する関数。
    
    1. すでに reader.py 側で判定済みの場合は、その結果をそのまま利用する。
    2. 記録がない場合は、エクセル定義（LAYOUT_CHECK_MAP）を元に動的に判定する。
    """
    # --- パターンA: すでに reader.py が判定して記録してくれている場合 ---
    if "layout_name" in df.attrs:
        layout_name = df.attrs["layout_name"]
        # Enumに定義されている妥当な名前であれば、その値をそのまま返す
        if layout_name in Layout_type.__members__:
            return Layout_type[layout_name].value

    # --- パターンB: 単体でデータフレームが渡され、再判定が必要な場合 ---
    # 条件の厳しい順（カラム数が多い順）に並び替えて、誤判定を防ぎつつループチェック
    sorted_layouts = sorted(LAYOUT_CHECK_MAP.items(), key=lambda x: len(x), reverse=True)
    
    for layout_name, check_cols in sorted_layouts:
        if all(col in df.columns for col in check_cols):
            return Layout_type[layout_name].value
            
    return Layout_type.UNKNOWN.value