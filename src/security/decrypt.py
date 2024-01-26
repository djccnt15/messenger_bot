from pathlib import Path

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA

from .model import Encrypted


def decrypt_rsa(
    encrypted: Encrypted,
    private_key: Path | str = "private.pem",
):
    with open(private_key) as k:
        private = RSA.import_key(extern_key=k.read())

    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(key=private)
    session_key = cipher_rsa.decrypt(ciphertext=encrypted.enc_session_key)

    # Decrypt the data with the AES session key
    cipher_aes = AES.new(
        key=session_key,
        mode=AES.MODE_EAX,
        nonce=encrypted.nonce,
    )

    return cipher_aes.decrypt_and_verify(
        ciphertext=encrypted.ciphertext,
        received_mac_tag=encrypted.tag,
    ).decode("utf-8")
