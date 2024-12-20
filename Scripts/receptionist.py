from entry import Entry

class Receptionist(Entry):
    def __init__(self, id, first_name, last_name):
        super().__init__(id, first_name, last_name)

    def __str__(self):
        return f"Dodano recepcjonistkę: {self.first_name} {self.last_name}"