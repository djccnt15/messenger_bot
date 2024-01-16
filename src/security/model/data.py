from pydantic import BaseModel


class Encrypted(BaseModel):
    enc_session_key: bytes
    nonce: bytes
    tag: bytes
    ciphertext: bytes
