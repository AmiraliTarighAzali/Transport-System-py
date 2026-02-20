import os
import json


class FileStorage:
    def __init__(self, folder="data"):
        self.folder = folder
        if not os.path.exists(folder):
            os.makedirs(folder)

        self.users_file = os.path.join(folder, "users.txt")
        self.employees_file = os.path.join(folder, "employees.txt")
        self.transactions_file = os.path.join(folder, "transactions.txt")
        self.tickets_file = os.path.join(folder, "tickets.txt")

        for f in [self.users_file, self.employees_file, self.transactions_file, self.tickets_file]:
            if not os.path.exists(f):
                with open(f, "w", encoding="utf-8") as _:
                    pass

    def append_json_line(self, filepath, data: dict):
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")

    def read_all_json_lines(self, filepath):
        items = []
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        items.append(json.loads(line))
                    except:
                        pass
        return items

    def write_all_json_lines(self, filepath, items):
        with open(filepath, "w", encoding="utf-8") as f:
            for it in items:
                f.write(json.dumps(it, ensure_ascii=False) + "\n")
