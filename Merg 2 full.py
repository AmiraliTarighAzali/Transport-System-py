import os
import re
import threading
import datetime
from BANK import API   



# =====================================================
#  VALIDATOR
# =====================================================

class ValidationError(Exception):
    pass


class Validator:

    @staticmethod
    def validate_phone(phone):
        if not isinstance(phone, str):
            return False
        phone = phone.strip()
        return bool(re.fullmatch(r"^09\d{9}$", phone))

    @staticmethod
    def validate_password(password):
        if not isinstance(password, str):
            return False
        password = password.strip()
        return bool(re.fullmatch(r"^(?=.*[A-Z])(?=.*\d).{6,}$", password))


# =====================================================
#  TRANSACTION
# =====================================================

class TransactionError(Exception):
    pass


class Transaction:

    ALLOWED_TYPES = {"charge", "payment"}

    def __init__(self, username, amount, transaction_type):
        if not isinstance(username, str) or not username.strip():
            raise TransactionError("Invalid username.")

        if not isinstance(amount, (int, float)) or amount <= 0:
            raise TransactionError("Invalid amount.")

        if transaction_type not in self.ALLOWED_TYPES:
            raise TransactionError("Invalid transaction type.")

        self.username = username.strip()
        self.amount = float(amount)
        self.transaction_type = transaction_type
        self.timestamp = datetime.datetime.now()

    def serialize(self):
        return (
            f"Type: {self.transaction_type} | "
            f"Amount: {self.amount:.2f} | "
            f"Date: {self.timestamp.strftime('%Y-%m-%d')} | "
            f"Time: {self.timestamp.strftime('%H:%M:%S')}\n"
        )


# =====================================================
# TRANSACTION REPOSITORY
# =====================================================

class TransactionRepository:

    _lock = threading.Lock()

    def __init__(self, base_path="transactions"):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    def _get_filename(self, username):
        return os.path.join(self.base_path, f"{username}_transactions.txt")

    def save(self, transaction):
        try:
            filename = self._get_filename(transaction.username)
            data = transaction.serialize()

            with self._lock:
                with open(filename, "a", encoding="utf-8") as f:
                    f.write(data)

            return True
        except Exception:
            return False

    def get_all(self, username):
        try:
            filename = self._get_filename(username)
            if not os.path.isfile(filename):
                return []
            with open(filename, "r", encoding="utf-8") as f:
                return f.readlines()
        except Exception:
            return []


# =====================================================
#  TRAIN
# =====================================================

class Train:

    def __init__(self, name_train, destination, capacity, price):
        if not name_train.strip():
            raise ValueError("Invalid train name.")
        if capacity < 0:
            raise ValueError("Capacity cannot be negative.")
        if price <= 0:
            raise ValueError("Invalid price.")

        self.name_train = name_train
        self.destination = destination
        self._capacity = capacity
        self.price = float(price)

    @property
    def capacity(self):
        return self._capacity

    def reduce_capacity(self, quantity):
        if quantity <= 0 or quantity > self._capacity:
            raise ValueError("Invalid capacity reduction.")
        self._capacity -= quantity

    def __str__(self):
        return (
            f"{self.name_train} | "
            f"{self.destination} | "
            f"Capacity: {self.capacity} | "
            f"Price: {self.price}"
        )


# =====================================================
#  TRAIN MANAGER
# =====================================================

class TrainManager:

    def __init__(self):
        self._trains = []

    def add_train(self, train):
        if not isinstance(train, Train):
            return False
        if any(t.name_train == train.name_train for t in self._trains):
            return False
        self._trains.append(train)
        return True

    def get_all_trains(self):
        return list(self._trains)

    def find_train_by_name(self, name):
        for train in self._trains:
            if train.name_train == name:
                return train
        return None


# =====================================================
#  TICKET FILE WRITER
# =====================================================

class TicketFileWriter:

    _lock = threading.Lock()

    @staticmethod
    def save(user_name, train, quantity, total_price):
        try:
            os.makedirs("tickets", exist_ok=True)
            filename = os.path.join("tickets", "tickets.txt")

            now = datetime.datetime.now()

            ticket_info = (
                f"Buyer: {user_name}\n"
                f"Train: {train.name_train}\n"
                f"Destination: {train.destination}\n"
                f"Quantity: {quantity}\n"
                f"Total: {total_price}\n"
                f"Time: {now}\n"
                f"{'-'*40}\n"
            )

            with TicketFileWriter._lock:
                with open(filename, "a", encoding="utf-8") as file:
                    file.write(ticket_info)

            return True
        except Exception:
            return False


# =====================================================
#  WALLET
# =====================================================

class Wallet:

    _lock = threading.Lock()

    def __init__(self, username):
        self.__balance = 0.0
        self.__cards = []
        self.__bank_api = API()
        self.__username = username
        self.__transaction_repo = TransactionRepository()

    @property
    def balance(self):
        return self.__balance

    @property
    def cards(self):
        return tuple(self.__cards)

    def add_money(self, card, exp_month, exp_year, password, cvv2, amount):
        try:
            if amount <= 0:
                return None

            payment_id = self.__bank_api.pay(
                card, exp_month, exp_year, password, cvv2, amount
            )

            with self._lock:
                self.__balance += float(amount)

            if card not in self.__cards:
                self.__cards.append(card)

            self.__transaction_repo.save(
                Transaction(self.__username, amount, "charge")
            )

            return payment_id

        except Exception:
            return None

    def pay(self, amount):
        try:
            with self._lock:
                if amount <= 0 or amount > self.__balance:
                    return False
                self.__balance -= float(amount)

            self.__transaction_repo.save(
                Transaction(self.__username, amount, "payment")
            )
            return True

        except Exception:
            return False


# =====================================================
#  USER
# =====================================================

class User:

    def __init__(self, username, password, full_name, phone):
        self.username = username
        self._password = password
        self.full_name = full_name
        self.phone = phone
        self.wallet = Wallet(username)

    def check_password(self, password):
        return self._password == password

    def change_password(self, old_password, new_password):
        if not self.check_password(old_password):
            return False
        self._password = new_password
        return True

    def serialize(self):
        return f"{self.username},{self._password},{self.full_name},{self.phone}\n"


# =====================================================
#  FILE USER REPOSITORY
# =====================================================

class FileUserRepository:

    def __init__(self, filename="users.txt"):
        self.filename = filename

    def save(self, user):
        try:
            with open(self.filename, "a", encoding="utf-8") as f:
                f.write(user.serialize())
            return True
        except Exception:
            return False

    def update(self, updated_user):
        try:
            users = []
            if os.path.exists(self.filename):
                with open(self.filename, "r", encoding="utf-8") as f:
                    users = f.readlines()

            with open(self.filename, "w", encoding="utf-8") as f:
                for line in users:
                    username = line.split(",")[0]
                    if username == updated_user.username:
                        f.write(updated_user.serialize())
                    else:
                        f.write(line)
            return True
        except Exception:
            return False


# =====================================================
#  PROFILE SERVICE
# =====================================================

def safe_action(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            print("Operation failed safely.")
    return wrapper


class ProfileService:

    def __init__(self, user, repository):
        self.user = user
        self.repository = repository

    @safe_action
    def change_phone(self, new_phone):
        if Validator.validate_phone(new_phone):
            self.user.phone = new_phone
            self.repository.update(self.user)

    @safe_action
    def change_password(self, old, new):
        if Validator.validate_password(new):
            if self.user.change_password(old, new):
                self.repository.update(self.user)


# =====================================================
#  TICKET SERVICE
# =====================================================

class TicketService:

    def __init__(self, wallet):
        self.wallet = wallet

    def buy_ticket(self, user_name, train, quantity):
        try:
            if quantity <= 0 or quantity > train.capacity:
                return False

            total_price = train.price * quantity

            if not self.wallet.pay(total_price):
                return False

            train.reduce_capacity(quantity)

            TicketFileWriter.save(
                user_name, train, quantity, total_price
            )

            return True

        except Exception:
            return False
#----------------------


class UserMenu:

    def __init__(self, user, train_manager, user_repository):
        self.user = user
        self.train_manager = train_manager
        self.ticket_service = TicketService(user.wallet)
        self.profile_service = ProfileService(user, user_repository)

    def show(self):
        while True:
            try:
                print("\n====== USER PANEL ======")
                print("1. Buy Ticket")
                print("2. Profile")
                print("3. Exit")

                choice = input("Choice: ").strip()

                if choice == "1":
                    self.handle_buy()

                elif choice == "2":
                    self.profile_menu()

                elif choice == "3":
                    print("Logged out successfully.")
                    break

                else:
                    print("Invalid choice.")

            except Exception as e:
                print("[MENU ERROR]", e)

    def handle_buy(self):
        trains = self.train_manager.get_all_trains()

        if not trains:
            print("No trains available.")
            return

        for train in trains:
            print(train)

        name = input("Train name: ").strip()
        quantity = input("Quantity: ").strip()

        if not quantity.isdigit():
            print("Invalid quantity.")
            return

        quantity = int(quantity)

        train = self.train_manager.find_train_by_name(name)

        if not train:
            print("Train not found.")
            return

        if self.ticket_service.buy_ticket(self.user.username, train, quantity):
            print("Ticket purchased successfully.")
        else:
            print("Purchase failed.")

    def profile_menu(self):
        print("\n===== PROFILE MENU =====")
        print("1. Change Phone")
        print("2. Change Password")

        choice = input("Choice: ").strip()

        if choice == "1":
            phone = input("New phone: ")
            self.profile_service.change_phone(phone)

        elif choice == "2":
            old = input("Old password: ")
            new = input("New password: ")
            self.profile_service.change_password(old, new)

class UserRegister:

    def __init__(self, repository):
        self.repository = repository

    def register(self):
        try:
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            full_name = input("Full name: ").strip()
            phone = input("Phone: ").strip()

            if not Validator.validate_password(password):
                print("Weak password.")
                return None

            if not Validator.validate_phone(phone):
                print("Invalid phone.")
                return None

            user = User(username, password, full_name, phone)

            if self.repository.save(user):
                print("Registered successfully.")
                return user
            else:
                print("Registration failed.")
                return None

        except Exception as e:
            print("[REGISTER ERROR]", e)
            return None
#--------------
class UserLogin:

    def __init__(self, repository, train_manager):
        self.repository = repository
        self.train_manager = train_manager

    def login(self):
        try:
            username = input("Username: ").strip()
            password = input("Password: ").strip()

            if not os.path.exists(self.repository.filename):
                print("No registered users.")
                return None

            with open(self.repository.filename, "r", encoding="utf-8") as f:
                lines = f.readlines()

            for line in lines:
                data = line.strip().split(",")
                if len(data) != 4:
                    continue

                saved_username, saved_password, full_name, phone = data

                if saved_username == username and saved_password == password:
                    print("Login successful.")
                    return User(username, password, full_name, phone)

            print("Invalid credentials.")
            return None

        except Exception as e:
            print("[LOGIN ERROR]", e)
            return None





