import pandas as pd

from src.config import RESOURCES
from src.db import query
from src.exception import MessengerException
from src.security import decrypt, encrypt

from ..model import user_model
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


def read_first_user():
    data = query.read_first_user()
    if data is None:
        return None

    data = user_model.UserRead.model_validate(data)
    encrypted_data = encrypt.Encrypted(
        enc_session_key=data.enc_session_key,
        nonce=data.nonce,
        tag=data.tag,
        ciphertext=data.ciphertext,
    )

    user_token = decrypt.decrypt_rsa(
        encrypted=encrypted_data,
        private_key=RESOURCES / "private.pem",
    )

    user_data = user_model.UserModel(
        id=data.id,
        messenger=data.messenger,
        user_name=data.user_name,
        token=user_token,
    )
    return user_data
