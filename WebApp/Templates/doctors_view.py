def render_doctors_list_page(doctors):
    """
    Generuje stronę HTML z listą lekarzy na podstawie danych pobranych z bazy.
    """
    doctors_rows = ""

    for doctor in doctors:
        doctor_id = doctor[0]
        first_name = doctor[1]
        last_name = doctor[2]
        specialization = doctor[3]
        phone = doctor[4]
        deletion_date = doctor[5].strftime('%Y-%m-%d %H:%M:%S') if doctor[5] else "Lekarz aktywny"

        doctors_rows += f"""
        <tr>
            <td>{doctor_id}</td>
            <td>{first_name}</td>
            <td>{last_name}</td>
            <td>{specialization}</td>
            <td>{phone}</td>
            <td>{deletion_date}</td>
            <td>
                <div class="btn-group">
                    <a href="/doctor_details/{doctor_id}" class="btn btn-info btn-sm">Szczegóły</a>
                    <a href="/update_doctor/{doctor_id}" class="btn btn-edit btn-sm">Edytuj</a>
                    <a href="/delete_doctor/{doctor_id}" class="btn btn-danger btn-sm">Usuń</a>
                </div>
            </td>
        </tr>
        """

    # Wczytujemy szablon HTML z folderu templates
    with open("templates/doctors_list.html", "r", encoding="utf-8") as f:
        template = f.read()

    # Wstawiamy wygenerowane wiersze tabeli
    html = template.replace("{{ doctor_rows }}", doctors_rows)

    return html
