import glob
import os

from src.detect_layout import detect_layout
from src.exporter import export_csv
from src.handlers.factory import HandlerFactory
from src.logger import logger
from src.master_data import MasterData
from src.paths import INPUT_DIR, OUTPUT_DIR
from src.reader import read_excel


class FlightConverter:
    def __init__(self):
        self.master = MasterData()

    def run(self):
        logger.info("▽▽▽変換開始▽▽▽")
        self.master.load() 
        file_paths = glob.glob(f"{INPUT_DIR}/*.xlsx")
        for file_path in file_paths:
            fbasename = os.path.basename(file_path)
            logger.info(f"処理ファイル: {fbasename}")
            df = read_excel(file_path)
            layout =detect_layout(df)
            logger.info(f"レイアウトタイプ: {layout}")
            handler =HandlerFactory.create_handler(layout, self.master)
            
            if handler is None:
                logger.error(f"未対応のレイアウトです: {layout}")
                continue

            result = handler.process(df) 
            if result.has_errors:
                result.export()
                continue
            
            file_out_path = OUTPUT_DIR / fbasename.replace(".xlsx", ".csv")
            export_csv(df, file_out_path,layout)   
        logger.info("△△△変換完了△△△")
  
if __name__ == "__main__":
     FlightConverter().run()

