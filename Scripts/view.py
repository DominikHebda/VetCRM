
def ask_for_client():
        first_name = input("Podaj imię właściciela: ")
        last_name = input("Podaj nazwisko właściciela: ")
        phone = input("Podaj telefon właściciela: ")
        address = input("Podaj adres właściciela: ")
        return first_name, last_name, phone, address

def ask_for_search_client():
        first_name = input("Podaj imię szukanego klienta: ")
        last_name = input("Podaj nazwisko szukanego klienta: ")
        return first_name, last_name

def ask_for_update_client():
        first_name = input("Podaj imię klienta do zaktualizowania: ")
        last_name = input("Podaj nazwisko klienta do zaktualizowania: ")
        new_first_name = input("Podaj nowe imię klienta: ")
        new_last_name = input("Podaj nowe nazwisko klienta: ")
        new_phone = input("Podaj nowy telefon klienta: ")
        new_address = input("Podaj nowy adres klienta: ")
        return first_name, last_name, new_first_name, new_last_name, new_phone, new_address
        
def ask_for_delete_client():
        first_name = input("Podaj imię klienta do usunięcia: ")
        last_name = input("Podaj nazwisko klienta do usunięcia: ")
        return first_name, last_name

def ask_for_pet():  
        pet_name = input("Podaj imię zwierzęcia: ")
        species = input("Podaj gatunek zwierzęcia: ")
        breed = input("Podaj rasę zwierzęcia: ")
        age = input("Podaj wiek zwierzęcia: ")
        return pet_name, species, breed, int(age)
       

def ask_for_search_pet():
        pet_name = input("Podaj nazwę zwierzęcia: ")
        species = input("Podaj gatunek zwierzęcia: ")
        return pet_name, species

def ask_for_update_pet():
        pet_name = input("Podaj nazwę zwierzęcia do zaktualizowania: ")
        species = input("Podaj gatunek zwierzęcia do zaktualizowania: ")
        new_pet_name = input("Podaj nową nazwę zwierzęcia: ")
        new_species = input("Podaj nowy gatunek zwierzęcia: ")
        new_breed = input("Podaj nową rasę zwierzęcia: ")
        new_age = input("Podaj nowy wiek zwierzęcia: ")
        return pet_name, species, new_pet_name, new_species, new_breed, new_age

def ask_for_delete_pet():
        pet_name = input("Podaj nazwę zwirzęcia do usunięcia: ")
        species = input("Podaj gatunek zwierzęcia do usunięcia: ")
        return pet_name, species

def ask_for_doctor():
        first_name = input("Podaj imię lekarza: ")
        last_name = input("Podaj nazwisko lekarza: ")
        specialization = input("Podaj specjalizacje lekarza: ")
        return first_name, last_name, specialization
       

def ask_for_search_doctor():
        first_name = input("Podaj imię szukanego klienta: ")
        last_name = input("Podaj nazwisko szukanego klienta: ")
        return first_name, last_name

def ask_for_update_doctor():
        first_name = input("Podaj imię lekarza do zaktualizowania: ")
        last_name = input("Podaj nazwisko lekarza do zaktualizowania: ")
        new_first_name = input("Podaj nowe imię lekarza: ")
        new_last_name = input("Podaj nowe nazwisko lekarza: ")
        new_specialization = input("Podaj nową specjalizację lekarza: ")
        return first_name, last_name, new_first_name, new_last_name, new_specialization

def ask_for_delete_doctor():
        first_name = input("Podaj imię lekarza do usunięcia: ")
        last_name = input("Podaj nazwisko lekarza do usunięcia: ")
        return first_name, last_name

def ask_for_receptionist():
        first_name = input("Podaj imię recepcjonistki: ")
        last_name = input("Podaj nazwisko recepcjonistki: ")
        return first_name, last_name
        

def ask_for_search_receptionist():
        first_name = input("Podaj imię szukanej recepcjonistki: ")
        last_name = input("Podaj nazwisko szukanej recepcjonistki: ")
        return first_name, last_name

def ask_for_update_receptionist():
        first_name = input("Podaj imię recepcjonistki do zaktualizowania: ")
        last_name = input("Podaj nazwisko recepcjonistki do zaktualizowania: ")
        new_first_name = input("Podaj nowe imię recepcjonistki: ")
        new_last_name = input("Podaj nowe nazwisko recepcjonistki: ")
        return first_name, last_name, new_first_name, new_last_name

def ask_for_delete_receptionist():
        first_name = input("Podaj imię recepcjonistki do usunięcia: ")
        last_name = input("Podaj nazwisko recepcjonistki do usunięcia: ")
        return first_name, last_name

def ask_for_visit():
        date = input("Data wizyty (yyyy-mm-dd): ")
        pet_name = input("Imię zwierzęcia: ")
        doctor = input("Imię lekarza: ")
        diagnosis = input("Diagnoza: ")
        return date, pet_name, doctor, diagnosis

def ask_for_search_visit():
        date = input("Podaj datę szukanej wizyty: ")
        pet_name = input("Podaj imię szukanego zwierzęcia: ")
        return date, pet_name

def ask_for_update_visit():
        date = input("Podaj datę wizyty do uaktualnienia: ")
        pet_name = input("Podaj nazwę zwierzęcia: ")
        new_date = input("Podaj nową datę wizyty: ")
        new_pet_name = input("Podaj nową nazwę zwierzęcia: ")
        new_doctor = input("Podaj nowe nazwisko lekarza: ")
        new_diagnosis = input("Podaj nową diagnozę: ")
        return date, pet_name, new_date, new_pet_name, new_doctor, new_diagnosis

def ask_for_delete_visit():
        date = input("Podaj datę wizyty do usunięcia: ")
        pet_name = input("Podaj nazwę zwierzęcia: ")
        return date, pet_name