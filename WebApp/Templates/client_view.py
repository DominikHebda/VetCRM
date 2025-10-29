def render_client_details_page(client, pets):
    """
    Renderuje stronę szczegółów klienta oraz jego zwierząt.
    client - krotka: (id, first_name, last_name, phone, address, soft_delete)
    pets - lista krotek: (id, pet_name, species, breed, age, soft_delete)
    """
    id, first_name, last_name, phone, address, soft_delete = client
    client_status = "Klient aktywny" if not soft_delete else f"Usunięty: {soft_delete.strftime('%Y-%m-%d %H:%M:%S')}"

    # Generowanie wierszy zwierząt
    pets_rows = ""
    for pet in pets:
        pet_id, pet_name, species, breed, age, pet_soft_delete = pet
        pet_status = "Aktywne" if not pet_soft_delete else f"Usunięte: {pet_soft_delete.strftime('%Y-%m-%d %H:%M:%S')}"
        pets_rows += f"""
        <tr>
            <td>{pet_id}</td>
            <td>{pet_name}</td>
            <td>{species}</td>
            <td>{breed}</td>
            <td>{age}</td>
            <td>{pet_status}</td>
        </tr>
        """

    # Wczytanie szablonu HTML
    with open("templates/client_details.html", "r", encoding="utf-8") as f:
        template = f.read()

    html = template.replace("{{ client_first_name }}", first_name)
    html = html.replace("{{ client_last_name }}", last_name)
    html = html.replace("{{ client_phone }}", phone if phone else "-")
    html = html.replace("{{ client_address }}", address if address else "-")
    html = html.replace("{{ client_status }}", client_status)
    html = html.replace("{{ pets_rows }}", pets_rows)

    return html
