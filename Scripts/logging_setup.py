import logging


def setup_logger(logger_name, file_name):
    # create a named logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    # create file handler and set level to info
    logger_file = logging.FileHandler(filename=file_name)
    logger_file.setLevel(logging.INFO)

    # Check if the logger already has handlers to prevent duplicate logging
    if not logger.hasHandlers():
        # create formatter
        formatter = logging.Formatter('%(asctime)s | %(levelname)s: %(filename)s %(funcName)s %(name)s - %(message)s')
        formatter_console = logging.Formatter('%(asctime)s | %(message)s')

        # create console handler and set level to info
        logger_console = logging.StreamHandler()
        logger_console.setLevel(logging.INFO)

        # add formatter, console handler, and file handler
        logger_console.setFormatter(formatter_console)
        logger_file.setFormatter(formatter)
        logger.addHandler(logger_console)
        logger.addHandler(logger_file)

    return logger

def basic_logger():
    return logging.basicConfig(
        level=logging.NOTSET, format="%(asctime)s | %(levelname)s: %(filename)s %(funcName)s %(lineno)s - %(message)s"
        , filename='entapment.log')
