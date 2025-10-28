def render_clients_list_page(clients):
    """
    Generuje stronę HTML z listą klientów na podstawie danych pobranych z bazy.
    """
    client_rows = ""

    for client in clients:
        client_id = client[0]
        first_name = client[1]
        last_name = client[2]
        phone = client[3]
        address = client[4]
        deletion_date = client[5] if client[5] else ""

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

    # Wczytujemy szablon HTML
    with open("templates/clients_list.html", "r", encoding="utf-8") as f:
        template = f.read()

    # Wstawiamy wygenerowane wiersze do szablonu
    html = template.replace("{{ client_rows }}", client_rows)

    return html
