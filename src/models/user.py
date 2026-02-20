class User:
    def __init__(self, username, salt, password_hash, full_name, email, phone=""):
        self.username = username
        self.salt = salt
        self.password_hash = password_hash
        self.full_name = full_name
        self.email = email
        self.phone = phone
