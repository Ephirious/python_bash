import logging


class Logger:
    logger: logging.Logger

    def __init__(self):
        self._init_logger()
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def _init_logger() -> None:
        LOG_FORMAT = "[%(asctime)s.%(msecs)03d][%(levelname)s]  %(message)s"
        LOG_LEVEL = logging.INFO
        LOG_FILENAME = "shell.log"
        LOG_FILEMODE = "w"

        logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL, filename=LOG_FILENAME, filemode=LOG_FILEMODE)


    def info(self, message: str) -> None:
        self.logger.info(message)

    def print(self, message: str) -> None:
        print(message)

    def error(self, message: str) -> None:
        self.logger.error(message)