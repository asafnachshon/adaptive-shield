class LoadDataFromFileError(Exception):
    def __init__(self, error):
        error_message = f"failed to load data from file: {error}"
        super().__init__(error_message)


__all__ = ["LoadDataFromFileError"]
