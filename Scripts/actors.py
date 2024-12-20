
class Pet:
    def __init__(self, id, pet_name, species, breed, age):
        self.id = id
        self.pet_name = pet_name
        self.species = species
        self.breed = breed
        self.age = age
        self.delelted = False

    def __str__(self):
        return f"{self.name} ma ({self.species}, {self.breed}, {self.age} lat)"
    
    
class Visit:
    def __init__(self, id, date, pet_name, doctor, diagnosis):
        self.id = id
        self.date = date
        self.pet_name = pet_name
        self.doctor = doctor
        self.diagnosis = diagnosis
        self.deleted = False

    def __str__(self):
        return f"Wizyta {self.pet.name} u {self.doctor} w dniu {self.date}: {self.diagnosis}"