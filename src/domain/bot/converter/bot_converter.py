from src.config import RESOURCES
from src.db import user_entity
from src.security import decrypt, encrypt

from ...user import user_model
from ..model import telegrambot


def to_TelegramBot(user: user_entity.UserInfoEntity) -> telegrambot.TelegramBot:
    data = user_model.UserRead.model_validate(user)
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

    return telegrambot.TelegramBot(
        messenger=data.messenger,
        user_name=data.user_name,
        token=user_token,
    )
