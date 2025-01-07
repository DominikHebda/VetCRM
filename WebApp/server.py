from Database.operations_visits import fetch_scheduled_visits
from http.server import SimpleHTTPRequestHandler, HTTPServer

def render_visits_to_html():
    visits = fetch_scheduled_visits()  
    print(f"Fetch scheduled visits: {visits}")  
    if not visits:
        return "<p>Brak zaplanowanych wizyt.</p>"

    # Generowanie HTML dla tabeli wizyt
    visits_html = """
    <table border="1">
        <thead>
            <tr>
                <th>ID</th>
                <th>Data wizyty</th>
                <th>Nazwisko klienta</th>
                <th>Nazwa zwierzęcia</th>
                <th>Lekarz</th>
            </tr>
        </thead>
        <tbody>
    """

    for visit in visits:
        visit_id = visit[0]  
        visit_date = visit[5]  
        client_last_name = visit[2]  
        pet_name = visit[3] 
        doctor_name = visit[4]  
        visits_html += f"""
        <tr>
            <td>{visit_id}</td>
            <td>{visit_date}</td>
            <td>{client_last_name}</td>
            <td>{pet_name}</td>
            <td>{doctor_name}</td>
        </tr>
        """

    visits_html += "</tbody></table>"

    with open("templates/index.html", "r", encoding="utf-8") as f:
        html_template = f.read()

    final_html = html_template.replace("{{ visits_table }}", visits_html)

    return final_html


from http.server import SimpleHTTPRequestHandler, HTTPServer

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            visits_html = render_visits_to_html() 
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(visits_html.encode('utf-8'))
        else:
            super().do_GET()

def run_server():
    PORT = 8000
    with HTTPServer(("", PORT), MyHandler) as httpd:
        print(f"Serwer uruchomiony na porcie {PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
