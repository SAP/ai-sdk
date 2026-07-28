class ValidationCollector:
    """
    A class to collect and manage validation errors encountered during the orchestration configuration validation process.
    """

    def __init__(self):
        self.errors = []

    def add_error(self, internal_code, message):
        """
        Adds an error to the collector.
        Args:
            internal_code (str): The internal error code.
            message (str): The detailed error message.
        """
        self.errors.append((internal_code, message))

    def has_errors(self):
        """
        checks if the collector collected any errors
        """
        return len(self.errors) > 0

    def has_error_code(self, code):
        """checks if error code exists in the list of errors"""
        return any(error_code == code for error_code, _ in self.errors)

    def raise_if_errors(self):
        """
        Raises a ValidationError if there are any collected errors.
        """
        if self.has_errors():
            error_messages = "\n".join(
                [
                    f"Error Code: {code}, Detailed Message: {msg}"
                    for code, msg in self.errors
                ]
            )
            raise RuntimeError(
                f"\nConfiguration error(s) encountered:\n{error_messages}"
            )
