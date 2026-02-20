import datetime


class Ticket:
    _id_counter = 1

    def __init__(self, username, train, count, total):
        self.ticket_id = Ticket._id_counter
        Ticket._id_counter += 1
        self.username = username
        self.train_id = train.train_id
        self.train_name = train.name
        self.count = count
        self.total = total
        self.time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
