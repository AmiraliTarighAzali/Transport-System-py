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

            if request_num not in ["1","2","3","4","5","6","7","8","9"]:
                raise ValueError("No valid input.")
            
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

            
        
    def add_train(self):
        while True:

            #Train ID should be digits
            train_id = input("Enter train ID (Digits) Or press R to return to Employee Panel.").strip()

            if train_id.lower() == "r":
                return
            
            if not train_id:
                raise ValueError("Train ID cannot be empty.")

            if not train_id.isdigit():
                raise TypeError("Train ID must be digits only.")
            
            if train_id in self.train_dict:
                raise ValueError("This train already exists.")
            
            

            train_name = input("Insert train name: ").strip().lower()
    
            if not train_name:
                raise ValueError("Train name cannot be empty.")
            
            if not train_name.isalpha():
                raise TypeError("Train name must be alphabets only.")



            train_line = input("Insert train line: ").strip()

            if not train_line:
                raise ValueError("Train line cannot be empty.")
            
            #Train line should be digits
            if not train_line.isdigit():
                raise TypeError("Train line must be digits only.")
            
            
        
            #what is the condition for mean speed???
            mean_speed = input("Insert mean_speed: ").strip()

            if not mean_speed:
                raise ValueError("Mean speed cannot be empty.")
            
            if not isinstance(mean_speed, float):
                raise TypeError("Mean speed must be float.")
            


            #what is the condition for mean speed???
            stop_time = input("Insert stop time: ").strip()

            if not stop_time:
                raise ValueError("Stop time cannot be empty.")
            
            if not isinstance(stop_time, float):
                raise TypeError("Stop time must be float.")



            quality = input("Insert train quality (A/B/C): ").strip().upper()

            if not quality:
                raise ValueError("Quality cannot be empty.")

            if quality not in ["A", "B", "C"]:
                raise TypeError("Train quality must be A, B, or C only.")
      


            #what is the condition for mean speed???
            price = input("Insert train price: ").strip()

            if not price:
                raise ValueError("Price cannot be empty.")
           
            if not isinstance(price, float):
                raise TypeError("Price must be float.")



            capacity = input("Insert train capacity: ").strip()

            if not capacity:
                raise ValueError("Capacity cannot be empty.")
           
            if not isinstance(capacity, int):
                raise TypeError("Capacity must be integer.")


            self.train_dict[train_id] = Train(train_name,train_line,mean_speed,stop_time,quality,price,capacity)
            print("Train added")
            #return if want to go menu,nothing for getting another train

    
    def update_train_info(self):
        while True:

            train_id = input("Enter train ID (Digits) to update Or press R to return to Employee Panel.").strip()

            if train_id.lower() == "r":
                return
            
            if not train_id:
                raise ValueError("Train ID cannot be empty.")

            if not train_id.isdigit():
                raise TypeError("Train ID must be digits only.")
            
            if train_id not in self.train_dict:
                raise ValueError("This train does not exist.")


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

                update_num = input().strip()

                if update_num == "r":
                    return

                if update_num not in ["1","2","3","4","5","6","7"]:
                    raise ValueError("No valid input.")

                match update_num:
                    case "1":
                        new_value = input("Enter New value for Train name").strip().lower()

                        if not new_value:
                            raise ValueError("New value cannot be empty.")
                
                        if not new_value.isalpha():
                            raise TypeError("New value must be alphabets only.")

                        t.update_info("train_name",new_value)
                        

                    case "2":
                        new_value = input("Enter New value for Train Line").strip()

                        if not new_value:
                            raise ValueError("New value cannot be empty.")
            
                        if not new_value.isdigit():
                            raise TypeError("New value must be digits only.")

                        t.update_info("train_line",new_value)

                    case "3":
                        new_value = input("Enter New value for Train Mean Speed").strip()

                        if not new_value:
                            raise ValueError("New value cannot be empty.")
            
                        if not isinstance(new_value, float):
                            raise TypeError("New value must be float.")
                        
                        t.update_info("mean_speed",new_value)

                    case "4":
                        new_value = input("Enter New value for Train Stop Time").strip()

                        if not new_value:
                            raise ValueError("New value cannot be empty.")
                        
                        if not isinstance(new_value, float):
                            raise TypeError("New value must be float.")

                        t.update_info("stop_time",new_value)

                    case "5":
                        new_value = input("Enter New value for Train Quality").strip()
                        if not new_value:
                            raise ValueError("New value cannot be empty.")

                        if new_value not in ["A", "B", "C"]:
                            raise TypeError("New value must be A, B, or C only.")

                        t.update_info("quality",new_value)

                    case "6":
                        new_value = input("Enter New value for Train Price").strip()
                        
                        if not new_value:
                            raise ValueError("New value cannot be empty.")
                    
                        if not isinstance(new_value, float):
                            raise TypeError("New value must be float.")
                        
                        t.update_info("price",new_value)

                    case "7":
                        new_value = input("Enter New value for Train Capacity").strip()

                        if not new_value:
                            raise ValueError("New value cannot be empty.")
                    
                        if not isinstance(new_value, int):
                            raise TypeError("New value must be integer.")
                        
                        t.update_info("capacity",new_value)



    def delete_train(self):
        while True:

            train_id = input("Enter train ID to remove Or press R to return to Employee Panel").strip().lower()

            if train_id.lower() == "r":
                return
            
            if not train_id:
                raise ValueError("Train ID cannot be empty.")

            if not train_id.isdigit():
                raise TypeError("Train ID must be digits only.")
            
            if train_id not in self.train_dict:
                raise ValueError("Train with this ID does not exist.")
            
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



       
class Train():
    def __init__(self,train_name,train_line,mean_speed,stop_time,quality,price,capacity):
        self.train_name=train_name
        self.train_line=train_line
        self.mean_speed=mean_speed
        self.stop_time=stop_time
        self.quality=quality
        self.price=price
        self.capacity=capacity

    
    def update_info(self, update_case, new_value):
        setattr(self, update_case, new_value)


    def __str__(self):
            return f"Train Name: {self.train_name}, Train Line: {self.train_line}, Train Mean Speed: {self.mean_speed},Train Stop Time: {self.stop_time},Train Quality: {self.quality},Train Price: {self.price},Train Capacity: {self.capacity}"


