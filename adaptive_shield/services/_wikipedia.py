import os
from adaptive_shield.utils import http_get
from bson import json_util


PARAMS = {
    "action": "query",
    "format": "json",
    "formatversion": 2,
    "prop": "pageimages|pageterms",
    "piprop": "original",
}


def get_main_page_image_url(title):
    # 'WIKIPEDIA_HOST' value should be 'https://en.wikipedia.org' and the title is the page title.
    url = f"{os.getenv('WIKIPEDIA_HOST')}/w/api.php"
    params = {
        **PARAMS,
        "titles": title,
    }

    # using the wikipedia api to get the all the page information using GET API.
    response = http_get(url=url, params=params)
    json_data = json_util.loads(response.text)
    pages = json_data["query"]["pages"]

    # return None if no pages under this title.
    if not pages:
        return

    # 'source' value in 'original' object is the main page image link
    return pages[0].get("original", {}).get("source")


__all__ = ["get_main_page_image_url"]
