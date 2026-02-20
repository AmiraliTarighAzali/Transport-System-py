from utils.validators import Validators
from utils.password_hasher import PasswordHasher
from models.employee import Employee


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
