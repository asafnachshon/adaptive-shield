class LoadDataMissingFileError(Exception):
    def __init__(self, path):
        error_message = (
            f"missing file: {path}"
        )
        super().__init__(error_message)


__all__ = [
    "LoadDataMissingFileError"
]
