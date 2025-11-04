from Database.operations_visits import fetch_visits, find_visit, fetch_pets_for_client, update_visit, fetch_clients_to_visit, fetch_pets_to_visit, fetch_doctors_to_visit, add_visit, find_visit_by_id, soft_delete_visit, find_visits_by_client_id, find_visits_by_doctor_id, find_visits_by_pet_id, find_appointment_by_id, update_diagnosis, find_doctor_id_by_appointment_id, find_visit_details_by_id
from Database.operations_client import fetch_clients, add_client, find_client, find_client_by_id, update_client, soft_delete_client, find_client_to_details_by_id
from Database.operations_doctors import add_doctor, fetch_doctors, find_doctor_by_id, find_doctor, update_doctor, soft_delete_doctor, find_doctor_to_details_by_id
from Database.operations_pets import fetch_pets, add_pet, fetch_clients_to_indications, find_pet, find_pet_by_id, update_pet, soft_delete_pet, find_pets_by_client_id, find_pet_details_by_id, fetch_pet_owner_history
from Database.utils import paginate_list
from WebApp.Templates.clients_view import render_clients_list_page
from WebApp.Templates.client_view import render_client_details_page
from WebApp.Templates.doctors_view import render_doctors_list_page
from WebApp.Templates.doctor_view import render_doctor_details_page
from WebApp.Templates.pets_view import render_pets_list_page
from WebApp.Templates.pet_view import render_pet_details_page
from WebApp.Templates.visits_view import render_visits_list_page
from WebApp.Templates.visit_details import render_visit_details_page
from WebApp.Templates.edit_diagnosis_view import render_edit_diagnosis_page
from WebApp.Templates.pet_owner_history_view import render_pet_owner_history_page
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse, unquote, unquote_plus
import traceback  
import logging
import os


logging.basicConfig(level=logging.DEBUG)  # Ustawienie poziomu logowania na DEBUG


def render_home_page():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        home_page_html = f.read()
    
    return home_page_html

def render_add_next_visit():
    with open("templates/adding_visit.html", "r", encoding="utf-8") as f:
        add_next_visit_html = f.read()
    
    return add_next_visit_html

def render_add_client():
    with open("templates/adding_client.html", "r", encoding="utf-8") as f:
        add_client_html = f.read()

    return add_client_html

def render_add_doctor():
    with open("templates/adding_doctors.html", "r", encoding="utf-8") as f:
        add_doctor_form_html = f.read()

    return add_doctor_form_html

def render_add_pet():
    # Pobierz klientów
    clients = fetch_clients_to_indications()
    client_options = ""
    for client_id, first_name, last_name in clients:
        client_options += f'<option value="{client_id}">{first_name} {last_name}</option>'

    # Wczytaj HTML szablon
    template_path = os.path.join(os.getcwd(), 'Templates', 'adding_pet.html')
    with open(template_path, 'r', encoding='utf-8') as file:
        html = file.read()

    # Podmień placeholder
    html = html.replace("{{ client_options }}", client_options)
    return html

def render_add_visit(client_id=None):
    print(f"render_add_visit: client_id = {client_id}")
    clients = fetch_clients_to_visit()
    print(f"Liczba klientów: {len(clients)}")
    doctors = fetch_doctors_to_visit()
    print(f"Liczba lekarzy: {len(doctors)}")

    # Generujemy listę klientów do selecta
    client_options = "".join(
        [f"<option value='{c[0]}' {'selected' if client_id == c[0] else ''}>{c[1]} {c[2]}</option>" for c in clients]
    )

    # Jeśli podano client_id, pobieramy tylko zwierzęta tego klienta
    if client_id:
        pets = fetch_pets_to_visit(client_id)
    else:
        pets = []

    # Generujemy listę zwierząt do selecta
    pet_options = "".join([f"<option value='{p[0]}'>{p[1]}</option>" for p in pets])

    # Lista lekarzy
    doctor_options = "".join([f"<option value='{d[0]}'>{d[1]} {d[2]}</option>" for d in doctors])

    # Wczytanie szablonu HTML
    template_path = os.path.join(os.getcwd(), "Templates", "adding_visit.html")
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Podstawienie danych do HTML
    html = html.replace("{{ client_options }}", client_options)
    html = html.replace("{{ pet_options }}", pet_options)
    html = html.replace("{{ doctor_options }}", doctor_options)

    return html


def render_search_client():
    with open("templates/searching_client.html", "r", encoding="utf-8") as f:
        search_client_html = f.read()

    return search_client_html

def render_search_doctor():
    with open("templates/searching_doctor.html", "r", encoding="utf-8") as f:
        search_doctor_html = f.read()

    return search_doctor_html

def render_search_pet():
    with open("templates/searching_pet.html", "r", encoding="utf-8") as f:
        search_pet_html = f.read()

    return search_pet_html

def render_search_visit():
    with open("templates/searching_visit.html", "r", encoding="utf-8") as f:
        search_visit_html = f.read()

    return search_visit_html

def render_update_client():
    with open("templates/update_client", "r", encoding="utf-8") as f:
        update_client_html = f.read()

    return update_client_html

def render_update_doctor():
    with open("templates/update_doctor", "r", encoding="utf-8") as f:
        update_doctor_html = f.read()
    
    return update_doctor_html

def render_update_pet(pet_data):
    clients = fetch_clients_to_indications()
    client_options = ""
    for client_id, first_name, last_name in clients:
        selected = "selected" if client_id == pet_data["client_id"] else ""
        client_options += f'<option value="{client_id}" {selected}>{first_name} {last_name}</option>'

    # Wczytaj HTML szablon
    template_path = os.path.join(os.getcwd(), 'Templates', 'update_pet.html')
    with open(template_path, 'r', encoding='utf-8') as file:
        html = file.read()

    # Podmień placeholdery danych zwierzęcia
    for key, value in pet_data.items():
        html = html.replace(f"{{{{ {key} }}}}", str(value))

    # Podmień listę właścicieli
    html = html.replace("{{ client_options }}", client_options)

    return html

def render_visit_deleted(visit_id):
    with open("templates/visit_deleted.html", "r", encoding="utf-8") as f:
        visit_deleted_html = f.read()

    return visit_deleted_html

def render_home_page():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        home_page_html = f.read()
    
    return home_page_html


# ####################              do_GET              #####################################################


class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        print(f"Requested path: {self.path}") 
        print(globals().get('urlparse'))
        print(f"urlparse w do_GET: {urlparse}")


########################    WYŚWIETLANIE STRONY POWITALNEJ  ################

       # ###################   STRONA GŁÓWNA (index.html)   ##########################

        if self.path == "/":
            # Przekierowanie z "/" na "/index.html"
            self.send_response(303)
            self.send_header("Location", "/index.html")
            self.end_headers()

        elif self.path in ("/index", "/index.html"):
            try:
                home_page_html = render_home_page()
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(home_page_html.encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(f"<p>Błąd: {e}</p>".encode("utf-8"))



#######################    LISTA KLIENTÓW  #######################

        elif self.path.startswith("/clients_list/"):

            query = urlparse(self.path).query
            params = parse_qs(query)
            page = int(params.get("page", [1])[0])

            clients = fetch_clients()
            paginated_clients, total_pages = paginate_list(clients, page, 20)

            html_content = render_clients_list_page(paginated_clients, page, total_pages)

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html_content.encode("utf-8"))



#######################    SZCZEGÓŁY WYBRANEGO KLIENTA #######################

        elif self.path.startswith("/client_details/"):
            client_id = int(self.path.split("/")[-1])
            client = find_client_to_details_by_id(client_id)  
            pets = find_pets_by_client_id(client_id)  
            visits = find_visits_by_client_id(client_id)  
            html = render_client_details_page(client, pets, visits)

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))


#######################    LISTA LEKARZY  #######################

        elif self.path.startswith("/doctors_list/"):

            query = urlparse(self.path).query
            params = parse_qs(query)
            page = int(params.get("page", [1])[0])

            doctors = fetch_doctors()
            paginated_doctors, total_pages = paginate_list(doctors, page, 20)

            html_content = render_doctors_list_page(paginated_doctors, page, total_pages)

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html_content.encode("utf-8"))



#######################    SZCZEGÓŁY WYBRANEGO LEKARZA #######################


        elif self.path.startswith("/doctor_details/"):
            doctor_id = int(self.path.split("/")[-1])
            doctor = find_doctor_to_details_by_id(doctor_id)
            visits = find_visits_by_doctor_id(doctor_id)
            html = render_doctor_details_page(doctor, visits)

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))


#######################     EDYCJA/WPISANIE DIAGNOZY W WIDOKU LEKARZA #######################


        elif self.path.startswith("/edit_diagnosis/"):
            appointment_id = int(self.path.split("/")[-1])
            appointment = find_appointment_by_id(appointment_id)
            print("DEBUG appointment:", appointment)
            if appointment:
                doctor_id = appointment[4]  # kolumna doctor_id z bazy
                current_diagnosis = appointment[5]  # diagnoza
                html = render_edit_diagnosis_page(appointment_id, doctor_id, current_diagnosis)
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(html.encode("utf-8"))
            else:
                self.send_error(404, "Appointment not found")



#######################    LISTA ZWIERZĄT  #######################

        elif self.path.startswith("/pets_list/"):
            
            query = urlparse(self.path).query
            params = parse_qs(query)
            page = int(params.get("page", [1])[0])

            pets = fetch_pets()
            paginated_pets, total_pages = paginate_list(pets, page, 20)

            html_content = render_pets_list_page(paginated_pets, page, total_pages)

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html_content.encode("utf-8"))




#######################    SZCZEGÓŁY WYBRANEGO ZWIERZECIA #######################


        elif self.path.startswith("/pet_details/"):

            pet_id = int(self.path.split("/")[-1])
            print(f"\nRequested path: {self.path}")
            print(f"DEBUG: Szukam szczegółów dla zwierzęcia o ID = {pet_id}")

            pet = find_pet_details_by_id(pet_id)
            if pet is None:
                self.send_response(404)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(f"<h1>Nie znaleziono zwierzęcia.</h1>")
                return

            # 🔹 Rozpakowanie danych zwierzęcia zgodnie z Twoją strukturą tabeli:
            # id, pet_name, species, breed, age, soft_delete, client_id
            pet_id, pet_name, species, breed, age, soft_delete, client_id = pet
            print(f"DEBUG: Dane zwierzęcia -> ID={pet_id}, Imię={pet_name}, KlientID={client_id}")

            # 🔹 Pobranie właściciela po client_id
            client = None
            if client_id:
                print(f"DEBUG: Próba pobrania właściciela o ID={client_id}")
                client = find_client_to_details_by_id(client_id)
                print(f"DEBUG: Wynik zapytania klienta: {client}")
            else:
                print("⚠️ Brak przypisanego właściciela w rekordzie zwierzęcia!")

            # 🔹 Pobranie listy wizyt
            visits = find_visits_by_pet_id(pet_id)
            print(f"DEBUG: Liczba znalezionych wizyt = {len(visits) if visits else 0}")

            # 🔹 Wyrenderowanie strony
            html = render_pet_details_page(pet, client, visits)

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))


#######################    HISTORIA ZMIANY WŁAŚCICIELI ZWIERZĄT  #######################

        elif self.path.startswith("/pet_owner_history/"):
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            page = int(query_params.get("page", [1])[0])  # domyślnie 1
            
            history = fetch_pet_owner_history()
            history_page, total_pages = paginate_list(history, page=page, per_page=20)
            
            html = render_pet_owner_history_page(history_page, page, total_pages)
            

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))



#######################    LISTA WIZYT  #######################


        elif self.path.startswith("/visits_list"):

            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            page = int(query_params.get("page", [1])[0])  # domyślnie 1

            visits = fetch_visits()
            visits_page, total_pages = paginate_list(visits, page=page, per_page=20)

            # generujemy stronę HTML
            html = render_visits_list_page(visits_page, page, total_pages)

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))



#######################    SZCZEGÓŁY WYBRANEJ WIZYTY #######################


        elif self.path.startswith("/visit_details/"):
            appointment_id = int(self.path.split("/")[-1])
            print(f"\nRequested path: {self.path}")
            print(f"DEBUG: Szukam szczegółów wizyty ID = {appointment_id}")

            appointment = find_visit_details_by_id(appointment_id)
            if appointment is None:
                self.send_response(404)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("<h1>Nie znaleziono wizyty.</h1>".encode("utf-8"))
                return

            # Pobranie powiązanych rekordów
            client_id = appointment[1]
            pet_id = appointment[2]
            doctor_id = appointment[3]

            client = find_client_to_details_by_id(client_id) if client_id else None
            pet = find_pet_details_by_id(pet_id) if pet_id else None
            doctor = find_doctor_to_details_by_id(doctor_id) if doctor_id else None

            print(f"DEBUG: client={client}, pet={pet}, doctor={doctor}")

            html = render_visit_details_page(appointment, client, pet, doctor)

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))


########################    DODAWANIE KLIENTA  ################
    

        elif self.path == "/adding_client/":
            print(f"Handling GET request for {self.path}") 
            add_client_html = render_add_client()  
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(add_client_html.encode('utf-8'))


########################    DODAWANIE LEKARZA  ################
    

        elif self.path == "/adding_doctors/":
            print(f"Handling GET request for {self.path}") 
            add_doctor_html = render_add_doctor()  
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(add_doctor_html.encode('utf-8'))



########################    DODAWANIE ZWIERZĘCIA  ################
    

        elif self.path == "/adding_pet/":
            print(f"Handling GET request for {self.path}") 
            add_pet_html = render_add_pet()  
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(add_pet_html.encode('utf-8'))


########################    DODAWANIE WIZYTY      ################



        elif self.path.startswith("/adding_visit/"):
            try:
                parsed_url = urlparse(self.path)
                query_params = parse_qs(parsed_url.query)
                client_id_str = query_params.get('client_id', [None])[0]
                print(f"client_id_str: {client_id_str}")

                try:
                    client_id = int(client_id_str) if client_id_str and client_id_str.isdigit() else None
                except ValueError:
                    client_id = None
                    print(f"Niepoprawny client_id: {client_id_str}")


                html = render_add_visit(client_id)

                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(html.encode("utf-8"))

            except Exception as e:
                print("Błąd w obsłudze /adding_visit/:")
                print(traceback.format_exc())

                self.send_response(500)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                error_message = f"<h1>Błąd:</h1><pre>{traceback.format_exc()}</pre>"
                self.wfile.write(error_message.encode("utf-8"))



########################    WYSZUKIWANIE KLIENTA  ################

        elif self.path == "/searching_client/":
            search_client_html = render_search_client()  
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(search_client_html.encode('utf-8'))



########################    WYSZUKIWANIE LEKARZA ################

        elif self.path == "/searching_doctor/":
            search_doctor_html = render_search_doctor()  
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(search_doctor_html.encode('utf-8'))


########################    WYSZUKIWANIE ZWIERZĘCIA ################

        elif self.path == "/searching_pet/":
            search_pet_html = render_search_pet()  
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(search_pet_html.encode('utf-8'))


########################    WYSZUKIWANIE WIZYTY      ################

        elif self.path == "/searching_visit/":
            search_pet_html = render_search_visit()  
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(search_pet_html.encode('utf-8'))

########################    UAKTUALNIAMY DANE KLIENTA  ################


        elif self.path.startswith("/update_client/"):
            # Zakładając, że client_id jest częścią ścieżki URL
            client_id = self.path.split("/")[2]  # Wyciągamy client_id z URL

            # Sprawdzamy, czy klient istnieje na podstawie ID
            client = find_client_by_id(client_id)  # Wywołujemy find_client_by_id, która oczekuje client_id

            if client:
                # Przygotowujemy dane klienta do przekazania do szablonu
                client_data = {
                    "client_id": client[0],
                    "first_name": client[1],
                    "last_name": client[2],
                    "phone": client[3],
                    "address": client[4]
                }

                # Wczytanie szablonu HTML
                try:
                    template_path = os.path.join(os.path.dirname(__file__), 'Templates', 'update_client.html')
                    print(f"Template path: {template_path}")  # Dodajemy logowanie ścieżki

                    if os.path.exists(template_path):
                        with open(template_path, "r", encoding="utf-8") as f:
                            template = f.read()
                        
                        # Zastępujemy zmienne w szablonie
                        for key, value in client_data.items():
                            template = template.replace(f"{{{{ {key} }}}}", str(value))

                        # Wysyłamy odpowiedź z HTML
                        self.send_response(200)
                        self.send_header("Content-type", "text/html; charset=utf-8")
                        self.end_headers()
                        self.wfile.write(template.encode('utf-8'))
                    else:
                        self.send_error(404, "Plik szablonu nie znaleziony")
                except FileNotFoundError:
                    self.send_error(404, "Plik szablonu nie znaleziony")
            else:
                self.send_error(404, "Klient nie znaleziony")


########################    UAKTUALNIAMY DANE LEKARZA  ################


        elif self.path.startswith("/update_doctor/"):
                    # Zakładając, że doctor_id jest częścią ścieżki URL
                    doctor_id = self.path.split("/")[2]  # Wyciągamy doctor_id z URL

                    # Sprawdzamy, czy doktor istnieje na podstawie ID
                    doctor = find_doctor_by_id(doctor_id)  # Wywołujemy find_doctor, która oczekuje doctor_id

                    if doctor:
                        # Przygotowujemy dane doktora do przekazania do szablonu
                        doctor_data = {
                            "doctor_id": doctor[0],
                            "first_name": doctor[1],
                            "last_name": doctor[2],
                            "specialization": doctor[3],
                            "phone": doctor[4]
                        }

                        # Wczytanie szablonu HTML
                        try:
                            template_path = os.path.join(os.path.dirname(__file__), 'Templates', 'update_doctor.html')
                            print(f"Template path: {template_path}")  # Dodajemy logowanie ścieżki

                            if os.path.exists(template_path):
                                with open(template_path, "r", encoding="utf-8") as f:
                                    template = f.read()
                                
                                # Zastępujemy zmienne w szablonie
                                for key, value in doctor_data.items():
                                    template = template.replace(f"{{{{ {key} }}}}", str(value))

                                # Wysyłamy odpowiedź z HTML
                                self.send_response(200)
                                self.send_header("Content-type", "text/html; charset=utf-8")
                                self.end_headers()
                                self.wfile.write(template.encode('utf-8'))
                            else:
                                self.send_error(404, "Plik szablonu nie znaleziony")
                        except FileNotFoundError:
                            self.send_error(404, "Plik szablonu nie znaleziony")
                    else:
                        self.send_error(404, "Doctor nie znaleziony")


########################    UAKTUALNIAMY DANE ZWIERZĘCIA     ################


        elif self.path.startswith("/update_pet/"):
                    # Zakładając, że pet_id jest częścią ścieżki URL
                    pet_id = self.path.split("/")[2]  # Wyciągamy pet_id z URL

                    # Sprawdzamy, czy zwierzę istnieje na podstawie ID
                    pet = find_pet_by_id(pet_id)  # Wywołujemy find_pet_by_id, która oczekuje pet_id

                    if pet:
                        # Przygotowujemy dane zwierzęcia do przekazania do szablonu
                        pet_data = {
                            "pet_id": pet[0],
                            "pet_name": pet[1],
                            "species": pet[2],
                            "breed": pet[3],
                            "age": pet[4],
                            "client_id": pet[6]
                        }

                        # Wczytanie szablonu HTML
                        try:
                            template_path = os.path.join(os.path.dirname(__file__), 'Templates', 'update_pet.html')
                            print(f"Template path: {template_path}")  # Dodajemy logowanie ścieżki

                            if os.path.exists(template_path):
                                with open(template_path, "r", encoding="utf-8") as f:
                                    template = f.read()
                                
                                # Zastępujemy zmienne w szablonie
                                for key, value in pet_data.items():
                                    template = template.replace(f"{{{{ {key} }}}}", str(value))

                                html = render_update_pet(pet_data)

                                self.send_response(200)
                                self.send_header("Content-type", "text/html; charset=utf-8")
                                self.end_headers()
                                self.wfile.write(html.encode("utf-8"))

                            else:
                                self.send_error(404, "Plik szablonu nie znaleziony")
                        except FileNotFoundError:
                            self.send_error(404, "Plik szablonu nie znaleziony")
                    else:
                        self.send_error(404, "Zwierzę nie znaleziony")            


#########################   UAKTUALNIAMY DANE WIZYTY    ##########################################

        elif self.path.startswith("/update_visit/"):

            parsed_url = urlparse(self.path)
            path_parts = parsed_url.path.split("/")
            visit_id = path_parts[2]

            # Wczytaj dane wizyty
            visit = find_visit_by_id(visit_id)

            if visit:
                # Rozpakuj dane
                visit_data = {
                    "visit_id": visit[0],
                    "created_at": visit[1],
                    "client_id": visit[2],
                    "pet_id": visit[3],
                    "doctor_id": visit[4],
                    "visit_date": visit[5],
                    "visit_time": visit[6]
                }

                # Obsłuż ręczne nadpisanie client_id z query string
                query_params = parse_qs(parsed_url.query)
                if "client_id" in query_params:
                    visit_data["client_id"] = int(query_params["client_id"][0])

                # Pobierz dane do selectów
                clients = fetch_clients()
                pets = fetch_pets_for_client(visit_data["client_id"])  # ważne!
                doctors = fetch_doctors()

                # Buduj selecty
                client_options = ""
                for client in clients:
                    selected = "selected" if str(client[0]) == str(visit_data["client_id"]) else ""
                    full_name = f"{client[1]} {client[2]}"
                    client_options += f'<option value="{client[0]}" {selected}>{full_name}</option>\n'

                pet_options = ""
                for pet in pets:
                    selected = "selected" if str(pet[0]) == str(visit_data["pet_id"]) else ""
                    pet_options += f'<option value="{pet[0]}" {selected}>{pet[1]}</option>\n'

                doctor_options = ""
                for doctor in doctors:
                    selected = "selected" if str(doctor[0]) == str(visit_data["doctor_id"]) else ""
                    full_name = f"{doctor[1]} {doctor[2]}"
                    doctor_options += f'<option value="{doctor[0]}" {selected}>{full_name}</option>\n'

                # Załaduj template i podmień dane
                try:
                    template_path = os.path.join(os.path.dirname(__file__), 'Templates', 'update_visit.html')

                    with open(template_path, "r", encoding="utf-8") as f:
                        template = f.read()

                    for key, value in visit_data.items():
                        template = template.replace(f"{{{{ {key} }}}}", str(value))

                    template = template.replace("{{ client_options }}", client_options)
                    template = template.replace("{{ pet_options }}", pet_options)
                    template = template.replace("{{ doctor_options }}", doctor_options)

                    self.send_response(200)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(template.encode("utf-8"))

                except FileNotFoundError:
                    self.send_error(404, "Plik szablonu nie znaleziony")
            else:
                self.send_error(404, "Wizyta nie znaleziona")


#########################   WYŚWIETLAMY KOMUNIKAT O ZAKTUALIZOWANEJ WIZYCIE   ##########################################


        elif self.path.startswith("/visit_updated/"):
            parsed_url = urlparse(self.path)
            visit_id = parsed_url.path.split("/")[-1]

            try:
                template_path = os.path.join(os.path.dirname(__file__), 'Templates', 'visit_updated.html')
                with open(template_path, "r", encoding="utf-8") as f:
                    template = f.read()

                # Podmień ID w linku powrotu
                template = template.replace("{{ visit_id }}", visit_id)

                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(template.encode("utf-8"))

            except FileNotFoundError:
                self.send_error(404, "Plik szablonu visit_updated.html nie znaleziony")

#########################   WYŚWIETLAMY KOMUNIKAT O USUNIĘCIU WIZYTY       ##########################################

        elif self.path.startswith("/visit_deleted/"):
            try:
                visit_deleted_html = render_visit_deleted("visit_deleted.html")  # np. prosty szablon potwierdzenia
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(visit_deleted_html.encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(f"<p>Błąd: {e}</p>".encode("utf-8"))



########################    DODAWANIE NOWEJ WIZYTY  ################

        elif self.path.startswith("/add_next_visit/"):
            try:
                add_next_visit_html = render_add_next_visit()
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset+utf-8")
                self.end_headers()
                self.wfile.write(add_next_visit_html.encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(f"<p>Błąd: {e}".encode("utf-8"))



# ###################       USUWAMY KLIENTA - SOFT DELETE       ##########################


        elif self.path.startswith("/delete_client/"):
                client_id = self.path.split('/')[-1]  # Pobieramy ID klienta z URL

                # Usuwamy klienta (soft delete) z bazy danych
                try:
                    soft_delete_client(client_id)  # Funkcja, która oznacza klienta jako usuniętego
                    # Przekierowanie na stronę z listą klientów po usunięciu
                    self.send_response(303)  # Kod statusu: See Other (przekierowanie)
                    self.send_header('Location', '/clients_list/')  # Przekierowanie do listy klientów
                    self.end_headers()

                except Exception as e:
                    # Obsługa błędów, np. klient nie został znaleziony
                    self.send_response(500)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    error_message = f"Error deleting client: {e}"
                    self.wfile.write(error_message.encode('utf-8'))


# ###################       USUWAMY LEKARZA - SOFT DELETE       ##########################


        elif self.path.startswith("/delete_doctor/"):
                doctor_id = self.path.split('/')[-1]  # Pobieramy ID lekarza z URL

                # Usuwamy lekarza (soft delete) z bazy danych
                try:
                    soft_delete_doctor(doctor_id)  # Funkcja, która oznacza lekarza jako usuniętego
                    # Przekierowanie na stronę z listą lekarzy po usunięciu
                    self.send_response(303)  # Kod statusu: See Other (przekierowanie)
                    self.send_header('Location', '/doctors_list/')  # Przekierowanie do listy lekarzy
                    self.end_headers()

                except Exception as e:
                    # Obsługa błędów, np. lekarza nie został znaleziony
                    self.send_response(500)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    error_message = f"Error deleting client: {e}"
                    self.wfile.write(error_message.encode('utf-8'))



# ###################       USUWAMY ZWIERZĘ - SOFT DELETE       ##########################


        elif self.path.startswith("/delete_pet/"):
                pet_id = self.path.split('/')[-1]  # Pobieramy ID zwierzęcia z URL

                # Usuwamy zwierzę (soft delete) z bazy danych
                try:
                    soft_delete_pet(pet_id)  # Funkcja, która oznacza zwierzę jako usunięte
                    # Przekierowanie na stronę z listą zwierząt po usunięciu
                    self.send_response(303)  # Kod statusu: See Other (przekierowanie)
                    self.send_header('Location', '/pets_list/')  # Przekierowanie do listy zwierząt
                    self.end_headers()

                except Exception as e:
                    # Obsługa błędów, np. zwierzę nie zostało znalezione
                    self.send_response(500)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    error_message = f"Error deleting pet: {e}"
                    self.wfile.write(error_message.encode('utf-8'))


# ###################       USUWAMY WIZYTĘ - SOFT DELETE       ##########################


        elif self.path.startswith("/delete_visit/"):
                visit_id = int(self.path.split('/')[-1])  

                try:
                    soft_delete_visit(visit_id)  # Funkcja, która oznacza wizytę jako usunięte
                    self.send_response(303) 
                    self.send_header('Location', '/visit_deleted/')  # Przekierowanie do listy wizyt
                    self.end_headers()

                except Exception as e:
                    # Obsługa błędów, np. wizyta nie zostało znalezione
                    self.send_response(500)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    error_message = f"Error deleting visit: {e}"
                    self.wfile.write(error_message.encode('utf-8'))

        else:
            super().do_GET()


# #########################             do_POST             ###########################################


    def do_POST(self):

        if self.path.startswith("/visits_table/"):
            try:
                # Odczyt danych z formularza
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode('utf-8')

                # Rozbicie danych na parametry
                data = {item.split('=')[0]: unquote(item.split('=')[1]) for item in post_data.split('&')}
                print(f"Received POST data: {data}")  # Logowanie danych z formularza

                # Przetwarzanie danych
                # W zależności od tego, co robisz z tymi danymi, np. zapis do bazy danych
                # Jeśli dane są poprawne, wykonaj odpowiednią akcję (np. edytuj wizytę)
                if "visit_id" in data:
                    visit_id = data["visit_id"]
                    # Edytuj wizytę lub wykonaj jakąś akcję związaną z wizytą
                    # Możesz tu wywołać jakąś funkcję aktualizującą bazę danych lub model
                    
                    self.send_response(302)  # 302 - Przekierowanie po udanej operacji
                    self.send_header('Location', '/visits_table/')  # Przekierowanie na stronę z listą wizyt
                    self.end_headers()

                else:
                    # Obsługa przypadku, kiedy brak wymaganych danych (np. brak visit_id)
                    self.send_response(400)  # 400 - Błędne żądanie
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(f"<p>Błąd: brak wymaganych danych.</p>")

            except Exception as e:
                self.send_response(500)  # 500 - Błąd serwera
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(f"<p>Błąd: {e}".encode("utf-8"))





###################     DODAJEMY NOWEGO KLIENTA      ##################################

        elif self.path == "/adding_client/":
            # Odczytujemy dane POST
            content_length = int(self.headers.get('Content-Length'))
            post_data = self.rfile.read(content_length)
            post_data = post_data.decode('utf-8')

            # Tworzymy słownik z danymi
            data = {item.split('=')[0]: unquote_plus(item.split('=')[1]) for item in post_data.split('&')}

            # Wywołanie metody obsługującej dodanie klienta
            self.handle_add_client_post(data)


###############         DODAJEMY NOWEGO LEKARZA         ###########################


        elif self.path == "/adding_doctors/":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = post_data.decode('utf-8')

            print("RAW post_data:")
            print(post_data)

            data = {item.split('=')[0]: unquote_plus(item.split('=')[1]) for item in post_data.split('&')}
            
            print("Parsed data:")
            print(data)

            print(post_data)  # Sprawdzić, co jest przesyłane
            self.handle_add_doctor_post(data)


###############         DODAJEMY DIAGNOZĘ W SZCZEGÓŁACH LEKARZA         ###########################


        elif self.path.startswith("/update_diagnosis/"):
            appointment_id = int(self.path.split("/")[-1])
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')

            # Prosty parser danych formularza
            form = parse_qs(post_data)
            diagnosis = form.get("diagnosis", [""])[0]

            update_diagnosis(appointment_id, diagnosis)

            # Po zapisie przekierowanie z powrotem
            self.send_response(303)
            self.send_header("Location", f"/doctor_details/{find_doctor_id_by_appointment_id(appointment_id)}")
            self.end_headers()




###############         DODAJEMY NOWE ZWIERZĘ         ###########################


        elif self.path == "/adding_pet/":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = post_data.decode('utf-8')

            print("RAW post_data:")
            print(post_data)

            data = {item.split('=')[0]: unquote_plus(item.split('=')[1]) for item in post_data.split('&')}
            
            print("Parsed data:")
            print(data)

            print(post_data)  # Sprawdzić, co jest przesyłane
            self.handle_add_pet_post(data)


###############         DODAJEMY NOWĄ WIZYTĘ        ###########################


        elif self.path == "/adding_visit/":
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode("utf-8")
                data = parse_qs(post_data)

                client_id = int(data.get("client_id", [0])[0])
                pet_id = int(data.get("pet_id", [0])[0])
                doctor_id = int(data.get("doctor_id", [0])[0])
                visit_date = data.get("visit_date", [""])[0]
                visit_time = data.get("visit_time", [""])[0]

                print(f"Dane do zapisu wizyty: {client_id=}, {pet_id=}, {doctor_id=}, {visit_date=}, {visit_time=}")
                if visit_time and len(visit_time) == 5:
                    visit_time += ":00"  # "20:05" → "20:05:00"

                # Wywołanie funkcji dodającej wizytę do bazy
                add_visit(client_id, pet_id, doctor_id, visit_date, visit_time)
                if not all([client_id, pet_id, doctor_id, visit_date, visit_time]):
                    raise ValueError("Niekompletne dane wizyty - uzupełnij wszystkie pola.")

                # Potwierdzenie
                self.send_response(303)  # redirect after post
                self.send_header("Location", "/visits_list/")
                self.end_headers()

            except Exception as e:
                import traceback
                print(traceback.format_exc())
                self.send_response(500)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(f"<h1>Błąd zapisu wizyty:</h1><pre>{e}</pre>".encode("utf-8"))


                

###################     WYSZUKUJEMY KLIENTA      ##################################

        elif self.path == "/searching_client/":
            content_length = int(self.headers.get('Content-Length'))
            post_data = self.rfile.read(content_length)
            data = {item.split('=')[0]: unquote_plus(item.split('=')[1]) for item in post_data.decode('utf-8').split('&')}

            # Pobierz dane z formularza
            first_name = data.get('first_name', '')
            last_name = data.get('last_name', '')

            # Upewnij się, że wartości zostały przypisane
            if not first_name or not last_name:
                self.send_error(400, "Brak wymaganych danych (first_name, last_name).")
                return

            clients = find_client(first_name, last_name)

            if clients:
                # Jeśli znaleziono klientów, wyświetlamy tabelę
                # Wczytaj widok HTML
                with open("templates/output_searching_client.html", "r", encoding="utf-8") as file:
                    html_content = file.read()

                # Generowanie wierszy dla każdego klienta
                clients_rows = ""
                for client in clients:
                    # Generowanie wiersza z danymi klienta
                    client_row = f"""
                        <tr>
                            <td>{client[0]}</td>
                            <td>{client[1]}</td>
                            <td>{client[2]}</td>
                            <td>{client[3]}</td>
                            <td>{client[4]}</td>
                            <td>
                                <div class="btn-group">
                                    <a href="/update_client/{client[0]}" class="btn btn-edit">Edytuj</a>
                                    <a href="/delete_client/{client[0]}" class="btn btn-danger">Usuń</a>
                                </div>
                            </td>
                        </tr>
                    """
                    clients_rows += client_row  # Dodajemy wiersz do tabeli

                # Zastąpienie zmiennych w szablonie
                html_content = html_content.replace("{{ client_rows }}", clients_rows)

                # Wyślij odpowiedź HTML z danymi klientów
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(html_content.encode('utf-8'))
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("<p>Nie znaleziono klientów.</p>".encode('utf-8'))



###################     WYSZUKUJEMY LEKARZA    ##################################

        elif self.path == "/searching_doctor/":
            content_length = int(self.headers.get('Content-Length'))
            post_data = self.rfile.read(content_length)
            data = {item.split('=')[0]: unquote_plus(item.split('=')[1]) for item in post_data.decode('utf-8').split('&')}

            # Pobierz dane z formularza
            first_name = data.get('first_name', '')
            last_name = data.get('last_name', '')

            # Upewnij się, że wartości zostały przypisane
            if not first_name or not last_name:
                self.send_error(400, "Brak wymaganych danych (first_name, last_name).")
                return

            doctors = find_doctor(first_name, last_name)

            if doctors:
                # Jeśli znaleziono klientów, wyświetlamy tabelę
                # Wczytaj widok HTML
                with open("templates/output_searching_doctor.html", "r", encoding="utf-8") as file:
                    html_content = file.read()

                # Generowanie wierszy dla każdego klienta
                doctors_rows = ""
                for doctor in doctors:
                    # Generowanie wiersza z danymi klienta
                    doctor_row = f"""
                        <tr>
                            <td>{doctor[0]}</td>
                            <td>{doctor[1]}</td>
                            <td>{doctor[2]}</td>
                            <td>{doctor[3]}</td>
                            <td>{doctor[4]}</td>
                            <td>
                                <div class="btn-group">
                                    <a href="/update_doctor/{doctor[0]}" class="btn btn-edit">Edytuj</a>
                                    <a href="/delete_doctor/{doctor[0]}" class="btn btn-danger">Usuń</a>
                                </div>
                            </td>
                        </tr>
                    """
                    doctors_rows += doctor_row  # Dodajemy wiersz do tabeli

                # Zastąpienie zmiennych w szablonie
                html_content = html_content.replace("{{ doctor_rows }}", doctors_rows)

                # Wyślij odpowiedź HTML z danymi klientów
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(html_content.encode('utf-8'))
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("<p>Nie znaleziono klientów.</p>".encode('utf-8'))



###################     WYSZUKUJEMY ZWIERZĘ    ##################################

        elif self.path == "/searching_pet/":
            content_length = int(self.headers.get('Content-Length'))
            post_data = self.rfile.read(content_length)
            data = {item.split('=')[0]: unquote_plus(item.split('=')[1]) for item in post_data.decode('utf-8').split('&')}

            # Pobierz dane z formularza
            pet_name = data.get('pet_name', '')
            species = data.get('species', '')

            # Upewnij się, że wartości zostały przypisane
            if not pet_name or not species:
                self.send_error(400, "Brak wymaganych danych (pet_name, species).")
                return

            pets = find_pet(pet_name, species)

            if pets:
                # Jeśli znaleziono zwierzęta, wyświetlamy tabelę
                # Wczytaj widok HTML
                with open("templates/output_searching_pet.html", "r", encoding="utf-8") as file:
                    html_content = file.read()

                # Generowanie wierszy dla każdego zwierzęcia
                pets_rows = ""
                for pet in pets:
                    deletion_date = pet[5].strftime('%Y-%m-%d %H:%M:%S') if pet[5] else "Zwierzę aktywne"
                    pet_row = f"""
                        <tr>
                            <td>{pet[0]}</td>
                            <td>{pet[1]}</td>
                            <td>{pet[2]}</td>
                            <td>{pet[3]}</td>
                            <td>{pet[4]}</td>
                            <td>{deletion_date}</td>
                            <td>{pet[6]} {pet[7]}</td>
                            <td>
                                <div class="btn-group">
                                    <a href="/update_pet/{pet[0]}" class="btn btn-edit">Edytuj</a>
                                    <a href="/delete_pet/{pet[0]}" class="btn btn-danger">Usuń</a>
                                </div>
                            </td>
                        </tr>
                    """

                    pets_rows += pet_row

                # Zastąpienie zmiennych w szablonie
                html_content = html_content.replace("{{ pet_rows }}", pets_rows)

                # Wyślij odpowiedź HTML z danymi zwierząt
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(html_content.encode('utf-8'))
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("<p>Nie znaleziono klientów.</p>".encode('utf-8'))    


###################     WYSZUKUJEMY WIZYTĘ    ##################################
            
        elif self.path == "/searching_visit/":
            content_length = int(self.headers.get('Content-Length'))
            post_data = self.rfile.read(content_length)
            data = {item.split('=')[0]: unquote_plus(item.split('=')[1]) for item in post_data.decode('utf-8').split('&')}

            # Pobierz dane z formularza
            first_name = data.get('first_name', '')
            last_name = data.get('last_name', '')
            pet_name = data.get('pet_name', '')

            if not first_name or not last_name or not pet_name:
                self.send_error(400, "Brak wymaganych danych (first_name, last_name, pet_name).")
                return

            visits = find_visit(first_name, last_name, pet_name)

            if visits:
                with open("templates/output_searching_visit.html", "r", encoding="utf-8") as file:
                    html_content = file.read()

                visit_rows = ""
                for visit in visits:
                    visit_id, pet_name, client_name, visit_date, visit_time, diagnosis = visit
                    visit_row = f"""
                        <tr>
                            <td>{visit_id}</td>
                            <td>{pet_name}</td>
                            <td>{client_name}</td>
                            <td>{visit_date}</td>
                            <td>{visit_time}</td>
                            <td>{diagnosis}</td>
                            <td>
                                <div class="btn-group">
                                    <a href="/update_visit/{visit_id}" class="btn btn-edit">Edytuj</a>
                                    <a href="/delete_visit/{visit_id}" class="btn btn-danger">Usuń</a>
                                </div>
                            </td>
                        </tr>
                    """
                    visit_rows += visit_row

                html_content = html_content.replace("{{ visit_rows }}", visit_rows)

                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(html_content.encode('utf-8'))

            else:
                self.send_response(404)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("<p>Nie znaleziono wizyt dla podanych danych.</p>".encode('utf-8'))


###################     UAKTUALNIAMY DANE KLIENTA      ##################################


        
        elif self.path.startswith("/update_client/"):
            # Pobieranie danych z formularza
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = parse_qs(post_data.decode('utf-8'))

            # Logowanie danych z formularza
            print(f"Dane przesłane z formularza: {data}")

            client_id = data.get('client_id', [''])[0]

            # Szukamy klienta na podstawie ID
            client = find_client_by_id(client_id)

            if client:
                # Jeżeli klient został znaleziony, przechodzimy do aktualizacji
                first_name = data.get('client_first_name', [''])[0]
                last_name = data.get('client_last_name', [''])[0]
                phone = data.get('client_phone', [''])[0]
                address = data.get('client_address', [''])[0]

                # Wywołanie funkcji do aktualizacji danych klienta
                update_client(client_id, first_name, last_name, phone, address)

                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("<p>Dane klienta zostały zaktualizowane.</p>".encode('utf-8'))
            else:
                # Jeżeli klient nie został znaleziony, zwróć błąd
                self.send_error(404, "Nie znaleziono klienta.")



###################     UAKTUALNIAMY DANE LEKARZA     ##################################


        elif self.path.startswith("/update_doctor/"):
            # Pobieranie danych z formularza
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = parse_qs(post_data.decode('utf-8'))

            # Logowanie danych z formularza
            print(f"Dane przesłane z formularza: {data}")

            doctor_id = data.get('doctor_id', [''])[0]

            # Szukamy lekarza na podstawie ID
            doctor = find_doctor_by_id(doctor_id)

            if doctor:
                # Jeżeli klient został znaleziony, przechodzimy do aktualizacji
                first_name = data.get('doctor_first_name', [''])[0]
                last_name = data.get('doctor_last_name', [''])[0]
                specialization = data.get('doctor_specialization', [''])[0]
                phone = data.get('doctor_phone', [''])[0]

                # Wywołanie funkcji do aktualizacji danych klienta
                update_doctor(doctor_id, first_name, last_name, specialization, phone)

                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("<p>Dane lekarza zostały zaktualizowane.</p>".encode('utf-8'))
            else:
                # Jeżeli klient nie został znaleziony, zwróć błąd
                self.send_error(404, "Nie znaleziono lekarza.")


###################     UAKTUALNIAMY DANE ZWIERZĘCIA     ##################################


        elif self.path.startswith("/update_pet/"):
            # Pobieranie danych z formularza
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = parse_qs(post_data.decode('utf-8'))

            # Logowanie danych z formularza
            print(f"Dane przesłane z formularza: {data}")

            pet_id = data.get('pet_id', [''])[0]

            # Szukamy zwierzęcia na podstawie ID
            pet = find_pet_by_id(pet_id)

            if pet:
                # Jeżeli zwierzę zostało znalezione, przechodzimy do aktualizacji
                pet_name = data.get('pet_name', [''])[0]
                species = data.get('species', [''])[0]
                breed = data.get('breed', [''])[0]
                age = data.get('age', [''])[0]
                client_id = data.get('client_id', [''])[0]

                # Wywołanie funkcji do aktualizacji danych zwierzecia
                update_pet(pet_id, pet_name, species, breed, age, client_id)

                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("<p>Dane zwierzecia zostały zaktualizowane.</p>".encode('utf-8'))
            else:
                # Jeżeli zwierzę nie zostało znalezione, zwróć błąd
                self.send_error(404, "Nie znaleziono zwierzęcia.")


###################     UAKTUALNIAMY DANE WIZYTY     ##################################

        elif self.path.startswith("/update_visit/"):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = parse_qs(post_data.decode('utf-8'))

            try:
                visit_id = self.path.split("/")[2]
                client_id = data.get("client_id", [""])[0]
                pet_id = data.get("pet_id", [""])[0]
                doctor_id = data.get("doctor_id", [""])[0]
                visit_date = data.get("visit_date", [""])[0]
                visit_time = data.get("visit_time", [""])[0]

                update_visit(visit_id, client_id, pet_id, doctor_id, visit_date, visit_time)

                self.send_response(303)
                self.send_header("Location", f"/visit_updated/{visit_id}")  # lub inna ścieżka
                self.end_headers()
 
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                error_html = f"<h1>Błąd podczas zapisu wizyty</h1><pre>{e}</pre>"
                self.wfile.write(error_html.encode("utf-8", errors="replace"))


# ############################  DEF ADDING POST  ################################


    def handle_add_client_post(self, data):
        first_name = data.get('client_first_name', '')
        last_name = data.get('client_last_name', '')
        phone = data.get('client_phone', '')
        address = data.get('client_address', '')

        try:
            add_client(first_name, last_name, phone, address)
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("<p>Client został dodany do bazy danych!</p>".encode('utf-8'))
        except Exception as e:
                # Wysłanie odpowiedzi HTTP w przypadku błędu
            self.send_response(500)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(f"<p>Wystąpił błąd: {e}</p>".encode('utf-8'))


    def handle_add_doctor_post(self, data):
        first_name = data.get('doctor_first_name', '')
        last_name = data.get('doctor_last_name', '')
        specialization = data.get('doctor_specialization', '')
        phone = data.get('telefon', '')
        try:
            add_doctor(first_name, last_name, specialization, phone)
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("<p>Doktor został dodany do bazy danych!<p>".encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(f"<p>Wystąpił błąd: {e}<p>".encode('utf-8'))


    def handle_add_pet_post(self, data):
        pet_name = data.get('pet_name', '')
        species = data.get('species', '')
        breed = data.get('breed', '')
        age = data.get('age', '')
        client_id = data.get('client_id', '')
        try:
            add_pet(pet_name, species, breed, age, client_id)
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("<p>Zwierzę zostało dodane do bazy danych!<p>".encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(f"<p>Wystąpił błąd: {e}<p>".encode('utf-8'))


def run_server():
    PORT = 8000
    with HTTPServer(("", PORT), MyHandler) as httpd:
        print(f"Serwer uruchomiony na porcie {PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
