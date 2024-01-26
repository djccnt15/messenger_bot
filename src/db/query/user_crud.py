from sqlalchemy.sql import insert, select

from src.db import database, user_entity


def create_user(data: list[dict[str, bytes]]):
    q = insert(user_entity.UserInfoEntity).values(data)

    with database.get_db() as db:
        db.execute(q)
        db.commit()


def read_first_user():
    q = select(user_entity.UserInfoEntity)

    with database.get_db() as db:
        res = db.execute(q).scalar()
    return res


def user_list():
    q = select(user_entity.UserInfoEntity)

    with database.get_db() as db:
        res = db.execute(q).scalars()
        return res.all()
