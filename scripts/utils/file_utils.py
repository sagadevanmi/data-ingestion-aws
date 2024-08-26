import json
import os
from pathlib import Path

from definitions import SCRIPTS_DIR
from utils.log_utils import Logger

logger = Logger().set_logger()


class FileUtils:
    @staticmethod
    def read_config_file(file_name: str) -> dict:
        ROOT_DIR = Path(SCRIPTS_DIR).parent.absolute()
        path = os.path.join(ROOT_DIR, "config", "source", file_name)
        with open(path, "r") as file:
            config_data = json.loads(file.read())
            return config_data

    @staticmethod
    def move_files_to_archival(src_path: str, dest_path: str):
        os.rename(src_path, dest_path)
