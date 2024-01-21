from pydantic import BaseModel, ConfigDict, field_validator

from src.common.model import common
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


class UserRead(common.Id[int], UserCreate):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


class UserModel(common.Id[int], UserBase):
    token: str
