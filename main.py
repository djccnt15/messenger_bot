import asyncio

from utils import create_bots


async def create_bot(list_bot: list[str]):
    bot_list = await asyncio.gather(*[create_bots(bot) for bot in list_bot])
    return bot_list


async def send_msg(bot_list: list, msg: str):
    await asyncio.gather(*[bot.send_msg(msg % bot.name) for bot in bot_list])


if __name__ == '__main__':
    from datetime import datetime

    print('your code')

    list_bot = ['bot_t.csv', 'bot_t.json']
    bots_t = [b for bot in asyncio.run(create_bot(list_bot)) for b in bot]

    now = datetime.now().replace(microsecond=0)
    msg = f'{now} : test message from %s'
    asyncio.run(send_msg(bots_t, msg))

    print('your code')