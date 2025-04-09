# Imports
import os
import logging


# Set directory and file name for the log file
logger_directory = 'app/store/data'
logger_filename = "irah.log"

# If directory does not exist, create one
if not os.path.exists(logger_directory):
    os.makedirs(logger_directory, exist_ok=True)

# Set handler details
handler = logging.FileHandler(f"{logger_directory}/{logger_filename}")
formatter = logging.basicConfig(format='%(asctime)s - %(module)s - %(lineno)d - %(levelname)s - %(message)s', handlers=[handler])
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)