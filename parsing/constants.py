from enum import Enum


class TokenType(Enum):
    NUMBER = 'NUMBER'
    FUNC = 'FUNC'
    OPERATOR = 'OPER'
    PARENTHESIS = 'PARENTHESIS'
    SPACE = 'SPACE'
    MISMATCH = 'MISMATCH'


TOKEN_TO_REGEX_MAP = {
    TokenType.NUMBER: r'\d+(\.\d*)?',
    TokenType.FUNC: r'[A-Za-z_][A-Za-z0-9_]*',
    TokenType.OPERATOR: r'[-~+*/%=<>?!:|&^@]+',
    TokenType.PARENTHESIS: r'[][(),.]',
    TokenType.SPACE: r'[ \t\n]+',
    TokenType.MISMATCH: r'.',
}

OPERATOR_TO_PRECEDENCE_MAP = {
    '(': 0,
    ')': 1,
    '-': 2,
    '+': 2,
    '*': 3,
    '/': 3,
}