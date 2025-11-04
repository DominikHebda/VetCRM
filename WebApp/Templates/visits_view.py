def render_visits_list_page(visits, current_page=1, total_pages=1):
    visit_rows = ""

    for visit in visits:
        visit_id = visit["id"]
        created_at = visit["created_at"]
        client_full_name = visit["client_full_name"]
        pet_name = visit["pet_name"]
        doctor_full_name = visit["doctor_full_name"]
        visit_date = visit["visit_date"]
        visit_time = visit["visit_time"]
        diagnosis = visit["diagnosis"]
        soft_delete = visit["soft_delete"]

        visit_status = (
            "Wizyta aktualna"
            if not soft_delete
            else soft_delete.strftime("%Y-%m-%d %H:%M:%S")
        )

        visit_rows += f"""
        <tr>
            <td>{visit_id}</td>
            <td>{created_at}</td>
            <td>{client_full_name}</td>
            <td>{pet_name}</td>
            <td>{doctor_full_name}</td>
            <td>{visit_date}</td>
            <td>{visit_time}</td>
            <td>{diagnosis}</td>
            <td>{visit_status}</td>
            <td>
                <div class="btn-group">
                    <a href="/visit_details/{visit_id}" class="btn btn-info btn-sm">Szczegóły</a>
                    <a href="/update_visit/{visit_id}" class="btn btn-edit btn-sm">Edytuj</a>
                    <a href="/delete_visit/{visit_id}" class="btn btn-danger btn-sm">Usuń</a>
                </div>
            </td>
        </tr>
        """

    # generujemy HTML do paginacji
    pagination_html = '<nav aria-label="Page navigation"><ul class="pagination justify-content-center">'
    for p in range(1, total_pages + 1):
        if p == current_page:
            pagination_html += f'<li class="page-item active"><a class="page-link" href="?page={p}">{p}</a></li>'
        else:
            pagination_html += f'<li class="page-item"><a class="page-link" href="?page={p}">{p}</a></li>'
    pagination_html += '</ul></nav>'

    # wczytujemy szablon HTML
    with open("templates/visits_list.html", "r", encoding="utf-8") as f:
        template = f.read()

    html = template.replace("{{ visit_rows }}", visit_rows)
    html = html.replace("{{ pagination }}", pagination_html)

    return html
