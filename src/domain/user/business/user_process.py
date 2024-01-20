import pandas as pd

from src.config import RESOURCES
from src.db import query
from src.exception import MessengerException
from src.security import encrypt

from ..service import user_logic


def create_user(file: str, col: str):
    user_df = pd.read_csv(RESOURCES / file)

    invalid_messenger = user_logic.validate_messenger(df=user_df, col=col)
    if invalid_messenger:
        raise MessengerException(invalid_messenger)

    token_list = (
        encrypt.encrypt_rsa(i, RESOURCES / "public.pem") for i in user_df.token
    )

    user_list = user_logic.create_user_list(user_df=user_df, token_list=token_list)

    query.create_user(user_list=user_list)
