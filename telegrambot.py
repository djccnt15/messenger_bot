from abc import ABCMeta, abstractmethod
import json
import csv

import requests


class ChatBot(metaclass=ABCMeta):
    def __init__(self, token: str) -> None:
        self.url = token

    @abstractmethod
    def send_msg(self, msg):
        ...


class BotTelegram(ChatBot):
    def __init__(self, token: str, mode: int = 0) -> None:
        super().__init__(token)
        self.url: str = f'https://api.telegram.org/bot{token}'
        self.mode: int = mode
        self.data: dict = {}

        # get chat id
        response = requests.get(url=f'{self.url}/getUpdates').json()['result']
        if response:
            self.name = requests.get(url=f'{self.url}/getMe').json()['result']['first_name']
            if self.mode == 0:
                self.chat_id_sol: str = response[0]['message']['chat']['id']
            else:
                self.chat_id_grp: str = response[0]['my_chat_member']['chat']['id']

    def send_msg(self, msg):
        """send message to DM if mode is 0, send message to group chat if mode is 1"""

        if self.mode == 0:
            self.data['chat_id'] = self.chat_id_sol
        elif self.mode == 1:
            self.data['chat_id'] = self.chat_id_grp
        self.data['text'] = msg
        requests.post(url=f'{self.url}/sendMessage', data=self.data)


def init_bots(key: str, token: str, mode: int) -> BotTelegram | None:
    try:
        return BotTelegram(token, mode)
    except KeyError as e:
        print(f'{key}: {e}')
    except IndexError as e:
        print(f'{key}: {e}')
    except Exception as e:
        print(f'{key}: {e}')


def find_ext(fn: str):
    return fn[fn.rfind('.') + 1:]


def create_bots(fn: str) -> list[BotTelegram]:
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
            init_bots(data, bot_data[data]['token'], int(bot_data[data]['mode']))
            for data in bot_data
        ] if bot is not None
    ]
    return bots


if __name__ == '__main__':
    from datetime import datetime

    print('your code')

    list_bot = ['bot_t.csv', 'bot_t.json']
    bots_t = [b for bot in [create_bots(bot) for bot in list_bot] for b in bot]
    for bot in bots_t:
        bot.send_msg(
            f'{datetime.now().replace(microsecond=0)} : test message from {bot.name}'
        )

    print('your code')