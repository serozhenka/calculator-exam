from .constants import TokenType, OPERATOR_TO_PRECEDENCE_MAP
from .exceptions import ParserException
from .tokenizer import Tokenizer
from utils.data_structures import Stack, Queue


class Parser:
    def __init__(self):
        self.operator_stack = Stack()
        self.output_queue = Queue()

    def parse(self, expression: str, token_to_regex_map):
        tokenizer = Tokenizer(token_to_regex_map)

        for token in tokenizer.tokenize(expression):
            match token.token_type:
                case TokenType.NUMBER.value:
                    self.output_queue.push(token.value)

                case TokenType.FUNC.value:
                    self.operator_stack.push(token)

                case TokenType.OPERATOR.value:
                    while operator := self.operator_stack.pop():
                        if (
                            operator.value == "(" or
                            OPERATOR_TO_PRECEDENCE_MAP[operator.value] < OPERATOR_TO_PRECEDENCE_MAP[token.value]
                        ):
                            break

                        self.output_queue.push(operator.value)

                    self.operator_stack.push(token)

                case TokenType.PARENTHESIS.value:
                    if token.value == "(":
                        self.operator_stack.push(token)

                    elif token.value == ")":
                        while operator := self.operator_stack.pop():
                            if operator.value == "(":
                                break
                            self.output_queue.push(operator.value)

                        if self.operator_stack.top().value == "(":
                            self.operator_stack.pop()

                        if self.operator_stack.top().token_type == TokenType.FUNC:
                            self.output_queue.push(self.operator_stack.pop())

        while operator := self.operator_stack.pop():
            if operator.value == "(":
                raise ParserException("Parenthesis mismatch")
            self.output_queue.push(operator.value)

        return self.output_queue