class Train:
    _id_counter = 1

    def __init__(self, name, line_name, speed_kmh, stop_min, quality, price, capacity, departure_time):
        self.train_id = Train._id_counter
        Train._id_counter += 1

        self.name = name
        self.line_name = line_name
        self.speed_kmh = float(speed_kmh)
        self.stop_min = float(stop_min)
        self.quality = quality
        self.price = float(price)
        self.capacity = int(capacity)
        self.available = int(capacity)
        self.departure_time = departure_time  # "HH:MM"

    def book(self, count):
        if count <= 0:
            return False, "Count must be positive"
        if count > self.available:
            return False, f"Only {self.available} seats available"
        self.available -= count
        return True, "Booked"

    def update_info(self, field, new_value):
        setattr(self, field, new_value)

    def __str__(self):
        return f"ID:{self.train_id} | {self.name} | Line:{self.line_name} | Price:{self.price} | Seats:{self.available}/{self.capacity}"
