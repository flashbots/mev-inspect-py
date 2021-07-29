import os
import configparser


THIS_FILE_DIRECTORY = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(THIS_FILE_DIRECTORY, "config.ini")


def load_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    return config
