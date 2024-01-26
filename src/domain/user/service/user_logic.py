from typing import Generator

import pandas as pd

from src.domain import user
from src.exception import InvalidMessengerError
from src.security.model import Encrypted


def validate_messenger(df: pd.DataFrame, col: str):
    invalid_messenger: set[str] = set()

    for row in df.itertuples():
        try:
            user.UserBase(user_name=row.user_name, messenger=getattr(row, col))
        except InvalidMessengerError:
            invalid_messenger.add(row.messenger)

    return sorted(list(invalid_messenger)) if invalid_messenger else None


def create_user_list(
    user_df: pd.DataFrame,
    token_list: Generator[Encrypted, None, None],
):
    user_encrypt_df = pd.DataFrame([t.model_dump() for t in token_list])

    user_df = pd.concat(
        objs=[user_df[["user_name", "messenger"]], user_encrypt_df],
        axis=1,
    )
    user_list = (user.UserCreate(**v) for v in user_df.to_dict(orient="records"))  # type: ignore
    return user_list
