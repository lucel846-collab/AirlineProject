import logging
from src.paths import LOG_FILE

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    filename=LOG_FILE,
    encoding="utf-8",
)

logger = logging.getLogger(__name__)