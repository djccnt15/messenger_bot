from pydantic import BaseModel, field_validator

from src.exception import InvalidMessengerError

from .enums import MsgIntercace


class UserBase(BaseModel):
    user_name: str
    messenger: str

    @field_validator("messenger")
    @classmethod
    def validate_messenger(cls, v: str):
        if v not in MsgIntercace.to_list():
            raise InvalidMessengerError
        return v


class UserCreate(UserBase):
    enc_session_key: bytes
    nonce: bytes
    tag: bytes
    ciphertext: bytes
