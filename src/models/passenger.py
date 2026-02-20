from models.user import User
from models.wallet import Wallet


class Passenger(User):
    def __init__(self, username, salt, password_hash, full_name, email, phone=""):
        super().__init__(username, salt, password_hash, full_name, email, phone)
        self.wallet = Wallet(owner_username=username)
