from pathlib import Path

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes


def encrypt_rsa(
    data: str,
    public_key: Path | str = "public.pem",
):
    session_key = get_random_bytes(16)

    # Encrypt the session key with the public RSA key
    with open(public_key) as key:
        cipher_rsa = PKCS1_OAEP.new(RSA.import_key(key.read()))
    enc_session_key = cipher_rsa.encrypt(session_key)

    # Encrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data.encode("utf-8"))

    return enc_session_key, cipher_aes.nonce, tag, ciphertext
