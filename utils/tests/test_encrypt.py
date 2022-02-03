import unittest
from utils.encrypt import Encrypt, EncryptJson


class TestEncrypt(unittest.TestCase):

    def test_encrypt_str(self):
        x = "this is a test"
        e = Encrypt()
        encrypted = e.encrypt(x)
        self.assertEquals(x, e.decrypt(encrypted))

    def test_bad_decrypt_str(self):
        e = Encrypt()
        self.assertIsNone(e.decrypt("badstringasdfsadf"))

    def test_encrypt_json(self):
        x = {"x": "this is a test"}
        e = EncryptJson()
        encrypted = e.encrypt(x)
        self.assertEquals(x, e.decrypt(encrypted))

    def test_bad_decrypt_json(self):
        e = EncryptJson()
        self.assertIsNone(e.decrypt("badstringasdfsadf"))


if __name__ == "__main__":
    unittest.main()
