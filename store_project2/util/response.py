class Response:
    def __init__(self, status, status_code, data, message):
        """

        :rtype: object
        """
        self.status = status
        self.status_code = status_code
        self.data = data
        self.message = message

    def __str__(self):
        return f"status_code: {self.status_code}, data: {self.data}, message: {self.message}"
