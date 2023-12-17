from sqlalchemy.schema import Column
from sqlalchemy.types import String

from .base_entity import BaseEntity


class UserInfoEntity(BaseEntity):
    __tablename__ = "user_list"

    user_name = Column(type_=String(50), name="user_name", nullable=False)
    enc_session_key = Column(type_=String(1000), name="enc_session_key", nullable=False)
    nonce = Column(type_=String(100), name="nonce", nullable=False)
    tag = Column(type_=String(100), name="tag", nullable=False)
    ciphertext = Column(type_=String(100), name="ciphertext", nullable=False)
