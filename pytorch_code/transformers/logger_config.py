import logging
import os
from datetime import datetime


# create a logs directory if it does not exists
LOGS_DIR = "./logs"
os.makedirs(LOGS_DIR, exist_ok=True)

# create unique log file for each run.
log_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log"
log_filepath = os.path.join(LOGS_DIR, log_filename)

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(filename)s:%(funcName)s:%(lineno)d | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(log_filepath, encoding="utf-8"),
        logging.StreamHandler()  # Optional: also print logs to console
    ]
)

# export the logger
logger = logging.getLogger(__name__)
