
from actors import Pet, Visit
from client import Client
from doctor import Doctor
from receptionist import Receptionist

class VeterinaryCRM:

    def __init__(self):
        self.clients = []
        self.doctors = []
        self.visits = []
        self.receptionist = []
        self.pets = []

    # Dodawanie klienta
    def add_client(self, first_name, last_name, phone, address):
        client = Client(first_name, last_name, phone, address)
        self.clients.append(client)
        print(f"Dodano klienta {first_name} {last_name} ({phone}) {address}")


    # Odczyt klienta po imieniu i nazwisku
    def read_client(self, first_name, last_name):
        for client in self.clients:
            print(f"Porównywanie: {client.first_name.strip().lower()} {client.last_name.strip().lower()} z {first_name.strip().lower()} {last_name.strip().lower()}")  # Debugowanie
            if client.first_name.strip().lower() == first_name.strip().lower() and \
               client.last_name.strip().lower() == last_name.strip().lower():
                print(f"Znaleziono klienta: {client.first_name} {client.last_name}")
                return client
            
        print(f"Nie znaleziono klienta {first_name} {last_name}.")
        return None

    # Aktualizacja danych klienta
    def update_client(self, first_name, last_name, new_first_name, new_last_name, new_phone, new_address):
        client = self.read_client(first_name, last_name)
    
    # Debugowanie: Wyświetl, co jest porównywane
        print(f"Szukane dane: {first_name} {last_name}")
        if client:
            print(f"Znaleziono klienta: {client.first_name} {client.last_name}")
            if new_first_name:
                client.first_name = new_first_name
            if new_last_name:
                client.last_name = new_last_name
            if new_phone:
                client.phone = new_phone
            if new_address:
                client.address = new_address
            return print(f"Dane klienta {first_name} {last_name} zostały zaktualizowane na następujące dane: {new_first_name}, {new_last_name}, {new_phone}, {new_address}.")
        else:
            print("Nie znaleziono klienta!")
            print(f"Lista klientów: {[f'{client.first_name} {client.last_name}' for client in self.clients]}")
            print("Nie można zaktualizować nieistniejącego klienta.")


    # Miękkie usunięcie klienta (soft delete)
    def soft_delete_client(self, first_name, last_name):
        client = self.read_client(first_name, last_name)
        if client:
            client.deleted = True
            print(f"Klient {client.first_name} {client.last_name} został oznaczony jako usunięty.")
        else:
            print("Nie można usunąć nieistniejącego klienta.")


    # Dodawanie zwierzęcia
    def add_pet(self, pet_name, species, breed, age):
        pet = Pet(pet_name, species, breed, age)
        self.pets.append(pet)


    # Wyszukiwanie zwierzęcia
    def read_pet(self, pet_name, species):
        for pet in self.pets:
            if pet.pet_name.strip().lower() == pet_name.strip().lower() and \
               pet.species.strip().lower() == species.strip().lower():
                print(f"Znaleziono zwierzę: {pet.pet_name} {pet.species}")
                return pet
            
        print(f"Nie znaleziono zwierzęcia {pet_name} {species}.")
        return None
    

    # Aktualizacja danych zwierzęcia
    def update_pet(self, pet_name, species, new_pet_name, new_species, new_breed, new_age):
        pet = self.read_pet(pet_name, species)
        if pet:
            if new_pet_name:
                pet.pet_name = new_pet_name
            if new_species:
                pet.species = new_species
            if new_breed:
                pet.breed = new_breed
            if new_age:
                pet.age = new_age
            return print(f"Dane zwierzęcia {pet_name} {species} zostały zaktualizowane na następujące dane: {new_pet_name}, {new_species}, {new_breed}, {new_age}.")
        else:
            print("Nie znaleziono zwierzęcia!")
    

    # Miękkie usunięcie zwierzęcia(soft delete)
    def soft_delete_pet(self, pet_name, species):
        pet = self.read_pet(pet_name, species)
        if pet:
            pet.deleted = True
            print(f"Zwierzę {pet.pet_name} {pet.species} zostało oznaczone jako usunięte.")
        else:
            print("Nie można usunąć nieistniejącego zwierzęcia.")
  

    # Dodawanie lekarza  
    def add_doctor(self, first_name, last_name, specialization):
        doctor = Doctor(first_name, last_name, specialization)
        self.doctors.append(doctor)

    
    # Wyszukiwanie lekarza
    def read_doctor(self, first_name, last_name):
        for doctor in self.doctors:
            print(f"Porównywanie: {doctor.first_name.strip().lower()} {doctor.last_name.strip().lower()} z {first_name.strip().lower()} {last_name.strip().lower()}")  # Debugowanie
            if doctor.first_name.strip().lower() == first_name.strip().lower() and \
               doctor.last_name.strip().lower() == last_name.strip().lower():
                print(f"Znaleziono lekarza: {doctor.first_name} {doctor.last_name}")
                return doctor   
        print(f"Nie znaleziono lekarza {first_name} {last_name}.")
        return None
    

    # Aktualizacja danych lekarza
    def update_doctor(self, first_name, last_name, new_first_name, new_last_name, new_specialization):
        doctor = self.read_doctor(first_name, last_name)
    
    # Debugowanie: Wyświetl, co jest porównywane
        print(f"Szukane dane: {first_name} {last_name}")
        if doctor:
            print(f"Znaleziono lekarza: {doctor.first_name} {doctor.last_name}")
            if new_first_name:
                doctor.first_name = new_first_name
            if new_last_name:
                doctor.last_name = new_last_name
            if new_specialization:
                doctor.phone = new_specialization
           
            return print(f"Dane lekarza {first_name} {last_name} zostały zaktualizowane na następujące dane: {new_first_name}, {new_last_name}, {new_specialization}")
        else:
            print("Nie znaleziono lekarza!")
            print(f"Lista lekarzy: {[f'{doctor.first_name} {doctor.last_name}' for doctor in self.doctor]}")
            print("Nie można zaktualizować nieistniejącego lekarza.")

    
    # Miękkie usunięcie lekarza (soft delete)
    def soft_delete_doctor(self, first_name, last_name):
        doctor = self.read_doctor(first_name, last_name)
        if doctor:
            doctor.deleted = True
            print(f"Lekarz {doctor.first_name} {doctor.last_name} został oznaczony jako usunięty.")
        else:
            print("Nie można usunąć nieistniejącego lekarza.")

    
    # Dodawanie recepcjonistki
    def add_receptionist(self, first_name, last_name):
        receptionist = Receptionist(first_name, last_name)
        self.receptionist.append(receptionist)


    # Wyszukiwanie recepcjonistki
    def read_receptionist(self, first_name, last_name):
        for receptionist in self.receptionist:
            # print(f"Porównywanie: {receptionist.first_name.strip().lower()} {receptionist.last_name.strip().lower()} z {receptionist.strip().lower()} {receptionist.strip().lower()}")  # Debugowanie
            if receptionist.first_name.strip().lower() == first_name.strip().lower() and \
               receptionist.last_name.strip().lower() == last_name.strip().lower():
                print(f"Znaleziono recepcjonistkę: {receptionist.first_name} {receptionist.last_name}")
                return receptionist   
        print(f"Nie znaleziono recepcjonistki {first_name} {last_name}.")
        return None


    # Aktualizowanie danych recepcjonistki
    def update_receptionist(self, first_name, last_name, new_first_name, new_last_name):
            receptionist = self.read_receptionist(first_name, last_name)
            print(f"Szukane dane: {first_name} {last_name}")
            if receptionist:
                print(f"Znaleziono recepcjonistkę: {receptionist.first_name} {receptionist.last_name}")
                if new_first_name:
                    receptionist.first_name = new_first_name
                if new_last_name:
                    receptionist.last_name = new_last_name
            
                return print(f"Dane recepcjonistki {first_name} {last_name} zostały zaktualizowane na następujące dane: {new_first_name}, {new_last_name}")
            else:
                print("Nie znaleziono recepcjonistki!")
                print(f"Lista recepcjonistki: {[f'{receptionist.first_name} {receptionist.last_name}' for receptionist in self.receptionist]}")
                print("Nie można zaktualizować nieistniejącego recepcjonistki.")


    # Miękkie usunięcie recepcjonistki (soft delete)
    def soft_delete_receptionist(self, first_name, last_name):
        receptionist = self.read_receptionist(first_name, last_name)
        if receptionist:
            receptionist.deleted = True
            print(f"Recepcjonistka {receptionist.first_name} {receptionist.last_name} została oznaczona jako usunięta.")
        else:
            print("Nie można usunąć nieistniejącego recepcjonistki.")

    # Dodawanie wizyty
    def add_visit(self, date, pet, doctor, diagnosis):
        visit = Visit(date, pet, doctor, diagnosis)
        self.visits.append(visit)
        
    # Szukanie wizyty
    def read_visit(self, date, pet_name):
        for visit in self.visits:
            if visit.date == date and \
               visit.pet_name.strip().lower() == pet_name.strip().lower():
                print(F"Znaleziono wizytę: {visit.date} {visit.pet_name}")
                return visit
        print(f"Nie znaleziono wizyty: {visit.date} {visit.pet_name}")
        return None

    # Uaktualnianie wizyty
    def update_visit(self, date, pet_name, new_date, new_pet_name, new_doctor, new_diagnosis):
        visit = self.read_visit(date, pet_name)
        if visit:
            if new_date:
                visit.date = new_date
            if new_pet_name:
                visit.pet_name = new_pet_name
            if new_doctor:
                visit.doctor = new_doctor
            if new_diagnosis:
                visit.diagnosis = new_diagnosis
            print(f"Wizyta {date} {pet_name} została uaktualniona na następującą {new_date} {new_pet_name} {new_doctor} {new_diagnosis}")
            return visit
        else:
            print("Nie znaleziono wizyty!")
            return None

    # Usuwanie wizyty
    def soft_delete_visit(self, date, pet_name):
        visit = self.read_visit(date, pet_name)
        if visit:
            visit.deleted = True
            print(f"Wizyta {visit.date} {visit.pet_name} została oznaczona jako usunięta.")
        else:
            print("Nie można usunąć wizyty")

