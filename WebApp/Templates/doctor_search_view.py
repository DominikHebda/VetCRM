def render_doctor_search_results(doctors):
    with open("templates/output_searching_doctor.html", "r", encoding="utf-8") as f:
        html = f.read()

    rows = ""
    for doctor in doctors:
        rows += f"""
            <tr>
                <td>{doctor[0]}</td>
                <td>{doctor[1]}</td>
                <td>{doctor[2]}</td>
                <td>{doctor[3]}</td>
                <td>{doctor[4]}</td>
                <td>
                    <div class="btn-group">
                        <a href="/update_doctor/{doctor[0]}" class="btn btn-edit">Edytuj</a>
                        <a href="/delete_doctor/{doctor[0]}" class="btn btn-danger">Usuń</a>
                    </div>
                </td>
            </tr>
        """

    return html.replace("{{ doctor_rows }}", rows)


def render_doctor_not_found():
    return "<p>Nie znaleziono lekarzy.</p>"
