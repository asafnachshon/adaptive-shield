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
    # getting an array of rows of `Terms by species or taxon` from `https://en.wikipedia.org/wiki/List_of_animal_names`
    animals_table_rows = get_animals_table()

    # for each row, creating an object of name, collateral_adjective and image_local_link.
    # image local link is created when `get_row_animal_data_cells` function downloads an image.
    # image download is an external event that takes time - good for threading
    with ThreadPoolExecutor() as executor:
        responses = executor.map(get_row_animal_data_cells, animals_table_rows)

    # sorting the extracted data in an array of objects, each objects has a unique collateral_adjective and all the
    # animals (and local link of each animal image) belongs to it.
    data = sort_animals_data_to_parsable_object(itr=responses)

    # converting the data object to html file (convert_object_to_html_table(obj=data)) and saving it to a file.
    # env variable `LOCAL_COLLATERAL_ADJECTIVE_HTML` is the key of the html file path.
    save_data_to_file(
        data=convert_object_to_html_table(obj=data),
        file_path=os.getenv("LOCAL_COLLATERAL_ADJECTIVE_HTML"),
    )


__all__ = ["animals_by_collateral_adjective"]
