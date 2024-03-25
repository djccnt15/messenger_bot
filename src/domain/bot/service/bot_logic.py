import asyncio
from typing import Iterable, Sequence

from src.db import user_entity

from ..converter import bot_converter
from ..model import telegrambot


async def create_bot(
    user_entity: Sequence[user_entity.UserInfoEntity],
) -> Iterable[telegrambot.TelegramBot]:
    user_list = (bot_converter.to_TelegramBot(user=user) for user in user_entity)
    bot_list = await asyncio.gather(*[bot.initialize() for bot in user_list])
    result = (bot for bot in bot_list if bot is not None)
    return result


async def send_msg(
    bots: Iterable[telegrambot.TelegramBot],
    message: str,
):
    for bot in bots:
        await bot.send_msg(message=message)
