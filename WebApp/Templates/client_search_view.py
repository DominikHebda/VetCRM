def render_client_search_results(clients, template_path="templates/output_searching_client.html"):
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()

    rows = ""
    for c in clients:
        row = f"""
            <tr>
                <td>{c[0]}</td>
                <td>{c[1]}</td>
                <td>{c[2]}</td>
                <td>{c[3]}</td>
                <td>{c[4]}</td>
                <td>
                    <div class="btn-group">
                        <a href="/update_client/{c[0]}" class="btn btn-edit">Edytuj</a>
                        <a href="/delete_client/{c[0]}" class="btn btn-danger">Usuń</a>
                    </div>
                </td>
            </tr>
        """
        rows += row

    return html.replace("{{ client_rows }}", rows)



def render_client_not_found():
    return "<p>Nie znaleziono klientów.</p>"
