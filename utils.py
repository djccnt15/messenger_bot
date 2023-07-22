import json
import csv

from telegrambot import BotTelegram


def find_ext(fn: str):
    return fn[fn.rfind('.') + 1:]


async def create_bots(fn):
    if find_ext(fn) == 'json':
        with open(fn) as f:
            bot_data = json.load(f)
    elif find_ext(fn) == 'csv':
        with open(fn) as f:
            bot_data = {
                row[0]: {'token': row[1], 'api': row[2], 'mode': row[3]}
                for row in csv.reader(f)
            }
    else:
        raise ValueError

    bots = [
        bot for bot in [
            await BotTelegram(
                data,
                bot_data[data]['token'],
                bot_data[data]['api'],
                int(bot_data[data]['mode'])
            ).init_bot()
            for data in bot_data if bot_data[data]['api'] == 'telegram'
        ] if bot is not None
    ]
    return bots