def render_client_details_page(client, pets, visits):
    """
    Renderuje stronę szczegółów klienta, jego zwierząt i wizyt.
    client - (id, first_name, last_name, phone, address, soft_delete)
    pets - [(id, pet_name, species, breed, age, soft_delete), ...]
    visits - [(pet_name, visit_date, visit_time, doctor_full_name, diagnosis), ...]
    """
    id, first_name, last_name, phone, address, soft_delete = client
    client_status = "Klient aktywny" if not soft_delete else f"Usunięty: {soft_delete.strftime('%Y-%m-%d %H:%M:%S')}"

    # 🐾 Zwierzęta
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

    # 🗓️ Wizyty
    visits_rows = ""
    if visits:
        for visit in visits:
            pet_name, visit_date, visit_time, doctor_full_name, diagnosis = visit
            diagnosis_text = diagnosis if diagnosis and diagnosis.strip() else "brak diagnozy"
            visits_rows += f"""
            <tr>
                <td>{pet_name}</td>
                <td>{visit_date.strftime('%Y-%m-%d') if hasattr(visit_date, 'strftime') else visit_date}</td>
                <td>{visit_time.strftime('%H:%M') if hasattr(visit_time, 'strftime') else visit_time}</td>
                <td>{doctor_full_name}</td>
                <td>{diagnosis_text}</td>
            </tr>
            """
    else:
        visits_rows = """
        <tr>
            <td colspan="5" class="text-center text-muted">Brak wizyt dla tego klienta.</td>
        </tr>
        """

    # 🔹 Wczytanie szablonu
    with open("templates/client_details.html", "r", encoding="utf-8") as f:
        template = f.read()

    # 🔹 Podmiana znaczników
    html = template.replace("{{ client_first_name }}", first_name)
    html = html.replace("{{ client_last_name }}", last_name)
    html = html.replace("{{ client_phone }}", phone if phone else "-")
    html = html.replace("{{ client_address }}", address if address else "-")
    html = html.replace("{{ client_status }}", client_status)
    html = html.replace("{{ pets_rows }}", pets_rows)
    html = html.replace("{{ visits_rows }}", visits_rows)

    return html
