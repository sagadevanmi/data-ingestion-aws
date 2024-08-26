import json

import boto3
from botocore.exceptions import ClientError
from utils.log_utils import Logger

logger = Logger()


class SecretManagerUtils:
    """Class for handling secrets manager operations"""

    @staticmethod
    def load_secret(secret_name: str, region_name: str = "ca-central-1") -> dict:
        """Function which fetches secret value from AWS secrets manager

        Args:
            secret_name (str): name of the secret which need to be fetched
            region_name (str, Optional): region where the service is running. Defaults to us-east-2
        Raises:
            exc: boto3 exception

        Returns:
            dict: secrets_dict
        """
        session = boto3.session.Session()
        client = session.client(service_name="secretsmanager", region_name=region_name)
        secret_manager_details = None
        try:
            logger.log("info", f"Secretname: {secret_name}, regionname: {region_name}")
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)
            # logger.log("info", str(get_secret_value_response))
            if get_secret_value_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                secret_string = get_secret_value_response["SecretString"]
                secret_manager_details = json.loads(secret_string)
            else:
                logger.log(
                    "info", f"Did not receive HTTPStatusCode 200 while reading secret"
                )
                logger.log("exception", f"{get_secret_value_response}")

        except ClientError as exc:
            message = None
            if exc.response["Error"]["Code"] == "ResourceNotFoundException":
                message = f"The requested secret {secret_name} was not found"
            elif exc.response["Error"]["Code"] == "InvalidRequestException":
                message = f"The SM request was invalid due to: {exc}"
            elif exc.response["Error"]["Code"] == "InvalidParameterException":
                message = f"The SM request had invalid params: {exc}"
            elif exc.response["Error"]["Code"] == "DecryptionFailure":
                message = f"The requested secret can't be decrypted using the provided KMS key: {exc}"
            elif exc.response["Error"]["Code"] == "InternalServiceError":
                message = f"An error occurred on SM service side: {exc}"

            logger.log("exception", message)
            raise Exception(message)
        return secret_manager_details
