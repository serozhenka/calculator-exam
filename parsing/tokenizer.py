import re

from .constants import TokenType
from .exceptions import ParserException
from evaluating.constants import STR_FUNC_TO_FUNC_MAP


class Token:
    """Class representing token found on the lexical analysis."""

    def __init__(self, token_type: TokenType.value, value):
        self.token_type = token_type
        self.value = value

    def __str__(self):
        return f"Token: type='{self.token_type}', value='{self.value}'"

    def __repr__(self):
        return self.value


class Tokenizer:
    """Class representing string to token splitter."""

    def __init__(self, token_to_regex_map: dict):
        self.token_to_regex_map = token_to_regex_map

    def tokenize(self, expression: str):
        """
        Function to parse string into generator of tokens
        determined by regular expression.

        :param expression: arithmetical expression string
        :return: generator of Tokens
        """

        token_regex = '|'.join('(?P<%s>%s)' % (k.value, v) for k, v in self.token_to_regex_map.items())

        for match in re.finditer(token_regex, expression):
            token_type = match.lastgroup
            value = match.group(token_type)

            if token_type == TokenType.SPACE.value:  # pass if value is space symbol
                continue
            elif token_type == TokenType.FUNC.value:
                if value not in STR_FUNC_TO_FUNC_MAP:
                    # if function is not present in available functions raise exception
                    raise ParserException(
                        f"Function {value} at {match.start(token_type)}-{match.end(token_type)} not available"
                    )

            elif token_type == TokenType.MISMATCH.value:
                # if unknown token found raise exception
                raise ParserException(f"Token mismatch at {match.start(token_type)}-{match.end(token_type)}")

            yield Token(token_type, value)
