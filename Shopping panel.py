
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


### edit_profile
 
### logout
    