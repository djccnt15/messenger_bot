from abc import ABCMeta, abstractmethod


class BaseBot(metaclass=ABCMeta):
    def __init__(self, key: str, token: str, api: str) -> None:
        self.key = key
        self.url = token
        self.api = api

    @abstractmethod
    async def _post_init(): ...

    @abstractmethod
    async def init_bot(): ...

    @abstractmethod
    async def send_msg(): ...
