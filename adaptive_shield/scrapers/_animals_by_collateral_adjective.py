import os

from adaptive_shield.services import (
    get_animals_table,
    get_row_animal_data_cells,
    sort_animals_data_to_parsable_object,
)
from adaptive_shield.utils import (
    convert_object_to_html_table,
    save_data_to_file,
)
from concurrent.futures import ThreadPoolExecutor


def animals_by_collateral_adjective():
    animals_table_rows = get_animals_table()
    with ThreadPoolExecutor() as executor:
        responses = executor.map(get_row_animal_data_cells, animals_table_rows)

    data = sort_animals_data_to_parsable_object(itr=responses)
    save_data_to_file(
        data=convert_object_to_html_table(obj=data),
        file_path=os.getenv("LOCAL_COLLATERAL_ADJECTIVE_HTML"),
    )


__all__ = ["animals_by_collateral_adjective"]
