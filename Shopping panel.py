

### menu

class Train:
    def __init__(self, name_train, destination, capacity, price):
        self.name_train = name_train
        self.destination = destination
        self.capacity = capacity
        self.price = price

    def show_information(self):
        information = (
            f"Name Train: {self.name_train}\n"
            f"Destination: {self.destination}\n"
            f"Remaining Capacity: {self.capacity}\n"
            f"Price: {self.price}\n"
        )
        return information

    def reduce_capacity(self, quantity):
        if quantity <= 0:
            raise ValueError("Invalid ticket quantity.")
        if quantity > self.capacity:
            raise ValueError("Capacity is full or not enough seats.")
        self.capacity -= quantity






from BANK import API
class Wallet:
    def __init__(self):
        self.__balance = 0
        self.__card = []
        self.__bank_api = API()

        def get_balance(self):
            return self.__balance
        def get_cards(self):
            return self.__card
        

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

    

    

### edit_profile
 
### logout
    