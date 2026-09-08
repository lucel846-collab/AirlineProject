from pathlib import Path

import pandas as pd

from src.paths import DEFINITION_EXCEL_PATH

# 外部のモジュールから参照させるための空の辞書を初期化
LAYOUT_COLUMNS_MAP = {}     # 各データ型ごとの「全カラムのリスト」
LAYOUT_CHECK_MAP = {}       # レイアウト判定用（黒太字のみのリスト）
NUMERIC_CHECK_MAP = {}      # 数値チェック用（「NUM」が指定されたカラムのみのリスト）
REQUIRED_CHECK_MAP = {}     # 必須チェック用（「必須」が指定されたカラムのみのリスト）
REINDEXED_COLUMNS_MAP = {}  # 出力用（出力定義としてが指定されたカラムのみのリスト）

def load_constants_from_excel(path: Path) -> None:
    """定義書エクセルを3列ずつのブロックとして読み込み、各種定数マップを動的に構築する"""
    if not path.exists():
        raise FileNotFoundError(f"レイアウト定義書が見つかりません: {path}")

    # ヘッダーをなし(None)としてExcelをまるごと読み込む
    df_all = pd.read_excel(path, header=None)

    # 3列1セット（項目、レイアウト判定、NUM/必須）で横にループを回す
    # df_all.shape[1] は全体の列数
    for start_col in range(0, df_all.shape[1], 5):
        # 5列分のデータをスライスで切り出す
        df_block = df_all.iloc[:, start_col:start_col + 5]

        # 切り出したブロックの1行目（インデックス0）からデータ型名（DAILY, DAILY2など）を取得
        layout_name = df_block.iloc[0, 0]
        if pd.isna(layout_name) or str(layout_name).strip() == "":
            continue

        layout_name = str(layout_name).strip()

        # 4行目（インデックス3）以降が実際のデータ行
        df_data = df_block.iloc[3:].dropna(how='all')

        all_cols = []
        layout_cols = []
        num_cols = []
        req_cols = []
        reidx_cols = []

        # 1行ずつチェック
        for _, row in df_data.iterrows():
            item_val = row.iloc[0]    # 1列目: カラム定義
            layout_val = row.iloc[1]  # 2列目: レイアウト判定
            check_val = row.iloc[2]   # 3列目: NUM/必須判定
            req_val = row.iloc[3]     # 4列目: 必須チェック判定
            reidx_val = row.iloc[4]   # 5列目: 出力定義

            if pd.notna(item_val) and str(item_val).strip() != "":
                all_cols.append(str(item_val).strip())

            if pd.notna(layout_val) and str(layout_val).strip() != "":
                layout_cols.append(str(layout_val).strip())

            if pd.notna(check_val) and str(check_val).strip() != "":
                num_cols.append(str(check_val).strip())

            if pd.notna(req_val) and str(req_val).strip() != "":
                req_cols.append(str(req_val).strip())

            if pd.notna(reidx_val) and str(reidx_val).strip() != "":
                reidx_cols.append(str(reidx_val).strip())

        # 綺麗に仕分けたリストを、データ型名をキーにして辞書に登録
        LAYOUT_COLUMNS_MAP[layout_name] = all_cols
        LAYOUT_CHECK_MAP[layout_name] = layout_cols
        NUMERIC_CHECK_MAP[layout_name] = num_cols
        REQUIRED_CHECK_MAP[layout_name] = req_cols
        REINDEXED_COLUMNS_MAP[layout_name] = reidx_cols


# モジュールがインポートされた瞬間に、エクセルから定数を自動で一括読込する
load_constants_from_excel(DEFINITION_EXCEL_PATH)

# 前のステップとの互換性のため、全レイアウトのリスト一覧もタプルで提供
ALL_LAYOUT_COLUMNS = tuple(LAYOUT_CHECK_MAP.values())