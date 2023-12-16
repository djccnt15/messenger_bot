from pathlib import Path

from Crypto.PublicKey import RSA


def create_keys_rsa(
    private_key: Path | str = "private.pem",
    public_key: Path | str = "public.pem",
    length: int = 2048,
):
    key = RSA.generate(length)

    private = key.export_key()
    with open(private_key, "wb") as f:
        f.write(private)

    public = key.publickey().export_key()
    with open(public_key, "wb") as f:
        f.write(public)
