from pathlib import Path

import pandas as pd
from src.logger import logger


def export_csv(df, path: Path) -> pd.DataFrame:
    logger.info("CSV出力開始")
    df.to_csv(path, index=False, encoding="utf-8-sig")
    logger.info("CSV出力完了")