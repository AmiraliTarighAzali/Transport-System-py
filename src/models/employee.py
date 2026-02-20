class Employee:
    def __init__(self, first, last, username, salt, password_hash, email):
        self.first = first
        self.last = last
        self.username = username
        self.salt = salt
        self.password_hash = password_hash
        self.email = email
