from adaptive_shield.utils import http_get
from bs4 import BeautifulSoup


def parsed_html(url, parser="lxml"):
    html = http_get(url=url).text
    return BeautifulSoup(markup=html, features=parser)


def get_all_tables(parsed_html_obj):
    tables = parsed_html_obj.find_all("table", {"class": "wikitable"})

    table_bodies = [table.find("tbody") for table in tables]
    return [table_body.find_all("tr") for table_body in table_bodies]


def get_text_without_superscript(data_cell):
    return [
        elem.text.strip()
        for elem in data_cell
        if elem not in data_cell.find_all("sup") and elem.text.strip()
    ]


__all__ = ["get_all_tables", "get_text_without_superscript", "parsed_html"]
