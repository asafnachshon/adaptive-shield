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
    url = f"{os.getenv('WIKIPEDIA_HOST')}/w/api.php"
    params = {
        **PARAMS,
        "titles": title,
    }
    response = http_get(url=url, params=params)
    json_data = json_util.loads(response.text)
    pages = json_data["query"]["pages"]
    if not pages:
        return
    return pages[0].get("original", {}).get("source")


__all__ = ["get_main_page_image_url"]
