def paginate_list(data_list, page=1, per_page=20):
    """
    Dzieli listę danych na strony.
    Zwraca:
        - items_for_page: elementy dla danej strony
        - total_pages: liczba wszystkich stron
    """
    total_items = len(data_list)
    total_pages = (total_items + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    return data_list[start:end], total_pages
