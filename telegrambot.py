from aiohttp import ClientSession

from basebot import BaseBot


class BotTelegram(BaseBot):
    def __init__(self, key: str, token: str, api: str, mode: int = 0) -> None:
        super().__init__(key, token, api)
        self.url = f"https://api.telegram.org/bot{token}"
        self.mode = mode
        self.data: dict = {}

    async def _post_init(self):
        async with ClientSession() as session:
            async with session.get(f"{self.url}/getUpdates") as response:
                res = await response.json()
            if res["ok"]:
                res = res["result"][0]
                async with session.get(f"{self.url}/getMe") as response:
                    res_getMe = await response.json()
                    self.name = res_getMe["result"]["first_name"]
                # get chat id
                if self.mode == 0:
                    self.chat_id_sol: int = res["message"]["chat"]["id"]
                else:
                    self.chat_id_grp: int = res["my_chat_member"]["chat"]["id"]
            else:
                raise Exception(f"not able to initializ")
        return self

    async def init_bot(self):
        try:
            return await self._post_init()
        except KeyError as e:
            print(f"{self.key}: {e}")
        except IndexError as e:
            print(f"{self.key}: {e}")
        except Exception as e:
            print(f"{self.key}: {e}")

    async def send_msg(self, msg):
        """send message to DM if mode is 0, send message to group chat if mode is 1"""

        if self.mode == 0:
            self.data["chat_id"] = self.chat_id_sol
        elif self.mode == 1:
            self.data["chat_id"] = self.chat_id_grp
        self.data["text"] = msg

        async with ClientSession() as session:
            async with session.post(
                url=f"{self.url}/sendMessage", data=self.data
            ) as response:
                await response.text()
