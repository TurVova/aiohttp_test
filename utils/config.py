import pathlib
from os import path
from configparser import ConfigParser


CONFIG_FILE = 'config.ini'
BASE_DIR = pathlib.Path(__file__).parent.parent


def load_config(file_path=BASE_DIR):
    config = ConfigParser()
    config.read(path.join(file_path, CONFIG_FILE))

    return config