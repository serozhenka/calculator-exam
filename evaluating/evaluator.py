from .constants import OPERATOR_TO_FUNC_MAP, STR_FUNC_TO_FUNC_MAP
from .exceptions import EvaluatorException
from parsing.constants import TokenType
from parsing.tokenizer import Token
from utils.data_structures import Stack


class Evaluator:
    """
    Class which evaluates parsed arithmetical expressions
    written in RPN (Reversed Polish Notation).
    """

    def __init__(self):
        self.stack = Stack()

    def evaluate(self, token_list) -> float:
        """
        Function which evaluates RPN expression.

        :param token_list: list[Token] - list of tokens written in RPN
        :return: decimal number: result of evaluated expression
        :rtype: float
        """

        for token in token_list:
            match token.token_type:  # pattern matching on token_type (TokenType)
                case TokenType.NUMBER.value:  # just push number to the stack
                    self.stack.push(token)

                case TokenType.OPERATOR.value:
                    # get last 2 elements from stack and proceed them with appropriate 2 param function

                    operand2, operand1 = float(self.stack.pop().value), float(self.stack.pop().value)
                    result = OPERATOR_TO_FUNC_MAP[token.value](operand1, operand2)
                    result_token = Token(TokenType.NUMBER.value, str(result))
                    self.stack.push(result_token)

                case TokenType.FUNC.value:
                    # get last element from stack and proceed it with appropriate 1 param function

                    operand = float(self.stack.pop().value)
                    function = STR_FUNC_TO_FUNC_MAP.get(token.value)
                    if not function:  # raise exception if function is unavailable
                        raise EvaluatorException(f"Unknown function: {token.value}")

                    result = function(operand)
                    result_token = Token(TokenType.NUMBER.value, str(result))
                    self.stack.push(result_token)

        return float(self.stack.pop().value)
