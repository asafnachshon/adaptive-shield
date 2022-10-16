import os
import shutil
import requests


def download_file(url, local_directory):
    stream = requests.get(url=url, stream=True)
    local_path = f"{local_directory}/{os.path.basename(url)}"
    with open(local_path, "wb") as out_file:
        shutil.copyfileobj(fsrc=stream.raw, fdst=out_file)
    return local_path


def load_data_from_file(file_path):
    try:
        with open(file_path, "r") as file_:
            return file_.read()
    except FileNotFoundError:
        raise Exception(f"{file_path} does not exist")
    except IsADirectoryError:
        raise Exception(f"{file_path} is not a file")


def save_data_to_file(data, file_path):
    # create path to file if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # save data to file path
    with open(file_path, "w") as file_:
        file_.write(data)


__all__ = ["download_file", "load_data_from_file", "save_data_to_file"]
