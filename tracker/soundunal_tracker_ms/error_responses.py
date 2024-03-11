class ErrorResponse():
    """
    Class representing an error response.

    Attributes:
        message (str): A message describing the error.
    """

    def __init__(self, message, status):
        self.message = message
        self.status = status
