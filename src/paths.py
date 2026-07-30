from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_DIR = BASE_DIR / "Input"
OUTPUT_DIR = BASE_DIR / "Output"
MASTER_DIR = BASE_DIR / "Master"

INPUT_FILE = INPUT_DIR / "flightData.xlsx"
OUTPUT_FILE = OUTPUT_DIR / "flightData.csv"
ERROR_FILE = OUTPUT_DIR / "ValidationError.csv"

AIRPORT_MASTER_FILE = MASTER_DIR / "airportCodeMst.csv"
AIRLINE_MASTER_FILE = MASTER_DIR / "airlineCodeMst.csv"
ROUTE_MASTER_FILE = MASTER_DIR / "routeCodeMst.csv"