def render_pets_list_page(pets):
    """
    Renderuje stronę z listą zwierząt.
    Dane (pets) to lista krotek: (id, name, species, breed, sex, soft_delete, owner_first_name, owner_last_name)
    """
    pets_rows = ""

    for pet in pets:
        pet_id = pet[0]
        name = pet[1]
        species = pet[2]
        breed = pet[3]
        sex = pet[4]
        deletion_date = pet[5].strftime('%Y-%m-%d %H:%M:%S') if pet[5] else "Zwierzę aktywne"
        owner_name = f"{pet[6]} {pet[7]}" if pet[6] and pet[7] else "Brak danych"

        pets_rows += f"""
        <tr>
            <td>{pet_id}</td>
            <td>{name}</td>
            <td>{species}</td>
            <td>{breed}</td>
            <td>{sex}</td>
            <td>{deletion_date}</td>
            <td>{owner_name}</td>
            <td>
                <div class="btn-group">
                    <a href="/pet_details/{pet_id}" class="btn btn-info">Szczegóły</a>
                    <a href="/update_pet/{pet_id}" class="btn btn-edit">Edytuj</a>
                    <a href="/delete_pet/{pet_id}" class="btn btn-danger">Usuń</a>
                </div>
            </td>
        </tr>
        """
        

    # Wczytanie szablonu HTML
    with open("templates/pets_list.html", "r", encoding="utf-8") as f:
        template = f.read()

    # Wstawienie wygenerowanych wierszy do szablonu
    html = template.replace("{{ pets_rows }}", pets_rows)
    return html
 