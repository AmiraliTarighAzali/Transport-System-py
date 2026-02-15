"""
Railway Transport Management System - Admin Module
This module implements the admin panel functionality as per project requirements.
"""

import re

# Predefined admin credentials
ADMIN_USERNAME = "Admin_Train"
ADMIN_PASSWORD = "Pass_Train"

# In-memory storage for employees (list of dictionaries)
employees = []


def validate_password(password):
    """Check if password contains letters, numbers, and @ or &."""
    if not any(c.isalpha() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    if not any(c in '@&' for c in password):
        return False
    return True


def validate_email(email):
    """Simple email validation: must contain @ and a dot after @."""
    if '@' not in email:
        return False
    local, domain = email.split('@', 1)
    if '.' not in domain:
        return False
    return True


def admin_login():
    """Handle admin login with predefined credentials."""
    print("\n--- Admin Login ---")
    attempts = 0
    while True:
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            print("Login successful! Welcome Admin.")
            return True
        else:
            print("Invalid username or password. Please try again.")
            attempts += 1
            # Option to go back to start panel
            choice = input(
                "Enter 0 to return to start menu, or any other key to try again: ").strip()
            if choice == '0':
                return False


def add_employee():
    """Add a new employee with validation."""
    print("\n--- Add Employee ---")
    while True:
        # Get employee details
        first_name = input("First name (or 0 to go back): ").strip()
        if first_name == '0':
            return
        last_name = input("Last name: ").strip()
        email = input("Email: ").strip()
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        # Validate email
        if not validate_email(email):
            print("Invalid email format. Must contain '@' and a domain with dot.")
            continue

        # Validate password
        if not validate_password(password):
            print(
                "Password must contain letters, numbers, and at least one of '@' or '&'.")
            continue

        # Check uniqueness of username and email
        username_exists = any(emp['username'] == username for emp in employees)
        email_exists = any(emp['email'] == email for emp in employees)
        if username_exists:
            print("Username already exists. Please choose a different one.")
            continue
        if email_exists:
            print("Email already registered. Please use a different email.")
            continue

        # All validations passed, add employee
        employees.append({
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'username': username,
            'password': password
        })
        print("Employee added successfully!")
        # Ask if user wants to add another or go back
        choice = input(
            "Enter 1 to add another employee, or 0 to go back: ").strip()
        if choice == '0':
            return
        # else continue loop


def remove_employee():
    """Remove an employee by username."""
    print("\n--- Remove Employee ---")
    while True:
        if not employees:
            print("No employees to remove.")
            return
        username = input(
            "Enter username of employee to remove (or 0 to go back): ").strip()
        if username == '0':
            return
        # Find employee
        for i, emp in enumerate(employees):
            if emp['username'] == username:
                print(
                    f"Employee found: {emp['first_name']} {emp['last_name']} ({emp['username']})")
                confirm = input(
                    "Are you sure you want to remove? (y/n): ").strip().lower()
                if confirm == 'y':
                    del employees[i]
                    print("Employee removed.")
                else:
                    print("Removal cancelled.")
                break
        else:
            print("Username not found. Please try again.")
            # Option to retry or go back is handled by loop


def list_employees():
    """Display all employees."""
    print("\n--- Employee List ---")
    if not employees:
        print("No employees found.")
    else:
        for emp in employees:
            print(f"Username: {emp['username']}")
            print(f"Name: {emp['first_name']} {emp['last_name']}")
            print(f"Email: {emp['email']}")
            print("-" * 20)
    input("Press Enter to go back to admin menu.")


def admin_panel():
    """Main admin menu."""
    while True:
        print("\n--- Admin Panel ---")
        print("1. Add employee")
        print("2. Remove employee")
        print("3. View employees")
        print("4. Logout (back to start menu)")
        choice = input("Choose an option: ").strip()

        if choice == '1':
            add_employee()
        elif choice == '2':
            remove_employee()
        elif choice == '3':
            list_employees()
        elif choice == '4':
            print("Logging out...")
            return
        else:
            print("Invalid option. Please try again.")


def start_panel():
    """Main start menu."""
    while True:
        print("\n=== Railway Transport Management System ===")
        print("1. Admin")
        print("2. Train Staff")
        print("3. Regular User")
        print("4. Exit")
        choice = input("Select your role: ").strip()

        if choice == '1':
            if admin_login():
                admin_panel()
        elif choice == '2':
            print("Staff panel not implemented yet.")
            # Placeholder for future
        elif choice == '3':
            print("User panel not implemented yet.")
            # Placeholder for future
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-4.")


if __name__ == "__main__":
    start_panel()
