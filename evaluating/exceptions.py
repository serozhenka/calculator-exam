class EvaluatorException(Exception):
    """Exception which might be raised when evaluating expression."""

    def __init__(self, message):
        message = "\nEvaluator exception.\n%s" % message
        super(EvaluatorException, self).__init__(message)
