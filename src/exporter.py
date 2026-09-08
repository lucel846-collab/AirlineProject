from pathlib import Path

import pandas as pd

from src.constants import REINDEXED_COLUMNS_MAP
from src.logger import logger


def export_csv(df, path: Path,layout:str) -> pd.DataFrame:
    logger.info("CSV出力開始")
    selector = REINDEXED_COLUMNS_MAP.get(layout)
    #print(selector)
    df_reindexed =df.reindex(columns=selector)
    df_reindexed.to_csv(path, index=False, encoding="utf-8-sig")
    logger.info("CSV出力完了")