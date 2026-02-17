
#================
#      menu
#================
class UserMenu:
    def __init__(self, user, train_manager):
        self.user = user
        self.train_manager = train_manager
        self.wallet = user.wallet
        self.ticket_service = TicketService(self.wallet)

    def show(self):
        while True:
            print("====== panel ======")
            print("1. Buy ticket")
            print("2.View & update info")
            print("3.Exit")

            choice = input("Choice:")
            if choice == '1':
                self.by_ticket()
            elif choice == '2':
                self.edit_profile()
            elif choice == '3':
                self.logout()
                break
            else:
                raise ValueError("Please try again")

    def handle_buy(self):
        self.train_manager.exept_trains_to_file()

        for train in self.train_manager.get_all_trains():
            print(train)

        name = input("name train:")
        quantity = int(input("Number of Trains:"))

        train = self.train_manager.find_train_by_name(name)

        try:
            self.ticket_service.buy_ticket(self.user.username, train, quantity)
            print("Purchase completed successfully.")
        except ValueError as e:
            print("Error:", e)

    def edit_profile(self):
        print("Profile section (Coming next step...)")

    def logout(self):
        print("Logged out successfully.")

#______________________
from BANK import API
import datetime

# =========================
#        TRAIN
# =========================

class Train:
    def __init__(self, name_train, destination, capacity, price):
        self.name_train = name_train
        self.destination = destination
        self.capacity = capacity
        self.price = price

    @property
    def capacity(self):
        return self._capacity
    

    def reduce_capacity(self, quantity):
        if quantity <= 0:
            raise ValueError("Invalid ticket quantity.")
        if quantity > self.capacity:
            raise ValueError("Capacity is full or not enough seats.")
        self.capacity -= quantity

    def __str__(self):
        return  (
            f"Name Train: {self.name_train}"
            f"Destination: {self.destination}"
            f"Remaining Capacity: {self.capacity}"
            f"Price: {self.price}"
        )
#==========================
#    TRAIN MANAGER
#==========================

class TrainManager:
    def __init__(self):
        self._trains = []
        
    def add_train(self, train):
        self._trains.append(train)

    def get_all_trains(self):
        for train in self._trains:
            yield train

    def find_train_by_name(self, name):
        for train in self._trains:
            if train.name_train == name:
                return train
        raise ValueError ("train not found")


#===================
#     WALLET
#===================


class Wallet:
    def __init__(self):
        self.__balance = 0
        self.__card = []
        self.__bank_api = API()

    @property
    def balance(self):
        return self.__balance

    @property
    def get_cards(self):
        return tuple(self.__card)
    

    def add_money(self, card, exp_month, exp_year, password, cvv2, amount):
        
        if amount <= 0:
            raise ValueError("Amount must be positive.")

        payment_id = self.__bank_api.pay(card, exp_month, exp_year, password, cvv2, amount)

        self.__balance += amount

        if card not in self.__cards:
            self.__cards.append(card)
        return payment_id

    def pay(self, amount):
        if amount <= 0:
            raise ValueError("Invalid payment amount.")
        if amount > self.__balance:
            raise ValueError("Insufficient funds.")
        self.__balance -= amount

#=====================
#    FILE WRITER
#=====================
class TicketFileWriter:
    @staticmethod
    def save(user_name, train, quantity, total_price):
        now = datetime.datetime.now()

        ticket_info = (
            f"Buyer Name: {user_name}\n"
            f"Train Name: {train.name_train}\n"
            f"Destination: {train.destination}\n"
            f"Ticket Count: {quantity}\n"
            f"Total Price: {total_price}\n"
            f"Purchase Time: {now}\n"
            f"{'-'*40}\n"
)
        with open ("tickets.txt", "a" , encoding= "utf-8") as file:
            file.write(ticket_info)

#=======================
#     TICKET SERVICE
#=======================
class TicketServise:
    def __init__ (self, wallet):
        self.wallet = wallet

    def by_ticket(self, user_name, train , quantity):
        if quantity <= 0:
            raise ValueError ("Invalid ticket quantity.")

        total_price = train.price * quantity

        if quantity > train.capacity:
            raise ValueError ("Not enough capacity. Capacity full!")

        if total_price > self.wallet.balance:
            raise ValueError("Insufficient wallet balance.")
    
        train.reduce_capacity(quantity)
        self.wallet.pay(total_price)

        TicketFileWriter.save(user_name, train, quantity, total_price)

#========================
#       USER MODEL
#========================

import re

class User:
    def __init__(self, username, password, full_name, phone, wallet):
        self.username = username
        self._password = password
        self.full_name = full_name
        self.phone = phone
        self.wallet = wallet

    def check_password(self, password):
        return self._password == password

    def change_password(self, old_password, new_password):
        if not self.check_password(old_password):
            raise ValueError("Current password is incorrect.")
        self._password = new_password

    def update_full_name(self, new_name):
        self.full_name = new_name

    def update_phone(self, new_phone):
        self.phone = new_phone

    def serialize(self):
        return f"{self.username},{self._password},{self.full_name},{self.phone}\n"

    def __str__(self):
        return (
            f"Username: {self.username}\n"
            f"Full Name: {self.full_name}\n"
            f"Phone: {self.phone}\n"
            f"Wallet Balance: {self.wallet.balance}\n"
            f"Saved Cards: {self.wallet.cards}\n"
        )

#========================
#       VALIDATOR.           #انتزاعی
#========================

class Validator:

    @staticmethod
    def validate_phone(phone):
        pattern = r"^09\d{9}$"
        if not re.match(pattern, phone):
            raise ValueError("Phone must start with 09 and be 11 digits.")

    @staticmethod
    def validate_password(password):
        pattern = r"^(?=.*[A-Z])(?=.*\d).{6,}$"
        if not re.match(pattern, password):
            raise ValueError(
                "Password must be at least 6 chars, include 1 uppercase and 1 digit."
            )

#============================
#       FILE USER REPOSITORY 
#============================

class FileUserRepository(UserRepository):

    def __init__(self, filename="users.txt"):
        self.filename = filename

    def save(self, user):
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(user.serialize())

    def update(self, updated_user):
        users = []

        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                users = f.readlines()
        except FileNotFoundError:
            pass

        with open(self.filename, "w", encoding="utf-8") as f:
            for line in users:
                username = line.split(",")[0]
                if username == updated_user.username:
                    f.write(updated_user.serialize())
                else:
                    f.write(line)


#============================
#       DECORATOR
#============================

def safe_action(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            raise("Error:", e)
    return wrapper

#==================================
#        EDIT PROFILE SECTION
#==================================

class ProfileService:

    def __init__(self, user, repository):
        self.user = user
        self.repository = repository

    @safe_action
    def view_profile(self):
        print("\n--- User Information ---")
        print(self.user)

    @safe_action
    def change_full_name(self):
        new_name = input("New full name: ")
        self.user.update_full_name(new_name)
        self.repository.update(self.user)
        print("Full name updated successfully.")

    @safe_action
    def change_phone(self):
        new_phone = input("New phone: ")
        Validator.validate_phone(new_phone)
        self.user.update_phone(new_phone)
        self.repository.update(self.user)
        print("Phone updated successfully.")

    @safe_action
    def change_password(self):
        old = input("Current password: ")
        new = input("New password: ")
        Validator.validate_password(new)
        self.user.change_password(old, new)
        self.repository.update(self.user)
        print("Password changed successfully.")

#==================================
#       LOGOUT SECTION
#==================================

    def logout(self):
        print("Saving user data...")
        print("Logged out successfully.")
