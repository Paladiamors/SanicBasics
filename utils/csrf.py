import os
from base64 import b64decode, b64encode

from cryptography.fernet import Fernet, InvalidToken

from settingsManager import settingsManager


class CSRF:

    # These are the HTTP methods that we want to enforce CSRF upon
    HTTP_UNSAFE_METHODS = ("POST", "PUT", "PATCH", "DELETE")

    CSRF_REF_BYTES = 16

    def __init__(self, secret=None):
        """Initialises the CSRF class

        Parameters
        ----------
        secret : binary, optional
            binary string representing the secret, by default None
        """
        self.CSRF_SECRET = secret or settingsManager.get_setting("CSRF_SECRET").encode() or Fernet.generate_key()

    def generate_csrf_token(self) -> str:

        cipher = Fernet(self.CSRF_SECRET)

        # Some random bytes of a known length
        csrf_ref = os.urandom(self.CSRF_REF_BYTES)

        # Encrypt those bytes with our secret
        token = cipher.encrypt(csrf_ref)

        # Append the reference and base64 encode for transport, so that when we
        # decode the token later (again using our secret) we can verify that
        # (1) it is authentic, and (2) it has not been tampered with
        csrf_token = b64encode(csrf_ref + token)

        return csrf_token.decode("utf-8")

    def verify_csrf_token(self, csrf_token: str, ttl: int = None) -> bool:
        """Run the generate_csrf_token function in reverse"""
        global app

        cipher = Fernet(self.CSRF_SECRET)

        try:
            raw = b64decode(csrf_token)

            # Break the raw bytes based upon our known length
            csrf_ref = raw[:self.CSRF_REF_BYTES]
            token = raw[self.CSRF_REF_BYTES:]

            # decode the token
            decoded = cipher.decrypt(token, ttl)

            # Make sure the token matches our original reference
            return decoded == csrf_ref

        except InvalidToken:
            # logger.error(e)
            return False

    # def is_pass_csrf(self, request: Request) -> bool:
    #     if request.method in HTTP_UNSAFE_METHODS:
    #         return verify_csrf_token(request.headers.get("x-xsrf-token", ""))
    #     return True


if __name__ == "__main__":
    csrf = CSRF()
    print(csrf.CSRF_SECRET)
