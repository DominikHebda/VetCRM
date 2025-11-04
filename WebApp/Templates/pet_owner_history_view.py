def render_pet_owner_history_page(history_records, current_page=1, total_pages=1):
    """
    Generuje stronę HTML z historią właścicieli zwierząt z obsługą paginacji.
    """
    history_rows = ""

    for rec in history_records:
        record_id = rec[0]
        pet_name = rec[1] or "Brak danych"
        owner_name = rec[2] or "—"
        ownership_start = rec[3].strftime('%Y-%m-%d %H:%M:%S') if rec[3] else "—"
        ownership_end = rec[4].strftime('%Y-%m-%d %H:%M:%S') if rec[4] else "—"
        status = rec[5] or "Brak statusu"

        previous_owner = owner_name if status == "Zakończona" else "—"
        current_owner = owner_name if status == "Aktywna" else "—"

        history_rows += f"""
        <tr>
            <td>{record_id}</td>
            <td>{pet_name}</td>
            <td>{previous_owner}</td>
            <td>{current_owner}</td>
            <td>{ownership_start}</td>
            <td>{ownership_end}</td>
            <td>{status}</td>
        </tr>
        """

    # 🔹 PAGINACJA
    pagination_html = ""
    if total_pages > 1:
        pagination_html = '<nav aria-label="Stronicowanie"><ul class="pagination justify-content-center">'
        if current_page > 1:
            pagination_html += f'<li class="page-item"><a class="page-link" href="/pet_owner_history/?page={current_page - 1}">«</a></li>'
        for p in range(1, total_pages + 1):
            active = "active" if p == current_page else ""
            pagination_html += f'<li class="page-item {active}"><a class="page-link" href="/pet_owner_history/?page={p}">{p}</a></li>'
        if current_page < total_pages:
            pagination_html += f'<li class="page-item"><a class="page-link" href="/pet_owner_history/?page={current_page + 1}">»</a></li>'
        pagination_html += '</ul></nav>'

    # Wczytaj szablon
    with open("templates/pet_owner_history.html", "r", encoding="utf-8") as f:
        template = f.read()

    html = template.replace("{{ history_rows }}", history_rows)
    html = html.replace("{{ pagination }}", pagination_html)

    return html
