from PyQt6.QtWidgets import QTextEdit

from evaluating.constants import STR_FUNC_TO_FUNC_MAP, CUSTOM_FUNC_TO_STR_MAP
from .validator import Validator

from ui.constants import OPERATORS


class InputHandler:

    def __init__(self, field: QTextEdit):
        self.field = field
        self.validator = Validator()
        self.cursor_position = 0
        self.text = None

    @staticmethod
    def get_next(string: str, pos: int, n: int):
        start = min(pos, len(string) - 1)
        end = min(pos + n, len(string))
        return string[start:end]

    @staticmethod
    def get_prev(string, pos, n):
        start = max(pos - n, 0)
        end = min(pos, len(string))
        return string[start:end]

    def handle(self, inp):
        self.cursor_position = 0

        text = self.field.toPlainText()
        cursor = self.field.textCursor()
        pos = cursor.position()
        self.field.setFocus()

        if pos == 0:
            if inp in ["."] + OPERATORS:
                return

        match inp:
            case "⇇":
                if pos == 0:
                    return
                self.field.setText(text[0:pos-1] + text[pos:])
                self.cursor_position = 1
                cursor.setPosition(pos - 1)
                self.field.setTextCursor(cursor)

            case "←" | "→":
                add = 1 if inp == "→" else -1
                self.cursor_position = 1
                cursor.setPosition(pos + add)
                self.field.setTextCursor(cursor)

            case ".":
                if not self.validator.validate_point(text, pos):
                    return

            case "x":
                if not self.validator.validate_param(text, pos):
                    return

            case '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9':
                if not self.validator.validate_number(text, pos):
                    return
            case " ":
                if not self.validator.validate_space(text, pos):
                    return

                if self.get_next(text, pos, 1) == " ":
                    cursor.setPosition(pos + 1)
                    self.field.setTextCursor(cursor)

            case "(" | ")":
                pass

            case "+" | "-" | "*" | "/" | "^":
                if not self.validator.validate_operator(text, inp, pos):
                    return

                if inp == "-":
                    if self.get_prev(text, pos, 1) == "(":
                        # [(]{insert}
                        self.text = text[:pos] + inp + text[pos:]
                        self.cursor_position = pos + 1

                    elif self.get_prev(text, pos, 1) in OPERATORS:
                        # [+-/*]{insert}
                        self.text = text[:pos] + f" ({inp}" + text[pos + 1:]
                        self.cursor_position = pos + 2

                    elif (
                        self.get_prev(text, pos - 1, 1).strip() in OPERATORS
                        and self.get_prev(text, pos, 1).isspace()
                    ):
                        # [+-/*] {insert}
                        self.text = text[:pos] + f"({inp}" + text[pos:]
                        self.cursor_position = pos + 2

                else:
                    if (
                        self.get_prev(text, pos - 1, 1) != "(" and
                        self.get_prev(text, pos, 1) in OPERATORS
                    ):
                        # [+-/*]{insert}
                        self.text = text[:pos - 1] + inp + text[pos:]
                        self.cursor_position = pos + 1

                    elif (
                        self.get_prev(text, pos - 2, 1) != "(" and
                        self.get_prev(text, pos - 1, 1).strip() in OPERATORS
                        and self.get_prev(text, pos, 1).isspace()
                    ):
                        self.text = text[:pos - 2] + inp + text[pos - 1:]
                        self.cursor_position = pos

                if not self.cursor_position:
                    if self.get_next(text, pos, 1) in OPERATORS:
                        self.text = text[:pos] + inp + text[pos + 1:]
                        self.cursor_position = pos + 1

                    elif (
                        self.get_next(text, pos + 1, 1) in OPERATORS and
                        self.get_next(text, pos, 1).isspace()
                    ):
                        self.text = text[:pos+1] + inp + text[pos + 2:]
                        self.cursor_position = pos + 2

                if self.cursor_position:
                    self.field.setText(self.text)
                    cursor.setPosition(self.cursor_position)
                    self.field.setTextCursor(cursor)
            case _:
                if inp in [*STR_FUNC_TO_FUNC_MAP.keys(), *CUSTOM_FUNC_TO_STR_MAP.keys()]:
                    if not self.validator.validate_function(text, pos):
                        return

                    if self.get_next(text, pos, 2).strip().isdigit():
                        inp += "("
                    else:
                        inp += "()"

                elif inp.isalpha():
                    if not self.validator.validate_identifier(text, pos):
                        return

        if not self.cursor_position:
            if inp in OPERATORS:
                inp = f"{'' if self.get_prev(text, pos, 1).isspace() else ' '}{inp} "

            self.field.setText(text[0:pos] + inp + text[pos:])

            if inp[-2:] == "()":
                cursor.setPosition(pos + len(inp) - 1)
            else:
                cursor.setPosition(pos + len(inp))

            self.field.setTextCursor(cursor)


