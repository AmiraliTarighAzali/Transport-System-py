import re


class Validators:
    EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
    PHONE_RE = re.compile(r"^09\d{9}$")  # 11 digits, starts with 09
    USERNAME_RE = re.compile(r"^[A-Za-z0-9_]{3,30}$")
    PASSWORD_RE = re.compile(
        r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@&])[A-Za-z\d@&]{8,}$")

    @staticmethod
    def valid_email(email: str) -> bool:
        return bool(Validators.EMAIL_RE.match(email))

    @staticmethod
    def valid_phone(phone: str) -> bool:
        return bool(Validators.PHONE_RE.match(phone))

    @staticmethod
    def valid_username(username: str) -> bool:
        return bool(Validators.USERNAME_RE.match(username))

    @staticmethod
    def valid_password(password: str) -> bool:
        return bool(Validators.PASSWORD_RE.match(password))
