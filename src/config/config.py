from configparser import ConfigParser

from src.config.common import RESOURCES

parser = ConfigParser()
parser.read(RESOURCES / "config.ini")
