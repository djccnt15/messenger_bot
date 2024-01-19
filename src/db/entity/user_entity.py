from sqlalchemy.schema import Column
from sqlalchemy.types import LargeBinary, String

from .base_entity import BaseEntity


class UserInfoEntity(BaseEntity):
    __tablename__ = "user_list"

    user_name = Column(
        type_=String(50),
        name="user_name",
        nullable=False,
    )
    messenger = Column(
        type_=String(20),
        name="messenger",
        nullable=False,
    )
    enc_session_key = Column(
        type_=LargeBinary(512),
        name="enc_session_key",
        nullable=False,
    )
    nonce = Column(
        type_=LargeBinary(32),
        name="nonce",
        nullable=False,
    )
    tag = Column(
        type_=LargeBinary(32),
        name="tag",
        nullable=False,
    )
    ciphertext = Column(
        type_=LargeBinary(512),
        name="ciphertext",
        nullable=False,
    )
