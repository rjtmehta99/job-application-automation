import configparser
import logging.config

def config_logging():
    config = configparser.ConfigParser()
    config.read('logging_config.ini')
    logging.config.dictConfig(config)