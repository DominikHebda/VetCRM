import http.server
import socketserver

from vetcrm import VeterinaryCRM
import view

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Hello, World!")

PORT = 8000

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serwer działa na porcie {PORT}")
    httpd.serve_forever()



def main():
    crm = VeterinaryCRM()
    action = "Start"

    while action != "End":
        action = input("Co chcesz zrobić? [1, 2, 3, 4, 5, 6, 7, 8, End]")
            # 11 - Dodaj klienta
            # 12 - Odszukaj klienta
            # 13 - Zaktualizuj dane klienta
            # 14 - Usuń klienta

            # 21 - Dodaj zwierzę
            # 22 - Odszukaj zwierzę
            # 23 - Zaktualizuj dane zwierzęcia
            # 24 - Usuń zwierzę

            # 31 - Dodaj lekarza
            # 32 - Odszukaj lekarza
            # 33 - Zaktualizuj dane lekarza
            # 34 - Usuń lekarza

            # 41 - Dodaj recepcjonistkę
            # 42 - Odszukaj recepcjonistkę
            # 43 - Zaktualizuj dane recepcjonistkę
            # 44 - Usuń recepcjonistkę

            # 51 - Dodaj wizytę
            # 52 - Pokaż wizyty
            # 53 - Uaktualnij wizytę
            # 54 - Usuń wizytę

        # Client
        if action == "11":
            first_name, last_name, phone, addres, = view.ask_for_client()
            crm.add_client(first_name, last_name, phone, addres)
        elif action == "12":
            first_name, last_name = view.ask_for_search_client()
            crm.read_client(first_name, last_name)
        elif action == "13":
            first_name, last_name, new_first_name, new_last_name, new_phone, new_address = view.ask_for_update_client()
            crm.update_client(first_name, last_name, new_first_name, new_last_name, new_phone, new_address)
        elif action == "14":
            first_name, last_name = view.ask_for_delete_client()
            crm.soft_delete_client(first_name, last_name)

        # Pet
        elif action == "21":
            pet_name, species, breed, age, = view.ask_for_pet()
            crm.add_pet(pet_name, species, breed, age)
        elif action == "22":
           pet_name, species = view.ask_for_search_pet()
           crm.read_pet(pet_name, species)
        elif action == "23":
            pet_name, species, new_pet_name, new_species, new_breed, new_age = view.ask_for_update_pet()
            crm.update_pet(pet_name, species, new_pet_name, new_species, new_breed, new_age)
        elif action == "24":
            pet_name, species = view.ask_for_delete_pet()
            crm.soft_delete_pet(pet_name, species)

        # Doctor
        elif action == "31":
            first_name, last_name, specialization = view.ask_for_doctor()
            crm.add_doctor(first_name, last_name, specialization)
        elif action == "32":
            first_name, last_name = view.ask_for_search_doctor()
            crm.read_doctor(first_name, last_name)
        elif action == "33":
            first_name, last_name, new_first_name, new_last_name, new_specialization = view.ask_for_update_doctor()
            crm.update_doctor(first_name, last_name, new_first_name, new_last_name, new_specialization)
        elif action == "34":
            first_name, last_name= view.ask_for_delete_doctor()
            crm.soft_delete_doctor(first_name, last_name)

        # Receptionist
        elif action == "41":
            first_name, last_name = view.ask_for_receptionist()
            crm.add_receptionist(first_name, last_name)
        elif action == "42":
            first_name, last_name = view.ask_for_search_receptionist()
            crm.read_receptionist(first_name, last_name)
        elif action == "43":
            first_name, last_name, new_first_name, new_last_name = view.ask_for_update_receptionist()
            crm.update_receptionist(first_name, last_name, new_first_name, new_last_name)
        elif action == "44":
            first_name, last_name = view.ask_for_delete_receptionist()
            crm.soft_delete_receptionist(first_name, last_name)

        # Visit
        elif action == "51":
            date, pet_name, doctor, diagnosis = view.ask_for_visit()
            crm.add_visit(date, pet_name, doctor, diagnosis) 
        elif action == "52":
            date, pet_name = view.ask_for_search_visit()
            crm.read_visit(date, pet_name)
        elif action == "53":
            date, pet_name, new_date, new_pet_name, new_doctor, new_diagnosis = view.ask_for_update_visit()
            crm.update_visit(date, pet_name, new_date, new_pet_name, new_doctor, new_diagnosis)     
        elif action == "54":
            date, pet_name = view.ask_for_delete_visit()
            crm.soft_delete_visit(date, pet_name)


if __name__ == "__main__":
    main()

    