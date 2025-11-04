def render_clients_list_page(clients, current_page=1, total_pages=1):
    """
    Generuje stronę HTML z listą klientów z paginacją.
    """
    client_rows = ""

    for client in clients:
        client_id = client[0]
        first_name = client[1]
        last_name = client[2]
        phone = client[3]
        address = client[4]
        deletion_date = client[5].strftime('%Y-%m-%d %H:%M:%S') if client[5] else "Klient aktywny"

        client_rows += f"""
        <tr>
            <td>{client_id}</td>
            <td>{first_name}</td>
            <td>{last_name}</td>
            <td>{phone}</td>
            <td>{address}</td>
            <td>{deletion_date}</td>
            <td>
                <div class="btn-group">
                    <a href="/client_details/{client_id}" class="btn btn-info btn-sm">Szczegóły</a>
                    <a href="/update_client/{client_id}" class="btn btn-edit btn-sm">Edytuj</a>
                    <a href="/delete_client/{client_id}" class="btn btn-danger btn-sm">Usuń</a>
                </div>
            </td>
        </tr>
        """

    # --- Generowanie sekcji paginacji ---
    pagination_html = ""
    if total_pages > 1:
        pagination_html = '<nav aria-label="Stronicowanie"><ul class="pagination justify-content-center">'

        # Przycisk poprzedniej strony
        if current_page > 1:
            pagination_html += f'<li class="page-item"><a class="page-link" href="/clients_list/?page={current_page - 1}">«</a></li>'

        # Numery stron
        for p in range(1, total_pages + 1):
            active = "active" if p == current_page else ""
            pagination_html += f'<li class="page-item {active}"><a class="page-link" href="/clients_list/?page={p}">{p}</a></li>'

        # Przycisk następnej strony
        if current_page < total_pages:
            pagination_html += f'<li class="page-item"><a class="page-link" href="/clients_list/?page={current_page + 1}">»</a></li>'

        pagination_html += '</ul></nav>'

    # --- Wczytanie szablonu HTML ---
    with open("templates/clients_list.html", "r", encoding="utf-8") as f:
        template = f.read()

    # --- Podmiana znaczników ---
    html = template.replace("{{ client_rows }}", client_rows)
    html = html.replace("{{ pagination }}", pagination_html)

    return html
