from pathlib import Path

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

from .model import Encrypted


def encrypt_rsa(
    data: str,
    public_key: Path | str = "public.pem",
) -> Encrypted:
    session_key = get_random_bytes(16)

    # Encrypt the session key with the public RSA key
    with open(public_key) as key:
        rsa_key = RSA.import_key(extern_key=key.read())
    cipher_rsa = PKCS1_OAEP.new(key=rsa_key)
    enc_session_key = cipher_rsa.encrypt(message=session_key)

    # Encrypt the data with the AES session key
    cipher_aes = AES.new(
        key=session_key,
        mode=AES.MODE_EAX,
    )
    ciphertext, tag = cipher_aes.encrypt_and_digest(plaintext=data.encode("utf-8"))

    return Encrypted(
        enc_session_key=enc_session_key,
        nonce=cipher_aes.nonce,
        tag=tag,
        ciphertext=ciphertext,
    )
