def render_doctors_list_page(doctors, current_page=1, total_pages=1):
    """
    Generuje stronę HTML z listą lekarzy z obsługą paginacji.
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

    # --- Generowanie sekcji paginacji ---
    pagination_html = ""
    if total_pages > 1:
        pagination_html = '<nav aria-label="Stronicowanie"><ul class="pagination justify-content-center">'

        # Przycisk "poprzednia strona"
        if current_page > 1:
            pagination_html += f'<li class="page-item"><a class="page-link" href="/doctors_list/?page={current_page - 1}">«</a></li>'

        # Numery stron
        for p in range(1, total_pages + 1):
            active = "active" if p == current_page else ""
            pagination_html += f'<li class="page-item {active}"><a class="page-link" href="/doctors_list/?page={p}">{p}</a></li>'

        # Przycisk "następna strona"
        if current_page < total_pages:
            pagination_html += f'<li class="page-item"><a class="page-link" href="/doctors_list/?page={current_page + 1}">»</a></li>'

        pagination_html += '</ul></nav>'

    # --- Wczytanie szablonu HTML ---
    with open("templates/doctors_list.html", "r", encoding="utf-8") as f:
        template = f.read()

    # --- Podmiana zmiennych w szablonie ---
    html = template.replace("{{ doctor_rows }}", doctors_rows)
    html = html.replace("{{ pagination }}", pagination_html)

    return html
