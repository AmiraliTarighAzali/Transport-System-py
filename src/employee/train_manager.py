from dataclasses import dataclass

@dataclass
class Staff:
    username: str
    password: str


class EmployeePanel:
    def __init__(self, staff):
        self.staff = staff
        self.train_dict = {}

    def menu(self):
        while True:
            print(
                "Here is train's staff panel. Please choose an action:\n"
                "1. Add Line\n"
                "2. Update Line Info\n"
                "3. Delete Line\n"
                "4. Show Lines\n"
                "5. Add Train\n"
                "6. Update Train Info\n"
                "7. Delete Train\n"
                "8. Show Trains\n"
                "9. Logout"
            )

            request_num = input()
            match request_num:
                case "1":
                    pass
                case "2":
                    pass
                case "3":
                    pass
                case "4":
                    pass
                case "5":
                    self.add_train()
                case "6":
                    self.update_train_info()
                case "7":
                    self.delete_train()
                case "8":
                    self.show_trains()
                case "9":
                    break
                case _:
                    print("No valid input")
            
            
    
    def add_train(self):
        while True:
            print("Enter Train ID Or press r to return to Employee Panel")
            train_id= input()

            if train_id=="":
                print("This can not be Empty")
                continue

            if train_id =="r":
                return
    
            if train_id in self.train_dict:
                print("This Train Already Exist!")
                continue


            train_name = input("Insert Train Name: ")
            train_line = input("Insert Train Line: ")
            mean_speed = input("Insert Train Mean Speed: ")
            stop_time = input("Insert Train Stop Time: ")
            quality = input("Insert Train Quality: ")
            price = input("Insert Train Price: ")
            capacity = input("Insert Train Capacity: ")

            if not all([train_name, train_line, mean_speed, stop_time, quality, price, capacity]):
                print("Fields cannot be empty")
                continue

            self.train_dict[train_id]=Train(train_name,train_line,mean_speed,stop_time,quality,price,capacity)
            print("Train added")
            #return if want to go menu,nothing for getting another train

    
    def update_train_info(self):
        while True:
            print("Enter Train ID to update Or press r to return to Employee Panel")
            train_id= input()

            if train_id=="":
                print("This can not be Empty")
                continue

            if train_id =="r":
                return
    
            if train_id not in self.train_dict:
                print("No Train with this ID")
                continue
            
            t = self.train_dict[train_id]
            while True:
                print("Indicate updating item or press r to return to Employee Panel" \
                "Press 1 to update Train name" \
                "Press 2 to update Train Line" \
                "Press 3 to update Train Mean Speed" \
                "Press 4 to update Train Stop Time" \
                "Press 5 to update Train Quality" \
                "Press 6 to update Train Price" \
                "Press 7 to update Train Capacity")   
                update_num = input()
                if update_num == "r":
                    return
                match update_num:
                    case "1":
                        new_value=input("Enter New value for Train name")
                        t.update_info("train_name",new_value)
                        
                    case "2":
                        new_value=input("Enter New value for Train Line")
                        t.update_info("train_line",new_value)

                    case "3":
                        new_value=input("Enter New value for Train Mean Speed")
                        t.update_info("mean_speed",new_value)

                    case "4":
                        new_value=input("Enter New value for Train Stop Time")
                        t.update_info("stop_time",new_value)

                    case "5":
                        new_value=input("Enter New value for Train Quality")
                        t.update_info("quality",new_value)

                    case "6":
                        new_value=input("Enter New value for Train Price")
                        t.update_info("price",new_value)

                    case "7":
                        new_value=input("Enter New value for Train Capacity")
                        t.update_info("capacity",new_value)

                    case _:
                        print("No valid input")

    def delete_train(self):
        while True:
            print("Enter Train ID to remove Or press r to return to Employee Panel")
            train_id= input()

            if train_id=="":
                print("This can not be Empty")
                continue

            if train_id =="r":
                return
    
            if train_id not in self.train_dict:
                print("Train with this ID doesn't Exist!")
                continue
            del self.train_dict[train_id]
            print(f"Train ID:{train_id} is removed")


    def show_trains(self):
        while True:
            if not self.train_dict:
                print("No trains available.")
                #what to do now?

            for train in self.train_dict.values():
                print(train)
                # check this!

            inp=input("Press r to return to Employee Panel")
            if inp =="r":
                return

 
        





       
class Train():
    def __init__(self,train_name,train_line,mean_speed,stop_time,quality,price,capacity):
        self.train_name=train_name
        self.train_line=train_line
        self.mean_speed=mean_speed
        self.stop_time=stop_time
        self.quality=quality
        self.price=price
        self.capacity=capacity

    '''def update_info(self,update_case,new_value):
        if update_case =="train_name":
            self.train_name=new_value
            return

        if update_case =="train_line":
            self.train_line=new_value
            return

        if update_case =="mean_speed":
            self.mean_speed=new_value
            return
        
        if update_case =="stop_time":
            self.stop_time=new_value
            return
        
        if update_case =="quality":
            self.quality=new_value
            return
        
        if update_case =="price":
            self.price=new_value
            return

        if update_case =="capacity":
            self.capacity=new_value
            return'''
    
    def update_info(self, update_case, new_value):
        setattr(self, update_case, new_value)


    def __str__(self):
            return f"Train Name: {self.train_name}, Train Line: {self.train_line}, Train Mean Speed: {self.mean_speed},Train Stop Time: {self.stop_time},Train Quality: {self.quality},Train Price: {self.price},Train Capacity: {self.capacity}"





 



   
    
