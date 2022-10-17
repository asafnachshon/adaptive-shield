import os

from adaptive_shield.services import get_main_page_image_url
from adaptive_shield.utils import (
    download_file,
    get_all_tables,
    get_text_without_superscript,
    parsed_html,
)


def get_animals_table():
    # 'WIKIPEDIA_HOST' value should be 'https://en.wikipedia.org'.
    # the parsed html object is BeautifulSoup object of the wiki page 'List_of_animal_names'
    parsed_html_obj = parsed_html(
        url=f"{os.getenv('WIKIPEDIA_HOST')}/wiki/List_of_animal_names"
    )

    # in the browser, using inspect to get the 'Terms by species or taxon' table class.
    # getting an array of all the tables in the 'List_of_animal_names' wiki page with class "wikitable".
    # each table is an array of table rows.
    tables = get_all_tables(parsed_html_obj=parsed_html_obj, table_class="wikitable")

    # the 'Terms by species or taxon' table is the last table in the page, and the last one in the table array.
    return tables[-1]


def download_animal_main_page_image(animal_name, local_directory):
    # getting the animal main page image url using wikipedia API.
    image_url = get_main_page_image_url(title=animal_name)
    if image_url is None:
        return "missing"

    # downloading the file to a local directory ('/tmp') and getting the file full local path
    file_path = download_file(url=image_url, local_directory=local_directory)
    return file_path


def get_row_animal_data_cells(row):
    # get all cells of type data from a table row.
    # creates an array of data cells and filters out all the header cells.
    cells = row.find_all("td")
    if not cells:
        return

    # removing all super script out of the name cell (first cell) that might be extracted from the cell text.
    # 'get_text_without_superscript' returns an array, and for the name cell it will return with one sting.
    name = get_text_without_superscript(data_cell=cells[0])[0]

    # 'download_animal_main_page_image' downloads the image and returns the image local link.
    # collateral adjective is represented in the sixth cell, and may be one or more, so the value here is an array.
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

    # go over an iterator of animal data cells (that were created for row using 'get_row_animal_data_cells').
    # each cells_data is one (unique) animal data.
    for cells_data in itr:

        # if an empty object
        if not cells_data:
            continue

        # go over all the collateral adjectives of the animal.
        # if collateral adjective is already exists in the data dic, add the animal data (name and local link) to the
        # array. else, create a new key of collateral adjective with an array of one animal.
        for adjective in cells_data["collateral_adjective"]:
            if adjective in data:
                data[adjective].append(cells_data["animal"])
                continue
            data[adjective] = [cells_data["animal"]]

    # sort the data dictionary to array of dictionaries, each with the same keys.
    # similar keys will halp parse the data to html table later on.
    return [
        {"collateral_adjective": key, "animals": value} for key, value in data.items()
    ]


__all__ = [
    "download_animal_main_page_image",
    "get_animals_table",
    "get_row_animal_data_cells",
    "sort_animals_data_to_parsable_object",
]
