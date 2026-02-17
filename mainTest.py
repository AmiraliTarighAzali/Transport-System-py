import re
import datetime
import os
from dataclasses import dataclass

# ==================== Default Credentials ====================
ADMIN_USERNAME = "Admin_Train"
ADMIN_PASSWORD = "Pass_Train"

# ==================== Storage Dictionaries ====================
employees = []  # List of employees
users = []  # All users list
lines = {}  # Lines dictionary
trains = {}  # Trains dictionary
train_dict_global = {}  # Trains dictionary (backup)


# ==================== Validation Classes ====================
class Validators:
    """Validation class"""

    @staticmethod
    def check_username(username, users_list):
        for user in users_list:
            if user.username == username:
                return False, "This username already exists!"
        return True, "Username is valid"

    @staticmethod
    def check_email(email, users_list):
        if '@' not in email:
            return False, "Email must have @"

        parts = email.split('@')
        if len(parts) != 2:
            return False, "Invalid email format"

        if '.' not in parts[1]:
            return False, "Domain must have a dot"

        for user in users_list:
            if user.email == email:
                return False, "This email is already registered!"

        return True, "Email is valid"

    @staticmethod
    def check_password(password):
        if len(password) < 8:
            return False, "Password must be at least 8 characters"

        has_letter = False
        has_number = False
        has_special = False

        for c in password:
            if c.isalpha():
                has_letter = True
            elif c.isdigit():
                has_number = True
            elif c in '@&':
                has_special = True

        if not has_letter:
            return False, "Password must have at least one letter"
        if not has_number:
            return False, "Password must have at least one number"
        if not has_special:
            return False, "Password must have @ or &"

        return True, "Password is valid"

    @staticmethod
    def check_phone(phone):
        if phone and (not phone.startswith('09') or len(phone) != 11 or not phone.isdigit()):
            return False, "Phone must start with 09 and be 11 digits"
        return True, "Phone is valid"


# ==================== Base Classes ====================
class User:
    """Base user class"""

    def __init__(self, username, password, full_name=None, email=None, phone=None):
        self.username = username
        self.password = password
        self.full_name = full_name
        self.email = email
        self.phone = phone

    def check_password(self, password):
        return self.password == password

    def change_password(self, old, new):
        if self.password != old:
            return False, "Wrong password"
        self.password = new
        return True, "Password changed"


@dataclass
class Staff:
    username: str
    password: str


# ==================== Wallet and Bank Classes ====================
class BankAPI:
    """Bank simulator"""

    @staticmethod
    def pay(card, month, year, password, cvv2, amount):
        # Dummy validation
        if card == "1234567812345678" and month == "12" and year == "25" and cvv2 == "123":
            return "PAY123456"
        if card == "8765432187654321" and month == "06" and year == "24" and cvv2 == "456":
            return "PAY654321"

        return None


class Wallet:
    """Wallet class"""

    def __init__(self):
        self.balance = 0
        self.cards = []
        self.transactions = []

    def add_money(self, card, month, year, password, cvv2, amount):
        if amount <= 0:
            return False, "Amount must be positive"

        payment_id = BankAPI.pay(card, month, year, password, cvv2, amount)

        if payment_id:
            self.balance += amount
            if card not in self.cards:
                self.cards.append(card[-4:])  # Save last 4 digits

            # Save transaction
            trans = {
                'type': 'deposit',
                'amount': amount,
                'balance': self.balance,
                'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.transactions.append(trans)

            return True, f"Added {amount} tomans. Payment ID: {payment_id}"

        return False, "Card information is wrong"

    def pay(self, amount):
        if amount <= 0:
            return False, "Invalid amount"
        if amount > self.balance:
            return False, "Not enough money"

        self.balance -= amount

        # Save transaction
        trans = {
            'type': 'purchase',
            'amount': amount,
            'balance': self.balance,
            'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.transactions.append(trans)

        return True, "Payment successful"


# ==================== Line and Train Classes ====================
class Line:
    """Line class"""

    def __init__(self, name, origin, destination, stations):
        self.name = name
        self.origin = origin
        self.destination = destination
        self.stations = stations
        self.trains = []

    def add_train(self, train):
        self.trains.append(train)

    def remove_train(self, train_id):
        new_list = []
        for t in self.trains:
            if t.train_id != train_id:
                new_list.append(t)
        self.trains = new_list


class Train:
    """Train class"""

    _id_counter = 1

    def __init__(self, name, line_name, speed, stop_time, quality, price, capacity, departure="08:00"):
        self.train_id = Train._id_counter
        Train._id_counter += 1

        self.name = name
        self.line_name = line_name
        self.speed = float(speed)
        self.stop_time = float(stop_time)
        self.quality = quality.upper()
        self.price = float(price)
        self.capacity = int(capacity)
        self.available = int(capacity)
        self.departure = departure

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
                if key == 'capacity':
                    self.available = int(value)

    def book(self, count):
        if count <= 0:
            return False, "Count must be positive"
        if count > self.available:
            return False, f"Only {self.available} seats available"

        self.available -= count
        return True, "Booked"

    def __str__(self):
        return (f"ID: {self.train_id} | {self.name} | Line: {self.line_name} | "
                f"Price: {self.price} | Available: {self.available}/{self.capacity}")


class TrainManager:
    """Train manager"""

    def __init__(self):
        self.all_trains = []

    def add_train(self, train):
        self.all_trains.append(train)

    def get_all(self):
        return self.all_trains

    def find_by_name(self, name):
        for t in self.all_trains:
            if t.name == name:
                return t
        return None


# ==================== Ticket Classes ====================
class Ticket:
    """Ticket class"""

    _id_counter = 1

    def __init__(self, username, train, count, total):
        self.ticket_id = Ticket._id_counter
        Ticket._id_counter += 1

        self.username = username
        self.train_name = train.name
        self.train_id = train.train_id
        self.count = count
        self.total = total
        self.time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def save_ticket_to_file(ticket, username):
    """Save ticket to file"""
    if not os.path.exists('data'):
        os.makedirs('data')

    filename = f"data/tickets_{username}.txt"

    with open(filename, 'a', encoding='utf-8') as f:
        f.write(f"Ticket ID: {ticket.ticket_id}\n")
        f.write(f"Train: {ticket.train_name}\n")
        f.write(f"Count: {ticket.count}\n")
        f.write(f"Total: {ticket.total} Tomans\n")
        f.write(f"Time: {ticket.time}\n")
        f.write("-" * 30 + "\n")


def save_trains_to_file(trains, username):
    """Save trains list to file"""
    if not os.path.exists('data'):
        os.makedirs('data')

    filename = f"data/trains_{username}.txt"

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Available Trains - {datetime.datetime.now()}\n")
        f.write("=" * 40 + "\n\n")

        for t in trains:
            f.write(f"ID: {t.train_id}\n")
            f.write(f"Name: {t.name}\n")
            f.write(f"Line: {t.line_name}\n")
            f.write(f"Price: {t.price} Tomans\n")
            f.write(f"Available: {t.available}/{t.capacity}\n")
            f.write("-" * 20 + "\n")


def save_transaction_to_file(trans, username):
    """Save transaction to file"""
    if not os.path.exists('data'):
        os.makedirs('data')

    filename = f"data/transactions_{username}.txt"

    with open(filename, 'a', encoding='utf-8') as f:
        f.write(f"[{trans['time']}] ")
        if trans['type'] == 'deposit':
            f.write(
                f"Charge: +{trans['amount']} | Balance: {trans['balance']}\n")
        else:
            f.write(
                f"Purchase: -{trans['amount']} | Balance: {trans['balance']}\n")


# ==================== User Classes ====================
class Admin(User):
    """Admin class"""

    def __init__(self, first, last, username, password, email):
        full = f"{first} {last}"
        super().__init__(username, password, full, email)
        self.first = first
        self.last = last


class Employee(User):
    """Employee class"""

    def __init__(self, first, last, username, password, email):
        full = f"{first} {last}"
        super().__init__(username, password, full, email)
        self.first = first
        self.last = last


class Passenger(User):
    """Passenger class"""

    def __init__(self, first, last, username, password, email):
        full = f"{first} {last}"
        super().__init__(username, password, full, email)
        self.first = first
        self.last = last
        self.wallet = Wallet()
        self.my_tickets = []
        self.my_cards = []


# ==================== Admin Panel ====================
class AdminPanel:
    """Admin panel"""

    def __init__(self):
        self.employees_list = []

    def show_menu(self):
        while True:
            print("\n--- ADMIN PANEL ---")
            print("1. Add Employee")
            print("2. Remove Employee")
            print("3. Show Employees")
            print("4. Back to Main Menu")
            print("0. Logout")

            ch = input("Choose: ").strip()

            if ch == '1':
                self.add_emp()
            elif ch == '2':
                self.remove_emp()
            elif ch == '3':
                self.show_emps()
            elif ch == '4' or ch == '0':
                print("Going back...")
                break
            else:
                print("Wrong choice!")

    def add_emp(self):
        while True:
            print("\n--- Add Employee ---")
            print("(Enter 0 to go back)")

            first = input("First name: ").strip()
            if first == '0':
                return

            last = input("Last name: ").strip()
            if last == '0':
                return

            username = input("Username: ").strip()
            if username == '0':
                return

            # Check username
            exists = False
            for e in self.employees_list:
                if e['username'] == username:
                    exists = True
                    break

            if exists:
                print("Username already exists!")
                cont = input("Try again? (y/n): ").lower()
                if cont == 'y':
                    continue
                else:
                    return

            email = input("Email: ").strip()
            if email == '0':
                return

            # Check email
            if '@' not in email or '.' not in email.split('@')[1]:
                print("Invalid email!")
                cont = input("Try again? (y/n): ").lower()
                if cont == 'y':
                    continue
                else:
                    return

            password = input("Password: ").strip()
            if password == '0':
                return

            # Check password
            good, msg = Validators.check_password(password)
            if not good:
                print(msg)
                cont = input("Try again? (y/n): ").lower()
                if cont == 'y':
                    continue
                else:
                    return

            # Add employee
            self.employees_list.append({
                'first': first,
                'last': last,
                'username': username,
                'email': email,
                'password': password
            })

            print("Employee added!")

            cont = input("Add another? (y/n): ").lower()
            if cont != 'y':
                return

    def remove_emp(self):
        while True:
            print("\n--- Remove Employee ---")

            if not self.employees_list:
                print("No employees!")
                input("Press Enter to go back...")
                return

            for i, e in enumerate(self.employees_list, 1):
                print(f"{i}. {e['first']} {e['last']} ({e['username']})")

            print("0. Back")

            try:
                ch = int(input("Choose number: "))
                if ch == 0:
                    return

                if 1 <= ch <= len(self.employees_list):
                    emp = self.employees_list[ch-1]
                    print(f"Remove {emp['first']} {emp['last']}?")
                    conf = input("y/n: ").lower()

                    if conf == 'y':
                        self.employees_list.pop(ch-1)
                        print("Removed!")

                    cont = input("Remove another? (y/n): ").lower()
                    if cont != 'y':
                        return
                else:
                    print("Wrong number!")
            except:
                print("Invalid input!")

    def show_emps(self):
        print("\n--- Employees ---")

        if not self.employees_list:
            print("No employees")
        else:
            for e in self.employees_list:
                print(f"Name: {e['first']} {e['last']}")
                print(f"Username: {e['username']}")
                print(f"Email: {e['email']}")
                print("-" * 20)

        input("Press Enter to go back...")


# ==================== Employee Panel ====================
class EmployeePanel:
    """Employee panel"""

    def __init__(self, emp_data):
        self.emp = emp_data
        self.my_lines = {}
        self.my_trains = {}

    def show_menu(self):
        while True:
            print("\n--- EMPLOYEE PANEL ---")
            print(f"Welcome {self.emp['first']} {self.emp['last']}")
            print("1. Line Management")
            print("2. Train Management")
            print("3. Back to Main Menu")
            print("0. Logout")

            ch = input("Choose: ").strip()

            if ch == '1':
                self.line_menu()
            elif ch == '2':
                self.train_menu()
            elif ch == '3' or ch == '0':
                print("Going back...")
                break
            else:
                print("Wrong choice!")

    def line_menu(self):
        while True:
            print("\n--- LINE MANAGEMENT ---")
            print("1. Add Line")
            print("2. Update Line")
            print("3. Delete Line")
            print("4. Show Lines")
            print("5. Back")

            ch = input("Choose: ").strip()

            if ch == '1':
                self.add_line()
            elif ch == '2':
                self.update_line()
            elif ch == '3':
                self.delete_line()
            elif ch == '4':
                self.show_lines()
            elif ch == '5':
                break
            else:
                print("Wrong choice!")

    def add_line(self):
        while True:
            print("\n--- Add Line ---")
            print("(Enter 0 to go back)")

            name = input("Line name: ").strip()
            if name == '0':
                return

            if name in self.my_lines:
                print("This name already exists!")
                cont = input("Try again? (y/n): ").lower()
                if cont == 'y':
                    continue
                else:
                    return

            origin = input("Origin: ").strip()
            if origin == '0':
                return

            dest = input("Destination: ").strip()
            if dest == '0':
                return

            stations = []
            while True:
                st = input("Station (Enter to finish): ").strip()
                if not st:
                    break
                if st == '0':
                    return
                stations.append(st)

            # Create line
            line = Line(name, origin, dest, stations)
            self.my_lines[name] = line

            print(f"Line '{name}' added!")

            cont = input("Add another? (y/n): ").lower()
            if cont != 'y':
                return

    def show_lines(self):
        print("\n--- Lines ---")

        if not self.my_lines:
            print("No lines")
        else:
            for name, line in self.my_lines.items():
                print(f"Name: {line.name}")
                print(f"Route: {line.origin} -> {line.destination}")
                print(f"Stations: {', '.join(line.stations)}")
                print(f"Trains: {len(line.trains)}")
                print("-" * 30)

        input("Press Enter to go back...")

    def delete_line(self):
        while True:
            print("\n--- Delete Line ---")

            if not self.my_lines:
                print("No lines!")
                input("Press Enter...")
                return

            names = list(self.my_lines.keys())
            for i, n in enumerate(names, 1):
                print(f"{i}. {n}")

            print("0. Back")

            try:
                ch = int(input("Choose number: "))
                if ch == 0:
                    return

                if 1 <= ch <= len(names):
                    name = names[ch-1]

                    # Remove trains of this line
                    to_remove = []
                    for tid, t in self.my_trains.items():
                        if t.line_name == name:
                            to_remove.append(tid)

                    for tid in to_remove:
                        del self.my_trains[tid]

                    del self.my_lines[name]
                    print(f"Line '{name}' deleted!")

                    cont = input("Delete another? (y/n): ").lower()
                    if cont != 'y':
                        return
                else:
                    print("Wrong number!")
            except:
                print("Invalid input!")

    def update_line(self):
        while True:
            print("\n--- Update Line ---")

            if not self.my_lines:
                print("No lines!")
                input("Press Enter...")
                return

            names = list(self.my_lines.keys())
            for i, n in enumerate(names, 1):
                print(f"{i}. {n}")

            print("0. Back")

            try:
                ch = int(input("Choose line: "))
                if ch == 0:
                    return

                if 1 <= ch <= len(names):
                    name = names[ch-1]
                    line = self.my_lines[name]

                    print(f"\nUpdating: {name}")
                    print("1. Origin")
                    print("2. Destination")
                    print("3. Stations")
                    print("4. Cancel")

                    opt = input("Choose: ").strip()

                    if opt == '1':
                        new = input("New origin: ").strip()
                        if new and new != '0':
                            line.origin = new
                            print("Updated!")
                    elif opt == '2':
                        new = input("New destination: ").strip()
                        if new and new != '0':
                            line.destination = new
                            print("Updated!")
                    elif opt == '3':
                        stations = []
                        while True:
                            st = input("Station (Enter to finish): ").strip()
                            if not st:
                                break
                            stations.append(st)
                        if stations:
                            line.stations = stations
                            print("Updated!")

                    cont = input("Update another? (y/n): ").lower()
                    if cont != 'y':
                        return
                else:
                    print("Wrong number!")
            except:
                print("Invalid input!")

    def train_menu(self):
        while True:
            print("\n--- TRAIN MANAGEMENT ---")
            print("1. Add Train")
            print("2. Update Train")
            print("3. Delete Train")
            print("4. Show Trains")
            print("5. Back")

            ch = input("Choose: ").strip()

            if ch == '1':
                self.add_train()
            elif ch == '2':
                self.update_train()
            elif ch == '3':
                self.delete_train()
            elif ch == '4':
                self.show_trains()
            elif ch == '5':
                break
            else:
                print("Wrong choice!")

    def add_train(self):
        while True:
            print("\n--- Add Train ---")

            if not self.my_lines:
                print("No lines! Add a line first.")
                input("Press Enter...")
                return

            print("Available lines:")
            for name in self.my_lines:
                print(f"- {name}")

            print("(Enter 0 to go back)")

            line_name = input("Line name: ").strip()
            if line_name == '0':
                return

            if line_name not in self.my_lines:
                print("Line not found!")
                continue

            name = input("Train name: ").strip()
            if name == '0':
                return

            try:
                speed = float(input("Speed (km/h): "))
                stop = float(input("Stop time (min): "))

                qual = input("Quality (A/B/C): ").strip().upper()
                if qual not in ['A', 'B', 'C']:
                    print("Must be A, B, or C")
                    continue

                price = float(input("Price: "))
                cap = int(input("Capacity: "))
                dep = input("Departure (HH:MM) [08:00]: ").strip() or "08:00"

                # Create train
                train = Train(name, line_name, speed,
                              stop, qual, price, cap, dep)
                self.my_trains[train.train_id] = train
                self.my_lines[line_name].add_train(train)

                print(f"Train added! ID: {train.train_id}")

                cont = input("Add another? (y/n): ").lower()
                if cont != 'y':
                    return

            except:
                print("Invalid numbers!")

    def show_trains(self):
        print("\n--- Trains ---")

        if not self.my_trains:
            print("No trains")
        else:
            for tid, t in self.my_trains.items():
                print(t)
                print("-" * 30)

        input("Press Enter to go back...")

    def delete_train(self):
        while True:
            print("\n--- Delete Train ---")

            if not self.my_trains:
                print("No trains!")
                input("Press Enter...")
                return

            ids = list(self.my_trains.keys())
            for i, tid in enumerate(ids, 1):
                t = self.my_trains[tid]
                print(f"{i}. ID: {tid} - {t.name} ({t.line_name})")

            print("0. Back")

            try:
                ch = int(input("Choose number: "))
                if ch == 0:
                    return

                if 1 <= ch <= len(ids):
                    tid = ids[ch-1]
                    train = self.my_trains[tid]

                    print(f"Delete {train.name}?")
                    conf = input("y/n: ").lower()

                    if conf == 'y':
                        # Remove from line
                        if train.line_name in self.my_lines:
                            self.my_lines[train.line_name].remove_train(tid)

                        del self.my_trains[tid]
                        print("Deleted!")

                    cont = input("Delete another? (y/n): ").lower()
                    if cont != 'y':
                        return
                else:
                    print("Wrong number!")
            except:
                print("Invalid input!")

    def update_train(self):
        while True:
            print("\n--- Update Train ---")

            if not self.my_trains:
                print("No trains!")
                input("Press Enter...")
                return

            ids = list(self.my_trains.keys())
            for i, tid in enumerate(ids, 1):
                t = self.my_trains[tid]
                print(f"{i}. ID: {tid} - {t.name}")

            print("0. Back")

            try:
                ch = int(input("Choose train: "))
                if ch == 0:
                    return

                if 1 <= ch <= len(ids):
                    tid = ids[ch-1]
                    train = self.my_trains[tid]

                    print(f"\nUpdating: {train.name}")
                    print("1. Name")
                    print("2. Quality")
                    print("3. Price")
                    print("4. Capacity")
                    print("5. Speed")
                    print("6. Stop Time")
                    print("7. Cancel")

                    opt = input("Choose: ").strip()

                    updates = {}
                    if opt == '1':
                        new = input("New name: ").strip()
                        if new:
                            updates['name'] = new
                    elif opt == '2':
                        new = input("New quality (A/B/C): ").strip().upper()
                        if new in ['A', 'B', 'C']:
                            updates['quality'] = new
                    elif opt == '3':
                        new = float(input("New price: "))
                        updates['price'] = new
                    elif opt == '4':
                        new = int(input("New capacity: "))
                        updates['capacity'] = new
                    elif opt == '5':
                        new = float(input("New speed: "))
                        updates['speed'] = new
                    elif opt == '6':
                        new = float(input("New stop time: "))
                        updates['stop_time'] = new

                    if updates:
                        train.update(**updates)
                        print("Updated!")

                    cont = input("Update another? (y/n): ").lower()
                    if cont != 'y':
                        return
                else:
                    print("Wrong number!")
            except:
                print("Invalid input!")


# ==================== User Panel ====================
class UserPanel:
    """User panel"""

    def __init__(self, user, train_mgr):
        self.user = user
        self.train_mgr = train_mgr

    def show_menu(self):
        while True:
            print("\n--- USER PANEL ---")
            print(f"Welcome {self.user.full_name}")
            print("1. Buy Ticket")
            print("2. My Wallet")
            print("3. My Profile")
            print("4. My Cards")
            print("5. My Transactions")
            print("6. Back to Main Menu")
            print("0. Logout")

            ch = input("Choose: ").strip()

            if ch == '1':
                self.buy_ticket()
            elif ch == '2':
                self.wallet_menu()
            elif ch == '3':
                self.profile_menu()
            elif ch == '4':
                self.show_cards()
            elif ch == '5':
                self.show_transactions()
            elif ch == '6' or ch == '0':
                print("Going back...")
                break
            else:
                print("Wrong choice!")

    def wallet_menu(self):
        while True:
            print("\n--- WALLET ---")
            print(f"Balance: {self.user.wallet.balance} Tomans")
            print("1. Charge Wallet")
            print("2. Back")

            ch = input("Choose: ").strip()

            if ch == '1':
                self.charge_wallet()
            elif ch == '2':
                break

    def charge_wallet(self):
        print("\n--- Charge Wallet ---")

        try:
            amount = float(input("Amount: "))
            if amount <= 0:
                print("Amount must be positive")
                return

            print("Card info:")
            card = input("Card number: ").strip()
            month = input("Exp month (MM): ").strip()
            year = input("Exp year (YY): ").strip()
            passw = input("Password: ").strip()
            cvv2 = input("CVV2: ").strip()

            ok, msg = self.user.wallet.add_money(
                card, month, year, passw, cvv2, amount)

            if ok:
                print(msg)
                # Save to file
                if self.user.wallet.transactions:
                    save_transaction_to_file(
                        self.user.wallet.transactions[-1], self.user.username)
            else:
                print(msg)

        except:
            print("Something went wrong!")

    def buy_ticket(self):
        print("\n--- Buy Ticket ---")

        all_trains = self.train_mgr.get_all()

        if not all_trains:
            print("No trains available!")
            input("Press Enter...")
            return

        # Show trains
        available = []
        for t in all_trains:
            if t.available > 0:
                available.append(t)

        if not available:
            print("All trains are full!")
            input("Press Enter...")
            return

        # Save to file
        save_trains_to_file(available, self.user.username)

        print("\nAvailable Trains:")
        for i, t in enumerate(available, 1):
            print(
                f"{i}. {t.name} - Line: {t.line_name} - Price: {t.price} - Seats: {t.available}")

        try:
            ch = int(input("\nChoose train: ")) - 1
            if ch < 0 or ch >= len(available):
                print("Wrong choice!")
                return

            train = available[ch]

            count = int(input("How many tickets: "))
            if count <= 0:
                print("Invalid number")
                return

            total = train.price * count

            if total > self.user.wallet.balance:
                print(
                    f"Not enough money! You have {self.user.wallet.balance}, need {total}")
                return

            # Book
            ok, msg = train.book(count)
            if not ok:
                print(msg)
                return

            # Pay
            ok, msg = self.user.wallet.pay(total)
            if not ok:
                print(msg)
                return

            # Create ticket
            ticket = Ticket(self.user.username, train, count, total)
            self.user.my_tickets.append(ticket)

            # Save to file
            save_ticket_to_file(ticket, self.user.username)

            # Save transaction
            if self.user.wallet.transactions:
                save_transaction_to_file(
                    self.user.wallet.transactions[-1], self.user.username)

            print(f"Purchase successful! Total: {total} Tomans")
            print(f"Ticket ID: {ticket.ticket_id}")

        except:
            print("Invalid input!")

    def profile_menu(self):
        while True:
            print("\n--- PROFILE ---")
            print(f"Username: {self.user.username}")
            print(f"Name: {self.user.full_name}")
            print(f"Email: {self.user.email}")
            print(f"Phone: {self.user.phone}")
            print("\n1. Change Name")
            print("2. Change Phone")
            print("3. Change Password")
            print("4. Back")

            ch = input("Choose: ").strip()

            if ch == '1':
                new = input("New full name: ").strip()
                if new:
                    self.user.full_name = new
                    print("Updated!")
            elif ch == '2':
                new = input("New phone: ").strip()
                ok, _ = Validators.check_phone(new)
                if ok:
                    self.user.phone = new
                    print("Updated!")
                else:
                    print("Invalid phone!")
            elif ch == '3':
                old = input("Old password: ").strip()
                new = input("New password: ").strip()
                ok, msg = Validators.check_password(new)
                if not ok:
                    print(msg)
                else:
                    ok, msg = self.user.change_password(old, new)
                    print(msg)
            elif ch == '4':
                break

    def show_cards(self):
        print("\n--- My Cards ---")

        if not self.user.wallet.cards:
            print("No cards saved")
        else:
            for i, card in enumerate(self.user.wallet.cards, 1):
                print(f"{i}. **** **** **** {card}")

        input("Press Enter...")

    def show_transactions(self):
        print("\n--- Transactions ---")

        if not self.user.wallet.transactions:
            print("No transactions")
        else:
            for t in self.user.wallet.transactions[-10:]:  # Last 10
                typ = "Charge" if t['type'] == 'deposit' else "Purchase"
                print(
                    f"[{t['time']}] {typ}: {t['amount']} | Balance: {t['balance']}")

        input("Press Enter...")


# ==================== Main System ====================
class RailwaySystem:
    """Main system"""

    def __init__(self):
        self.all_users = []
        self.all_lines = {}
        self.all_trains = {}
        self.train_manager = TrainManager()

        # Create default admin
        default_admin = Admin("Admin", "User", ADMIN_USERNAME,
                              ADMIN_PASSWORD, "admin@rail.com")
        self.all_users.append(default_admin)

        # Admin panel
        self.admin_panel = AdminPanel()

        # Current user
        self.current_user = None

    def start(self):
        while True:
            print("\n" + "="*50)
            print("    RAILWAY TRANSPORT SYSTEM")
            print("="*50)
            print("1. Admin Login")
            print("2. Employee Login")
            print("3. User Menu")
            print("4. Exit")
            print("="*50)

            ch = input("Choose: ").strip()

            if ch == '1':
                self.admin_login()
            elif ch == '2':
                self.employee_login()
            elif ch == '3':
                self.user_main_menu()
            elif ch == '4':
                print("Goodbye!")
                break
            else:
                print("Wrong choice!")

    def admin_login(self):
        print("\n--- Admin Login ---")
        print("(Enter 0 to go back)")

        user = input("Username: ").strip()
        if user == '0':
            return

        passw = input("Password: ").strip()
        if passw == '0':
            return

        if user == ADMIN_USERNAME and passw == ADMIN_PASSWORD:
            print("Welcome Admin!")
            self.admin_panel.show_menu()
        else:
            print("Wrong username or password!")

    def employee_login(self):
        print("\n--- Employee Login ---")
        print("(Enter 0 to go back)")

        user = input("Username: ").strip()
        if user == '0':
            return

        passw = input("Password: ").strip()
        if passw == '0':
            return

        # Check in admin's employees list
        found = None
        for e in self.admin_panel.employees_list:
            if e['username'] == user and e['password'] == passw:
                found = e
                break

        if found:
            print(f"Welcome {found['first']}!")

            # Create employee panel
            emp_panel = EmployeePanel(found)

            # Share global data
            emp_panel.my_lines = self.all_lines
            emp_panel.my_trains = self.all_trains

            emp_panel.show_menu()

            # Update global data
            self.all_lines = emp_panel.my_lines
            self.all_trains = emp_panel.my_trains

            # Update train manager
            self.train_manager.all_trains = list(self.all_trains.values())
        else:
            print("Wrong username or password!")

    def user_main_menu(self):
        while True:
            print("\n--- USER MENU ---")
            print("1. Register")
            print("2. Login")
            print("3. Back")

            ch = input("Choose: ").strip()

            if ch == '1':
                self.user_register()
            elif ch == '2':
                self.user_login()
            elif ch == '3':
                break
            else:
                print("Wrong choice!")

    def user_register(self):
        while True:
            print("\n--- Register ---")
            print("(Enter 0 to go back)")

            first = input("First name: ").strip()
            if first == '0':
                return

            last = input("Last name: ").strip()
            if last == '0':
                return

            user = input("Username: ").strip()
            if user == '0':
                return

            # Check username
            exists = False
            for u in self.all_users:
                if u.username == user:
                    exists = True
                    break

            if exists:
                print("Username already exists!")
                cont = input("Try again? (y/n): ").lower()
                if cont == 'y':
                    continue
                else:
                    return

            email = input("Email: ").strip()
            if email == '0':
                return

            # Check email
            if '@' not in email:
                print("Email must have @")
                cont = input("Try again? (y/n): ").lower()
                if cont == 'y':
                    continue
                else:
                    return

            parts = email.split('@')
            if '.' not in parts[1]:
                print("Domain must have a dot")
                cont = input("Try again? (y/n): ").lower()
                if cont == 'y':
                    continue
                else:
                    return

            # Check email exists
            for u in self.all_users:
                if u.email == email:
                    print("Email already registered!")
                    cont = input("Try again? (y/n): ").lower()
                    if cont == 'y':
                        continue
                    else:
                        return

            passw = input("Password: ").strip()
            if passw == '0':
                return

            # Check password
            good, msg = Validators.check_password(passw)
            if not good:
                print(msg)
                cont = input("Try again? (y/n): ").lower()
                if cont == 'y':
                    continue
                else:
                    return

            phone = input("Phone (optional): ").strip()

            # Create user
            new_user = Passenger(first, last, user, passw, email)
            if phone:
                new_user.phone = phone

            self.all_users.append(new_user)
            print("Registered! You can now login.")

            cont = input("Register another? (y/n): ").lower()
            if cont != 'y':
                return

    def user_login(self):
        print("\n--- Login ---")
        print("(Enter 0 to go back)")

        user = input("Username: ").strip()
        if user == '0':
            return

        passw = input("Password: ").strip()
        if passw == '0':
            return

        found = None
        for u in self.all_users:
            if isinstance(u, Passenger) and u.username == user and u.password == passw:
                found = u
                break

        if found:
            print(f"Welcome {found.full_name}!")

            # Update train manager
            self.train_manager.all_trains = list(self.all_trains.values())

            # Create user panel
            user_panel = UserPanel(found, self.train_manager)
            user_panel.show_menu()
        else:
            print("Wrong username or password!")


# ==================== Run ====================
if __name__ == "__main__":
    system = RailwaySystem()
    system.start()
