from Database.operations_visits import fetch_scheduled_visits, fetch_visits_details, update_visit_in_db
from http.server import SimpleHTTPRequestHandler, HTTPServer

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
                <th>Godzina wizyty<th>
                <th>Pokaż szczegóły</th>
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
        visit_time = visit[10]

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
    <form method="POST" action="/update/{visit_id}" enctype="application/x-www-form-urlencoded; charset=UTF-8>
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

def run_server():
    PORT = 8000
    with HTTPServer(("", PORT), MyHandler) as httpd:
        print(f"Serwer uruchomiony na porcie {PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()


