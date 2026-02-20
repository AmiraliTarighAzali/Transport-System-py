import os
import hashlib


class PasswordHasher:
    @staticmethod
    def make_salt() -> str:
        return os.urandom(16).hex()

    @staticmethod
    def hash_password(password: str, salt: str) -> str:
        data = (salt + password).encode("utf-8")
        return hashlib.sha256(data).hexdigest()

    @staticmethod
    def verify(password: str, salt: str, hashed: str) -> bool:
        return PasswordHasher.hash_password(password, salt) == hashed
