from Database.operations_visits import fetch_scheduled_visits, fetch_visits_details, update_visit_in_db, format_visit_time, add_next_visit, get_client_id, get_current_time
from Database.operations_client import add_client, add_client_and_pet_s
from Database.operations_doctors import add_doctor
from Database.operations_receptionist import add_receptionist
from Database.operations_pets import add_pet
from Database.connection import create_connection
from http.server import SimpleHTTPRequestHandler, HTTPServer
import urllib.parse
import logging

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
            .list-group-item {
                background-color: #e9f7e1; /* Jasny zielony dla linków */
                border: 1px solid #d6e9c6; /* Zielona ramka */
            }
            .list-group-item:hover {
                background-color: #d4edda; /* Trochę ciemniejszy zielony przy najechaniu */
                cursor: pointer;
            }
            .btn {
                font-size: 16px; /* Większy tekst na przyciskach */
            }
            .btn-primary {
                background-color: #28a745; /* Zielony przycisk */
                border-color: #28a745;
            }
            .btn-primary:hover {
                background-color: #218838; /* Ciemniejszy zielony przy hover */
                border-color: #1e7e34;
            }
            .btn-lg {
                margin-bottom: 15px; /* Przerwa między przyciskami */
            }
        </style>
    </head>
    <body>
        <div class="container mt-5">
            <h1 class="text-center">Witamy w VetCRM</h1>
            <p class="text-center">Wybierz jedną z opcji, aby zarządzać przychodnią weterynaryjną:</p>
            
            <div class="list-group">
                <a href="/add_next_visit/" class="list-group-item list-group-item-action btn btn-primary btn-lg">Dodaj nową wizytę</a>
                <a href="/adding_client_and_pet/" class="list-group-item list-group-item-action btn btn-success btn-lg">Dodaj klienta i jego zwierzę</a>
                <a href="/add_doctor/" class="list-group-item list-group-item-action btn btn-warning btn-lg">Dodaj lekarza</a>
                <a href="/add_receptionist/" class="list-group-item list-group-item-action btn btn-info btn-lg">Dodaj recepcjonistkę</a>
                <a href="/visits_table/" class="list-group-item list-group-item-action btn btn-secondary btn-lg">Pokaż listę wizyt</a>
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




def render_visits_to_html():
    visits = fetch_scheduled_visits() 
    if not visits:
        return "<p>Brak zaplanowanych wizyt.</p>"

    visits_html = """
    <div class="container">
        <h2>Lista zaplanowanych wizyt</h2>
        <a href="/adding/" class="btn btn-primary mb-3">Dodaj wizytę</a>
        <table class="table table-striped table-bordered">
            <thead class="thead-dark">
                <tr>
                    <th>ID</th>
                    <th>Data utworzenia wizyty</th>
                    <th>Nazwisko klienta</th>
                    <th>Nazwa zwierzęcia</th>
                    <th>Lekarz</th>
                    <th>Data następnej wizyty</th>
                    <th>Godzina wizyty</th>
                    <th>Pokaż szczegóły</th>
                    <th>Edytuj wizytę</th>
                </tr>
            </thead>
            <tbody>
    """

    for visit in visits:
        visit_id = visit[0]  
        date = visit[1]  
        client_last_name = visit[2] 
        pet_name = visit[3]  
        doctor_name = visit[4] 
        date_of_visit = visit[5]  
        visit_time = visit[6]  

        # Formatowanie godziny wizyty
        visit_time = format_visit_time(visit_time)

        visit_details_link = f'<a href="/visit/{visit_id}" class="btn btn-info btn-sm">Pokaż szczegóły</a>'
        visit_edit_link = f'<a href="/update/{visit_id}" class="btn btn-warning btn-sm">Edytuj wizytę</a>'

        visits_html += f"""
        <tr>
            <td>{visit_id}</td>
            <td>{date}</td>
            <td>{client_last_name}</td>
            <td>{pet_name}</td>
            <td>{doctor_name}</td>
            <td>{date_of_visit}</td>
            <td>{visit_time}</td>
            <td>{visit_details_link}</td>
            <td>{visit_edit_link}</td>
        </tr>
        """
    
    visits_html += """
            </tbody>
        </table>
    </div>
    """

    with open("templates/index.html", "r", encoding="utf-8") as f:
        html_template = f.read()

    final_html = html_template.replace("{{ visits_table }}", visits_html)

    return final_html

def render_visit_details(visit_id):
    visit = fetch_visits_details(visit_id)
    if not visit:
        return "<p>Wizyta o podanym ID nie została znaleziona.</p>"

    visit_id = visit[0]
    date = visit[1]
    client_last_name = visit[2]
    pet_name = visit[3]
    doctor_name = visit[4]
    date_of_visit = visit[5]
    visit_time = visit[6]

    visit_details_html = f"""
    <h1>Szczegóły wizyty</h1>
    <p><strong>ID wizyty:</strong> {visit_id}</p>
    <p><strong>Data utworzenia wizyty:</strong> {date}</p>
    <p><strong>Nazwisko klienta:</strong> {client_last_name}</p>
    <p><strong>Nazwa zwierzęcia:</strong> {pet_name}</p>
    <p><strong>Lekarz:</strong> {doctor_name}</p>
    <p><strong>Data następnej wizyty:</strong> {date_of_visit}</p>
    <p><strong>Godzina wizyty:</strong> {visit_time}</p>
    <p><a href="/update/{visit_id}">Edytuj wizytę</a></p>
    <p><a href="/">Powrót do listy wizyt</a></p>
    """

    return visit_details_html

def render_add_doctor_form():
    with open("templates/adding_doctors.html", "r", encoding="utf-8") as f:
        add_doctor_form_html = f.read()

    return add_doctor_form_html


def render_add_receptionist_form():
    with open("templates/adding_receptionist.html", "r", encoding="utf-8") as f:
        add_receptionist_form_html = f.read()

    return add_receptionist_form_html

def render_add_next_visit():
    with open("templates/adding_visit.html", "r", encoding="utf-8") as f:
        add_next_visit_html = f.read()
    
    return add_next_visit_html

def render_add_client_and_pet_form():
    with open("templates/adding_client_and_pet.html", "r", encoding="utf-8") as f:
        add_client_and_pet_html = f.read()

    return add_client_and_pet_html   

###################     DODAJEMY NOWEGO KLIENTA I JEGO ZWIERZĘ      ##################################

def render_add_new_client_and_pet():
    add_new_client_and_pet_html = """
    <h1>Dodaj nową wizytę</h1>
    <form method="POST" action="/add_new_client_and_pet/" enctype="application/x-www-form-urlencoded; charset=UTF-8">
    <meta charset="UTF-8">
        
        <label for="client_first_name">Podaj imię klienta:</label>
        <input type="text" id="client_first_name" name="client_first_name" /><br><br>

        <label for="client_last_name">Podaj nazwisko klienta:</label>
        <input type="text" id="client_last_name" name="client_last_name" /><br><br>
        
        <label for="client_phone">Podaj numer telefonu klienta:</label>
        <input type="text" id="client_phone" name="client_phone" /><br><br>
        
        <label for="client_address">Podaj adres klienta:</label>
        <input type="text" id="client_address" name="client_address" /><br><br>
        
        <label for="pet_name">Podaj nazwę zwierzęcia:</label>
        <input type="text" id="pet_name" name="pet_name" /><br><br>
        
        <label for="doctor_name">Podaj nazwisko lekarza:</label>
        <input type="text" id="doctor_name" name="doctor_name" /><br><br>
        
        <label for="date_of_visit">Podaj datę wizyty:</label>
        <input type="date" id="date_of_visit" name="date_of_visit" /><br><br>

        <label for="visit_time">Podaj wiek zwierzęcia:</label>
        <input type="time" id="visit_time" name="visit_time" /><br><br>

        <input type="submit" value="Zapisz nową wizytę" />
    </form>
    <p><a href="/">Powrót do listy wizyt</a></p>
    """

    return add_new_client_and_pet_html

def render_visit_edit_form(visit_id):
    visit = fetch_visits_details(visit_id)
    if not visit:
        return "<p>Wizyta o podanym ID nie została znaleziona.</p>"

    visit_id = visit[0]
    date = visit[1]
    client_last_name = visit[2]
    pet_name = visit[3]
    doctor_name = visit[4]
    date_of_visit = visit[5]
    visit_time = visit[10]

    visit_edit_form_html = f"""
    <h1>Edytuj wizytę</h1>
    <form method="POST" action="/update/{visit_id}" enctype="application/x-www-form-urlencoded; charset=UTF-8">
    <meta charset="UTF-8">
        <label for="date">Data utworzenia wizyty:</label>
        <input type="text" id="date" name="date" value="{date}" /><br><br>
        
        <label for="client_last_name">Nazwisko klienta:</label>
        <input type="text" id="client_last_name" name="client_last_name" value="{client_last_name}" /><br><br>
        
        <label for="pet_name">Nazwa zwierzęcia:</label>
        <input type="text" id="pet_name" name="pet_name" value="{pet_name}" /><br><br>
        
        <label for="doctor_name">Lekarz:</label>
        <input type="text" id="doctor_name" name="doctor_name" value="{doctor_name}" /><br><br>
        
        <label for="date_of_visit">Data następnej wizyty:</label>
        <input type="text" id="date_of_visit" name="date_of_visit" value="{date_of_visit}" /><br><br>

        <label for="visit_time">Godzina wizyty:</label>
        <input type="time" id="visit_time" name="visit_time" value="{visit_time}" /><br><br>

        <input type="submit" value="Zaktualizuj wizytę" />
    </form>
    <p><a href="/">Powrót do listy wizyt</a></p>
    """

    return visit_edit_form_html


class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):

########################    WYŚWIETLANIE STRONY POWITALNEJ  ################


        if self.path == "/":
            home_page_html = render_home_page()  # Wyświetl stronę powitalną
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(home_page_html.encode('utf-8'))

        elif self.path.startswith("/visit/"):
            visit_id = self.path.split("/visit/")[1]
            try:
                visit_id = int(visit_id)
                print(f"Requested visit ID: {visit_id}") 
                visit_details_html = render_visit_details(visit_id)
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(visit_details_html.encode('utf-8'))
            except ValueError:
                print(f"Invalid visit ID format: {visit_id}") 
                self.send_response(404)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("<p>Niepoprawne ID wizyty.</p>".encode('utf-8'))

########################    WYŚWIETLANIE LISTY WIZYT  ################


        elif self.path.startswith("/visits_table/"):
            try:
                final_html = render_visits_to_html()
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset+utf-8")
                self.end_headers()
                self.wfile.write(final_html.encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(f"<p>Błąd: {e}".encode("utf-8"))


        # elif self.path.startswith("/update/"):
        #     visit_id = self.path.split("/update/")[1]
        #     try:
        #         visit_id = int(visit_id)
        #         visit_edit_form_html = render_visit_edit_form(visit_id) 
        #         self.send_response(200)
        #         self.send_header("Content-type", "text/html; charset=utf-8")
        #         self.end_headers()
        #         self.wfile.write(visit_edit_form_html.encode('utf-8'))
        #     except ValueError:
        #         print(f"Invalid visit ID format: {visit_id}")  
        #         self.send_response(404)
        #         self.send_header("Content-type", "text/html; charset=utf-8")
        #         self.end_headers()
        #         self.wfile.write("<p>Niepoprawne ID wizyty.</p>".encode('utf-8'))



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

        elif self.path.startswith("/adding_client_and_pet/"):
            adding_client_and_pet_form_html = render_add_client_and_pet_form()
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(adding_client_and_pet_form_html.encode('utf-8'))

        elif self.path == "/add_doctor/":
            try:
                final_html = render_add_doctor_form()
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(final_html.encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(f"<p>Błąd: {e}".encode("utf-8"))


        elif self.path == "/add_receptionist/":
            try:
                final_html_html = render_add_receptionist_form()
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(final_html_html.encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(f"<p>Błąd: {e}".encode("utf-8"))

        

        # elif self.path == "/add_new_client_and_pet/":
        #     add_new_client_and_pet_html = render_add_new_client_and_pet()
        #     self.send_response(200)
        #     self.send_header("Content-type", "text/html; charset=utf-8")
        #     self.end_headers()
        #     self.wfile.write(add_new_client_and_pet_html.encode('utf-8'))


        else:
            super().do_GET()

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


###################     DODAJEMY NOWEGO KLIENTA I JEGO ZWIERZĘ      ##################################

        elif self.path.startswith("/adding_client_and_pet/"):
            try:
                # Parsowanie danych z formularza
                content_length = int(self.headers.get('Content-Length'))
                post_data = self.rfile.read(content_length)
                data = urllib.parse.parse_qs(post_data.decode('utf-8'))

                first_name = data.get('client_first_name', [''])[0]
                last_name = data.get('client_last_name', [''])[0]
                phone = data.get('client_phone', [''])[0]
                address = data.get('client_address', [''])[0]
                pet_name = data.get('pet_name', [''])[0]
                species = data.get('species', [''])[0]
                breed = data.get('breed', [''])[0]
                age = int(data.get('age', ['0'])[0])

                # Dodanie klienta i zwierzęcia
                added_client_and_pet = add_client_and_pet_s(
                    first_name=first_name,
                    last_name=last_name,
                    phone=phone,
                    address=address,
                    pet_name=pet_name,
                    species=species,
                    breed=breed,
                    age=age
                )

                if added_client_and_pet:
                    self.send_response(200)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write("<p>Klient i zwierzę zostali zapisani</p>".encode('utf-8'))
                else:
                    print("Klient i zwierzę nie zostali zapisani.")
                    self.send_response(500)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write("<p>Wystąpił błąd podczas zapisywania klienta i zwierzęcia.</p>".encode('utf-8'))

            except Exception as e:
                print(f"Błąd podczas przetwarzania POST: {e}")
                self.send_response(500)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(f"<p>Błąd: {e}</p>".encode('utf-8'))

        elif self.path == "/add_doctor/":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = {item.split('=')[0]: urllib.parse.unquote_plus(item.split('=')[1]) for item in post_data.split('&')}
            self.handle_add_doctor_post(data)
            
            print(post_data)  # Sprawdzić, co jest przesyłane

        elif self.path == "/add_receptionist/":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = {item.split('=')[0]: urllib.parse.unquote_plus(item.split('=')[1]) for item in post_data.split('&')}
            self.handle_add_receptionist_post(data)


    # Przenosimy metodę handle_add_doctor_post na poziom klasy
    def handle_add_doctor_post(self, data):
        first_name = data.get('doctor_first_name', '')
        last_name = data.get('doctor_last_name', '')
        specialization = data.get('doctor_specialization', '')

        try:
            # Wywołanie funkcji do dodania lekarza
            add_doctor(first_name, last_name, specialization)

            # Wysłanie odpowiedzi HTTP
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("<p>Doktor został dodany do bazy danych!</p>".encode('utf-8'))
        except Exception as e:
            # Wysłanie odpowiedzi HTTP w przypadku błędu
            self.send_response(500)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(f"<p>Wystąpił błąd: {e}</p>".encode('utf-8'))

    def handle_add_receptionist_post(self, data):
        first_name = data.get('receptionist_first_name', '')
        last_name = data.get('receptionist_last_name', '')

        try:
            add_receptionist(first_name, last_name)

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("<p>Recepcjonistka została dodana.</p>".encode('utf-8'))

        except Exception as e:
            # Wysłanie odpowiedzi HTTP w przypadku błędu
            self.send_response(500)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(f"<p>Wystąpił błąd: {e}</p>".encode('utf-8'))


def run_server():
    PORT = 8000
    with HTTPServer(("", PORT), MyHandler) as httpd:
        print(f"Serwer uruchomiony na porcie {PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()


