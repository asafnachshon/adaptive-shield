from adaptive_shield.utils import http_get
from bs4 import BeautifulSoup


def parsed_html(url, parser="lxml"):
    # string response from a successful http GET request (in a html structure)
    html = http_get(url=url).text
    # using BeautifulSoup to return a data structure of parsed html document
    return BeautifulSoup(markup=html, features=parser)


def get_all_tables(parsed_html_obj, table_class):
    # getting all the parsed html (beautifulSoup object) tables with a specific class.
    tables = parsed_html_obj.find_all("table", {"class": table_class})

    # filter only the tables bodies from the tables.
    table_bodies = [table.find("tbody") for table in tables]

    # return an array of arrays.
    # each array contains all the rows of one table.
    return [table_body.find_all("tr") for table_body in table_bodies]


def get_text_without_superscript(data_cell):
    # removing the superscript from a data cell and return the cell text in an array.
    return [
        elem.text.strip()
        for elem in data_cell
        if elem not in data_cell.find_all("sup") and elem.text.strip()
    ]


__all__ = ["get_all_tables", "get_text_without_superscript", "parsed_html"]
