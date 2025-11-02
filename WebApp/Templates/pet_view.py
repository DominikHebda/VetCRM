from datetime import datetime

def render_pet_details_page(pet, client, visits):
    """
    pet - (id, pet_name, species, breed, age, client_id, soft_delete)
    client - (id, first_name, last_name, phone, address, soft_delete) lub None
    visits - [(appointment_id, visit_date, visit_time, doctor_full_name, diagnosis), ...]
    """
    pet_id, pet_name, species, breed, age, soft_delete, client_id = pet
    if not soft_delete or str(soft_delete).strip() in ("0", "", "None", "null"):
        pet_status = "Aktywne"
    else:
        try:
            # Jeśli to string, próbujemy sparsować datę
            soft_delete_dt = (
                soft_delete if hasattr(soft_delete, "strftime")
                else datetime.strptime(str(soft_delete), "%Y-%m-%d %H:%M:%S")
            )
            pet_status = f"Usunięte: {soft_delete_dt.strftime('%Y-%m-%d %H:%M:%S')}"
        except Exception:
            pet_status = f"Usunięte ({soft_delete})"


    # 🧩 Jeśli klient nie istnieje
    if client is None:
        first_name = last_name = phone = address = client_status = "-"
    else:
        client_id, first_name, last_name, phone, address, client_soft_delete = client
        client_status = "Aktywny" if not client_soft_delete else f"Usunięty: {client_soft_delete.strftime('%Y-%m-%d %H:%M:%S')}"


    visits_rows = ""
    if visits:
        for v in visits:
            appointment_id, visit_date, visit_time, doctor_full_name, diagnosis = v
            diagnosis_text = diagnosis if diagnosis and str(diagnosis).strip() else "brak diagnozy"

            visits_rows += f"""
            <tr>
                <td>{visit_date.strftime('%Y-%m-%d') if hasattr(visit_date, 'strftime') else visit_date}</td>
                <td>{visit_time.strftime('%H:%M') if hasattr(visit_time, 'strftime') else visit_time}</td>
                <td>{doctor_full_name}</td>
                <td>{diagnosis_text}</td>
            </tr>
            """
    else:
        visits_rows = """
        <tr><td colspan="5" class="text-center text-muted">Brak wizyt dla tego zwierzęcia.</td></tr>
        """

    # Wczytanie szablonu HTML
    with open("templates/pet_details.html", "r", encoding="utf-8") as f:
        template = f.read()

    html = template
    html = html.replace("{{ pet_name }}", str(pet_name or "-"))
    html = html.replace("{{ pet_species }}", str(species or "-"))
    html = html.replace("{{ pet_breed }}", str(breed or "-"))
    html = html.replace("{{ pet_age }}", str(age or "-"))
    html = html.replace("{{ pet_status }}", pet_status)
    html = html.replace("{{ owner_first_name }}", str(first_name or "-"))
    html = html.replace("{{ owner_last_name }}", str(last_name or "-"))
    html = html.replace("{{ owner_phone }}", str(phone or "-"))
    html = html.replace("{{ owner_address }}", str(address or "-"))
    html = html.replace("{{ owner_status }}", client_status)
    html = html.replace("{{ visits_rows }}", visits_rows)

    return html
