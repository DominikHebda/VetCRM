from Database.operations_visits import fetch_visits, update_visit_in_db, add_next_visit, get_client_id, get_client_data_by_id, get_current_time, fetch_clients_to_visit, fetch_pets_to_visit, fetch_doctors_to_visit, add_visit, find_visit_by_id
from Database.operations_client import fetch_clients, add_client, find_client, find_client_by_id, update_client, soft_delete_client
import Database.operations_doctors
print(dir(Database.operations_doctors))
print(">>> Ładuje się właściwy plik operations_doctors.py")

from Database.operations_doctors import add_doctor, fetch_doctors, find_doctor_by_id, find_doctor, update_doctor, soft_delete_doctor
from Database.operations_pets import fetch_pets, add_pet, fetch_clients_to_indications, find_pet, find_pet_by_id, update_pet, soft_delete_pet
from http.server import SimpleHTTPRequestHandler, HTTPServer
import urllib.parse
from urllib.parse import parse_qs, urlparse
import traceback  
import logging
import os


logging.basicConfig(level=logging.DEBUG)  # Ustawienie poziomu logowania na DEBUG


def render_home_page():
    home_page_html = """
    <!DOCTYPE html>
    <html lang="pl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Witamy w VetCRM</title>
        <!-- Załączenie CSS Bootstrapa -->
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background-color: #f7fdf4; /* Jasnozielone tło */
            }
            h1 {
                color: #3c763d; /* Zielony kolor dla nagłówka */
            }
            p {
                color: #5bc0de; /* Jasny niebieski, przyjazny kolor dla tekstu */
            }
            .btn {
                font-size: 18px; /* Większy tekst na przyciskach */
                width: 100%; /* Pełna szerokość przycisków */
                margin-bottom: 15px; /* Odstęp między przyciskami */
            }
            .btn-primary {
                background-color: #007b9e; /* Stonowany niebieski */
                border-color: #007b9e;
            }
            .btn-primary:hover {
                background-color: #00688b; /* Ciemniejszy niebieski przy hover */
                border-color: #005a74;
            }
            .btn-success {
                background-color: #218838; /* Intensywniejszy zielony dla Zwierząt */
                border-color: #218838;
            }
            .btn-success:hover {
                background-color: #1c7430; /* Ciemniejszy odcień zielonego przy hover */
                border-color: #1a5b29;
            }
            .btn-warning {
                background-color: #e67e22; /* Ciemniejszy, bardziej profesjonalny żółty dla Lekarzy */
                border-color: #e67e22;
            }
            .btn-warning:hover {
                background-color: #d35400; /* Ciemniejszy odcień żółtego przy hover */
                border-color: #c0392b;
            }
            .btn-success.darker {
                background-color: #2d6a4f; /* Ciemniejszy zielony dla Wizyt */
                border-color: #2d6a4f;
            }
            .btn-success.darker:hover {
                background-color: #245d42; /* Ciemniejszy odcień zielonego przy hover */
                border-color: #1e4a35;
            }
            .container {
                max-width: 600px; /* Szerokość kontenera */
                padding-top: 50px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="text-center">Witamy w VetCRM</h1>
            <p class="text-center">Wybierz jedną z opcji, aby zarządzać przychodnią weterynaryjną:</p>
            
            <div class="row">
                <div class="col-md-6 mb-3">
                    <a href="/clients_list/" class="btn btn-primary">Klienci</a>
                </div>
                <div class="col-md-6 mb-3">
                    <a href="/pets_list/" class="btn btn-success">Zwierzęta</a>
                </div>
            </div>
            <div class="row">
                <div class="col-md-6 mb-3">
                    <a href="/doctors_list/" class="btn btn-warning">Lekarze</a>
                </div>
                <div class="col-md-6 mb-3">
                    <a href="/visits_list/" class="btn btn-success darker">Wizyty</a>
                </div>
            </div>
        </div>

        <!-- Załączenie skryptów JS Bootstrapa -->
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    </body>
    </html>
    """
    return home_page_html



# ########          FRAGMENT KODU DO SPRAWDZENIA                  ##########################################################################################3



def render_add_receptionist_form():
    with open("templates/adding_receptionist.html", "r", encoding="utf-8") as f:
        add_receptionist_form_html = f.read()

    return add_receptionist_form_html

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


# ####################              do_GET              #####################################################


class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        print(f"Requested path: {self.path}") 

########################    WYŚWIETLANIE STRONY POWITALNEJ  ################


        if self.path == "/":
            home_page_html = render_home_page()  # Wyświetl stronę powitalną
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(home_page_html.encode('utf-8'))


#######################    LISTA KLIENTÓW  #######################


        elif self.path == "/clients_list/":
            # Pobieramy klientów z bazy danych
            clients = fetch_clients()

            # Debugowanie: sprawdzamy, co zostało pobrane
            # print(f"Pobrane dane: {clients}")

            # Ścieżka do szablonu HTML
            template_path = os.path.join(os.getcwd(), 'Templates', 'clients_list.html')

            try:
                # Odczytujemy zawartość pliku HTML
                with open(template_path, 'r', encoding='utf-8') as file:
                    template_content = file.read()

                # Przygotowujemy dane do wstawienia w HTML
                clients_html = ""
                for client in clients:
                    client_id = client[0]  # ID klienta
                    deletion_date = client[5].strftime('%Y-%m-%d %H:%M:%S') if client[5] else "Klient aktywny"

                    # Tworzymy wiersz tabeli, uwzględniając datę usunięcia
                    client_row = f"""
                    <tr>
                        <td>{client[0]}</td>
                        <td>{client[1]}</td>
                        <td>{client[2]}</td>
                        <td>{client[3]}</td>
                        <td>{client[4]}</td>
                        <td>{deletion_date}</td>  <!-- Dodajemy datę usunięcia -->
                        <td>
                            <div class="btn-group">
                                <a href="/update_client/{client_id}" class="btn btn-edit">Edytuj</a>
                                <a href="/delete_client/{client_id}" class="btn btn-danger">Usuń</a>
                            </div>
                        </td>
                    </tr>
                    """
                    clients_html += client_row  # Dodajemy wiersz dla każdego klienta

                # Zamieniamy placeholder {{ client_rows }} w szablonie na wygenerowany HTML z klientami
                rendered_content = template_content.replace("{{ client_rows }}", clients_html)

                # Wysyłamy odpowiedź HTTP
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(rendered_content.encode('utf-8'))

            except Exception as e:
                self.send_response(500)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                error_message = f"Error rendering page: {e}"
                self.wfile.write(error_message.encode('utf-8'))


#######################    LISTA LEKARZY  #######################


        elif self.path == "/doctors_list/":
            # Pobieramy lekarzyklientów z bazy danych
            doctors = fetch_doctors()

            # Debugowanie: sprawdzamy, co zostało pobrane
            print(f"Pobrane dane: {doctors}")

            # Ścieżka do szablonu HTML
            template_path = os.path.join(os.getcwd(), 'Templates', 'doctors_list.html')

            try:
                # Odczytujemy zawartość pliku HTML
                with open(template_path, 'r', encoding='utf-8') as file:
                    template_content = file.read()

                # Przygotowujemy dane do wstawienia w HTML
                doctors_html = ""
                for doctor in doctors:
                    doctor_id = doctor[0]  # ID lekarza
                    deletion_date = doctor[5].strftime('%Y-%m-%d %H:%M:%S') if doctor[5] else "Lekarz aktywny"

                    # Tworzymy wiersz tabeli, uwzględniając datę usunięcia
                    doctor_row = f"""
                    <tr>
                        <td>{doctor[0]}</td>
                        <td>{doctor[1]}</td>
                        <td>{doctor[2]}</td>
                        <td>{doctor[3]}</td>
                        <td>{doctor[4]}</td>
                        <td>{deletion_date}</td>  <!-- Dodajemy datę usunięcia -->
                        <td>
                            <div class="btn-group">
                                <a href="/update_doctor/{doctor_id}" class="btn btn-edit">Edytuj</a>
                                <a href="/delete_doctor/{doctor_id}" class="btn btn-danger">Usuń</a>
                            </div>
                        </td>
                    </tr>
                    """
                    doctors_html += doctor_row  # Dodajemy wiersz dla każdego klienta

                # Zamieniamy placeholder {{ doctors_rows }} w szablonie na wygenerowany HTML z klientami
                rendered_content = template_content.replace("{{ doctor_rows }}", doctors_html)

                # Wysyłamy odpowiedź HTTP
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(rendered_content.encode('utf-8'))

            except Exception as e:
                self.send_response(500)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                error_message = f"Error rendering page: {e}"
                self.wfile.write(error_message.encode('utf-8'))


#######################    LISTA ZWIERZĄT  #######################


        elif self.path == "/pets_list/":
            pets = fetch_pets()
            print(f"Pobrane dane: {pets}")
            template_path = os.path.join(os.getcwd(), 'Templates', 'pets_list.html')

            try:
                with open(template_path, 'r', encoding='utf-8') as file:
                    template_content = file.read()

                pets_html = ""
                for pet in pets:
                    pet_id = pet[0]
                    deletion_date = pet[5].strftime('%Y-%m-%d %H:%M:%S') if pet[5] else "Zwierzę aktywne"
                    owner_name = f"{pet[6]} {pet[7]}" if pet[6] and pet[7] else "Brak danych"

                    pet_row = f"""
                        <tr>
                            <td>{pet[0]}</td>
                            <td>{pet[1]}</td>
                            <td>{pet[2]}</td>
                            <td>{pet[3]}</td>
                            <td>{pet[4]}</td>
                            <td>{deletion_date}</td>
                            <td>{owner_name}</td>
                            <td>
                                <div class="btn-group">
                                    <a href="/update_pet/{pet_id}" class="btn btn-edit">Edytuj</a>
                                    <a href="/delete_pet/{pet_id}" class="btn btn-danger">Usuń</a>
                                </div>
                            </td>
                        </tr>
                    """
                    pets_html += pet_row

                rendered_content = template_content.replace("{{ pets_rows }}", pets_html)
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(rendered_content.encode('utf-8'))

            except Exception as e:
                self.send_response(500)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                error_message = f"Error rendering page: {e}"
                self.wfile.write(error_message.encode('utf-8'))



#######################    LISTA WIZYT  #######################


        elif self.path == "/visits_list/":
            # Pobieramy listę wizyt z bazy danych
            visits = fetch_visits()

            # Debugowanie: sprawdzamy, co zostało pobrane
            print(f"Pobrane dane: {visits}")

            # Ścieżka do szablonu HTML
            template_path = os.path.join(os.getcwd(), 'Templates', 'visits_list.html')

            try:
                # Odczytujemy zawartość pliku HTML
                with open(template_path, 'r', encoding='utf-8') as file:
                    template_content = file.read()

                # Przygotowujemy dane do wstawienia w HTML
                visits_html = ""
                for visit in visits:
                    visit_id = visit['id']  # ID klienta
                    diagnosis = visit['diagnosis'] if visit['diagnosis'] not in [None, ""] else "brak diagnozy"

                    deletion_date = visit['soft_delete'].strftime('%Y-%m-%d %H:%M:%S') if visit['soft_delete'] else "Wizyta aktualna"

                    # Tworzymy wiersz tabeli, uwzględniając datę usunięcia
                    visit_row = f"""
                    <tr>
                        <td>{visit_id}</td>
                        <td>{visit['created_at']}</td>
                        <td>{visit['client_full_name']}</td>
                        <td>{visit['pet_name']}</td>
                        <td>{visit['doctor_full_name']}</td>
                        <td>{visit['visit_date']}</td>
                        <td>{visit['visit_time']}</td>
                        <td>{diagnosis}</td>
                        <td>{deletion_date}</td>  <!-- Dodajemy datę usunięcia -->
                        <td>
                            <div class="btn-group">
                                <a href="/update_visit/{visit_id}" class="btn btn-edit">Edytuj</a>
                                <a href="/delete_visit/{visit_id}" class="btn btn-danger">Usuń</a>
                            </div>
                        </td>
                    </tr>
                    """
                    visits_html += visit_row  # Dodajemy wiersz dla każdej wizyty

                # Zamieniamy placeholder {{ visit_row }} w szablonie na wygenerowany HTML z wizyty
                rendered_content = template_content.replace("{{ visit_rows }}", visits_html)

                # Wysyłamy odpowiedź HTTP
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(rendered_content.encode('utf-8'))

            except Exception as e:
                print("Błąd podczas renderowania strony:")
                traceback.print_exc()  # To wyświetli pełny stos błędów
                self.send_response(500)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(f"<h1>Błąd renderowania strony:</h1><pre>{traceback.format_exc()}</pre>".encode("utf-8"))


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
            visit_id = self.path.split("/")[2]  # np. /update_visit/5

            visit = find_visit_by_id(visit_id)

            if visit:
                # Rozpakowanie danych wizyty
                visit_data = {
                    "visit_id": visit[0],
                    "created_at": visit[1],  # Możesz nie używać w formularzu
                    "client_id": visit[2],
                    "pet_id": visit[3],
                    "doctor_id": visit[4],
                    "visit_date": visit[5],
                    "visit_time": visit[6],
                    "diagnosis": visit[7]
                }

                # Wczytanie danych do selectów
                clients = fetch_clients()
                pets = fetch_pets()
                doctors = fetch_doctors()

                # Budowanie opcji <select>
                client_options = ""
                for client in clients:
                    selected = "selected" if str(client[0]) == str(visit_data["client_id"]) else ""
                    client_options += f'<option value="{client[0]}" {selected}>{client[1]}</option>\n'

                pet_options = ""
                for pet in pets:
                    selected = "selected" if str(pet[0]) == str(visit_data["pet_id"]) else ""
                    pet_options += f'<option value="{pet[0]}" {selected}>{pet[1]}</option>\n'

                doctor_options = ""
                for doctor in doctors:
                    selected = "selected" if str(doctor[0]) == str(visit_data["doctor_id"]) else ""
                    doctor_options += f'<option value="{doctor[0]}" {selected}>{doctor[1]}</option>\n'

                try:
                    template_path = os.path.join(os.path.dirname(__file__), 'Templates', 'update_visit.html')

                    if os.path.exists(template_path):
                        with open(template_path, "r", encoding="utf-8") as f:
                            template = f.read()

                        # Podstawianie danych do szablonu
                        for key, value in visit_data.items():
                            template = template.replace(f"{{{{ {key} }}}}", str(value))

                        template = template.replace("{{ client_options }}", client_options)
                        template = template.replace("{{ pet_options }}", pet_options)
                        template = template.replace("{{ doctor_options }}", doctor_options)

                        self.send_response(200)
                        self.send_header("Content-type", "text/html; charset=utf-8")
                        self.end_headers()
                        self.wfile.write(template.encode("utf-8"))

                    else:
                        self.send_error(404, "Plik szablonu nie znaleziony")
                except FileNotFoundError:
                    self.send_error(404, "Plik szablonu nie znaleziony")
            else:
                self.send_error(404, "Wizyta nie znaleziona")




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

        else:
            super().do_GET()


# #########################             do_POST             ###########################################


    def do_POST(self):

        if self.path.startswith("/update/"):
            visit_id = self.path.split("/update/")[1]
            try:
                visit_id = int(visit_id)

                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode('utf-8')
                data = {item.split('=')[0]: item.split('=')[1] for item in post_data.split('&')}

                updated = update_visit_in_db(
                    visit_id,
                    data.get('date'),
                    data.get('client_last_name'),
                    data.get('pet_name'),
                    data.get('doctor_name'),
                    data.get('date_of_visit'),
                    data.get('visit_time')
                )

                if updated:
                    self.send_response(200)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write("<p>Wizyta została zaktualizowana!</p>".encode('utf-8'))
                else:
                    self.send_response(500)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write("<p>Wystąpił błąd podczas aktualizacji wizyty.</p>".encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(f"<p>Błąd: {e}</p>".encode('utf-8'))



        elif self.path.startswith("/visits_table/"):
            try:
                # Odczyt danych z formularza
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode('utf-8')

                # Rozbicie danych na parametry
                data = {item.split('=')[0]: urllib.parse.unquote(item.split('=')[1]) for item in post_data.split('&')}
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





########################    DODAWANIE NOWEJ WIZYTY  ################


        elif self.path.startswith("/add_next_visit/"):
            try:
                # Odczyt danych z formularza
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode('utf-8')
                
                # Rozbicie danych
                data = {item.split('=')[0]: urllib.parse.unquote(item.split('=')[1]) for item in post_data.split('&')}
                print(f"Received POST data: {data}")  # Logowanie danych z formularza
                
                first_name = data.get('client_first_name')
                last_name = data.get('client_last_name')
                phone = data.get('client_phone')
                address = data.get('client_address')
                pet_name = data.get('pet_name')
                species = data.get('species')
                breed = data.get('breed')
                age = data.get('age')
                doctor = data.get('doctor_name')
                date_of_visit = data.get('date_of_visit')
                visit_time = data.get('visit_time')

                breed = urllib.parse.unquote_plus(breed)
                print(f"Breed after decoding: {breed}")

                if not first_name or not last_name or not phone or not address:
                    print("Błąd: Nie wszystkie dane klienta zostały wprowadzone.")
                    raise ValueError("Nie wszystkie dane klienta zostały wprowadzone.")
                
                # Logowanie danych przed próbą dodania klienta
                print(f"Próbuję znaleźć klienta o nazwisku: {last_name}")
                
                client_id = get_client_id(last_name)
                if client_id is None:
                    print(f"Brak klienta o nazwisku {last_name} w bazie danych. Dodaję nowego klienta...")
                    add_client(first_name, last_name, phone, address)
                    client_id = get_client_id(last_name)
                    print(f"Ponownie sprawdzam ID klienta: {client_id}")
                
                # Logowanie przed próbą dodania wizyty
                print(f"Próbuję dodać wizytę: {first_name}, {last_name}, {pet_name}, {doctor}, {date_of_visit}, {visit_time}")
                print(f"species: {species}, breed: {breed}, age: {age}")  # Logowanie wartości breed przed dodaniem do bazy

                added = add_next_visit(
                    current_time=get_current_time(),
                    last_name_client=last_name,
                    pet_name=pet_name,
                    species=species,
                    breed=breed,
                    age=age,
                    doctor=doctor,
                    date_of_visit=date_of_visit,
                    visit_time=visit_time,
                    first_name=first_name,
                    phone=phone,
                    address=address
                )

                if added:
                    self.send_response(200)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write("<p>Wizyta została zapisana!</p>".encode('utf-8'))
                else:
                    print("Wizyta nie została zapisana.")
                    self.send_response(500)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write("<p>Wystąpił błąd podczas zapisywania wizyty.<p/>".encode('utf-8'))

            except Exception as e:
                print(f"Błąd podczas przetwarzania POST: {e}")
                self.send_response(500)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(f"<p>Błąd: {e}</p>".encode('utf-8'))


###################     DODAJEMY NOWEGO KLIENTA      ##################################

        elif self.path == "/adding_client/":
            # Odczytujemy dane POST
            content_length = int(self.headers.get('Content-Length'))
            post_data = self.rfile.read(content_length)
            post_data = post_data.decode('utf-8')

            # Tworzymy słownik z danymi
            data = {item.split('=')[0]: urllib.parse.unquote_plus(item.split('=')[1]) for item in post_data.split('&')}

            # Wywołanie metody obsługującej dodanie klienta
            self.handle_add_client_post(data)


###############         DODAJEMY NOWEGO LEKARZA         ###########################


        elif self.path == "/adding_doctors/":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = post_data.decode('utf-8')

            print("RAW post_data:")
            print(post_data)

            data = {item.split('=')[0]: urllib.parse.unquote_plus(item.split('=')[1]) for item in post_data.split('&')}
            
            print("Parsed data:")
            print(data)

            print(post_data)  # Sprawdzić, co jest przesyłane
            self.handle_add_doctor_post(data)



###############         DODAJEMY NOWE ZWIERZĘ         ###########################


        elif self.path == "/adding_pet/":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = post_data.decode('utf-8')

            print("RAW post_data:")
            print(post_data)

            data = {item.split('=')[0]: urllib.parse.unquote_plus(item.split('=')[1]) for item in post_data.split('&')}
            
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
            data = {item.split('=')[0]: urllib.parse.unquote_plus(item.split('=')[1]) for item in post_data.decode('utf-8').split('&')}

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
            data = {item.split('=')[0]: urllib.parse.unquote_plus(item.split('=')[1]) for item in post_data.decode('utf-8').split('&')}

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
            data = {item.split('=')[0]: urllib.parse.unquote_plus(item.split('=')[1]) for item in post_data.decode('utf-8').split('&')}

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

# ####################      DODAWANIE RECEPCJONISTKI        ############################################

        elif self.path == "/add_receptionist/":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = {item.split('=')[0]: urllib.parse.unquote_plus(item.split('=')[1]) for item in post_data.split('&')}
            self.handle_add_receptionist_post(data)




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

