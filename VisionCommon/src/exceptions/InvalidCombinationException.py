class InvalidCombinationException(Exception):
    """Exception for when an invalid combination of arguments is passed"""

    def __init__(self, message="Invalid Argument Combination"):
        self.message = message
        super().__init__(self.message)
