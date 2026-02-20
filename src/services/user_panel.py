import datetime
from models.ticket import Ticket
from utils.validators import Validators


class UserPanel:
    def __init__(self, system, user):
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
