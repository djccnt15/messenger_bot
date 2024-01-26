from enum import StrEnum


class LogEnum(StrEnum):
    START = "Program Starts"
    FINISH = "Program Finished"
    USER_INPUT = "user input: %s"
