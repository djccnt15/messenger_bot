import abc

from pydantic import BaseModel


class BaseBotAbs(BaseModel, abc.ABC):
    user_name: str
    messenger: str
    token: str

    @abc.abstractmethod
    async def _post_init(): ...

    @abc.abstractmethod
    async def initialize(): ...

    @abc.abstractmethod
    async def send_msg(): ...
