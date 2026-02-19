
Line_dict = {}

class Train:
    def __init__(self, train_name, train_line, mean_speed,
                 stop_time, quality, price, capacity):

        if not train_name.isalpha():
            raise ValueError("Train name must contain only letters.")

        if quality not in ["A", "B", "C"]:
            raise ValueError("Train quality must be A, B or C.")

        if mean_speed <= 0:
            raise ValueError("Mean speed must be positive.")

        if stop_time < 0:
            raise ValueError("Stop time must be >= 0.")

        if price <= 0:
            raise ValueError("Price must be positive.")

        if capacity <= 0:
            raise ValueError("Capacity must be positive.")

        self.train_name = train_name
        self.train_line = train_line
        self.mean_speed = mean_speed
        self.stop_time = stop_time
        self.quality = quality
        self.price = price
        self.capacity = capacity

    def update_info(self, field, new_value):
        if not hasattr(self, field):
            raise ValueError("Invalid field")

        if field == "quality" and new_value not in ["A","B","C"]:
            raise ValueError("Quality must be A/B/C")

        if field in ["mean_speed","stop_time","price"] and float(new_value) < 0:
            raise ValueError("Value must be positive")

        if field == "capacity" and int(new_value) <= 0:
            raise ValueError("Capacity must be positive")

        setattr(self, field, new_value)

    def __str__(self):
        return (f"{self.train_name} | Line:{self.train_line} | "
                f"Speed:{self.mean_speed} | Stop:{self.stop_time} | "
                f"Quality:{self.quality} | Price:{self.price} | "
                f"Capacity:{self.capacity}")


class EmployeePanel:

    def __init__(self):
        self.train_dict = {}


    def menu(self):
        while True:
            print("\nEmployee Panel")
            print("1. Add Line")
            print("2. Update Line")
            print("3. Delete Line")
            print("4. Show Lines")
            print("5. Add Train")
            print("6. Update Train")
            print("7. Delete Train")
            print("8. Show Trains")
            print("9. Logout")

            choice = input("Select: ")

            if choice == "1":
                self.add_line()
            elif choice == "2":
                self.update_line()
            elif choice == "3":
                self.delete_line()
            elif choice == "4":
                self.show_lines()
            elif choice == "5":
                self.add_train()
            elif choice == "6":
                self.update_train()
            elif choice == "7":
                self.delete_train()
            elif choice == "8":
                self.show_trains()
            elif choice == "9":
                print("Logged out.")
                break
            else:
                print("Invalid option")



    def add_line(self):
        name = input("Line name: ").lower().strip()

        if not name:
            print("Name cannot be empty")
            return

        if name in Line_dict:
            print("Line name must be unique")
            return

        origin = input("Origin: ")
        destination = input("Destination: ")

        if origin == destination:
            print("Origin and destination cannot match")
            return

        count = int(input("Number of stations: "))
        stations = []

        for i in range(count):
            st = input(f"Station {i+1}: ")
            if st in stations:
                print("Duplicate station!")
                return
            stations.append(st)

        Line_dict[name] = {
            "origin": origin,
            "destination": destination,
            "stations": stations
        }

        print("Line added successfully")

    def update_line(self):
        name = input("Enter line name: ").lower()

        if name not in Line_dict:
            print("Line not found")
            return

        line = Line_dict[name]

        print("1. origin")
        print("2. destination")
        print("3. stations")

        choice = input("Select field: ")

        if choice == "1":
            line["origin"] = input("New origin: ")
        elif choice == "2":
            line["destination"] = input("New destination: ")
        elif choice == "3":
            count = int(input("New station count: "))
            stations = []
            for i in range(count):
                stations.append(input(f"Station {i+1}: "))
            line["stations"] = stations

        print("Updated")

    def delete_line(self):
        name = input("Line name to delete: ").lower()

        if name not in Line_dict:
            print("Line not found")
            return

        del Line_dict[name]
        print("Line deleted")

    def show_lines(self):
        if not Line_dict:
            print("No lines available")
            return

        for name, info in Line_dict.items():
            print(name, "=>", info)



    def add_train(self):
        if not Line_dict:
            print("Add line first")
            return

        train_id = input("Train ID: ")

        if not train_id.isdigit():
            print("ID must be digits")
            return

        if train_id in self.train_dict:
            print("Duplicate ID")
            return

        name = input("Train name: ")
        line = input("Line: ")

        if line not in Line_dict:
            print("Line not exist")
            return

        speed = float(input("Mean speed: "))
        stop = float(input("Stop time: "))
        quality = input("Quality (A/B/C): ").upper()
        price = float(input("Price: "))
        cap = int(input("Capacity: "))

        self.train_dict[train_id] = Train(
            name, line, speed, stop, quality, price, cap
        )

        print("Train added")

    def update_train(self):
        tid = input("Train ID: ")

        if tid not in self.train_dict:
            print("Train not found")
            return

        train = self.train_dict[tid]

        field = input("Field (name/line/speed/stop/quality/price/capacity): ")

        mapping = {
            "name":"train_name",
            "line":"train_line",
            "speed":"mean_speed",
            "stop":"stop_time",
            "quality":"quality",
            "price":"price",
            "capacity":"capacity"
        }

        if field not in mapping:
            print("Invalid field")
            return

        value = input("New value: ")
        if field in ["speed","stop","price"]:
            value = float(value)
        if field == "capacity":
            value = int(value)

        train.update_info(mapping[field], value)
        print("Train updated")

    def delete_train(self):
        tid = input("Train ID: ")
        if tid not in self.train_dict:
            print("Not found")
            return
        del self.train_dict[tid]
        print("Deleted")

    def show_trains(self):
        if not self.train_dict:
            print("No trains")
            return

        for tid, train in self.train_dict.items():
            print(tid, "=>", train)
