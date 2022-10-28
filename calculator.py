from parsing.constants import TOKEN_TO_REGEX_MAP
from parsing.parser import Parser
from evaluating.evaluator import Evaluator


class Calculator:

    @staticmethod
    def calculate(expression: str):
        parser = Parser()
        result = parser.parse(expression, TOKEN_TO_REGEX_MAP)
        evaluator = Evaluator()
        return evaluator.evaluate(result)

