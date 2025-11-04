def render_pets_list_page(pets, current_page=1, total_pages=1):
    """
    Generuje stronę HTML z listą zwierząt z obsługą paginacji (bez linku do właściciela).
    """
    pets_rows = ""

    for pet in pets:
        pet_id = pet[0]
        pet_name = pet[1]
        species = pet[2]
        breed = pet[3]
        age = pet[4]
        deletion_date = pet[5].strftime('%Y-%m-%d %H:%M:%S') if pet[5] else "Zwierzę aktywne"
        owner_first_name = pet[6] or ""
        owner_last_name = pet[7] or ""

        owner_full_name = f"{owner_first_name} {owner_last_name}".strip() if (owner_first_name or owner_last_name) else "Brak właściciela"

        pets_rows += f"""
        <tr>
            <td>{pet_id}</td>
            <td>{pet_name}</td>
            <td>{species}</td>
            <td>{breed}</td>
            <td>{age}</td>
            <td>{deletion_date}</td>
            <td>{owner_full_name}</td>
            <td>
                <div class="btn-group">
                    <a href="/pet_details/{pet_id}" class="btn btn-info btn-sm">Szczegóły</a>
                    <a href="/update_pet/{pet_id}" class="btn btn-edit btn-sm">Edytuj</a>
                    <a href="/delete_pet/{pet_id}" class="btn btn-danger btn-sm">Usuń</a>
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
            pagination_html += f'<li class="page-item"><a class="page-link" href="/pets_list/?page={current_page - 1}">«</a></li>'

        # Numery stron
        for p in range(1, total_pages + 1):
            active = "active" if p == current_page else ""
            pagination_html += f'<li class="page-item {active}"><a class="page-link" href="/pets_list/?page={p}">{p}</a></li>'

        # Przycisk "następna strona"
        if current_page < total_pages:
            pagination_html += f'<li class="page-item"><a class="page-link" href="/pets_list/?page={current_page + 1}">»</a></li>'

        pagination_html += '</ul></nav>'

    # --- Wczytanie szablonu HTML ---
    with open("templates/pets_list.html", "r", encoding="utf-8") as f:
        template = f.read()

    # --- Podmiana zmiennych w szablonie ---
    html = template.replace("{{ pets_rows }}", pets_rows)
    html = html.replace("{{ pagination }}", pagination_html)

    return html
