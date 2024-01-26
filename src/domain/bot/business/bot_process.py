import asyncio

from src.db import user_crud
from src.exception import EmptyUserList

from ..service import bot_logic


def send_msg(message: str):
    user_entity = user_crud.user_list()
    if not user_entity:
        raise EmptyUserList
    bots = asyncio.run(bot_logic.create_bot(user_entity=user_entity))
    asyncio.run(bot_logic.send_msg(bots=bots, message=message))
