from cryptography.fernet import Fernet
import json
from json.decoder import JSONDecodeError
from base64 import b64encode, b64decode
import binascii


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
