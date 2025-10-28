def render_visits_list_page(visits):
 
    visits_rows = ""

    for visit in visits:
        visit_id = visit['id']
        diagnosis = visit.get('diagnosis', 'Brak danych')
        deletion_date = (
            visit['soft_delete'].strftime('%Y-%m-%d %H:%M:%S')
            if visit.get('soft_delete')
            else "Wizyta aktywna"
        )

        visits_rows += f"""
        <tr>
            <td>{visit_id}</td>
            <td>{visit['created_at']}</td>
            <td>{visit['client_full_name']}</td>
            <td>{visit['pet_name']}</td>
            <td>{visit['doctor_full_name']}</td>
            <td>{visit['visit_date']}</td>
            <td>{visit['visit_time']}</td>
            <td>{diagnosis}</td>
            <td>{deletion_date}</td>
            <td>
                <div class="btn-group">
                    <a href="/visit_details/{visit_id}" class="btn btn-info">Szczegóły</a>
                    <a href="/update_visit/{visit_id}" class="btn btn-edit">Edytuj</a>
                    <a href="/delete_visit/{visit_id}" class="btn btn-danger">Usuń</a>
                </div>
            </td>
        </tr>
        """

    # Wczytanie szablonu HTML
    with open("templates/visits_list.html", "r", encoding="utf-8") as f:
        template = f.read()

    # Wstawienie danych do szablonu
    html = template.replace("{{ visit_rows }}", visits_rows)
    return html
