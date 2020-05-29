import os
import jwt


JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")
SECRET_KEY = os.environ.get("SECRET_KEY")


def encode_jwt(data):
    return jwt.encode(data, SECRET_KEY, algorithm=JWT_ALGORITHM).decode("utf-8")


def decode_jwt(access_token):
    return jwt.decode(
        access_token,
        SECRET_KEY,
        algorithms=[JWT_ALGORITHM],
        issuer="Redux Todo Web Backend",
        options={"verify_aud": False},
    )
