class ScheduleHelper:
    @staticmethod
    def parse_time_hhmm(t: str):
        parts = t.strip().split(":")
        if len(parts) != 2:
            return None
        if not parts[0].isdigit() or not parts[1].isdigit():
            return None
        h = int(parts[0])
        m = int(parts[1])
        if h < 0 or h > 23 or m < 0 or m > 59:
            return None
        return h * 60 + m

    @staticmethod
    def format_minutes(mins: int):
        h = mins // 60
        m = mins % 60
        return f"{h:02d}:{m:02d}"

    @staticmethod
    def build_station_windows(line, train):
        dep0 = ScheduleHelper.parse_time_hhmm(train.departure_time)
        if dep0 is None:
            return None

        travel_min = int(round((line.distance_km / train.speed_kmh) * 60))
        stop_min = int(round(train.stop_min))

        all_stations = [line.origin] + line.stations + [line.destination]

        windows = {}
        current_depart = dep0

        windows[all_stations[0]] = (current_depart, current_depart)

        for i in range(1, len(all_stations)):
            arrival = current_depart + travel_min
            depart = arrival + stop_min
            windows[all_stations[i]] = (arrival, depart)
            current_depart = depart

        return windows

    @staticmethod
    def has_collision(line, new_train):
        new_windows = ScheduleHelper.build_station_windows(line, new_train)
        if new_windows is None:
            return True, "Invalid departure time"

        for old_train in line.trains:
            old_windows = ScheduleHelper.build_station_windows(line, old_train)
            if old_windows is None:
                continue

            for station in new_windows:
                if station in old_windows:
                    a1, d1 = new_windows[station]
                    a2, d2 = old_windows[station]

                    if not (d1 <= a2 or d2 <= a1):
                        msg = (
                            f"Collision! Train '{new_train.name}' conflicts with Train '{old_train.name}' "
                            f"at station '{station}' "
                            f"(new: {ScheduleHelper.format_minutes(a1)}-{ScheduleHelper.format_minutes(d1)} "
                            f"old: {ScheduleHelper.format_minutes(a2)}-{ScheduleHelper.format_minutes(d2)})"
                        )
                        return True, msg

        return False, "No collision"
