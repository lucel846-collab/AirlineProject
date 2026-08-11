import pandas as pd
from src.logger import logger
from src.paths import (
    AIRLINE_MASTER_FILE,
    AIRPORT_ALIAS_FILE,
    AIRPORT_MASTER_FILE,
    AIRPORT_OFFICE_FILE,
    ROUTE_ALIAS_FILE,
    ROUTE_MASTER_FILE,
)


class MasterData:
    def __init__(self):
        self.airline_master: pd.DataFrame | None = None
        self.airport_alias: pd.DataFrame | None = None
        self.airport_master: pd.DataFrame | None = None
        self.airport_Office: pd.DataFrame | None = None
        self.route_alias: pd.DataFrame | None = None
        self.route_master: pd.DataFrame | None = None
     
        self.airport_alias_dict: dict[str, str] = {}
        self.airline_name_dict: dict[str, str] = {}
        self.airport_Office_dict: dict[str, str] = {}
        self.route_alias_dict: dict[tuple[str, str, str], str] = {}
        self.route_code_dict: dict[str, str] = {}

    # Validationで使用するDataFrame
    def load_data(self) -> None:
        self.airline_master: pd.DataFrame = pd.read_csv(AIRLINE_MASTER_FILE)
        self.airport_alias: pd.DataFrame = pd.read_csv(AIRPORT_ALIAS_FILE)
        self.airport_master: pd.DataFrame = pd.read_csv(AIRPORT_MASTER_FILE)
        self.airport_Office: pd.DataFrame= pd.read_csv(AIRPORT_OFFICE_FILE)
        self.route_alias: pd.DataFrame = pd.read_csv(ROUTE_ALIAS_FILE)
        self.route_master: pd.DataFrame = pd.read_csv(ROUTE_MASTER_FILE)
    # 高速検索用の辞書
    def create_dicts(self) -> None:
        self.airline_name_dict: dict[str, str] = {
            row["AirlineCD"]: row["AirlineName"]
            for _, row in self.airline_master.iterrows()
        }

        self.route_alias_dict: dict[tuple[str, str, str], str] =  {
            (
            row["AirlineCD"],
            row["AirportOffice"],
            row["RouteAlias"]
            ): row["RouteCD"]
            for _, row in self.route_alias.iterrows()
        }

        self.route_name_dict: dict[tuple[str, str], str] = {
            (
            row["RouteCD"],
            row["AirportOffice"]
            ): row["RouteName"]
            for _, row in self.route_master.iterrows()
        }

        self.airport_alias_dict: dict[str, str] = {
            row["AirportAlias"]: row["AirportCD"]
            for _, row in self.airport_alias.iterrows()
        }    
        self.airport_office_dict: dict[str, str] = {
            row["AirportOffice"]: row["AirportOfficeName"]
            for _, row in self.airport_Office.iterrows()
        }    

    # mainで使用する関数
    def load(self) -> None:
        logger.info("マスタファイルを読込")
        self.load_data()
        logger.info("マスタファイルを読込完了")
        logger.info("辞書作成開始")
        self.create_dicts()
        logger.info("辞書作成完了")

    def get_route_code(self, airline_cd: str, airport_office: str, route_alias: str) -> str | None:
        return self.route_alias_dict.get(
            (airline_cd, 
            airport_office,
            route_alias), 
            None)

    # Validationで使用する関数
    def get_route_name(self, route_cd: str,AirportOffice:str) -> str  | None:
        return self.route_name_dict.get(
            (route_cd, AirportOffice),
            None)

    def get_airport_cd(self, airport_alias: str) -> str | None:
        return self.airport_alias_dict.get(
            airport_alias, 
            None) 
    
    def get_airline_name(self, airline_cd: str) -> str | None:        
        return self.airline_name_dict.get(airline_cd, None)

    def get_airport_office_name(self, airport_office_cd: str) -> str | None:
        return self.airport_office_dict.get(airport_office_cd, None)

    def exists_airline_code(self, airline_cd: str) -> bool:
        return airline_cd in self.airline_name_dict

    def exists_airport_alias(self, airport_alias: str) -> bool:
        return airport_alias in self.airport_alias_dict

    def exists_route_alias(self, airline_cd: str, airport_office: str, route_alias: str) -> bool:
        return (airline_cd, airport_office, route_alias) in self.route_alias_dict

    def exists_airline_name(self, airline_name: str) -> bool:
        return airline_name in self.airline_name_dict
    
    def exists_airport_office(self, airport_office_cd: str) -> bool:
        return airport_office_cd in self.airport_office_dict
