from entry import Entry

class Doctor(Entry):
    def __init__(self, id, first_name, last_name, specialization):
        super().__init__(id, first_name, last_name)
        self.specialization = specialization

        def __str__(self):
            return f"Dodano lekarza: {self.first_name} {self.last_name} {self.specialization}"

