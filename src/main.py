
class User:
    """کلاس پایه برای کاربران"""

    def __init__(self, username, password, first_name, last_name, email):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Admin(User):
    def __init__(self):
        super().__init__("Admin_Train", "Pass_Train", "Admin", "User", "admin@train.com")

    def show_menu(self):
        """نمایش منوی ادمین"""
        print("\n" + "="*50)
        print("پنل مدیریت".center(50))
        print("="*50)
        print("1. اضافه کردن کارمند جدید")
        print("2. حذف کارمند")
        print("3. مشاهده لیست کارمندان")
        print("4. خروج از پنل مدیریت")
        print("-"*50)


class Employee(User):
    """کلاس کارمندان قطار"""

    def __init__(self, username, password, first_name, last_name, email):
        super().__init__(username, password, first_name, last_name, email)


class EmployeeManager:
    def __init__(self):
        self.employees = []

    def email_exists(self, email):
        """بررسی تکراری بودن ایمیل"""
        for emp in self.employees:
            if emp.email == email:
                return True
        return False

    def username_exists(self, username):
        """بررسی تکراری بودن نام کاربری"""
        for emp in self.employees:
            if emp.username == username:
                return True
        return False

    def validate_password(self, password):
        """بررسی رمز عبور - باید شامل حرف، عدد و @ یا & باشه"""
        has_letter = False
        has_number = False
        has_special = False

        for char in password:
            if char.isalpha():
                has_letter = True
            elif char.isdigit():
                has_number = True
            elif char == '@' or char == '&':
                has_special = True

        if has_letter and has_number and has_special:
            return True
        return False

    def validate_email(self, email):
        """بررسی ایمیل - باید @ و نقطه داشته باشه"""
        if '@' not in email:
            return False

        at_index = 0
        for i in range(len(email)):
            if email[i] == '@':
                at_index = i
                break

        # بعد از @ باید یه نقطه باشه
        has_dot_after_at = False
        for i in range(at_index + 1, len(email)):
            if email[i] == '.':
                has_dot_after_at = True
                break

        return has_dot_after_at

    def add_employee(self):
        """اضافه کردن کارمند جدید"""
        print("\n" + "-"*40)
        print("فرم ثبت کارمند جدید")
        print("-"*40)

        while True:
            first_name = input("نام: ").strip()
            if first_name == "0":
                return

            last_name = input("نام خانوادگی: ").strip()
            email = input("ایمیل: ").strip()

            # اعتبارسنجی ایمیل
            if not self.validate_email(email):
                print("ایمیل نامعتبر است! ایمیل باید دارای @ و نقطه باشد.")
                again = input("ادامه؟ (1 برای ادامه، 0 برای بازگشت): ")
                if again == "0":
                    return
                continue

            # بررسی تکراری نبودن ایمیل
            if self.email_exists(email):
                print("این ایمیل قبلاً ثبت شده است!")
                again = input("ادامه؟ (1 برای ادامه، 0 برای بازگشت): ")
                if again == "0":
                    return
                continue

            username = input("نام کاربری: ").strip()

            # بررسی تکراری نبودن نام کاربری
            if self.username_exists(username):
                print("این نام کاربری قبلاً ثبت شده است!")
                again = input("ادامه؟ (1 برای ادامه، 0 برای بازگشت): ")
                if again == "0":
                    return
                continue

            password = input("رمز عبور: ").strip()

            # اعتبارسنجی رمز عبور
            if not self.validate_password(password):
                print("رمز عبور باید شامل حرف، عدد و @ یا & باشد!")
                again = input("ادامه؟ (1 برای ادامه، 0 برای بازگشت): ")
                if again == "0":
                    return
                continue

            # ساخت کارمند جدید
            new_employee = Employee(
                username, password, first_name, last_name, email)
            self.employees.append(new_employee)
            print("کارمند با موفقیت اضافه شد!")

            choice = input("1 برای ثبت کارمند دیگر، 0 برای بازگشت: ")
            if choice == "0":
                return

    def remove_employee(self):
        """حذف کارمند با نام کاربری"""
        print("\n" + "-"*40)
        print("حذف کارمند")
        print("-"*40)

        if len(self.employees) == 0:
            print("هیچ کارمندی برای حذف وجود ندارد!")
            input("Enter بزنید تا برگردید...")
            return

        while True:
            username = input(
                "نام کاربری کارمند مورد نظر (0 برای بازگشت): ").strip()

            if username == "0":
                return

            # پیدا کردن کارمند
            found_index = -1
            for i in range(len(self.employees)):
                if self.employees[i].username == username:
                    found_index = i
                    break

            if found_index == -1:
                print("این نام کاربری یافت نشد!")
                continue

            # نمایش اطلاعات کارمند
            emp = self.employees[found_index]
            print(f"\nکارمند پیدا شد: {emp.get_full_name()} - {emp.email}")
            confirm = input("آیا مطمئن هستید؟ (y/n): ").lower()

            if confirm == 'y':
                del self.employees[found_index]
                print(" کارمند با موفقیت حذف شد!")
                return
            else:
                print("عملیات لغو شد.")
                return

    def show_employees(self):
        """نمایش لیست کارمندان"""
        print("\n" + "="*50)
        print("لیست کارمندان".center(50))
        print("="*50)

        if len(self.employees) == 0:
            print("هیچ کارمندی ثبت نشده است.")
        else:
            for i, emp in enumerate(self.employees, 1):
                print(f"\n{i}. {emp.get_full_name()}")
                print(f"   نام کاربری: {emp.username}")
                print(f"   ایمیل: {emp.email}")
                print("   " + "-"*30)

        input("\nEnter بزنید تا برگردید...")


class LoginSystem:
    """سیستم ورود به پنل‌ها"""

    @staticmethod
    def admin_login():
        """ورود ادمین با اطلاعات ثابت"""
        print("\n" + "="*40)
        print("ورود ادمین".center(40))
        print("="*40)

        max_attempts = 3
        attempts = 0

        while attempts < max_attempts:
            username = input("نام کاربری: ").strip()
            password = input("رمز عبور: ").strip()

            if username == "Admin_Train" and password == "Pass_Train":
                print("ورود موفق! خوش آمدید.")
                return True
            else:
                attempts += 1
                remaining = max_attempts - attempts
                print(
                    f" نام کاربری یا رمز عبور اشتباه است! {remaining} تلاش دیگر باقی است.")

                if attempts < max_attempts:
                    go_back = input(
                        "0 برای بازگشت به منوی اصلی، Enter برای ادامه: ")
                    if go_back == "0":
                        return False

        print("تعداد تلاش‌های مجاز تمام شد!")
        return False


class MainMenu:
    """منوی اصلی برنامه"""

    def __init__(self):
        self.admin = Admin()
        self.employee_manager = EmployeeManager()
        self.login_system = LoginSystem()

    def show_start_menu(self):
        """نمایش منوی شروع"""
        print("\n" + "="*60)
        print(" سیستم مدیریت حمل و نقل ریلی".center(60))
        print("="*60)
        print("1. ورود ادمین کل")
        print("2. ورود کارمند قطار")
        print("3. ورود کاربر عادی")
        print("4. خروج")
        print("-"*60)

    def run(self):
        """اجرای اصلی برنامه"""
        while True:
            self.show_start_menu()
            choice = input("انتخاب شما: ").strip()

            if choice == "1":
                # پنل ادمین
                if self.login_system.admin_login():
                    self.admin_panel()

            elif choice == "2":
                print("\n این بخش در حال پیاده‌سازی است...")
                input("Enter بزنید تا برگردید...")

            elif choice == "3":
                print("\n این بخش در حال پیاده‌سازی است...")
                input("Enter بزنید تا برگردید...")

            elif choice == "4":
                print("\n خداحافظ!")
                break

            else:
                print(" انتخاب نامعتبر!")

    def admin_panel(self):
        """پنل مدیریت ادمین"""
        while True:
            self.admin.show_menu()
            choice = input("انتخاب شما: ").strip()

            if choice == "1":
                self.employee_manager.add_employee()

            elif choice == "2":
                self.employee_manager.remove_employee()

            elif choice == "3":
                self.employee_manager.show_employees()

            elif choice == "4":
                print("خروج از پنل مدیریت...")
                break

            else:
                print(" انتخاب نامعتبر!")


if __name__ == "__main__":
    app = MainMenu()
    app.run()
