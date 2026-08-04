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
        logger.info("マスタファイルを読込完了")
        logger.info("辞書作成開始")
        self.create_dicts()
        logger.info("辞書作成完了")

    def get_route_code(self, airline_cd: str, airport_office: str, route_alias: str) -> str:
        return self.route_alias_dict.get(
            (airline_cd, 
            airport_office,
            route_alias), 
            None)

    def get_route_name(self, route_cd: str) -> str:
        return self.route_code_dict.get(
            route_cd, 
            None)

    def get_airport_cd(self, airport_alias: str) -> str:
        return self.airport_alias_dict.get(
            airport_alias, 
            None) 
    def get_airline_name(self, airline_cd: str) -> str:
        airline_row = self.airline_master[self.airline_master["AirlineCD"] == airline_cd]
        if not airline_row.empty:
            return airline_row.iloc[0]["AirlineName"]
        return None
    
    def exists_airline_code(self, airline_cd: str) -> bool:
        return airline_cd in self.airline_master["AirlineCD"].values

    def exists_airport_alias(self, airport_alias: str) -> bool:
        return airport_alias in self.airport_alias_dict

    def exists_route_alias(self, airline_cd: str, airport_office: str, route_alias: str) -> bool:
        return (airline_cd, airport_office, route_alias) in self.route_alias_dict
      
