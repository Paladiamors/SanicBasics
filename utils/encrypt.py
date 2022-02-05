import jwt
from sanic.request import Request
from cryptography.fernet import Fernet
import json
from json.decoder import JSONDecodeError
from base64 import b64encode, b64decode
import binascii
from settingsManager import get_settings

jwt_secret = get_settings().get_setting("sanic/config/SANIC_JWT_SECRET")


class Encrypt:
    """Used to encrypt and decrypt strings"""

    key = Fernet.generate_key()

    def __init__(self):
        self.fernet = Fernet(self.key)

    def encrypt(self, data):
        return b64encode(self.fernet.encrypt(data.encode())).decode()

    def decrypt(self, data):
        """Returns none if bad decryption"""
        try:
            return self.fernet.decrypt(b64decode(data.encode())).decode("utf8")
        except binascii.Error:
            return None


class EncryptJson(Encrypt):
    """Used to encrypt and decrypt json"""

    def encrypt(self, data):
        return super().encrypt(json.dumps(data))

    def decrypt(self, data):
        try:
            return json.loads(super().decrypt(data))
        except (TypeError, JSONDecodeError):
            return None


def decode_token(request: Request):
    token = f'{request.cookies["access_token"]}.{request.cookies["access_token_signature"]}'
    return jwt.decode(token, jwt_secret, algorithms=["HS256"])
