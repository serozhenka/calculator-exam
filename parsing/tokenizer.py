import re

from .constants import TokenType
from .exceptions import ParserException


class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value

    def __str__(self):
        return f"Token: type='{self.token_type}', value='{self.value}'"


class Tokenizer:
    def __init__(self, token_to_regex_map: dict):
        self.token_to_regex_map = token_to_regex_map

    def tokenize(self, code):
        token_regex = '|'.join('(?P<%s>%s)' % (k.value, v) for k, v in self.token_to_regex_map.items())

        for match in re.finditer(token_regex, code):
            token_type = match.lastgroup
            value = match.group(token_type)

            if token_type == TokenType.SPACE.value:
                continue
            elif token_type == TokenType.MISMATCH.value:
                raise ParserException("Token mismatch")

            yield Token(token_type, value)