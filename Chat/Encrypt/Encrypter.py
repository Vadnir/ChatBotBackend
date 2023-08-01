import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class Encrypter:
    def __init__(self, user_token: str):
        self.token = user_token.encode("utf-8")
        self.salt = os.urandom(16)
        self.kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=480000,
        )
        self.key = base64.urlsafe_b64encode(self.kdf.derive(self.token))

    def encrypt(self, content: str) -> str:
        f = Fernet(self.key)
        return f.encrypt(content.encode("utf-8")).decode("utf-8")

    def decrypt(self, content: str) -> str:
        f = Fernet(self.key)
        return f.decrypt(content.encode("uft-8")).decode("utf-8")



