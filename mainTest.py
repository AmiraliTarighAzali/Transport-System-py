import re
import os
import json
import hashlib
import datetime
from BANK import API

class BaseTrain():

    def __init__(self, train_name, train_line, mean_speed, stop_time, quality, price, capacity):
        self.train_name = train_name
        self.train_line = train_line
        self.mean_speed = mean_speed
        self.stop_time = stop_time
        self.quality = quality
        self.price = price
        self.capacity = capacity

    
    def update_info(self, update_case, new_value):
        setattr(self, update_case, new_value)


    def __str__(self):
        return (
            f"Train Name: {self.train_name}, "
            f"Train Line: {self.train_line}, "
            f"Train Mean Speed: {self.mean_speed}, "
            f"Train Stop Time: {self.stop_time}, "
            f"Train Quality: {self.quality}, "
            f"Train Price: {self.price}, "
            f"Train Capacity: {self.capacity}")    


# =========================
# Regex Validators
# =========================
class Validators:
    EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
    PHONE_RE = re.compile(r"^09\d{9}$")  # 11 digits, starts with 09
    USERNAME_RE = re.compile(r"^[A-Za-z0-9_]{3,30}$")
    # حداقل 8 کاراکتر + حداقل یک حرف + حداقل یک عدد + حداقل یکی از @ یا &
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


# =========================
# Password hashing
# =========================
class PasswordHasher:
    @staticmethod
    def make_salt() -> str:
        # ساده و آماتوری ولی کافی
        return os.urandom(16).hex()

    @staticmethod
    def hash_password(password: str, salt: str) -> str:
        data = (salt + password).encode("utf-8")
        return hashlib.sha256(data).hexdigest()

    @staticmethod
    def verify(password: str, salt: str, hashed: str) -> bool:
        return PasswordHasher.hash_password(password, salt) == hashed


# =========================
# Simple File Storage (JSON lines)
# =========================
class FileStorage:
    def __init__(self, folder="data"):
        self.folder = folder
        if not os.path.exists(folder):
            os.makedirs(folder)

        self.users_file = os.path.join(folder, "users.txt")
        self.employees_file = os.path.join(folder, "employees.txt")
        self.transactions_file = os.path.join(folder, "transactions.txt")
        self.tickets_file = os.path.join(folder, "tickets.txt")

        for f in [self.users_file, self.employees_file, self.transactions_file, self.tickets_file]:
            if not os.path.exists(f):
                with open(f, "w", encoding="utf-8") as _:
                    pass

    def append_json_line(self, filepath, data: dict):
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")

    def read_all_json_lines(self, filepath):
        items = []
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        items.append(json.loads(line))
                    except:
                        pass
        return items

    def write_all_json_lines(self, filepath, items):
        with open(filepath, "w", encoding="utf-8") as f:
            for it in items:
                f.write(json.dumps(it, ensure_ascii=False) + "\n")


# =========================
# Domain Classes
# =========================
class User:
    def __init__(self, username, salt, password_hash, full_name, email, phone=""):
        self.username = username
        self.salt = salt
        self.password_hash = password_hash
        self.full_name = full_name
        self.email = email
        self.phone = phone


class Passenger(User):
    def __init__(self, username, salt, password_hash, full_name, email, phone=""):
        super().__init__(username, salt, password_hash, full_name, email, phone)
        self.wallet = Wallet(owner_username=username)


class Employee:
    def __init__(self, first, last, username, salt, password_hash, email):
        self.first = first
        self.last = last
        self.username = username
        self.salt = salt
        self.password_hash = password_hash
        self.email = email


class Line:
    def __init__(self, name, origin, destination, stations, distance_km):
        self.name = name
        self.origin = origin
        self.destination = destination
        self.stations = stations  # list[str]
        self.distance_km = distance_km  # فاصله بین هر ایستگاه
        self.trains = []  # list[Train]


class Train:
    _id_counter = 1

    def __init__(self, name, line_name, speed_kmh, stop_min, quality, price, capacity, departure_time):
        self.train_id = Train._id_counter
        Train._id_counter += 1

        self.name = name
        self.line_name = line_name
        self.speed_kmh = float(speed_kmh)
        self.stop_min = float(stop_min)
        self.quality = quality
        self.price = float(price)
        self.capacity = int(capacity)
        self.available = int(capacity)
        self.departure_time = departure_time  # "HH:MM"

    def book(self, count):
        if count <= 0:
            return False, "Count must be positive"
        if count > self.available:
            return False, f"Only {self.available} seats available"
        self.available -= count
        return True, "Booked"

    def __str__(self):
        return f"ID:{self.train_id} | {self.name} | Line:{self.line_name} | Price:{self.price} | Seats:{self.available}/{self.capacity}"


class Ticket:
    _id_counter = 1

    def __init__(self, username, train: Train, count, total):
        self.ticket_id = Ticket._id_counter
        Ticket._id_counter += 1
        self.username = username
        self.train_id = train.train_id
        self.train_name = train.name
        self.count = count
        self.total = total
        self.time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class Wallet:
    def __init__(self, owner_username):
        self.owner_username = owner_username
        self.balance = 0
        self.cards = []
        self.transactions = []  # فقط برای ران تایم (به علاوه فایل)

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


# =========================
# Helper: schedule & collision (Bonus)
# =========================
class ScheduleHelper:
    @staticmethod
    def parse_time_hhmm(t: str):
        # "08:05" -> minutes from 00:00
        parts = t.strip().split(":")
        if len(parts) != 2:
            return None
        if not parts[0].isdigit() or not parts[1].isdigit():
            return None
        h = int(parts[0])
        m = int(parts[1])
        if h < 0 or h > 23 or m < 0 or m > 59:
            return None
        return h * 60 + m

    @staticmethod
    def format_minutes(mins: int):
        h = mins // 60
        m = mins % 60
        return f"{h:02d}:{m:02d}"

    @staticmethod
    def build_station_windows(line: Line, train: Train):
        """
        خروجی: dict station -> (arrival_min, departure_min)
        فرض ساده: بین هر دو ایستگاه فاصله ثابت line.distance_km است.
        travel_time(min) = distance / speed * 60
        """
        dep0 = ScheduleHelper.parse_time_hhmm(train.departure_time)
        if dep0 is None:
            return None

        travel_min = int(round((line.distance_km / train.speed_kmh) * 60))
        stop_min = int(round(train.stop_min))

        # لیست ایستگاه‌ها: origin + stations + destination
        all_stations = [line.origin] + line.stations + [line.destination]

        windows = {}
        current_depart = dep0

        # (arrival = depart)
        windows[all_stations[0]] = (current_depart, current_depart)

        for i in range(1, len(all_stations)):
            arrival = current_depart + travel_min
            depart = arrival + stop_min
            windows[all_stations[i]] = (arrival, depart)
            current_depart = depart

        return windows

    @staticmethod
    def has_collision(line: Line, new_train: Train):
        """
        برخورد یعنی در یک ایستگاه، بازه‌های (arrival..departure) دو قطار overlap داشته باشد.
        """
        new_windows = ScheduleHelper.build_station_windows(line, new_train)
        if new_windows is None:
            return True, "Invalid departure time"

        for old_train in line.trains:
            old_windows = ScheduleHelper.build_station_windows(line, old_train)
            if old_windows is None:
                continue

            # ایستگاه مشترک‌ها
            for station in new_windows:
                if station in old_windows:
                    a1, d1 = new_windows[station]
                    a2, d2 = old_windows[station]

                    # overlap check
                    if not (d1 <= a2 or d2 <= a1):
                        msg = (
                            f"Collision! Train '{new_train.name}' conflicts with Train '{old_train.name}' "
                            f"at station '{station}' "
                            f"(new: {ScheduleHelper.format_minutes(a1)}-{ScheduleHelper.format_minutes(d1)} "
                            f"old: {ScheduleHelper.format_minutes(a2)}-{ScheduleHelper.format_minutes(d2)})"
                        )
                        return True, msg

        return False, "No collision"


# =========================
# Panels (CLI)
# =========================
class AdminPanel:
    def __init__(self, system):
        self.system = system

    def menu(self):
        while True:
            print("\n--- ADMIN PANEL ---")
            print("1. Add Employee")
            print("2. Remove Employee")
            print("3. Show Employees")
            print("4. Back")
            ch = input("Choose: ").strip()

            if ch == "1":
                self.add_employee()
            elif ch == "2":
                self.remove_employee()
            elif ch == "3":
                self.show_employees()
            elif ch == "4":
                return
            else:
                print("Wrong choice!")

    def add_employee(self):
        print("\n--- Add Employee --- (0 to back)")
        first = self._ask_nonempty("First name: ")
        if first is None:
            return
        last = self._ask_nonempty("Last name: ")
        if last is None:
            return

        # username
        while True:
            username = input("Username: ").strip()
            if username == "0":
                return
            if not Validators.valid_username(username):
                print("Invalid username (3-30, letters/numbers/_).")
                continue
            if self.system.username_exists_everywhere(username):
                print("Username already exists!")
                continue
            break

        # email
        while True:
            email = input("Email: ").strip()
            if email == "0":
                return
            if not Validators.valid_email(email):
                print("Invalid email format!")
                continue
            if self.system.employee_email_exists(email):
                print("This email already exists for another employee!")
                continue
            break

        # password
        while True:
            password = input("Password (8+ with letter+number+@/&): ").strip()
            if password == "0":
                return
            if not Validators.valid_password(password):
                print("Invalid password format!")
                continue
            break

        salt = PasswordHasher.make_salt()
        ph = PasswordHasher.hash_password(password, salt)

        emp = Employee(first, last, username, salt, ph, email)
        self.system.add_employee(emp)
        print("Employee added successfully!")

    def remove_employee(self):
        print("\n--- Remove Employee ---")
        emps = self.system.employees
        if not emps:
            print("No employees.")
            return

        for i, e in enumerate(emps, 1):
            print(f"{i}. {e.first} {e.last} ({e.username})")

        try:
            ch = input("Choose number (0 back): ").strip()
            if ch == "0":
                return
            idx = int(ch) - 1
            if idx < 0 or idx >= len(emps):
                print("Wrong number!")
                return
            removed = emps[idx]
            self.system.remove_employee(removed.username)
            print("Removed!")
        except:
            print("Invalid input!")

    def show_employees(self):
        print("\n--- Employees ---")
        if not self.system.employees:
            print("No employees.")
            return
        for e in self.system.employees:
            print(
                f"Name: {e.first} {e.last} | Username: {e.username} | Email: {e.email}")

    def _ask_nonempty(self, prompt):
        while True:
            val = input(prompt).strip()
            if val == "0":
                return None
            if not val:
                print("Cannot be empty!")
                continue
            return val


class EmployeePanel:
    def __init__(self, system, employee: Employee):
        self.system = system
        self.employee = employee

    def menu(self):
        while True:
            print("\n--- EMPLOYEE PANEL ---")
            print(f"Welcome {self.employee.first} {self.employee.last}")
            print("1. Add Line")
            print("2. Update Line")
            print("3. Delete Line")
            print("4. Show Lines")
            print("5. Add Train (Bonus collision check)")
            print("6. Show Trains")
            print("7. Back")
            ch = input("Choose: ").strip()

            if ch == "1":
                self.add_line()
            elif ch == "2":
                self.update_line()
            elif ch == "3":
                self.delete_line()
            elif ch == "4":
                self.show_lines()
            elif ch == "5":
                self.add_train()
            elif ch == "6":
                self.show_trains()
            elif ch == "7":
                return
            else:
                print("Wrong choice!")

    def add_line(self):
        print("\n--- Add Line --- (0 back)")
        while True:
            name = input("Line name: ").strip().lower()
            if name == "0":
                return
            if not name:
                print("Name cannot be empty!")
                continue
            if name in self.system.lines:
                print("This line name already exists!")
                continue
            if not name.isalpha():
                print("Line name must be alphabets only.")
                continue
            break

        while True:
            origin = input("Origin: ").strip().lower()
            if origin == "0":
                return
            if not origin or not origin.isalpha():
                print("Origin must be alphabets only and not empty.")
                continue
            break

        while True:
            dest = input("Destination: ").strip().lower()
            if dest == "0":
                return
            if not dest or not dest.isalpha():
                print("Destination must be alphabets only and not empty.")
                continue
            if dest == origin:
                print("Origin and destination cannot be same.")
                continue
            break

        # فاصله بین ایستگاه‌ها
        while True:
            dk = input("Distance between stations (km) e.g. 20: ").strip()
            if dk == "0":
                return
            try:
                dk = float(dk)
                if dk <= 0:
                    print("Distance must be positive.")
                    continue
                break
            except:
                print("Invalid number.")

        while True:
            c = input("Number of middle stations: ").strip()
            if c == "0":
                return
            try:
                c = int(c)
                if c < 0:
                    print("Cannot be negative.")
                    continue
                break
            except:
                print("Must be integer.")

        stations = []
        for i in range(c):
            while True:
                st = input(f"Station {i+1}: ").strip().lower()
                if st == "0":
                    return
                if not st or not st.isalpha():
                    print("Station must be alphabets only and not empty.")
                    continue
                if st in stations:
                    print("Duplicate station!")
                    continue
                stations.append(st)
                break

        line = Line(name, origin, dest, stations, dk)
        self.system.lines[name] = line
        print("Line added!")

    def update_line(self):
        print("\n--- Update Line ---")
        if not self.system.lines:
            print("No lines.")
            return

        name = input("Line name (0 back): ").strip().lower()
        if name == "0":
            return
        if name not in self.system.lines:
            print("Line not found.")
            return

        line = self.system.lines[name]
        print("1. Origin")
        print("2. Destination")
        print("3. Stations")
        print("4. Distance(km)")
        opt = input("Choose: ").strip()

        if opt == "1":
            new = input("New origin: ").strip().lower()
            if new and new.isalpha():
                line.origin = new
                print("Updated.")
        elif opt == "2":
            new = input("New destination: ").strip().lower()
            if new and new.isalpha():
                line.destination = new
                print("Updated.")
        elif opt == "3":
            stations = []
            while True:
                st = input("Station (Enter to finish): ").strip().lower()
                if not st:
                    break
                if not st.isalpha():
                    print("Only alphabets.")
                    continue
                if st in stations:
                    print("Duplicate!")
                    continue
                stations.append(st)
            line.stations = stations
            print("Updated.")
        elif opt == "4":
            try:
                dk = float(input("New distance(km): "))
                if dk > 0:
                    line.distance_km = dk
                    print("Updated.")
            except:
                print("Invalid number.")

    def delete_line(self):
        print("\n--- Delete Line ---")
        if not self.system.lines:
            print("No lines.")
            return
        name = input("Line name (0 back): ").strip().lower()
        if name == "0":
            return
        if name not in self.system.lines:
            print("Line not found.")
            return

        del self.system.lines[name]
        self.system.trains = {
            tid: t for tid, t in self.system.trains.items() if t.line_name != name}
        print("Line deleted (and its trains removed).")

    def show_lines(self):
        print("\n--- Lines ---")
        if not self.system.lines:
            print("No lines.")
            return
        for ln, line in self.system.lines.items():
            all_st = [line.origin] + line.stations + [line.destination]
            print(
                f"Name: {ln} | Route: {line.origin}->{line.destination} | DistanceBetween:{line.distance_km}km")
            print("Stations:", ", ".join(all_st))
            print("-" * 30)

    def add_train(self):
        print("\n--- Add Train --- (0 back)")
        if not self.system.lines:
            print("No lines! Add a line first.")
            return

        # line choose
        print("Available lines:", ", ".join(self.system.lines.keys()))
        line_name = input("Line name: ").strip().lower()
        if line_name == "0":
            return
        if line_name not in self.system.lines:
            print("Line not found.")
            return
        line = self.system.lines[line_name]

        name = input("Train name: ").strip()
        if name == "0":
            return
        if not name:
            print("Name cannot be empty.")
            return

        # speed
        try:
            speed = float(input("Speed (km/h): ").strip())
            if speed <= 0:
                print("Speed must be positive.")
                return
        except:
            print("Invalid speed.")
            return

        # stop time
        try:
            stop_min = float(
                input("Stop time at each station (min): ").strip())
            if stop_min < 0:
                print("Stop time cannot be negative.")
                return
        except:
            print("Invalid stop time.")
            return

        # departure time HH:MM
        dep = input("Departure time (HH:MM) e.g. 08:00: ").strip()
        if dep == "0":
            return
        if ScheduleHelper.parse_time_hhmm(dep) is None:
            print("Invalid time format.")
            return

        # quality
        q = input("Quality (A/B/C): ").strip().upper()
        if q not in ["A", "B", "C"]:
            print("Quality must be A/B/C.")
            return

        # price
        try:
            price = float(input("Price: ").strip())
            if price < 0:
                print("Price cannot be negative.")
                return
        except:
            print("Invalid price.")
            return

        # capacity
        try:
            cap = int(input("Capacity: ").strip())
            if cap <= 0:
                print("Capacity must be positive.")
                return
        except:
            print("Invalid capacity.")
            return

        new_train = BaseTrain(name, line_name, speed, stop_min, q, price, cap)

        # ===== Bonus collision check =====
        coll, msg = ScheduleHelper.has_collision(line, new_train)
        if coll:
            print(msg)
            print("Train NOT added due to collision.")
            return

        self.system.trains[new_train.train_id] = new_train
        line.trains.append(new_train)
        print(f"Train added! ID: {new_train.train_id}")

        win = ScheduleHelper.build_station_windows(line, new_train)
        if win:
            print("Schedule:")
            for st, (a, d) in win.items():
                print(
                    f"- {st}: {ScheduleHelper.format_minutes(a)} -> {ScheduleHelper.format_minutes(d)}")

    def update_train_info(self):
        print('You are updating train info.\n')
        while True:
            try:
                train_id = input(
                    "Enter train ID to update or press R to return to Employee Panel.\n").strip().lower()

                if train_id == "r":
                    return

                if not train_id:
                    raise ValueError("Train ID cannot be empty.")

                if not train_id.isdigit():
                    raise TypeError("Train ID must be digits only.")

                if train_id not in self.train_dict:
                    raise ValueError("This train does not exist.")

                break
            except Exception as e:
                print(f"Error: {e}")

        t = self.train_dict[train_id]

        while True:
            try:
                print("Indicate updating item or press R to return to Employee Panel.\n"
                      "Press 1 to update Train name\n"
                      "Press 2 to update Train Line\n"
                      "Press 3 to update Train Mean Speed\n"
                      "Press 4 to update Train Stop Time\n"
                      "Press 5 to update Train Quality\n"
                      "Press 6 to update Train Price\n"
                      "Press 7 to update Train Capacity\n")

                update_num = input().strip().lower()

                if update_num == "r":
                    return

                if update_num not in ["1", "2", "3", "4", "5", "6", "7"]:
                    raise ValueError("No valid input.")

                match update_num:
                    case "1":
                        new_value = input(
                            "Enter new value for train name: ").strip().lower()

                        if not new_value:
                            raise ValueError("New value cannot be empty.")

                        if not new_value.isalpha():
                            raise TypeError(
                                "New value must be alphabets only.")

                        t.update_info("train_name", new_value)
                        print("Train name updated successfully.")

                    case "2":
                        print("Available train lines:",
                              ", ".join(self.Line_dict.keys()))
                        new_value = input(
                            "Enter new value for train line: ").strip().lower()

                        if not new_value:
                            raise ValueError("New value cannot be empty.")

                        if new_value not in self.Line_dict.keys():
                            raise ValueError("This line does not exist.")

                        t.update_info("train_line", new_value)
                        print("Train line updated successfully.")

                    case "3":
                        new_value = float(
                            input("Enter new value for train mean speed: ").strip())

                        if new_value < 0:
                            raise ValueError("New value cannot be negative.")

                        t.update_info("mean_speed", new_value)
                        print("Train mean speed updated successfully.")

                    case "4":
                        new_value = float(
                            input("Enter new value for train stop time: ").strip())

                        if new_value < 0:
                            raise ValueError("New value cannot be negative.")

                        t.update_info("stop_time", new_value)
                        print("Train stop time updated successfully.")

                    case "5":
                        new_value = input(
                            "Enter New value for train quality(A/B/C): ").strip().upper()
                        if not new_value:
                            raise ValueError("New value cannot be empty.")

                        if new_value not in ["A", "B", "C"]:
                            raise TypeError(
                                "New value must be A, B, or C only.")

                        t.update_info("quality", new_value)
                        print("Train quality updated successfully.")

                    case "6":
                        new_value = float(
                            input("Enter new value for train price: ").strip())

                        if new_value < 0:
                            raise ValueError("New value cannot be negative.")

                        t.update_info("price", new_value)
                        print("Train price updated successfully.")

                    case "7":
                        new_value = int(
                            input("Enter new value for train capacity: ").strip())

                        if new_value < 0:
                            raise ValueError("New value cannot be negative.")

                        t.update_info("capacity", new_value)
                        print("Train capacity updated successfully.")

                break
            except Exception as e:
                print(f"Error: {e}")

    def delete_train(self):
        print('You are deleting a train.\n')

        while True:
            try:
                if not self.train_dict:
                    print("There is no train to delete.")
                    return

                train_id = input(
                    "Enter train ID to remove or press R to return to Employee Panel.\n").strip().lower()

                if train_id == "r":
                    return

                if not train_id:
                    raise ValueError("Train ID cannot be empty.")

                if not train_id.isdigit():
                    raise TypeError("Train ID must be digits only.")

                if train_id not in self.train_dict:
                    raise ValueError("Train with this ID does not exist.")

                del self.train_dict[train_id]
                print(f"Train ID {train_id} deleted successfully.")

                break
            except Exception as e:
                print(f"Error: {e}")

    def show_trains(self):
        print("\n--- Trains ---")
        if not self.system.trains:
            print("No trains.")
            return
        for tid, t in self.system.trains.items():
            print(t)


class UserPanel:
    def __init__(self, system, user: Passenger):
        self.system = system
        self.user = user

    def menu(self):
        while True:
            print("\n--- USER PANEL ---")
            print(f"Welcome {self.user.full_name}")
            print("1. Buy Ticket")
            print("2. Wallet")
            print("3. Profile")
            print("4. Recent Transactions (Bonus)")
            print("5. Back")
            ch = input("Choose: ").strip()

            if ch == "1":
                self.buy_ticket()
            elif ch == "2":
                self.wallet_menu()
            elif ch == "3":
                self.profile_menu()
            elif ch == "4":
                self.show_recent_transactions()
            elif ch == "5":
                return
            else:
                print("Wrong choice!")

    def wallet_menu(self):
        while True:
            print("\n--- WALLET ---")
            print(f"Balance: {self.user.wallet.balance}")
            print("1. Charge Wallet")
            print("2. Back")
            ch = input("Choose: ").strip()

            if ch == "1":
                self.charge_wallet()
            elif ch == "2":
                return

    def charge_wallet(self):
        print("\n--- Charge Wallet ---")
        try:
            amount = float(input("Amount: ").strip())
            if amount <= 0:
                print("Amount must be positive.")
                return
        except:
            print("Invalid amount.")
            return

        card = input("Card number (16 digits): ").strip()
        month = input("Exp month (1-12): ").strip()
        year = input("Exp year (1403-1408): ").strip()
        password = input("Password (6 digits): ").strip()
        cvv2 = input("CVV2 (3 digits): ").strip()

        try:
            month_i = int(month)
            year_i = int(year)
        except:
            print("Month/Year must be number.")
            return

        ok, msg = self.user.wallet.add_money(
            card, month_i, year_i, password, cvv2, amount)
        print(msg)

        # ===== Bonus: save transaction to file + time/date =====
        if ok and self.user.wallet.transactions:
            last = self.user.wallet.transactions[-1]
            self.system.storage.append_json_line(
                self.system.storage.transactions_file, last)

    def show_recent_transactions(self):
        print("\n--- Recent Transactions (Last 10) ---")
        all_trans = self.system.storage.read_all_json_lines(
            self.system.storage.transactions_file)
        my = [t for t in all_trans if t.get("username") == self.user.username]
        my_last = my[-10:]
        if not my_last:
            print("No transactions.")
            return
        for t in my_last:
            typ = t.get("type")
            amount = t.get("amount")
            bal = t.get("balance")
            tm = t.get("time")
            print(f"[{tm}] {typ} | amount={amount} | balance={bal}")

    def buy_ticket(self):
        print("\n--- Buy Ticket ---")
        if not self.system.trains:
            print("No trains available.")
            return

        available = [t for t in self.system.trains.values() if t.available > 0]
        if not available:
            print("All trains are full.")
            return

        for i, t in enumerate(available, 1):
            print(
                f"{i}. {t.name} | Line:{t.line_name} | Price:{t.price} | Seats:{t.available}")

        try:
            idx = int(input("Choose train: ").strip()) - 1
            if idx < 0 or idx >= len(available):
                print("Wrong choice.")
                return
            train = available[idx]

            count = int(input("How many tickets: ").strip())
            if count <= 0:
                print("Invalid count.")
                return

            total = train.price * count
            if total > self.user.wallet.balance:
                print("Not enough money.")
                return

            ok, msg = train.book(count)
            if not ok:
                print(msg)
                return

            ok, msg = self.user.wallet.pay(total)
            if not ok:
                print(msg)
                return

            ticket = Ticket(self.user.username, train, count, total)
            print(f"Purchased! Ticket ID: {ticket.ticket_id}")

            self.system.storage.append_json_line(self.system.storage.tickets_file, {
                "ticket_id": ticket.ticket_id,
                "username": ticket.username,
                "train_id": ticket.train_id,
                "train_name": ticket.train_name,
                "count": ticket.count,
                "total": ticket.total,
                "time": ticket.time
            })

            if self.user.wallet.transactions:
                self.system.storage.append_json_line(
                    self.system.storage.transactions_file, self.user.wallet.transactions[-1])

        except:
            print("Invalid input.")

    def profile_menu(self):
        while True:
            print("\n--- PROFILE ---")
            print(f"Username: {self.user.username}")
            print(f"Name: {self.user.full_name}")
            print(f"Email: {self.user.email}")
            print(f"Phone: {self.user.phone}")
            print("1. Change Name")
            print("2. Change Phone")
            print("3. Back")
            ch = input("Choose: ").strip()

            if ch == "1":
                new = input("New full name: ").strip()
                if new:
                    self.user.full_name = new
                    print("Updated (only runtime).")
            elif ch == "2":
                new = input("New phone (09xxxxxxxxx): ").strip()
                if new and Validators.valid_phone(new):
                    self.user.phone = new
                    print("Updated (only runtime).")
                else:
                    print("Invalid phone.")
            elif ch == "3":
                return


# =========================
# Main System
# =========================
class RailwaySystem:
    ADMIN_USERNAME = "Admin_Train"
    ADMIN_PASSWORD = "Pass_Train"

    def __init__(self):
        self.storage = FileStorage()

        self.employees = []  # list[Employee]
        self.users = []      # list[Passenger]
        self.lines = {}      # name -> Line
        self.trains = {}     # id -> Train

        self.admin_panel = AdminPanel(self)

        # load employees & users from file
        self.load_all()

    # ---------- Load/Save ----------
    def load_all(self):
        # employees
        emp_items = self.storage.read_all_json_lines(
            self.storage.employees_file)
        self.employees = []
        for e in emp_items:
            try:
                self.employees.append(Employee(
                    e["first"], e["last"], e["username"], e["salt"], e["password_hash"], e["email"]
                ))
            except:
                pass

        # users
        user_items = self.storage.read_all_json_lines(self.storage.users_file)
        self.users = []
        for u in user_items:
            try:
                p = Passenger(
                    u["username"], u["salt"], u["password_hash"],
                    u["full_name"], u["email"], u.get("phone", "")
                )
                self.users.append(p)
            except:
                pass

    def save_employee_to_file(self, emp: Employee):
        self.storage.append_json_line(self.storage.employees_file, {
            "first": emp.first,
            "last": emp.last,
            "username": emp.username,
            "salt": emp.salt,
            "password_hash": emp.password_hash,
            "email": emp.email
        })

    def save_user_to_file(self, user: Passenger):
        self.storage.append_json_line(self.storage.users_file, {
            "username": user.username,
            "salt": user.salt,
            "password_hash": user.password_hash,
            "full_name": user.full_name,
            "email": user.email,
            "phone": user.phone
        })

    # ---------- Existence checks ----------
    def username_exists_everywhere(self, username):
        if username == self.ADMIN_USERNAME:
            return True
        for e in self.employees:
            if e.username == username:
                return True
        for u in self.users:
            if u.username == username:
                return True
        return False

    def employee_email_exists(self, email):
        for e in self.employees:
            if e.email == email:
                return True
        return False

    def add_employee(self, emp: Employee):
        self.employees.append(emp)
        self.save_employee_to_file(emp)

    def remove_employee(self, username):
        self.employees = [e for e in self.employees if e.username != username]
        items = []
        for e in self.employees:
            items.append({
                "first": e.first, "last": e.last, "username": e.username,
                "salt": e.salt, "password_hash": e.password_hash, "email": e.email
            })
        self.storage.write_all_json_lines(self.storage.employees_file, items)

    # ---------- Menus ----------
    def start(self):
        while True:
            print("\n" + "=" * 50)
            print("RAILWAY TRANSPORT SYSTEM")
            print("=" * 50)
            print("1. Admin Login")
            print("2. Employee Login")
            print("3. User Menu")
            print("4. Exit")
            ch = input("Choose: ").strip()

            if ch == "1":
                self.admin_login()
            elif ch == "2":
                self.employee_login()
            elif ch == "3":
                self.user_menu()
            elif ch == "4":
                print("Goodbye!")
                return
            else:
                print("Wrong choice!")

    def admin_login(self):
        print("\n--- Admin Login --- (0 back)")
        username = input("Username: ").strip()
        if username == "0":
            return
        password = input("Password: ").strip()
        if password == "0":
            return

        if username == self.ADMIN_USERNAME and password == self.ADMIN_PASSWORD:
            print("Welcome Admin!")
            self.admin_panel.menu()
        else:
            print("Wrong username or password!")

    def employee_login(self):
        print("\n--- Employee Login --- (0 back)")
        username = input("Username: ").strip()
        if username == "0":
            return
        password = input("Password: ").strip()
        if password == "0":
            return

        found = None
        for e in self.employees:
            if e.username == username and PasswordHasher.verify(password, e.salt, e.password_hash):
                found = e
                break

        if not found:
            print("Wrong username or password!")
            return

        print(f"Welcome {found.first}!")
        EmployeePanel(self, found).menu()

    def user_menu(self):
        while True:
            print("\n--- USER MENU ---")
            print("1. Register")
            print("2. Login")
            print("3. Back")
            ch = input("Choose: ").strip()

            if ch == "1":
                self.user_register()
            elif ch == "2":
                self.user_login()
            elif ch == "3":
                return
            else:
                print("Wrong choice!")

    def user_register(self):
        print("\n--- Register --- (0 back)")
        full_name = self._ask_nonempty("Full name: ")
        if full_name is None:
            return

        # username
        while True:
            username = input("Username: ").strip()
            if username == "0":
                return
            if not Validators.valid_username(username):
                print("Invalid username (3-30, letters/numbers/_).")
                continue
            if self.username_exists_everywhere(username):
                print("Username already exists!")
                continue
            break

        # email
        while True:
            email = input("Email: ").strip()
            if email == "0":
                return
            if not Validators.valid_email(email):
                print("Invalid email format.")
                continue
            # ایمیل تکراری برای یوزرها
            if any(u.email == email for u in self.users):
                print("Email already registered!")
                continue
            break

        # phone (optional)
        while True:
            phone = input("Phone (optional, 09xxxxxxxxx): ").strip()
            if phone == "0":
                return
            if phone == "":
                break
            if not Validators.valid_phone(phone):
                print("Invalid phone.")
                continue
            break

        # password
        while True:
            password = input("Password (8+ with letter+number+@/&): ").strip()
            if password == "0":
                return
            if not Validators.valid_password(password):
                print("Invalid password format.")
                continue
            break

        salt = PasswordHasher.make_salt()
        ph = PasswordHasher.hash_password(password, salt)

        new_user = Passenger(username, salt, ph, full_name, email, phone)
        self.users.append(new_user)
        self.save_user_to_file(new_user)

        print("Registered successfully!")

    def user_login(self):
        print("\n--- User Login --- (0 back)")
        username = input("Username: ").strip()
        if username == "0":
            return
        password = input("Password: ").strip()
        if password == "0":
            return

        found = None
        for u in self.users:
            if u.username == username and PasswordHasher.verify(password, u.salt, u.password_hash):
                found = u
                break

        if not found:
            print("Wrong username or password!")
            return

        print(f"Welcome {found.full_name}!")
        UserPanel(self, found).menu()

    def _ask_nonempty(self, prompt):
        while True:
            v = input(prompt).strip()
            if v == "0":
                return None
            if not v:
                print("Cannot be empty!")
                continue
            return v


# =========================
# Run
# =========================
if __name__ == "__main__":
    system = RailwaySystem()
    system.start()
