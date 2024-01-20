from enum import StrEnum, auto


class MsgIntercace(StrEnum):
    TELEGRAM = auto()
    LINE = auto()
    KAKAO = auto()

    @classmethod
    def to_list(cls):
        return [v.value for v in cls]
