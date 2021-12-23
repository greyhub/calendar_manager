import logging
import os
rootpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../logs'))


def logging_basic_config(filename=None):
    format = '%(asctime)s - [%(levelname)s] %(name)s - %(message)s'
    formatter = logging.Formatter(format)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    if filename is not None:
        filepath = os.path.join(rootpath, filename)
        file_handler = logging.FileHandler(filepath)
        file_handler.setFormatter(formatter)
        logging.basicConfig(level=logging.INFO, format=format, handlers=[stream_handler, file_handler])
    else:
        logging.basicConfig(level=logging.INFO, format=format)
