import re
import sys

# =========================
# Base User Class
# =========================
class User:
    """Base class for users"""

    def __init__(self, username, password, first_name, last_name, email):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Admin(User):
    pass


class Employee(User):
    pass


# =========================
# Validation Functions
# =========================

def validate_password(password):
    """
    Password must be:
    - at least 8 characters
    - contain letter
    - contain number
    - contain @ or &
    """
    pattern = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@&]).{8,}$'
    if not re.match(pattern, password):
        raise ValueError(
            "Password must be at least 8 characters and include a letter, number, and @ or & symbol."
        )
    return True


def validate_email(email):
    pattern = r'^[^@]+@[^@]+\.[^@]+$'
    if not re.match(pattern, email):
        raise ValueError("Invalid email format.")
    return True


# =========================
# Employee Management
# =========================

class EmployeeManager:
    def __init__(self):
        self.employees = []

    def add_employee(self):
        try:
            print("\n--- Add New Employee ---")

            username = input("Username: ").strip()
            if not username:
                raise ValueError("Username cannot be empty.")

            password = input("Password: ").strip()
            validate_password(password)

            first = input("First name: ").strip()
            last = input("Last name: ").strip()
            email = input("Email: ").strip()
            validate_email(email)

            emp = Employee(username, password, first, last, email)
            self.employees.append(emp)

            print("✅ Employee added successfully.\n")

        except ValueError as e:
            print(f"❌ Error: {e}")

        except Exception as e:
            print(f"❌ Unexpected error: {e}")

    def delete_employee(self):
        try:
            if not self.employees:
                print("No employees registered.")
                return

            username = input("Enter username to delete: ").strip()

            for emp in self.employees:
                if emp.username == username:
                    self.employees.remove(emp)
                    print("✅ Employee removed.")
                    return

            print("❌ Employee not found.")

        except Exception as e:
            print(f"❌ Unexpected error: {e}")

    def list_employees(self):
        if not self.employees:
            print("No employees registered.\n")
            return

        print("\n--- Employee List ---")
        for i, emp in enumerate(self.employees, 1):
            print(f"{i}. {emp.get_full_name()} | {emp.email}")
        print()


# =========================
# Menu System
# =========================

def admin_panel(manager):
    while True:
        try:
            print("\n==== Admin Panel ====")
            print("1. Add Employee")
            print("2. Delete Employee")
            print("3. List Employees")
            print("4. Exit")

            choice = input("Select: ").strip()

            if choice == "1":
                manager.add_employee()

            elif choice == "2":
                manager.delete_employee()

            elif choice == "3":
                manager.list_employees()

            elif choice == "4":
                print("Exiting admin panel...")
                break

            else:
                print("❌ Invalid choice. Try again.")

        except KeyboardInterrupt:
            print("\nInterrupted safely.")
            break

        except Exception as e:
            print(f"❌ Unexpected error: {e}")


# =========================
# Main Application
# =========================

def main():
    manager = EmployeeManager()

    while True:
        try:
            print("\n===== Rail Transport System =====")
            print("1. Admin Login")
            print("2. Exit")

            choice = input("Select: ").strip()

            if choice == "1":
                print("Login successful.")
                admin_panel(manager)

            elif choice == "2":
                print("Goodbye!")
                sys.exit()

            else:
                print("❌ Invalid option.")

        except KeyboardInterrupt:
            print("\nProgram safely terminated.")
            sys.exit()

        except Exception as e:
            print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
