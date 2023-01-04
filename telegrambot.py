import json
import csv
from dataclasses import dataclass

import requests


@dataclass(order=True, unsafe_hash=True)
class BotTelegram:
    """simple telegram bot, must be initialized with token data"""

    token: str
    mode: int = 0

    def __post_init__(self) -> None:
        # get url of chat bot
        self.url: str = f'https://api.telegram.org/bot{self.token}/'
        self.mode: int = self.mode
        self.data: dict = {}

        # get chat id
        response = requests.post(url=f'{self.url}getUpdates').json()['result']
        if response:
            self.name = requests.post(url=f'{self.url}getMe').json()['result']['first_name']
            self.chat_id_sol: str = response[0]['message']['chat']['id']
            try:
                self.chat_id_grp: str = response[0]['my_chat_member']['chat']['id']
            except:
                self.chat_id_grp: str = response[1]['my_chat_member']['chat']['id']

    def send_msg(self, msg) -> None:  # send message to your telegram chat bot
        """
        method to send message through bot
        send message to DM if mode is 0, send message to group chat if mode is 1
        """

        if self.mode == 0:
            self.data['chat_id'] = self.chat_id_sol
        elif self.mode == 1:
            self.data['chat_id'] = self.chat_id_grp
        self.data['text'] = msg
        requests.post(url=f'{self.url}sendMessage', data=self.data)


def init_bots(key: str, token: str, mode: int = 0) -> BotTelegram | None:
    """Error handling for initializing BotTelegram"""

    try:
        return BotTelegram(token, mode)
    except KeyError as e:
        print(f'{key}: token error')
    except IndexError as e:
        print(f'{key}: request error, Bot server might be unactivated')
    except Exception as e:
        print(f'{key}: {e}')


def find_ext(fn: str) -> str:
    """find filename extension"""

    return fn[fn.rfind('.') + 1:]


def create_bots(fn: str) -> list[BotTelegram]:
    """create instances of BotTelegram"""

    if find_ext(fn) == 'json':
        with open(file=fn, mode='r') as f:
            bot_data: dict = json.load(fp=f)
    elif find_ext(fn) == 'csv':
        with open(file=fn, mode='r') as f:
            bot_data: dict = {row[0]: {"token": row[1], "mode": row[2]} for row in csv.reader(f)}
    else:
        raise ValueError

    bots = [
        bot for bot in [
            init_bots(data, bot_data[data]["token"], int(bot_data[data]["mode"]))
            for data in bot_data
        ] if bot is not None
    ]
    return bots


if __name__ == '__main__':
    from datetime import datetime

    print('your code')

    now = datetime.now().replace(microsecond=0)

    list_bot = ['bot_t.csv', 'bot_t.json']
    bots = [b for bot in [create_bots(fn=bot) for bot in list_bot] for b in bot]
    [bot.send_msg(msg=f'{now} : test message from {bot.name}') for bot in bots]

    print('your code')