def render_pet_search_results(pets):
    with open("templates/output_searching_pet.html", "r", encoding="utf-8") as f:
        html = f.read()

    rows = ""
    for pet in pets:
        deletion_date = pet[5].strftime('%Y-%m-%d %H:%M:%S') if pet[5] else "Zwierzę aktywne"
        rows += f"""
            <tr>
                <td>{pet[0]}</td>
                <td>{pet[1]}</td>
                <td>{pet[2]}</td>
                <td>{pet[3]}</td>
                <td>{pet[4]}</td>
                <td>{deletion_date}</td>
                <td>{pet[6]} {pet[7]}</td>
                <td>
                    <div class="btn-group">
                        <a href="/update_pet/{pet[0]}" class="btn btn-edit">Edytuj</a>
                        <a href="/delete_pet/{pet[0]}" class="btn btn-danger">Usuń</a>
                    </div>
                </td>
            </tr>
        """
    return html.replace("{{ pet_rows }}", rows)


def render_pet_not_found():
    return "<p>Nie znaleziono zwierząt.</p>"
