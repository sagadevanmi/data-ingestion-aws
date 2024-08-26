from constants import API_BASE_URL, API_KEY
from utils.log_utils import Logger
from utils.source_connectors import SourceConnectors
from wrappers.base_connector import BaseConnector

logger = Logger().set_logger()


class ApiIngestion(BaseConnector):
    def read(self, config):
        record_count = 0
        base_url = config.get("base_url", API_BASE_URL)
        endpoint = config.get("endpoint")
        headers = {
            "x-api-Key": API_KEY,
        }

        json_res, error_message = SourceConnectors.read_from_api(
            base_url + endpoint, headers=headers
        )
        if error_message:
            raise Exception(error_message)

        record_count += len(json_res)

        logger.info(
            f"Finished data retrieval from: {endpoint}. Retrieved {record_count} records."
        )
        return json_res, record_count
