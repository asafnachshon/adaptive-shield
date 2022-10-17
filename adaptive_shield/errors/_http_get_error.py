class HttpGetError(Exception):
    def __init__(self, error):
        error_message = (
            f"http get request failed: {error}"
        )
        super().__init__(error_message)


__all__ = [
    "HttpGetError"
]
