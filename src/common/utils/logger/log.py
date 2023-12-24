import logging
from logging import StreamHandler
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from src.config import config

# set log directory
log_dir = Path("logs")
try:
    log_dir.mkdir()
except FileExistsError:
    ...

# set log format
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - [%(module)s:%(lineno)d] %(message)s"
)

# create TimedRotatingFileHandler
file_handler = TimedRotatingFileHandler(
    filename=log_dir / "log.log",
    when="midnight",  # rotate every midnight
    backupCount=3,  # define number of log files, set 0 to save infinity log files
    encoding="utf-8",
)
file_handler.setFormatter(formatter)

# create StreamHandler
stream_handler = StreamHandler()
stream_handler.setFormatter(formatter)

# create Logger instance
logger = logging.getLogger("logger")

# add log handler to logger
logger.addHandler(file_handler)
# logger.addHandler(stream_handler)

# set log level from config
log_level = config.parser["DEFAULT"]["log_level"]
log_level_list = [0, 10, 20, 30, 40, 50]

try:
    log_level = int(log_level)
except Exception as e:
    logger.exception(e)
    raise TypeError(e)

if log_level not in log_level_list:
    ERROR_MSG = "log_level must be one of %s" % log_level_list
    logger.critical(ERROR_MSG)
    raise AssertionError(ERROR_MSG)
logger.setLevel(log_level)
