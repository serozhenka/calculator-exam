import math
import operator


OPERATOR_TO_FUNC_MAP = {
    '-': operator.sub,
    '+': operator.add,
    '*': operator.mul,
    '/': operator.truediv,
    '^': math.pow,
    '**': math.pow,
}

STR_FUNC_TO_FUNC_MAP = {
    'sqrt': math.sqrt,
    'sin': math.sin,
    'cos': math.cos,
    'tg': math.tan,
    'ctg': lambda v: 1 / math.tan(v),
    'arcsin': math.asin,
    'arccos': math.acos,
    'arctg': math.atan,
    'arcctg': lambda v: math.atan(1 / v),
}
