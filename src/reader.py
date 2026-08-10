from pathlib import Path
import pandas as pd
from src.logger import logger


def read_excel(path: Path) -> pd.DataFrame:
    logger.info(path)
    df = pd.read_excel(path)
    return df