import os

from adaptive_shield.services import get_main_page_image_url
from adaptive_shield.utils import (
    download_file,
    get_all_tables,
    get_text_without_superscript,
    parsed_html,
)


def get_animals_table():
    parsed_html_obj = parsed_html(
        url=f"{os.getenv('WIKIPEDIA_HOST')}/wiki/List_of_animal_names"
    )
    tables = get_all_tables(parsed_html_obj=parsed_html_obj)
    return tables[-1]


def download_animal_main_page_image(animal_name, local_directory):
    image_url = get_main_page_image_url(title=animal_name)
    if image_url is None:
        return "missing"
    return download_file(url=image_url, local_directory=local_directory)


def get_row_animal_data_cells(row):
    cells = row.find_all("td")
    if not cells:
        return

    name = get_text_without_superscript(data_cell=cells[0])[0]

    return {
        "animal": {
            "name": name,
            "image_local_link": download_animal_main_page_image(
                animal_name=name, local_directory=os.getenv("LOCAL_IMAGE_DIRECTORY")
            ),
        },
        "collateral_adjective": get_text_without_superscript(data_cell=cells[5]),
    }


def sort_animals_data_to_parsable_object(itr):
    data = {}
    for cells_data in itr:
        if not cells_data:
            continue
        for adjective in cells_data["collateral_adjective"]:
            if adjective in data:
                data[adjective].append(cells_data["animal"])
                continue
            data[adjective] = [cells_data["animal"]]

    return [
        {"collateral_adjective": key, "animals": value} for key, value in data.items()
    ]


__all__ = [
    "download_animal_main_page_image",
    "get_animals_table",
    "get_row_animal_data_cells",
    "sort_animals_data_to_parsable_object",
]
