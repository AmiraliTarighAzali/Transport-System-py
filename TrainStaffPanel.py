class EmployeePanel:

    def __init__(self):
        self.Line_dict = {}
        self.train_dict = {}

    def menu(self):
        while True:
            choice=input("for return to employee panel press R: ").strip().lower()
            if choice=="r":
                #display main panel
                pass
            else:
                print(
                    "Here is Train Staff Panel. Please choose an action:\n"
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
                request_num = input("Please enter your choice: ").strip()

                if request_num not in ["1","2","3","4","5","6","7","8","9"]:
                    raise ValueError("No valid input.")

                match request_num:
                    case "1":
                        try:
                            self.addLine()
                        except Exception as e:
                            print(f"Error in add Line method: {e}")
                            continue
                    case "2":
                        try:
                            self.UpdateLine()
                        except Exception as e:
                            print(f"Error in UpdateLine method: {e}")
                            continue
                    case "3":
                        try:
                            self.RemoveLine()
                        except Exception as e:
                            print(f"Error in RemoveLine method: {e}")    
                            continue
                    case "4":
                        try:
                            self.RemoveLine()
                        except Exception as e:
                            print(f"Error in ShowLines method: {e}")  
                            continue
                    case "5":
                        try:
                            self.add_train()
                        except Exception as e:
                            print(f"Error in add_train method: {e}") 
                            continue
                    case "6":
                        try:
                            self.update_train_info()
                        except Exception as e:
                            print(f"Error in update_train_info method: {e}") 
                            continue
                    case "7":
                        try:
                            self.delete_train()
                        except Exception as e:
                            print(f"Error in delete_train method: {e}") 
                            continue
                    case "8":
                        try:
                            self.show_trains()
                        except Exception as e:
                            print(f"Error in show_trains method: {e}") 
                            continue
                    case "9":
                        break
                    
    #Line name must be alphabets only.
    #Origin name must be alphabets only.
    #Destination name must be alphabets only.
    #number of stations must be integer and can not be negative.
    #Station names must be alphabets only.

    def addLine(self):
        print('You are adding a new line.\n')

        while True:
            try:
                name = input('Enter name of line or press R to return to Employee Panel.\n":').strip().lower()

                if name == "r":
                    return
                
                if not name:
                    raise ValueError("The name can not be empty.")

                if name in self.Line_dict:
                    raise ValueError("This name already exists.")
                
                if not name.isalpha():
                    raise TypeError("Line name must be alphabets only.")
 
                break
            except Exception as e:
                print(f"Error: {e}")


        while True:
            try:
                origin = input('Origin name: ').strip().lower()
                if not origin:
                    raise ValueError('The origin can not be empty')
                
                if not origin.isalpha():
                    raise TypeError("Origin name must be alphabets only.")
                
                destination = input('Destination name: ').strip().lower()

                if not destination:
                    raise ValueError('The destination can not be empty.')
                
                if not destination.isalpha():
                    raise TypeError("Destination name must be alphabets only.")
                
                if origin == destination:
                    raise ValueError("Origin and destination can not be same.")
                
                break
            except Exception as e:
                print(f"Error: {e}")



        while True:
            try:
                countsStation = input('Number of Stations: ').strip()
                if not countsStation:
                    raise ValueError('Number of Stations can not be empty.')
                
                countsStation = int(countsStation)
                if countsStation <= 0:
                    raise ValueError('Number of Stations can not be negative or zero.')
                
                stations = []
                for i in range(countsStation):
                    temp_station = input(f'Enter Station {i+1}: ').strip().lower()

                    if not temp_station:
                        raise ValueError('Name station can not be empty.')
                    
                    if not temp_station.isalpha():
                        raise TypeError('Station name must be alphabets only.')
                    
                    if temp_station in stations:
                        raise ValueError('This station name is exists. please enter another station name.')
                   
                    stations.append(temp_station) 
                
                break
            except Exception as e:
                print(f"Error: {e}")

        newLineInfo = {"name_line":name,"origin": origin,"destination":destination,"countsStation":countsStation,"stations":stations}
        self.Line_dict[name] = newLineInfo
        print(f'Line of {name} added successfully.') 


    def UpdateLine(self):
        print('You are updating a line.')
        
        while True:
            try:
                name = input("Enter Line name to update or press R to return to Employee Panel.\n").strip().lower()

                if name == "r":
                    return
                
                if not name:
                    raise ValueError("Line name cannot be empty.")
                
                if name not in self.Line_dict:
                    raise ValueError("Line with this name does not exist.")
                
                #selectedName= self.Line_dict[name]["name_line"]
        
                print(f"Line Name: {self.Line_dict[name]['name_line']}")
                print(f"Origin: {self.Line_dict[name]['origin']}")
                print(f"Destination: {self.Line_dict[name]['destination']}")
                print(f"Number of Stations: {self.Line_dict[name]['countsStation']}")
                print(f"Station Names: {', '.join(self.Line_dict[name]['stations'])}")      

                break
            except Exception as e:
                print(f"Error: {e}")


        while True:
            try:
                print("Indicate updating item or press R to return to Employee Panel.\n" \
                "Press 1 to update Line name\n" \
                "Press 2 to update Line Origin\n" \
                "Press 3 to update Line Destination\n" \
                "Press 4 to update Number of Stations\n" \
                "Press 5 to update Station Names\n")  

                update_num = input().strip().lower()

                if update_num == "r":
                    return

                if update_num not in ["1","2","3","4","5"]:
                    raise ValueError("No valid input.")

                    
                match update_num:

                    case "1":
                        new_name = input("Enter new name: ").strip().lower()
                        if not new_name:
                            raise ValueError('The name can not be empty.')
                            
                        if new_name in self.Line_dict:
                            raise ValueError('This name is already exists.')
            
                        if not new_name.isalpha():
                            raise TypeError("New name must be alphabets only.")
                        
                        
                        self.Line_dict[name]["name_line"] = new_name
                        self.Line_dict[new_name] = self.Line_dict.pop(name)
                        print("Line name updated successfully.")

                    case "2":
                        new_origin = input("Enter the new origin: ").strip().lower()
                        if not new_origin:
                            raise ValueError('The new origin can not be empty.')
                            
                        if new_origin == self.Line_dict[name]["origin"]:
                            raise ValueError("The new origin is same as old origin.")
   
                        if not new_origin.isalpha():
                            raise TypeError("New origin must be alphabets only.")

                        self.Line_dict[name]["origin"] = new_origin
                        print("Line origin updated successfully.")

                    case "3":
                        new_destination = input("Enter the new destination: ").strip().lower()
                        if not new_destination:
                            raise ValueError('The destination can not be empty.')
                            
                        if new_destination == self.Line_dict[name]["destination"]:
                            raise ValueError("The new destination is same as old destination.")
                    
                        if not new_destination.isalpha():
                            raise TypeError("New destination must be alphabets only.")

                        self.Line_dict[name]["destination"] = new_destination
                        print("Line destination updated successfully.")

                    case "4":
                        new_count_state = input("Enter the new number of stations: ").strip()
                        if not new_count_state:
                            raise ValueError('The number of stations can not be empty.')
                        
                        new_count_state = int(new_count_state)
                        if new_count_state == self.Line_dict[name]["countsStation"]:
                            raise ValueError("The number of stations is same as old number of stations.")

                        if new_count_state < 0:
                            raise ValueError('Number of Stations can not be negative.')
  
                        self.Line_dict[name]["countsStation"] = new_count_state

                        new_stations=[]

                        for i in range(new_count_state):
                            temp_station = input(f'Enter Station {i+1}: ').strip().lower()
                            if not temp_station:
                                raise ValueError('Station name can not be empty.')
                            if not temp_station.isalpha():
                                raise TypeError('Station name must be alphabets only.')
                            if temp_station in new_stations:
                                raise ValueError('This station name alrady exists. please enter another station name.')
                         
                            new_stations.append(temp_station) 

                        self.Line_dict[name]["stations"] =  new_stations
                        print("Number and name of stations updated successfully.")

                    case "5":
                        new_stations = []
                        count_state = int(self.Line_dict[name]["countsStation"])

                        for i in range(count_state):
                            temp_station = input(f'Enter Station {i+1}: ').strip().lower()
                            if not temp_station:
                                raise ValueError('Name station can not be empty.')
                            if not temp_station.isalpha():
                                raise TypeError('Station name must be alphabets only.') 
                            if temp_station in new_stations:
                               raise ValueError('This station name already exists. please enter another station name.')
                            new_stations.append(temp_station) 
                            
                        self.Line_dict[name]["stations"] = new_stations
                        print("Line stations updated successfully.")

                break
            except Exception as e:
                print(f"Error: {e}")


    def RemoveLine(self):
        print('You are deleting a line.\n')
        while True:
            try:
                if not self.Line_dict:
                    print("There is no line to delete.")
                    return

                name_line = input("Enter line name to remove or press R to return to Employee Panel.\n").strip().lower()

                if name_line == "r":
                    return
                
                if not name_line:
                    raise ValueError("Line name cannot be empty.")

                if not name_line.isalpha():
                    raise TypeError("Line name must be alphabets only.")
                
                if name_line not in self.Line_dict:
                    raise ValueError("Line with this name does not exist.")

                del self.Line_dict[name_line]
                print(f"Line name: {name_line} deleted successfully.")

                break
            except Exception as e:
                print(f"Error: {e}")  


    def ShowLines(self):

        if not self.Line_dict:
            print("There is no line.")  
            return
        else:
            for v in self.Line_dict.values():
                print( v, end="\n")
                
            return


    #Train ID must be digits only.
    #Train name must be alphabets only.
    #Train line must be in Line_dict.If there is no line, train can not be added.
    #Mean speed must be float.
    #Stop time must be float.
    #Train quality must be A, B, or C only.
    #Price must be float.
    #Capacity must be integer.

    def add_train(self):
        print('You are adding a new train\n.')

        if not self.Line_dict:
            print("No train lines available(For adding train you need lines to be defined).Please first add a line.\n")
            return
        

        while True:
            try:
                train_id = input("Enter train ID or press R to return to Employee Panel.\n").strip().lower()

                if train_id == "r":
                    return
                
                if not train_id:
                    raise ValueError("Train ID cannot be empty.")

                if not train_id.isdigit():
                    raise TypeError("Train ID must be digits only.")
                
                if train_id in self.train_dict:
                    raise ValueError("This train already exists.")
                
                break
            except Exception as e:
                print(f"Error: {e}")
            
        while True:
            try:  
                train_name = input("Insert train name: ").strip().lower()

                if not train_name:
                    raise ValueError("Train name cannot be empty.")

                if not train_name.isalpha():
                    raise TypeError("Train name must be alphabets only.")
                
                break    
            except Exception as e:
                    print(f"Error: {e}")


        while True:
            try:
                print("Available train lines:", ", ".join(self.Line_dict.keys()))

                train_line = input("Insert train line: ").strip().lower()

                if not train_line:
                    raise ValueError("Train line cannot be empty.")

                if train_line not in self.Line_dict.keys():
                    raise ValueError("This line does not exist.")               
            
                break
            except Exception as e:
                    print(f"Error: {e}")

        while True:
            try:
                mean_speed = float(input("Insert train mean speed: ").strip())

                if mean_speed < 0:
                    raise ValueError("Train mean speed cannot be negative.")

                break
            except Exception as e:
                    print(f"Error: {e}")


        while True:
            try:
                stop_time = float(input("Insert train stop time: ").strip())

                if stop_time < 0:
                    raise ValueError("Train stop time cannot be negative.")

                break
            except Exception as e:
                    print(f"Error: {e}")  
          
        while True:
            try:
                quality = input("Insert train quality (A/B/C): ").strip().upper()

                if not quality:
                    raise ValueError("Quality cannot be empty.")

                if quality not in ["A", "B", "C"]:
                    raise TypeError("Train quality must be A, B, or C only.")

                break
            except Exception as e:
                    print(f"Error: {e}")           

        while True:
            try:
                price = float(input("Insert train price: ").strip())

                if price < 0:
                    raise ValueError("Train price cannot be negative.")
                
                break
            except Exception as e:
                    print(f"Error: {e}") 

        while True:
            try:
                capacity = int(input("Insert train capacity: ").strip())

                if capacity < 0:
                    raise ValueError("Capacity cannot be negative.")
                
                break
            except Exception as e:
                    print(f"Error: {e}") 

        self.train_dict[train_id] = BaseTrain(train_name, train_line, mean_speed, stop_time, quality, price, capacity)
        print(f'Train {train_name} added successfully.') 

 
    
    def update_train_info(self):
            print('You are updating train info.\n')
            while True:
                try:
                    train_id = input("Enter train ID to update or press R to return to Employee Panel.\n").strip().lower()

                    if train_id == "r":
                        return
                    
                    if not train_id:
                        raise ValueError("Train ID cannot be empty.")

                    if not train_id.isdigit():
                        raise TypeError("Train ID must be digits only.")
                    
                    if train_id not in self.train_dict:
                        raise ValueError("This train does not exist.")

                    break
                except Exception as e:
                    print(f"Error: {e}")

            t = self.train_dict[train_id]

            while True:
                try:
                    print("Indicate updating item or press R to return to Employee Panel.\n" \
                    "Press 1 to update Train name\n" \
                    "Press 2 to update Train Line\n" \
                    "Press 3 to update Train Mean Speed\n" \
                    "Press 4 to update Train Stop Time\n" \
                    "Press 5 to update Train Quality\n" \
                    "Press 6 to update Train Price\n" \
                    "Press 7 to update Train Capacity\n")  

                    update_num = input().strip().lower()

                    if update_num == "r":
                        return

                    if update_num not in ["1","2","3","4","5","6","7"]:
                        raise ValueError("No valid input.")

                    match update_num:
                        case "1":
                            new_value = input("Enter new value for train name: ").strip().lower()

                            if not new_value:
                                raise ValueError("New value cannot be empty.")
                    
                            if not new_value.isalpha():
                                raise TypeError("New value must be alphabets only.")

                            t.update_info("train_name",new_value)
                            print("Train name updated successfully.")
                            

                        case "2":
                            print("Available train lines:", ", ".join(self.Line_dict.keys()))
                            new_value = input("Enter new value for train line: ").strip().lower()

                            if not new_value:
                                raise ValueError("New value cannot be empty.")
                
                            if new_value not in self.Line_dict.keys():
                                raise ValueError("This line does not exist.") 

                            t.update_info("train_line",new_value)
                            print("Train line updated successfully.")

                        case "3":
                            new_value = float(input("Enter new value for train mean speed: ").strip())
                            
                            if new_value < 0:   
                                raise ValueError("New value cannot be negative.")
                
                            t.update_info("mean_speed",new_value)
                            print("Train mean speed updated successfully.")

                        case "4":
                            new_value = float(input("Enter new value for train stop time: ").strip())

                            if new_value < 0:   
                                raise ValueError("New value cannot be negative.")

                            t.update_info("stop_time",new_value)
                            print("Train stop time updated successfully.")

                        case "5":
                            new_value = input("Enter New value for train quality(A/B/C): ").strip().upper()
                            if not new_value:
                                raise ValueError("New value cannot be empty.")

                            if new_value not in ["A", "B", "C"]:
                                raise TypeError("New value must be A, B, or C only.")

                            t.update_info("quality",new_value)
                            print("Train quality updated successfully.")

                        case "6":
                            new_value = float(input("Enter new value for train price: ").strip())
                            
                            if new_value < 0:   
                                raise ValueError("New value cannot be negative.")   
                
                            t.update_info("price",new_value)
                            print("Train price updated successfully.")

                        case "7":
                            new_value = int(input("Enter new value for train capacity: ").strip())

                            if new_value < 0:   
                                raise ValueError("New value cannot be negative.")
                            
                            t.update_info("capacity",new_value)
                            print("Train capacity updated successfully.")

                    break
                except Exception as e:
                    print(f"Error: {e}")

    def delete_train(self):
        print('You are deleting a train.\n')

        while True:
            try:
                if not self.train_dict:
                    print("There is no train to delete.")
                    return

                train_id = input("Enter train ID to remove or press R to return to Employee Panel.\n").strip().lower()

                if train_id == "r":
                    return
                
                if not train_id:
                    raise ValueError("Train ID cannot be empty.")

                if not train_id.isdigit():
                    raise TypeError("Train ID must be digits only.")
                
                if train_id not in self.train_dict:
                    raise ValueError("Train with this ID does not exist.")
                
                del self.train_dict[train_id]
                print(f"Train ID {train_id} deleted successfully.")

                break
            except Exception as e:
                print(f"Error: {e}")    

    def show_trains(self):

        if not self.train_dict:
            print("No train available.")
            return

        for train in self.train_dict.values():
            print(train,end="\n")

        return


       
class BaseTrain():

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
        return (
            f"Train Name: {self.train_name}, "
            f"Train Line: {self.train_line}, "
            f"Train Mean Speed: {self.mean_speed}, "
            f"Train Stop Time: {self.stop_time}, "
            f"Train Quality: {self.quality}, "
            f"Train Price: {self.price}, "
            f"Train Capacity: {self.capacity}")      
    
