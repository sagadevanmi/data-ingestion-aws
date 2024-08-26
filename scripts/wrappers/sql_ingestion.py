from utils.log_utils import Logger
from utils.source_connectors import SourceConnectors
from wrappers.base_connector import BaseConnector

logger = Logger().set_logger()


class SQLIngestion(BaseConnector):
    def read(self, config):
        record_count = 0
        table_name = config.get("table_name")

        dataframe, error_message = SourceConnectors.read_from_database(table_name)
        if error_message:
            raise Exception(error_message)

        record_count += len(dataframe)

        logger.info(
            f"Finished data retrieval from: {table_name}. Retrieved {record_count} records."
        )
        return dataframe, record_count
