from Database.operations_visits import fetch_scheduled_visits, fetch_visits_details, update_visit_in_db, format_visit_time, add_next_visit, get_client_id, get_current_time
from Database.operations_client import add_client
from http.server import SimpleHTTPRequestHandler, HTTPServer
import urllib.parse
import logging

logging.basicConfig(level=logging.DEBUG)  # Ustawienie poziomu logowania na DEBUG



def render_visits_to_html():
    visits = fetch_scheduled_visits() 
    if not visits:
        return "<p>Brak zaplanowanych wizyt.</p>"

    visits_html = """
    <table border="1">
        <thead>
            <tr>
                <th>ID</th>
                <th>Data utworzenia wizyty</th>
                <th>Nazwisko klienta</th>
                <th>Nazwa zwierzęcia</th>
                <th>Lekarz</th>
                <th>Data następnej wizyty</th>
                <th>Godzina wizyty</th>
                <th>Pokaż szczegóły</th>
            </tr>
        </thead>
        <a href="/adding/">Dodaj wizytę</a>
        <tbody>
    """

    for visit in visits:
        visit_id = visit[0]  
        date = visit[1]  
        client_last_name = visit[2] 
        pet_name = visit[3]  
        doctor_name = visit[4] 
        date_of_visit = visit[5]  
        visit_time = visit[10]  

        visit_time = format_visit_time(visit_time)

        visit_details_link = f'<a href="/visit/{visit_id}">Pokaż szczegóły</a>'
        visit_edit_link = f'<a href="/update/{visit_id}">Edytuj wizytę</a>'

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
    
    visits_html += "</tbody></table>"

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
    visit_time = visit[10]

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

def render_add_next_visit():
    add_next_visit_form_html = """
    <h1>Dodaj wizytę</h1>
    <form method="POST" action="/adding/" enctype="application/x-www-form-urlencoded; charset=UTF-8">
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
        
        <label for="date_of_visit">Podaj datę następnej wizyty:</label>
        <input type="date" id="date_of_visit" name="date_of_visit" /><br><br>

        <label for="visit_time">Podaj godzinę wizyty:</label>
        <input type="time" id="visit_time" name="visit_time" /><br><br>

        <input type="submit" value="Zapisz wizytę" />
    </form>
    <p><a href="/">Powrót do listy wizyt</a></p>
    """ 

    return add_next_visit_form_html

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            visits_html = render_visits_to_html() 
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(visits_html.encode('utf-8'))
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

        elif self.path.startswith("/update/"):
            visit_id = self.path.split("/update/")[1]
            try:
                visit_id = int(visit_id)
                visit_edit_form_html = render_visit_edit_form(visit_id) 
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(visit_edit_form_html.encode('utf-8'))
            except ValueError:
                print(f"Invalid visit ID format: {visit_id}")  
                self.send_response(404)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("<p>Niepoprawne ID wizyty.</p>".encode('utf-8'))

        elif self.path.startswith("/adding/"):
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
                
        elif self.path.startswith("/adding/"):
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
                doctor = data.get('doctor_name')
                date_of_visit = data.get('date_of_visit')
                visit_time = data.get('visit_time')

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
                
                added = add_next_visit(
                    current_time=get_current_time(),
                    last_name_client=last_name,
                    pet_name=pet_name,
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



def run_server():
    PORT = 8000
    with HTTPServer(("", PORT), MyHandler) as httpd:
        print(f"Serwer uruchomiony na porcie {PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()


