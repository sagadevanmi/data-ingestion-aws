from typing import Dict, Type

from utils.file_utils import FileUtils
from utils.log_utils import Logger
from utils.s3_utils import S3Utils
from wrappers.api_ingestion import ApiIngestion
from wrappers.base_connector import BaseConnector
from wrappers.files_ingestion import FilesIngestion
from wrappers.sql_ingestion import SQLIngestion

logger = Logger().set_logger()

CONNECTOR_CLASSES: Dict[str, Dict] = {
    "1": {"connector": ApiIngestion, "config_file": "api_config.json"},
    "2": {"connector": FilesIngestion, "config_file": "files_config.json"},
    "3": {"connector": SQLIngestion, "config_file": "sql_config.json"},
}


def extract_connector_factory(
    source_id: str,
    source_name: str,
) -> Type[BaseConnector]:
    """
    Extracts data from various sources.

    Args:
        source_id (str): source_id (e.g., '1', '2', '3').
        source_name (str): source_name (e.g., 'API', 'Files', 'SQL').
    Returns:
        Any:
    """
    logger.info(f"Creating Connector class object for source: {source_name}")
    connector_class = CONNECTOR_CLASSES.get(source_id).get("connector")
    config_file = CONNECTOR_CLASSES.get(source_id).get("config_file")
    if not connector_class:
        raise ValueError(
            f"Unsupported source ID: {source_id}, source_name: {source_name}"
        )

    connector = connector_class()
    return connector, config_file


def main():
    source_id = "1"
    source_name = "api"

    connector, config_file = extract_connector_factory(source_id, source_name)
    config_dict = FileUtils.read_config_file(config_file)

    audit_dict = {
        "source_id": source_id,
        "source_name": source_name,
    }

    for table_name, table_details in config_dict["tables"].items():
        if not table_details.get("is_active", False):
            logger.info(f"{table_name} is set inactive, hence skipping")
            continue

        logger.info(f"Process started for {table_name}")
        audit_dict[table_name] = {
            "status": "inprogress",
        }
        table_details["table_name"] = table_name

        try:
            source_data, record_count = connector.read(table_details)
        except Exception as exc:
            audit_dict[table_name]["error_message"] = str(exc)
            audit_dict[table_name]["status"] = "failed"
            logger.exception(f"Read exception: {exc}")
            continue

        write_error = S3Utils.write_to_s3(
            table_name,
            source_data,
            config_dict["s3_config"],
            source_name,
            local_run=True,
        )

        if write_error:
            audit_dict[table_name]["status"] = "failure"
            audit_dict[table_name]["error_message"] = write_error

        audit_dict[table_name]["status"] = "success"
        audit_dict[table_name]["record_count"] = record_count
    print(audit_dict)


if __name__ == "__main__":
    main()
