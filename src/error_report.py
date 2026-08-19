import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def export_validation_errors(errors, path: Path)->  None: 

    df = pd.DataFrame(errors)

    path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(
        path,
        index=False,
        encoding="utf-8-sig",
    )
    logger.error(f"{len(errors)}件のエラーがあります。")
    logger.info("ValidationError.csv を確認してください。")
