import pandas as pd
from src.logger import logger
from src.paths import (
    AIRLINE_MASTER_FILE,
    AIRPORT_ALIAS_FILE,
    AIRPORT_MASTER_FILE,
    ROUTE_ALIAS_FILE,
    ROUTE_MASTER_FILE,
)


class MasterData:
    def __init__(self):
        self.airline_master = None
        self.airport_master = None
        self.route_master = None
        self.route_alias = None
        self.airport_alias = None

        self.route_alias_dict = {}
        self.route_code_dict = {}
        self.airport_alias_dict = {}

    # Validationで使用するDataFrame
    def load_data(self) -> None:
        self.airline_master = pd.read_csv(AIRLINE_MASTER_FILE)
        self.airport_master = pd.read_csv(AIRPORT_MASTER_FILE)
        self.route_master = pd.read_csv(ROUTE_MASTER_FILE)
        self.route_alias = pd.read_csv(ROUTE_ALIAS_FILE)
        self.airport_alias = pd.read_csv(AIRPORT_ALIAS_FILE)

    # 高速検索用の辞書
    def create_dicts(self) -> None:
        self.route_alias_dict =  {
            (
            row["AirlineCD"],
            row["AirportOffice"],
            row["RouteAlias"]
            ): row["RouteCD"]
            for _, row in self.route_alias.iterrows()
        }

        self.route_code_dict = {
        (
            row["RouteCD"] ): row["RouteName"]
            for _, row in self.route_master.iterrows()
        }

        self.airport_alias_dict= {
            row["AirportAlias"]: row["AirportCD"]
            for _, row in self.airport_alias.iterrows()
        }    

    def load(self) -> None:
        logger.info("マスタファイルを読込")
        self.load_data()
        logger.info("辞書作成開始")
        self.create_dicts()

