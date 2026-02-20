class Line:
    def __init__(self, name, origin, destination, stations, distance_km):
        self.name = name
        self.origin = origin
        self.destination = destination
        self.stations = stations  # list[str]
        self.distance_km = distance_km  # فاصله بین هر ایستگاه
        self.trains = []  # list[Train]
