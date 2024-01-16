from pathlib import Path

from Crypto.PublicKey import RSA


def create_keys_rsa(
    private_key: Path | str = "private.pem",
    public_key: Path | str = "public.pem",
    length: int = 2048,
):
    key = RSA.generate(bits=length)

    private = key.export_key()
    with open(file=private_key, mode="wb") as f:
        f.write(private)

    public = key.publickey().export_key()
    with open(file=public_key, mode="wb") as f:
        f.write(public)
