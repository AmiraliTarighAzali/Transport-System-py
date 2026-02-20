from models.line import Line
from models.train import Train
from utils.schedule_helper import ScheduleHelper


class EmployeePanel:
    def __init__(self, system, employee):
        self.system = system
        self.employee = employee

    def menu(self):
        while True:
            print("\n--- EMPLOYEE PANEL ---")
            print(f"Welcome {self.employee.first} {self.employee.last}")
            print("1. Add Line")
            print("2. Update Line")
            print("3. Delete Line")
            print("4. Show Lines")
            print("5. Add Train (Bonus collision check)")
            print("6. Update Train")
            print("7. Delete Train")
            print("8. Show Trains")
            print("9. Back")
            ch = input("Choose: ").strip()

            if ch == "1":
                self.add_line()
            elif ch == "2":
                self.update_line()
            elif ch == "3":
                self.delete_line()
            elif ch == "4":
                self.show_lines()
            elif ch == "5":
                self.add_train()
            elif ch == "6":
                self.update_train_info()
            elif ch == "7":
                self.delete_train()
            elif ch == "8":
                self.show_trains()
            elif ch == "9":
                return
            else:
                print("Wrong choice!")

    def add_line(self):
        print("\n--- Add Line --- (0 back)")
        while True:
            name = input("Line name: ").strip().lower()
            if name == "0":
                return
            if not name:
                print("Name cannot be empty!")
                continue
            if name in self.system.lines:
                print("This line name already exists!")
                continue
            if not name.isalpha():
                print("Line name must be alphabets only.")
                continue
            break

        while True:
            origin = input("Origin: ").strip().lower()
            if origin == "0":
                return
            if not origin or not origin.isalpha():
                print("Origin must be alphabets only and not empty.")
                continue
            break

        while True:
            dest = input("Destination: ").strip().lower()
            if dest == "0":
                return
            if not dest or not dest.isalpha():
                print("Destination must be alphabets only and not empty.")
                continue
            if dest == origin:
                print("Origin and destination cannot be same.")
                continue
            break

        while True:
            dk = input("Distance between stations (km) e.g. 20: ").strip()
            if dk == "0":
                return
            try:
                dk = float(dk)
                if dk <= 0:
                    print("Distance must be positive.")
                    continue
                break
            except:
                print("Invalid number.")

        while True:
            c = input("Number of middle stations: ").strip()
            if c == "0":
                return
            try:
                c = int(c)
                if c < 0:
                    print("Cannot be negative.")
                    continue
                break
            except:
                print("Must be integer.")

        stations = []
        for i in range(c):
            while True:
                st = input(f"Station {i+1}: ").strip().lower()
                if st == "0":
                    return
                if not st or not st.isalpha():
                    print("Station must be alphabets only and not empty.")
                    continue
                if st in stations:
                    print("Duplicate station!")
                    continue
                stations.append(st)
                break

        line = Line(name, origin, dest, stations, dk)
        self.system.lines[name] = line
        print("Line added!")

    def update_line(self):
        print("\n--- Update Line ---")
        if not self.system.lines:
            print("No lines.")
            return

        name = input("Line name (0 back): ").strip().lower()
        if name == "0":
            return
        if name not in self.system.lines:
            print("Line not found.")
            return

        line = self.system.lines[name]
        print("1. Origin")
        print("2. Destination")
        print("3. Stations")
        print("4. Distance(km)")
        opt = input("Choose: ").strip()

        if opt == "1":
            new = input("New origin: ").strip().lower()
            if new and new.isalpha():
                line.origin = new
                print("Updated.")
        elif opt == "2":
            new = input("New destination: ").strip().lower()
            if new and new.isalpha():
                line.destination = new
                print("Updated.")
        elif opt == "3":
            stations = []
            while True:
                st = input("Station (Enter to finish): ").strip().lower()
                if not st:
                    break
                if not st.isalpha():
                    print("Only alphabets.")
                    continue
                if st in stations:
                    print("Duplicate!")
                    continue
                stations.append(st)
            line.stations = stations
            print("Updated.")
        elif opt == "4":
            try:
                dk = float(input("New distance(km): "))
                if dk > 0:
                    line.distance_km = dk
                    print("Updated.")
            except:
                print("Invalid number.")

    def delete_line(self):
        print("\n--- Delete Line ---")
        if not self.system.lines:
            print("No lines.")
            return
        name = input("Line name (0 back): ").strip().lower()
        if name == "0":
            return
        if name not in self.system.lines:
            print("Line not found.")
            return

        del self.system.lines[name]
        self.system.trains = {
            tid: t for tid, t in self.system.trains.items() if t.line_name != name}
        print("Line deleted (and its trains removed).")

    def show_lines(self):
        print("\n--- Lines ---")
        if not self.system.lines:
            print("No lines.")
            return
        for ln, line in self.system.lines.items():
            all_st = [line.origin] + line.stations + [line.destination]
            print(
                f"Name: {ln} | Route: {line.origin}->{line.destination} | DistanceBetween:{line.distance_km}km")
            print("Stations:", ", ".join(all_st))
            print("-" * 30)

    def add_train(self):
        print("\n--- Add Train --- (0 back)")
        if not self.system.lines:
            print("No lines! Add a line first.")
            return

        print("Available lines:", ", ".join(self.system.lines.keys()))
        line_name = input("Line name: ").strip().lower()
        if line_name == "0":
            return
        if line_name not in self.system.lines:
            print("Line not found.")
            return
        line = self.system.lines[line_name]

        name = input("Train name: ").strip()
        if name == "0":
            return
        if not name:
            print("Name cannot be empty.")
            return

        try:
            speed = float(input("Speed (km/h): ").strip())
            if speed <= 0:
                print("Speed must be positive.")
                return
        except:
            print("Invalid speed.")
            return

        try:
            stop_min = float(
                input("Stop time at each station (min): ").strip())
            if stop_min < 0:
                print("Stop time cannot be negative.")
                return
        except:
            print("Invalid stop time.")
            return

        dep = input("Departure time (HH:MM) e.g. 08:00: ").strip()
        if dep == "0":
            return
        if ScheduleHelper.parse_time_hhmm(dep) is None:
            print("Invalid time format.")
            return

        q = input("Quality (A/B/C): ").strip().upper()
        if q not in ["A", "B", "C"]:
            print("Quality must be A/B/C.")
            return

        try:
            price = float(input("Price: ").strip())
            if price < 0:
                print("Price cannot be negative.")
                return
        except:
            print("Invalid price.")
            return

        try:
            cap = int(input("Capacity: ").strip())
            if cap <= 0:
                print("Capacity must be positive.")
                return
        except:
            print("Invalid capacity.")
            return

        new_train = Train(name, line_name, speed, stop_min, q, price, cap, dep)

        coll, msg = ScheduleHelper.has_collision(line, new_train)
        if coll:
            print(msg)
            print("Train NOT added due to collision.")
            return

        self.system.trains[new_train.train_id] = new_train
        line.trains.append(new_train)
        print(f"Train added! ID: {new_train.train_id}")

        win = ScheduleHelper.build_station_windows(line, new_train)
        if win:
            print("Schedule:")
            for st, (a, d) in win.items():
                print(
                    f"- {st}: {ScheduleHelper.format_minutes(a)} -> {ScheduleHelper.format_minutes(d)}")

    def update_train_info(self):
        print("\n--- Update Train ---")

        if not self.system.trains:
            print("No trains available.")
            return
        print("Available trains:")
        for tid, t in self.system.trains.items():
            print(f"ID: {tid} | {t.name} | Line: {t.line_name}")

        while True:
            try:
                train_id = input(
                    "\nEnter train ID to update (0 to back): ").strip()

                if train_id == "0":
                    return

                if not train_id:
                    print("Train ID cannot be empty!")
                    continue

                if not train_id.isdigit():
                    print("Train ID must be digits only!")
                    continue

                train_id = int(train_id)

                if train_id not in self.system.trains:
                    print("Train not found!")
                    continue

                break
            except:
                print("Invalid input!")

        train = self.system.trains[train_id]

        while True:
            try:
                print("\nWhat to update?")
                print("1. Name")
                print("2. Line")
                print("3. Speed")
                print("4. Stop Time")
                print("5. Quality")
                print("6. Price")
                print("7. Capacity")
                print("8. Back")

                choice = input("Choose: ").strip()

                if choice == "8":
                    return

                if choice not in ["1", "2", "3", "4", "5", "6", "7"]:
                    print("Invalid choice!")
                    continue

                if choice == "1":
                    new = input("New name: ").strip()
                    if new:
                        train.update_info("name", new)
                        print("Name updated!")

                elif choice == "2":
                    print("Available lines:", ", ".join(
                        self.system.lines.keys()))
                    new = input("New line: ").strip().lower()
                    if new in self.system.lines:
                        train.update_info("line_name", new)
                        print("Line updated!")
                    else:
                        print("Line not found!")

                elif choice == "3":
                    try:
                        new = float(input("New speed (km/h): "))
                        if new > 0:
                            train.update_info("speed_kmh", new)
                            print("Speed updated!")
                        else:
                            print("Speed must be positive!")
                    except:
                        print("Invalid number!")

                elif choice == "4":
                    try:
                        new = float(input("New stop time (min): "))
                        if new >= 0:
                            train.update_info("stop_min", new)
                            print("Stop time updated!")
                        else:
                            print("Stop time cannot be negative!")
                    except:
                        print("Invalid number!")

                elif choice == "5":
                    new = input("New quality (A/B/C): ").strip().upper()
                    if new in ["A", "B", "C"]:
                        train.update_info("quality", new)
                        print("Quality updated!")
                    else:
                        print("Quality must be A/B/C!")

                elif choice == "6":
                    try:
                        new = float(input("New price: "))
                        if new >= 0:
                            train.update_info("price", new)
                            print("Price updated!")
                        else:
                            print("Price cannot be negative!")
                    except:
                        print("Invalid number!")

                elif choice == "7":
                    try:
                        new = int(input("New capacity: "))
                        if new > 0:
                            old_cap = train.capacity
                            train.update_info("capacity", new)
                            if train.available == old_cap:
                                train.available = new
                            print("Capacity updated!")
                        else:
                            print("Capacity must be positive!")
                    except:
                        print("Invalid number!")

                again = input(
                    "\nUpdate another field? (y/n): ").strip().lower()
                if again != 'y':
                    return

            except Exception as e:
                print(f"Error: {e}")

    def delete_train(self):
        print("\n--- Delete Train ---")

        if not self.system.trains:
            print("No trains available.")
            return

        print("Available trains:")
        for tid, t in self.system.trains.items():
            print(f"ID: {tid} | {t.name} | Line: {t.line_name}")

        while True:
            try:
                train_id = input(
                    "\nEnter train ID to delete (0 to back): ").strip()

                if train_id == "0":
                    return

                if not train_id:
                    print("Train ID cannot be empty!")
                    continue

                if not train_id.isdigit():
                    print("Train ID must be digits only!")
                    continue

                train_id = int(train_id)

                if train_id not in self.system.trains:
                    print("Train not found!")
                    continue

                train = self.system.trains[train_id]
                print(f"\nTrain to delete: {train}")

                confirm = input("Are you sure? (y/n): ").strip().lower()

                if confirm == 'y':
                    line_name = train.line_name
                    if line_name in self.system.lines:
                        line = self.system.lines[line_name]
                        line.trains = [
                            t for t in line.trains if t.train_id != train_id]

                    del self.system.trains[train_id]
                    print(f"Train ID {train_id} deleted successfully!")

                break

            except Exception as e:
                print(f"Error: {e}")

    def show_trains(self):
        print("\n--- Trains ---")
        if not self.system.trains:
            print("No trains.")
            return
        for tid, t in self.system.trains.items():
            print(t)
