import os

from adaptive_shield.services import get_main_page_image_url
from adaptive_shield.utils import (
    download_file,
    get_all_tables,
    get_text_without_superscript,
    parsed_html,
    save_json_file,
)
from concurrent.futures import ThreadPoolExecutor


def download_animal_image(href, local_directory):
    image_url = get_main_page_image_url(title=href)
    if image_url is None:
        return "missing"
    return download_file(url=image_url, local_directory=local_directory)


def get_row_data_cells(row, name_cell=0, collateral_adjective_cell=5):
    cells = row.find_all("td")
    if not cells:
        return

    name = get_text_without_superscript(data_cell=cells[name_cell])[0]

    return {
        "animal": {
            "name": name,
            "image_url": download_animal_image(
                href=name, local_directory=os.getenv("LOCAL_IMAGE_DIRECTORY")
            ),
        },
        "collateral_adjective": get_text_without_superscript(
            data_cell=cells[collateral_adjective_cell]
        ),
    }


def animals_by_collateral_adjective():
    parsed_html_obj = parsed_html(
        url=f"https://en.wikipedia.org/wiki/List_of_animal_names"
    )
    tables = get_all_tables(parsed_html_obj=parsed_html_obj)
    rows = tables[-1]

    data = {}
    with ThreadPoolExecutor() as executor:
        responses = executor.map(get_row_data_cells, rows)

    for cells_data in responses:
        if not cells_data:
            continue
        for adjective in cells_data["collateral_adjective"]:
            if adjective in data:
                data[adjective].append(cells_data["animal"])
                continue
            data[adjective] = [cells_data["animal"]]

    save_json_file(
        json_data=data, file_path=os.getenv("LOCAL_COLLATERAL_ADJECTIVE_JSON")
    )

    return data


__all__ = ["animals_by_collateral_adjective"]
