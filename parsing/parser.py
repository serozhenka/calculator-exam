import math

from .constants import TokenType, OP_TO_PRECEDENCE_MAP
from .exceptions import ParserException
from .tokenizer import Tokenizer
from utils.data_structures import Stack, Queue


class Parser:
    """Class which parses arithmetical expression string."""

    def __init__(self):
        self.operator_stack = Stack()
        self.output_queue = Queue()

    def _tokenize(self, expression: str, token_to_regex_map: dict):
        """Function which gets list of tokens based on token_to_regex_map."""
        tokenizer = Tokenizer(token_to_regex_map)
        return tokenizer.tokenize(expression)

    def parse(self, expression: str, token_to_regex_map: dict):
        """
        Function that converts arithmetical expression string
        written in infix notation to postfix one (aka RPN (Reversed Polish Notation))
        using slightly improved Dijkstra's shunting yard algorithm.

        :param expression: str - arithmetical expression string
        :param token_to_regex_map: dict
        :return: list of tokens in RPN
        ":rtype: list[Token]
        """
        tokens = self._tokenize(expression, token_to_regex_map)

        for token in tokens:
            match token.token_type:  # pattern matching on token_type (TokenType)
                case TokenType.NUMBER.value:  # just push number to the output_queue
                    self.output_queue.push(token)

                case TokenType.FUNC.value:  # just push number to the operator stack
                    self.operator_stack.push(token)

                case TokenType.OPERATOR.value:
                    # While there is an operator o2 other than the left parenthesis at the top
                    # of the operator stack, and o2 has greater precedence than o1
                    # or they have the same precedence pop o2 to the output_queue.
                    # Push o1 to the operator_stack.

                    while operator := self.operator_stack.top():
                        if (
                            operator.value == "(" or
                            OP_TO_PRECEDENCE_MAP.get(operator.value, math.inf) < OP_TO_PRECEDENCE_MAP[token.value]
                        ):
                            break

                        self.output_queue.push(self.operator_stack.pop())

                    self.operator_stack.push(token)

                case TokenType.PARENTHESIS.value:
                    if token.value == "(":  # just push left parenthesis to the operator stack
                        self.operator_stack.push(token)

                    elif token.value == ")":
                        # While operator at the top of the operator stack is not a left parenthesis
                        # pop the operator from the operator stack into the output queue.
                        # If the stack runs out without finding a left parenthesis,
                        # then there are mismatched parentheses.

                        while operator := self.operator_stack.top():
                            if operator.value == "(":
                                break
                            self.output_queue.push(self.operator_stack.pop())
                        else:
                            # Mismatched parenthesis case
                            raise ParserException(
                                message=(
                                    "Parenthesis mismatch\n"
                                    "Some of the closing parenthesis doesn't have the opening one"
                                )
                            )

                        if getattr(self.operator_stack.top(), 'value', None) == "(":
                            # remove left parenthesis after finding it
                            self.operator_stack.pop()

                        if getattr(self.operator_stack.top(), 'token_type', None) == TokenType.FUNC:
                            # if function is on top of the operator stack pop it to the output queue
                            self.output_queue.push(self.operator_stack.pop())

        while operator := self.operator_stack.pop():
            # Pop the remaining items from the operator stack into the output queue.

            if operator.value == "(":
                # If the operator token on the top of the stack is a parenthesis,
                # then there are mismatched parentheses.

                raise ParserException(
                    message=(
                        "Parenthesis mismatch\n"
                        "Some of the opening parenthesis doesn't have the closing one"
                    )
                )
            self.output_queue.push(operator)

        return self.output_queue.get_copy()
