def render_edit_diagnosis_page(appointment_id, doctor_id, current_diagnosis):
    with open("templates/edit_diagnosis.html", "r", encoding="utf-8") as f:
        template = f.read()

    html = template.replace("{{ appointment_id }}", str(appointment_id))
    html = html.replace("{{ doctor_id }}", str(doctor_id))
    html = html.replace("{{ current_diagnosis }}", str(current_diagnosis or ""))

    return html
