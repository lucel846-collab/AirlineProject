import glob
import os

from src.detect_layout import Layout_type, detect_layout
from src.exporter import export_csv
from src.handlers.daily_flight import DailyFlightHandler
from src.handlers.daily_route import DailyRouteHandler
from src.handlers.foreign_cargo import ForeignCargoHandler
from src.handlers.monthly_cargo import MonthlyCargoHandler
from src.handlers.monthly_flight import MonthlyRouteHandler
from src.logger import logger
from src.master_data import MasterData
from src.paths import INPUT_DIR, OUTPUT_DIR
from src.reader import read_excel


class FlightConverter:
    def __init__(self):
        self.master = MasterData()

    def run(self):
        handlers = {
            Layout_type.DAILY_FLIGHT.value: DailyFlightHandler(self.master),
            Layout_type.MONTHLY_ROUTE.value: MonthlyRouteHandler(self.master),
            Layout_type.DAILY_ROUTE.value: DailyRouteHandler(self.master),
            Layout_type.MONTHLY_CARGO.value: MonthlyCargoHandler(self.master),
            Layout_type.FOREIGN_CARGO.value: ForeignCargoHandler(self.master),
            }
        logger.info("▽変換開始▽")
        self.master.load() 
        file_paths = glob.glob(f"{INPUT_DIR}/*.xlsx")
        for file_path in file_paths:
            fbasename = os.path.basename(file_path)
            logger.info(f"処理ファイル: {fbasename}")
            df = read_excel(file_path)
            layout =detect_layout(df)
            handler =handlers.get(layout)

            if handler is None:
                logger.error(f"未対応のレイアウトです: {layout}")
                continue

            result = handler.process(df) 
            if result.has_errors:
                result.export()
                continue
            
            file_out_path = OUTPUT_DIR / fbasename.replace(".xlsx", ".csv")
            export_csv(df, file_out_path,layout)   
        logger.info("△変換完了△")
  
if __name__ == "__main__":
     FlightConverter().run()

