class EvaluatorException(Exception):
    """Exception which might be raised when evaluating expression."""

    def __init__(self, message):
        self.type = "Evaluator exception"
        self.message = message
        super(EvaluatorException, self).__init__(message)
