class ParserException(Exception):
    """Exception which might be raised when parsing expression string."""

    def __init__(self, message, start=None, end=None):
        self.message = message
        self.type = "Parser exception"
        self.start = start
        self.end = end
        super(ParserException, self).__init__(self.message)
