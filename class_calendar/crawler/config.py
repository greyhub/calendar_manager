import logging
from logging.handlers import RotatingFileHandler


class MongoDBConfig:
    USERNAME = 'just_for_dev'
    PASSWORD = 'password_for_dev'
    HOST = '127.0.0.1'
    PORT = 27027
    DATABASE = 'is_schedule'
    CLASS_SCHEDULE_COL = 'class_schedule'


FORMATTER = logging.Formatter(fmt='[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s',
                              datefmt='%m-%d-%Y %H:%M:%S %Z')
LOG_FILE = 'logging.log'


def get_console_handler():
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_console_handler())
    # logger.addHandler(get_file_handler())
    return logger
