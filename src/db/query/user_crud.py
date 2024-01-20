from typing import Generator

from sqlalchemy.sql import insert

from src.db import entity, get_db
from src.domain import user


def create_user(user_list: Generator[user.UserCreate, None, None]):
    data = [u.model_dump() for u in user_list]
    q = insert(entity.UserInfoEntity).values(data)

    with get_db() as db:
        db.execute(q)
        db.commit()
