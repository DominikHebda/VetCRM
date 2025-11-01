def render_doctor_details_page(doctor, visits):
    """
    Renderuje stronę szczegółów lekarza i jego wizyt.
    doctor - (id, first_name, last_name, specialization, phone, email, soft_delete)
    visits - [(pet_name, client_full_name, visit_date, visit_time, diagnosis), ...]
    """
    id, first_name, last_name, specialization, phone, soft_delete = doctor
    doctor_status = "Aktywny" if not soft_delete else f"Usunięty: {soft_delete.strftime('%Y-%m-%d %H:%M:%S')}"

    # 🩺 Generowanie wierszy wizyt
    visits_rows = ""
    if visits:
        for v in visits:
            pet_name, client_full_name, visit_date, visit_time, diagnosis = v
            diagnosis_text = diagnosis if diagnosis and str(diagnosis).strip() else "brak diagnozy"
            visits_rows += f"""
            <tr>
                <td>{pet_name}</td>
                <td>{client_full_name}</td>
                <td>{visit_date.strftime('%Y-%m-%d') if hasattr(visit_date, 'strftime') else visit_date}</td>
                <td>{visit_time.strftime('%H:%M') if hasattr(visit_time, 'strftime') else visit_time}</td>
                <td>{diagnosis_text}</td>
            </tr>
            """
    else:
        visits_rows = """
        <tr>
            <td colspan="5" class="text-center text-muted">Brak wizyt przypisanych do tego lekarza.</td>
        </tr>
        """

    # 🔹 Wczytanie szablonu
    with open("templates/doctor_details.html", "r", encoding="utf-8") as f:
        template = f.read()

    # 🔹 Bezpieczna konwersja wszystkich pól na stringi
    html = template
    html = html.replace("{{ doctor_first_name }}", str(first_name or "-"))
    html = html.replace("{{ doctor_last_name }}", str(last_name or "-"))
    html = html.replace("{{ doctor_specialization }}", str(specialization or "-"))
    html = html.replace("{{ doctor_phone }}", str(phone or "-"))
    html = html.replace("{{ doctor_status }}", str(doctor_status))
    html = html.replace("{{ visits_rows }}", visits_rows)

    return html
