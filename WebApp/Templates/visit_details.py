from datetime import datetime

def render_visit_details_page(appointment, client, pet, doctor):
    """
    appointment: (id, client_id, pet_id, doctor_id, visit_date, visit_time, diagnosis, soft_delete)
    client: (id, first_name, last_name, phone, address, soft_delete) lub None
    pet: (id, pet_name, species, breed, age, soft_delete, client_id) lub None
    doctor: (id, first_name, last_name, phone, specialization, soft_delete) lub None
    """
    appointment_id, client_id, pet_id, doctor_id, visit_date, visit_time, diagnosis, soft_delete = appointment

    # Status wizyty
    if not soft_delete or str(soft_delete).strip() in ("0", "", "None", "null"):
        appointment_status = "Aktywna"
    else:
        try:
            soft_delete_dt = (
                soft_delete if hasattr(soft_delete, "strftime")
                else datetime.strptime(str(soft_delete), "%Y-%m-%d %H:%M:%S")
            )
            appointment_status = f"Usunięta: {soft_delete_dt.strftime('%Y-%m-%d %H:%M:%S')}"
        except Exception:
            appointment_status = f"Usunięta ({soft_delete})"

    # 🔹 Klient
    if client is None:
        client_first_name = client_last_name = client_phone = client_address = client_status = "-"
    else:
        _, client_first_name, client_last_name, client_phone, client_address, client_soft_delete = client
        client_status = "Aktywny" if not client_soft_delete else f"Usunięty: {client_soft_delete.strftime('%Y-%m-%d %H:%M:%S')}"

    # 🔹 Zwierzę
    if pet is None:
        pet_name = pet_species = pet_breed = pet_age = pet_status = "-"
    else:
        _, pet_name, pet_species, pet_breed, pet_age, pet_soft_delete, _ = pet
        if not pet_soft_delete or str(pet_soft_delete).strip() in ("0", "", "None", "null"):
            pet_status = "Aktywne"
        else:
            try:
                soft_delete_dt = (
                    pet_soft_delete if hasattr(pet_soft_delete, "strftime")
                    else datetime.strptime(str(pet_soft_delete), "%Y-%m-%d %H:%M:%S")
                )
                pet_status = f"Usunięte: {soft_delete_dt.strftime('%Y-%m-%d %H:%M:%S')}"
            except Exception:
                pet_status = f"Usunięte ({pet_soft_delete})"

    # 🔹 Weterynarz
    if doctor is None:
        doctor_first_name = doctor_last_name = doctor_phone = doctor_specialization = doctor_status = "-"
    else:
        _, doctor_first_name, doctor_last_name, doctor_phone, doctor_specialization, doctor_soft_delete = doctor
        doctor_status = "Aktywny" if not doctor_soft_delete else f"Usunięty: {doctor_soft_delete.strftime('%Y-%m-%d %H:%M:%S')}"

    # Wczytanie szablonu HTML
    with open("templates/visit_details.html", "r", encoding="utf-8") as f:
        template = f.read()

    html = template
    html = html.replace("{{ visit_date }}", str(visit_date))
    html = html.replace("{{ visit_time }}", str(visit_time))
    html = html.replace("{{ diagnosis }}", str(diagnosis or "-"))
    html = html.replace("{{ appointment_status }}", appointment_status)

    html = html.replace("{{ client_first_name }}", str(client_first_name))
    html = html.replace("{{ client_last_name }}", str(client_last_name))
    html = html.replace("{{ client_phone }}", str(client_phone))
    html = html.replace("{{ client_address }}", str(client_address))
    html = html.replace("{{ client_status }}", str(client_status))

    html = html.replace("{{ pet_name }}", str(pet_name))
    html = html.replace("{{ pet_species }}", str(pet_species))
    html = html.replace("{{ pet_breed }}", str(pet_breed))
    html = html.replace("{{ pet_age }}", str(pet_age))
    html = html.replace("{{ pet_status }}", str(pet_status))

    html = html.replace("{{ doctor_first_name }}", str(doctor_first_name))
    html = html.replace("{{ doctor_last_name }}", str(doctor_last_name))
    html = html.replace("{{ doctor_phone }}", str(doctor_phone))
    html = html.replace("{{ doctor_specialization }}", str(doctor_specialization))
    html = html.replace("{{ doctor_status }}", str(doctor_status))

    return html
