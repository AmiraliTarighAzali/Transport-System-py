from dataclasses import dataclass

@dataclass
class Staff:
    username: str
    password: str

Line_dict = {}

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
                    self.addLine()
                case "2":
                    self.UpdateLine()
                case "3":
                    self.Remove_Line()
                case "4":
                    self.ShowLines()
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



    def check_choice(self):

        choice = input("Do you want to continiue? yes/no").strip().lower()
        if choice == "no":
            self.ShowMenuTrain()
            return
        elif choice == "yes":
            return
        else:
            print("Wrong choice. please try again.")
            self.check_choice()


    def addLine(self):

        print('You are adding a new line.')
        self.check_choice()

        while True:
            name = input('Enter the Name of lines:').strip().lower()
            if name in Line_dict:
                print("This name is exists.")
                continue
            if not name:
                raise ValueError('The name can not be empty')
            
            origin = input('Origin name: ').strip().lower()
            if not origin:
                raise ValueError('The origin can not be empty')

            destination = input('Destination name: ').strip().lower()
            if not destination:
                raise ValueError('The Destination can not be empty')
            
            if origin == destination:
                print("origin and destination can not be same.")

            countsStation = input('Number of Stations: ')
            if not countsStation:
                raise ValueError('Number of Stations can not be empty')
            if not str(countsStation).isdigit():
                raise TypeError('Number of Stations is not digit')
            
            stations = []
            countsStation = int(countsStation)
            for i in range(countsStation):
                temp_station = input(f'Enter Station {i}: ')
                if not temp_station:
                    raise ValueError('Name station can not be empty')
                if temp_station in stations:
                    print('This station name is exists. please enter another station name')
                    i -= 1
                else:
                    stations.append(temp_station) 

            newLineInfo = {"name_line":name,"origin": origin,"destination":destination,"countsStation":countsStation,
                         "stations":stations}
            Line_dict[name] = newLineInfo
            print(f'Line of {name} added successfully.')
            choice = input("Do you want to continiue? yes/no").strip().lower()
            if choice != "yes":
                break

        self.ShowMenuTrain()



    def UpdateLine(self):
        print('You are updating a line.')
        self.check_choice()

        while True:
            name = input("Enter the name of line for update: ").strip().lower()
            selectedLine = None
            for l in Line_dict:
                if l["name_line"] == name:
                    selectedLine = l
                    break

            if selectedLine is None:
                print("This line is not exists")
                continue

            print("1. Name_line")
            print("2. Origin")
            print("3. Destination")
            print("4. Count_Statation")
            print("5. Stations")
            choice = input("select attribiute for update.").strip().lower()

            if choice == "1":
                new_name = input("Enter new name: ").strip().lower()
                if new_name in Line_dict:
                    print("This name is exists.")
                    continue
                if new_name == name:
                    print("The new name is same of old name")
                    continue
                if not new_name:
                    raise ValueError('The name can not be empty')
                selectedLine["name_line"] = new_name
                Line_dict.pop(name)
                Line_dict[new_name] = selectedLine
                print("The name of line was updated successfully.")
            elif choice == "2":
                new_origin = input("Enter the new origin: ").strip().lower()
                if new_origin == selectedLine["origin"]:
                    print("The new origin is same of old origin")
                    continue
                if not new_origin:
                    raise ValueError('The origin can not be empty')
                selectedLine["origin"] = new_origin
                Line_dict.pop(name)
                Line_dict[new_name]=selectedLine
                print("The origin of line was updated successfully.")
            elif choice == "3":
                new_destination = input("Enter the new destination: ").strip().lower()
                if new_destination == selectedLine["destination"]:
                    print("The new destination is same of old destination")
                    continue
                if not new_destination:
                    raise ValueError('The destination can not be empty')
                selectedLine["destination"] = new_destination
                Line_dict.pop(name)
                Line_dict[new_name] = selectedLine
                print("The destination of line was updated successfully.")
            elif choice == "4":
                new_count_state=input("Enter the new counts of stations: ").strip().lower()
                if new_count_state == selectedLine["countsStation"]:
                    print("The new countsStation is same of old countsStation")
                    continue
                if not new_count_state:
                    raise ValueError('The countsStation can not be empty')
                if not str(new_count_state).isdigit():
                    raise TypeError('Number of Stations is not digit')
                if not new_count_state == "0":
                    raise ValueError('Number of Stations can not be zero')
                selectedLine["countsStation"] = new_count_state

                new_stations = []

                for i in range(new_count_state):
                    temp_station = input(f'Enter Station {i}: ')
                    if not temp_station:
                        raise ValueError('Name station can not be empty')
                    if temp_station in new_stations:
                        print('This station name is exists. please enter another station name')
                        i -= 1
                    else:
                        new_stations.append(temp_station) 

                selectedLine["stations"] = new_stations

                Line_dict.pop(name)
                Line_dict[new_name] = selectedLine
                print("The count stations of line was updated successfully.")
            elif choice == "5":
                new_stations = []
                count_state=int(selectedLine["countsStation"])

                for i in range(count_state):
                    temp_station = input(f'Enter Station {i}: ')
                    if not temp_station:
                        raise ValueError('Name station can not be empty')
                    if temp_station in new_stations:
                        print('This station name is exists. please enter another station name')
                        i -= 1
                    else:
                        new_stations.append(temp_station) 

                selectedLine["stations"] = new_stations

                Line_dict.pop(name)
                Line_dict[new_name] = selectedLine
                print("The stations of line was updated successfully.")

                choice=input("Do you want to continiue? yes/no").strip().lower()
                if choice != "yes":
                    break

                self.ShowMenuTrain()

    def Remove_Line(self):
        print('You are removing a new line.')
        self.check_choice()

        while True:
            if len(Line_dict.items) == 0:
                print("There is no line.")
                break

            name_line=input("Enter the name line for delete").strip().lower()
            if not name_line:
                raise ValueError("Name line can not be empty.")
            if name_line not in Line_dict:
                print("This name is not exists.")
                continue

            choice=input("Are you sure for delete? yes/no").strip().lower()
            if choice == "no":
                continue
            elif choice == "yes":
                del Line_dict[name_line]
                print(f"The line of {name_line} was deleted successfully.")
                break
            else:
                print("your answer is not valid.")
                continue

        self.check_choice()

    def ShowLines(self):
        print('You are displaying a new line.')
        self.check_choice()

        if not Line_dict:
            print("There is no line.")  
            self.ShowLines()
        else:
            for l in Line_dict:
                print(l,end="\n")
            
        self.ShowMenuTrain()


    def ShowMenuTrain(self):
        input("Choose the item:\n1: Add new line.\n2: Uopdate line.\n3: Remove line.\n4: Show lines.\n5: " +
               "Add new train.\n6: Update train.\n7: Remove train.\n8: Show trains. ")
        
        choice=input("Enter your choice: ")
        if choice == "1":
            self.addLine()
        elif choice == "2":
            self.UpdateLine()
        elif choice == "3":
            self.Remove_Line()
        elif choice == "4":
            self.ShowLines()
        


    #Train ID must be digits only.
    #Train name must be alphabets only.
    #Train line must be digits only.
    #Mean speed must be float.
    #Stop time must be float.
    #Train quality must be A, B, or C only.
    #Price must be float.
    #Capacity must be integer.
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
            
            
        
          
            mean_speed = input("Insert mean_speed: ").strip()

            if not mean_speed:
                raise ValueError("Mean speed cannot be empty.")
            
            if not isinstance(mean_speed, float):
                raise TypeError("Mean speed must be float.")            



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

                print("Indicate updating item or press R to return to Employee Panel" \
                "Press 1 to update Train name" \
                "Press 2 to update Train Line" \
                "Press 3 to update Train Mean Speed" \
                "Press 4 to update Train Stop Time" \
                "Press 5 to update Train Quality" \
                "Press 6 to update Train Price" \
                "Press 7 to update Train Capacity")  

                update_num = input().strip().lower()

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

            train_id = input("Enter train ID to remove or press R to return to Employee Panel").strip().lower()

            if train_id == "r":
                return
            
            if not train_id:
                raise ValueError("Train ID cannot be empty.")

            if not train_id.isdigit():
                raise TypeError("Train ID must be digits only.")
            
            if train_id not in self.train_dict:
                raise ValueError("Train with this ID does not exist.")
            
            del self.train_dict[train_id]
            print(f"Train ID:{train_id} is removed")


    #!!!!!!!!! check this!
    def show_trains(self):

        if not self.train_dict:
            print("No trains available.")
            return

        for train in self.train_dict.values():
            print(train)

        return


       
class Train():

    def __init__(self, train_name, train_line, mean_speed, stop_time, quality, price, capacity):
        self.train_name = train_name
        self.train_line = train_line
        self.mean_speed = mean_speed
        self.stop_time = stop_time
        self.quality = quality
        self.price = price
        self.capacity = capacity

    
    def update_info(self, update_case, new_value):
        setattr(self, update_case, new_value)


    def __str__(self):
            return f"Train Name: {self.train_name}, Train Line: {self.train_line}, Train Mean Speed: {self.mean_speed},Train Stop Time: {self.stop_time},Train Quality: {self.quality},Train Price: {self.price},Train Capacity: {self.capacity}"
            