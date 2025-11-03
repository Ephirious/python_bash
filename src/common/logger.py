import logging


class Logger:
    logger: logging.Logger

    def __init__(self):
        """
        Initialize the logger wrapper and configure logging.
        :return: None
        :rtype: None
        """
        self._init_logger()
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def _init_logger() -> None:
        """
        Configure the application logger.
        :return: None
        :rtype: None
        """
        LOG_FORMAT = "[%(asctime)s.%(msecs)03d][%(levelname)s]  %(message)s"
        LOG_LEVEL = logging.INFO
        LOG_FILENAME = "shell.log"
        LOG_FILEMODE = "w"

        logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL, filename=LOG_FILENAME, filemode=LOG_FILEMODE)


    def info(self, message: str) -> None:
        """
        Log an informational message.
        :param message: Message to log.
        :type message: str
        :return: None
        :rtype: None
        """
        self.logger.info(message)

    def print(self, message: str) -> None:
        """
        Print a message to standard output.
        :param message: Message to print.
        :type message: str
        :return: None
        :rtype: None
        """
        print(message)

    def error(self, message: str) -> None:
        """
        Log an error message.
        :param message: Message to log.
        :type message: str
        :return: None
        :rtype: None
        """
        self.logger.error(message)