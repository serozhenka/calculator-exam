from enum import Enum


class TokenType(Enum):
    NUMBER = 'NUMBER'
    ID = 'IDENTIFIER'
    FUNC = 'FUNC'
    OPERATOR = 'OPER'
    PARENTHESIS = 'PARENTHESIS'
    SPACE = 'SPACE'
    MISMATCH = 'MISMATCH'


TOKEN_TO_REGEX_MAP = {
    TokenType.NUMBER: r'-?\d+(\.\d*)?',
    TokenType.FUNC: r'[A-Za-z_]{2,}',
    TokenType.OPERATOR: r'[-+*/^]+',
    TokenType.PARENTHESIS: r'[][()]',
    TokenType.SPACE: r'[ \t\n]+',
    TokenType.MISMATCH: r'.',
}


OP_TO_PRECEDENCE_MAP = {
    '(': 0,
    ')': 1,
    '-': 2,
    '+': 2,
    '*': 3,
    '/': 3,
    '**': 4,
    '^': 4,
}
