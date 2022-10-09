class ParserException(Exception):
    def __init__(self, message):
        message = "\nParser exception.\n%s" % message
        super(ParserException, self).__init__(message)