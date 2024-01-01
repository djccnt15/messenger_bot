import logging
from logging import StreamHandler
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from src.config import configs

config = configs.config.log

# set log directory
log_dir = Path("logs")
try:
    log_dir.mkdir()
except FileExistsError:
    ...

# create Logger instance
logger = logging.getLogger("logger")

# set log level from config
log_level = config.level
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

# set log format
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - [%(module)s:%(lineno)d] %(message)s"
)

# TimedRotatingFileHandler
if config.handlers.file:
    file_handler = TimedRotatingFileHandler(
        filename=log_dir / "log.log",
        when="midnight",  # rotate every midnight
        backupCount=3,  # define number of log files, set 0 to save infinity log files
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

# StreamHandler
if config.handlers.stream:
    stream_handler = StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
