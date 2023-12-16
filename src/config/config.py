from configparser import ConfigParser
from pathlib import Path

RESOURCES = Path("resources")

parser = ConfigParser()
parser.read(RESOURCES / "config.ini")
