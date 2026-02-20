import datetime
from BANK import API


class Wallet:
    def __init__(self, owner_username):
        self.owner_username = owner_username
        self.balance = 0
        self.cards = []
        self.transactions = []

    def add_money(self, card, month, year, password, cvv2, amount):
        if amount <= 0:
            return False, "Amount must be positive"

        bank = API()
        try:
            pay_id = bank.pay(card, month, year, password, cvv2, amount)
        except Exception:
            pay_id = None

        if not pay_id:
            return False, "Card information is wrong"

        self.balance += amount
        last4 = str(card)[-4:]
        if last4 not in self.cards:
            self.cards.append(last4)

        trans = {
            "username": self.owner_username,
            "type": "deposit",
            "amount": amount,
            "balance": self.balance,
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.transactions.append(trans)
        return True, f"Added {amount} Tomans. Payment ID: {pay_id}"

    def pay(self, amount):
        if amount <= 0:
            return False, "Invalid amount"
        if amount > self.balance:
            return False, "Not enough money"

        self.balance -= amount
        trans = {
            "username": self.owner_username,
            "type": "purchase",
            "amount": amount,
            "balance": self.balance,
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.transactions.append(trans)
        return True, "Payment successful"
