import aiohttp

from src.common.utils import logger
from src.exception import bot_exception

from .basebot import BaseBotAbs


class TelegramBot(BaseBotAbs):
    chat_id: int | None = None

    @property
    def url(self):
        return f"https://api.telegram.org/bot{self.token}"

    async def _post_init(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.url}/getUpdates") as response:
                response = await response.json()
            if response["ok"]:
                self.chat_id = response["result"][0]["message"]["chat"]["id"]
            else:
                raise bot_exception.BotInitException
            return self

    async def initialize(self):
        try:
            return await self._post_init()
        except bot_exception.BotInitException as e:
            logger.error(f"{self.user_name}: {e}")
        except Exception as e:
            logger.exception(e)

    async def send_msg(self, message):
        data = {"chat_id": self.chat_id, "text": message}
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=f"{self.url}/sendMessage", data=data
            ) as response:
                await response.text()
