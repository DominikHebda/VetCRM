from Database.operations_visits import fetch_scheduled_visits, fetch_visits_details
from http.server import SimpleHTTPRequestHandler, HTTPServer

def render_visits_to_html():
    visits = fetch_scheduled_visits()  
    if not visits:
        return "<p>Brak zaplanowanych wizyt.</p>"

    # Generowanie HTML dla tabeli wizyt
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
                <th>Pokaż szczegóły</th>
            </tr>
        </thead>
        <tbody>
    """

    for visit in visits:
        visit_id = visit[0]  
        visit_date = visit[1]  
        client_last_name = visit[2]  
        pet_name = visit[3] 
        doctor_name = visit[4]  
        date_of_next_visit = visit[5]

        visit_details_link = f'<a href="/visit/{visit_id}">Pokaż szczegóły</a>'
        visits_html += f"""
        <tr>
            <td>{visit_id}</td>
            <td>{visit_date}</td>
            <td>{client_last_name}</td>
            <td>{pet_name}</td>
            <td>{doctor_name}</td>
            <td>{date_of_next_visit}</td>
            <td>{visit_details_link}</td>
        </tr>
        """

    visits_html += "</tbody></table>"

    with open("templates/index.html", "r", encoding="utf-8") as f:
        html_template = f.read()

    final_html = html_template.replace("{{ visits_table }}", visits_html)

    return final_html

def render_visit_details(visit_id):
    # Fetch the visit details from the database
    # Zastąp poniższą funkcję fetch_visit_details odpowiednią funkcją, która pobierze szczegóły wizyty na podstawie ID.
    visit = fetch_visits_details(visit_id)
    if not visit:
        return "<p>Wizyta o podanym ID nie została znaleziona.</p>"

    visit_id = visit[0]
    visit_date = visit[1]
    client_last_name = visit[2]
    pet_name = visit[3]
    doctor_name = visit[4]
    date_of_next_visit = visit[5]

    # Generowanie HTML z danymi wizyty
    visit_details_html = f"""
    <h1>Szczegóły wizyty</h1>
    <p><strong>ID wizyty:</strong> {visit_id}</p>
    <p><strong>Data utworzenia wizyty:</strong> {visit_date}</p>
    <p><strong>Nazwisko klienta:</strong> {client_last_name}</p>
    <p><strong>Nazwa zwierzęcia:</strong> {pet_name}</p>
    <p><strong>Lekarz:</strong> {doctor_name}</p>
    <p><strong>Data następnej wizyty:</strong> {date_of_next_visit}</p>
    <p><a href="/">Powrót do listy wizyt</a></p>
    """

    return visit_details_html




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
                print(f"Requested visit ID: {visit_id}")  # Debug: print ID wizyty
                visit_details_html = render_visit_details(visit_id)
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(visit_details_html.encode('utf-8'))
            except ValueError:
                print(f"Invalid visit ID format: {visit_id}")  # Debug: print błąd formatu ID
                self.send_response(404)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("<p>Niepoprawne ID wizyty.</p>".encode('utf-8'))
        else:
            super().do_GET()


def run_server():
    PORT = 8000
    with HTTPServer(("", PORT), MyHandler) as httpd:
        print(f"Serwer uruchomiony na porcie {PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()


