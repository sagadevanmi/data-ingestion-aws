import logging


class Logger:
    """
    A class to manage logging functionality.

    Attributes:
        logger (logging.Logger): The logger object.
        detailed_logging (bool): Whether to enable detailed logging.
    """

    def __init__(self, name: str = "glue", detailed_logging: bool = False) -> None:
        """
        Initializes the logger object.

        Args:
            name (str, optional): The name of the logger. Defaults to "glue".
            detailed_logging (bool, optional): Whether to enable detailed logging. Defaults to False.
        """
        self.logger = logging.getLogger(name)

        # Set the logging level
        self.logger.setLevel(logging.INFO)

        # Configure the logging format
        formatter = logging.Formatter(
            "%(asctime)s.%(msecs)03d;%(levelname)s;%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Create a console handler and set the formatter
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # Add the console handler to the logger
        if not self.logger.hasHandlers():
            self.logger.addHandler(console_handler)

        # Set the detailed logging flag
        self.detailed_logging = detailed_logging

    def set_logger(self):
        return self.logger

    def detailed(self, message: str) -> None:
        """
        Logs a message only if self.detailed_logging is set to True.

        Args:
            message (str): The message to log.
        """

        if self.detailed_logging:
            self.logger.log(logging.INFO, message)
