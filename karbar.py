def display_user_panel():
    
    register = User_Register()
    login = User_Login()
    
    while True:
        print("1. Register\n2. Sign in\n3. Back")
        choice = input("Choose the option: ")
            
        if choice == "1":
            register.registration()
            
        elif choice == "2":
            login.login()

        elif choice == "3":
            star.namefirst

        else:
            raise "Please try again!"
            continue
        

class User_Register(User):             #This class have methods for regular user's registration
    
    def __init__(self, username="username", password=123, name="name", email="email"):
        super().__init__(username, password)
        self.name = name
        self.email = email

    def registration(self):             #This method defines regular user's registration
            
        while True:
            name = input("Enter name : ")
            email = input("Enter email : ")
            username = input("Enter username : ")
            password = input("Enter password : ")
            
            list_values = list(user_dict.values())
            
            if any(user["username"] == username for user in list_values):
                print("The username is already exist! Please try again!\n")
                continue
            
            if any(user["email"] == email for user in list_values):
                print("The email is already exist! Please try again!\n")
                continue
            
            if name == "" or username == "" or password == "" or email == "":
                print("Value of fields can not be empty !\n")
                continue

            if "@" not in email:
                print("The email is not valid ! Please try again !\n")
                continue
            
            new_user = {"name":name, "email":email, "username": username, "password": password}
            user_dict[username]= new_user
            print("You registered successfully! Now you can logging in ...\n") 
            display.display_user_panel()


class User_Login(User):
    
    def __init__(self, username="username", password=123):
        super().__init__(username, password)
        self.shopping = Shopping_Panel()

    def login(self):
        
        while True:
            choice = input("Do you want to back to the Main Panel or continue to login Panel (yes/no) ? : ").strip().lower()
        
            if choice == "yes":
                start.namefirst 
        
            else:
                username = input("Enter username : ")
                password = input("Enter password : ")

                if len(user_dict) == 0:
                    print("There is no users! Please complete the registration first!\n")
                    display.display_user_panel()
                
                if any(username == user["username"] and password == user["password"] for user in user_dict.values()):
                    print(f"You logged in successfully!\nWelcome {username} .\n")
                    self.shopping.display_shopping_panel()
                    break  
                
                else:
                    print("Username or Password is incorrect. Please try again!\n")  
                    continue
                    

