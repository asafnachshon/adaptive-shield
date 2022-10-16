import os
import shutil
import requests

from bson import json_util


def download_file(url, local_directory):
    stream = requests.get(url=url, stream=True)
    local_path = f"{local_directory}/{os.path.basename(url)}"
    with open(local_path, "wb") as out_file:
        shutil.copyfileobj(fsrc=stream.raw, fdst=out_file)
    return local_path


def load_json_file(file_path):
    with open(file_path, "r") as json_file:
        return json_util.loads(json_file.read())


def save_json_file(json_data, file_path):
    with open(file_path, "w") as json_file:
        json_file.write(json_util.dumps(json_data))


__all__ = ["download_file", "load_json_file", "save_json_file"]
