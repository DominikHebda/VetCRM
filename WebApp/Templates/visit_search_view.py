def render_visit_search_results(visits):
    with open("templates/output_searching_visit.html", "r", encoding="utf-8") as f:
        html = f.read()

    rows = ""
    for visit in visits:
        visit_id, pet_name, client_name, visit_date, visit_time, diagnosis = visit
        rows += f"""
            <tr>
                <td>{visit_id}</td>
                <td>{pet_name}</td>
                <td>{client_name}</td>
                <td>{visit_date}</td>
                <td>{visit_time}</td>
                <td>{diagnosis}</td>
                <td>
                    <div class="btn-group">
                        <a href="/update_visit/{visit_id}" class="btn btn-edit">Edytuj</a>
                        <a href="/delete_visit/{visit_id}" class="btn btn-danger">Usuń</a>
                    </div>
                </td>
            </tr>
        """
    return html.replace("{{ visit_rows }}", rows)


def render_visit_not_found():
    return "<p>Nie znaleziono wizyt dla podanych danych.</p>"
