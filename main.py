import glob
import os
from pathlib import Path

from src.exporter import export_csv
from src.handlers.factory import HandlerFactory
from src.logger import logger
from src.master_data import MasterData
from src.paths import INPUT_DIR, OUTPUT_DIR
from src.reader import read_excel


def main():
    logger.info("▽▽▽変換開始▽▽▽")

    master = MasterData()
    master.load()

    file_paths = glob.glob(f"{INPUT_DIR}/*.xlsx")

    for file_path in file_paths:
        fbasename = os.path.basename(file_path)

        if fbasename.startswith("~$"):
            continue

        logger.info(f"処理ファイル: {fbasename}")

        read_results = read_excel(file_path)

        for read_result in read_results:
            #print(read_result)
            df = read_result.df
            #layout = detect_layout(df)
            layout = read_result.layout
            logger.info(f"レイアウトタイプ: {layout}")

            handler = HandlerFactory.create_handler(layout, master)

            if handler is None:
                logger.error(f"未対応のレイアウトです: {layout}")
                continue

            result = handler.process(df)

            if result.has_errors:
                result.export()
                continue

            filename = Path(fbasename).stem
            file_out_path = OUTPUT_DIR / f"{filename}_{layout}.csv"
            export_csv(df, file_out_path, layout)

    logger.info("△△△変換完了△△△")


if __name__ == "__main__":
    main()
