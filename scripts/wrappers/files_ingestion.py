from utils.log_utils import Logger
from utils.source_connectors import SourceConnectors
from wrappers.base_connector import BaseConnector

logger = Logger().set_logger()


class FilesIngestion(BaseConnector):
    def read(self, config):
        record_count = 0
        base_path = config.get("base_path")
        table_name = config.get("table_name")
        file_extension = config.get("extension", "csv")

        file_name = table_name + "." + file_extension

        dataframe, error_message = SourceConnectors.read_from_files(
            file_name, base_path
        )
        if error_message:
            raise Exception(error_message)

        record_count += len(dataframe)

        logger.info(
            f"Finished data retrieval from: {file_name}. Retrieved {record_count} records."
        )
        return dataframe, record_count
