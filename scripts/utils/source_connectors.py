import os
from pathlib import Path
from typing import Any

import pandas as pd
import requests
from definitions import SCRIPTS_DIR
from requests.adapters import HTTPAdapter, Retry
from utils.db_utils import DbUtils
from utils.log_utils import Logger

logger = Logger().set_logger()


class SourceConnectors:
    @staticmethod
    def read_from_api(
        url,
        auth=None,
        headers=None,
        params=None,
        method="GET",
        response_format="json",
        data=None,
        timeout: int = 25,
    ):
        message = None
        try:
            session = requests.Session()
            retries = Retry(
                total=5, backoff_factor=5, status_forcelist=[429, 500, 502, 503, 504]
            )
            session.mount("http://", HTTPAdapter(max_retries=retries))
            session.mount("https://", HTTPAdapter(max_retries=retries))

            # logger.detailed("Trying to hit the endpoint")
            response = session.request(
                method,
                url,
                auth=auth,
                params=params,
                headers=headers,
                data=data,
                timeout=timeout,
            )
            if response.ok:
                if response_format == "json":
                    json_res = response.json()
                    return json_res, message
                elif response_format == "xml":
                    # Code to parse XML response
                    pass
                elif response_format == "text":
                    return response.text, message
                elif response_format == "binary":
                    return response.content, message
                else:
                    return None, "Unsupported response format"
            else:
                logger.error(response.content)
                return None, "Error: " + str(response.status_code) + " " + str(
                    response.content
                )
        except requests.exceptions.HTTPError as error_http:
            message = f"HTTP Error: {error_http}"
            logger.exception(message)
            return {}, message

        except requests.exceptions.ConnectionError as error_connection:
            message = f"Connection Error: {error_connection}"
            logger.exception(message)
            return {}, message

        except requests.exceptions.Timeout as error_timeout:
            message = f"Timeout Error: {error_timeout}"
            logger.exception(message)
            return {}, message

        except requests.exceptions.RequestException as error_request:
            message = f"Request Error: {error_request}"
            logger.exception(message)
            return {}, message

        except Exception as error:
            message = f"There was an error in API call: {error}"
            logger.exception(message)
            return {}, message

    @staticmethod
    def read_from_files(file_name, base_path: str) -> Any:
        """
        Reads file and returns it.

        Args:
            path (str): File path on the server.

        Returns:
            Any: Retrieved data from the file.
        """
        try:
            ROOT_DIR = Path(SCRIPTS_DIR).parent.absolute()
            FILES_DIR = Path(ROOT_DIR).parent.absolute()
            path = os.path.join(FILES_DIR, "SourceFiles", file_name)
            # with open(path, "r") as file:
            #     data = file.read()
            #     return data, None

            dataframe = pd.read_csv(path)
            return dataframe, None
        except Exception as error:
            message = f"There was an error in reading file: {error}"
            logger.exception(message)
            return {}, message

    def read_from_database(table_name: str) -> Any:
        """
        Reads file and returns it.

        Args:
            path (str): File path on the server.

        Returns:
            Any: Retrieved data from the file.
        """
        try:
            engine = DbUtils.create_sqlalchemy_engine()
            query = f"SELECT * FROM {table_name}"
            dataframe = pd.read_sql(query, con=engine)
            return dataframe, None
        except Exception as error:
            message = f"There was an error in reading sql: {error}"
            logger.exception(message)
            raise
