class ParserException(Exception):
    """Exception which might be raised when parsing expression string."""

    def __init__(self, message):
        message = "\nParser exception.\n%s" % message
        super(ParserException, self).__init__(message)
