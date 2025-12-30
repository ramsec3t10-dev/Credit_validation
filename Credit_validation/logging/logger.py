import os,sys
from datetime import datetime
import logging

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

LOG_DIR = os.path.join(os.getcwd(),"logs")
os.makedirs(LOG_DIR,exist_ok=True)
log_file_path = os.path.join(LOG_DIR,LOG_FILE)

logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s"

)
