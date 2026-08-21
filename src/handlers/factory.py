from src.detect_layout import Layout_type
from src.handlers.daily_flight import DailyFlightHandler
from src.handlers.daily_flight2 import DailyFlightHandler2
from src.handlers.daily_flight3 import DailyFlightHandler3
from src.handlers.daily_irregal import DailyIrregularHandler
from src.handlers.daily_route import DailyRouteHandler
from src.handlers.foreign_cargo import ForeignCargoHandler
from src.handlers.monthly_cargo import MonthlyCargoHandler
from src.handlers.monthly_flight import MonthlyRouteHandler
from src.master_data import MasterData


class HandlerFactory:
    @staticmethod
    def create_handler(layout_value: str, master: MasterData):
        """レイアウトタイプに応じたハンドラーのインスタンスを生成して返す"""
        
        # マッピング辞書（必要なときにだけインスタンス化されるように関数内で定義）
        handlers_map = {
            Layout_type.DAILY.value: DailyFlightHandler,
            Layout_type.DAILY2.value: DailyFlightHandler2,
            Layout_type.DAILY3.value: DailyFlightHandler3,
            Layout_type.MONTHLY_ROUTE.value: MonthlyRouteHandler,
            Layout_type.DAILY_ROUTE.value: DailyRouteHandler,
            Layout_type.MONTHLY_CARGO.value: MonthlyCargoHandler,
            Layout_type.FOREIGN_CARGO.value: ForeignCargoHandler,
            Layout_type.IRREGULAR.value: DailyIrregularHandler,
        }
        
        handler_class = handlers_map.get(layout_value)
        if handler_class is None:
            return None
            
        # ここでインスタンス化して返す
        return handler_class(master)
