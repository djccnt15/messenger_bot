from pathlib import Path

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA


def decrypt_rsa(
    enc_session_key: bytes,
    nonce: bytes,
    tag: bytes,
    ciphertext: bytes,
    private_key: Path | str = "private.pem",
):
    with open(private_key) as k:
        private = RSA.import_key(k.read())

    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(private)
    session_key = cipher_rsa.decrypt(enc_session_key)

    # Decrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    return cipher_aes.decrypt_and_verify(ciphertext, tag).decode("utf-8")
