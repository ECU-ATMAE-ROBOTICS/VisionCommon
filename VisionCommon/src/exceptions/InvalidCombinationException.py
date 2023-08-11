class InvalidCombinationException(Exception):
    def __init__(self, message="Invalid Argument Combination"):
        self.message = message
        super().__init__(self.message)
