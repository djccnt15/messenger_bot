from sqlalchemy.sql import insert, select

from src.db import database, user_entity


async def create_user(data: list[dict[str, bytes]]):
    q = insert(user_entity.UserInfoEntity).values(data)

    async with database.get_db() as db:
        await db.execute(q)
        await db.commit()


async def read_first_user():
    q = select(user_entity.UserInfoEntity)

    async with database.get_db() as db:
        res = await db.execute(q)
    return res.scalar()


async def user_list():
    q = select(user_entity.UserInfoEntity)

    async with database.get_db() as db:
        res = await db.execute(q)
    return res.scalars().all()
