# =========================
# Main System
# =========================

from utils.file_storage import FileStorage
from utils.validators import Validators
from utils.password_hasher import PasswordHasher
from models.passenger import Passenger
from models.employee import Employee
from services.admin_panel import AdminPanel
from services.employee_panel import EmployeePanel
from services.user_panel import UserPanel


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
