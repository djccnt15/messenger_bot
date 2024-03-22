from src.db import user_crud
from src.exception import EmptyUserList

from ..service import bot_logic


async def send_msg(message: str):
    user_entity = await user_crud.user_list()
    if not user_entity:
        raise EmptyUserList
    bots = await bot_logic.create_bot(user_entity=user_entity)
    await bot_logic.send_msg(bots=bots, message=message)
