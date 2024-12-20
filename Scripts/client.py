from entry import Entry
from actors import Pet

class Client(Entry):
    def __init__(self, id, first_name, last_name, phone, address):
        super().__init__(id, first_name, last_name)
        self.phone = phone
        self.addres = address
        self.deleted = False

    def __str__(self):
        return f"Dodano klienta {self.first_name} {self.last_name} ({self.phone})"