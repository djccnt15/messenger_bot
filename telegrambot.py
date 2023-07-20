from abc import ABCMeta, abstractmethod
import asyncio
import json
import csv
from datetime import datetime

from aiohttp import ClientSession


class ChatBot(metaclass=ABCMeta):
    def __init__(self, token: str) -> None:
        self.url = token

    @abstractmethod
    async def send_msg(self, msg): ...


class BotTelegram(ChatBot):
    def __init__(self, token: str, mode: int = 0) -> None:
        super().__init__(token)
        self.url = f'https://api.telegram.org/bot{token}'
        self.mode = mode
        self.data: dict = {}

    async def init_bot(self):
        async with ClientSession() as session:
            async with session.get(f'{self.url}/getUpdates') as response:
                res = await response.json()
                res = res['result'][0]
            if res:
                async with session.get(f'{self.url}/getMe') as response:
                    res_getMe = await response.json()
                    self.name = res_getMe['result']['first_name']
                # get chat id
                if self.mode == 0:
                    self.chat_id_sol: int = res['message']['chat']['id']
                else:
                    self.chat_id_grp: int = res['my_chat_member']['chat']['id']
        return self

    async def send_msg(self, msg):
        """send message to DM if mode is 0, send message to group chat if mode is 1"""

        if self.mode == 0:
            self.data['chat_id'] = self.chat_id_sol
        elif self.mode == 1:
            self.data['chat_id'] = self.chat_id_grp
        self.data['text'] = msg

        async with ClientSession() as session:
            async with session.post(url=f'{self.url}/sendMessage', data=self.data) as response:
                await response.text()


async def init_bots(key: str, token: str, mode: int) -> BotTelegram | None:
    try:
        return await BotTelegram(token, mode).init_bot()
    except KeyError as e:
        print(f'{key}: {e}')
    except IndexError as e:
        print(f'{key}: {e}')
    except Exception as e:
        print(f'{key}: {e}')


def find_ext(fn: str):
    return fn[fn.rfind('.') + 1:]


async def create_bots(fn: str) -> list[BotTelegram]:
    if find_ext(fn) == 'json':
        with open(fn) as f:
            bot_data = json.load(f)
    elif find_ext(fn) == 'csv':
        with open(fn) as f:
            bot_data = {row[0]: {'token': row[1], 'mode': row[2]} for row in csv.reader(f)}
    else:
        raise ValueError

    bots = [
        bot for bot in [
            await init_bots(data, bot_data[data]['token'], int(bot_data[data]['mode']))
            for data in bot_data
        ] if bot is not None
    ]
    return bots


async def corou_send_msg(dt: datetime, bot_list: list):
    await asyncio.gather(
        *[bot.send_msg(f'{dt} : test message from {bot.name}') for bot in bot_list]
    )


async def corou_create_bot(list_bot: list):
    bot_list = await asyncio.gather(*[create_bots(bot) for bot in list_bot])
    return bot_list


if __name__ == '__main__':
    print('your code')

    list_bot = ['bot_t.csv', 'bot_t.json']
    bots_t = [b for bot in asyncio.run(corou_create_bot(list_bot)) for b in bot]

    now = datetime.now().replace(microsecond=0)
    asyncio.run(corou_send_msg(now, bots_t))

    print('your code')