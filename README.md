#  Transport System Project

QBC11 Bootcamp Project 1

# Railway Transport Management System

A terminal-based railway transport management system developed in Python. This system allows different user roles (Admin, Employee, Passenger) to manage railway operations.

## Features

### User Roles
- **Admin**: Manage employees (add, remove, view)
- **Employee**: Manage railway lines and trains with collision detection
- **Passenger**: Register, login, buy tickets, manage wallet

### Core Functionalities
- **Admin Panel**
  - Add new employees with validation
  - Remove existing employees
  - View all employees

- **Employee Panel**
  - Add/Update/Delete railway lines
  - Add trains with collision detection (Bonus)
  - Update train information
  - View all lines and trains

- **Passenger Panel**
  - Register with validation (username, email, phone, password)
  - Login with password hashing
  - Buy tickets from available trains
  - Wallet system with recharge capability
  - View recent transactions (Bonus)
  - Update profile information

### Security Features
- Password hashing with salt (SHA256)
- Secure file-based storage
- Input validation for all fields

###  Data Storage
- JSON format files
- Separate files for users, employees, transactions, and tickets
- Persistent storage across sessions

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/railway-transport-system.git
cd railway-transport-system
