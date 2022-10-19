from ui.constants import OPERATORS


class Validator:

    @staticmethod
    def get_next(string: str, pos: int, n: int):
        start = min(pos, len(string))
        end = min(pos + n, len(string))
        return string[start:end]

    @staticmethod
    def get_prev(string, pos, n):
        start = max(pos - n, 0)
        end = min(pos, len(string))
        return string[start:end]

    @staticmethod
    def validate_float(text):
        try:
            float(text)
            return True
        except ValueError:
            return False

    def validate_point(self, text: str, pos: int) -> bool:
        result = (
            self.get_prev(text, pos, 1).isdigit()  # "[+./()]." - invalid
            and self.get_next(text, pos, 1) != "."  # ".[.]" - invalid
        )

        if result:
            # check to prevent multiple points in one number ("5.432." - invalid)
            index = pos
            while index:
                current = self.get_prev(text, index, 1)
                if not current.isdigit():
                    result = current != "."
                    break

                index -= 1

        return result

    def validate_number(self, text: str, pos: int) -> bool:
        if (
            not self.get_next(text, pos, 1).isalpha() and
            self.get_prev(text, pos, 1) in ['.', '(', ''] or  # valid after point, left parent. or at the beginning
            self.get_prev(text, pos, 1).isdigit() or  # valid after another number
            any([key in self.get_prev(text, pos, 2) for key in OPERATORS]) or  # valid after operator
            (
                self.get_prev(text, pos, 1).isalpha() and
                self.get_next(text, pos, 1) not in ['(']
            )
        ):
            return True
        return False

    def validate_identifier(self, text: str, pos: int) -> bool:
        result = self.validate_number(text, pos)
        result = (
            result and
            not self.get_prev(text, pos, 1).isdigit() and
            not self.get_next(text, pos, 1).isalpha() and
            not any([key.isdigit() for key in self.get_prev(text, pos, 2)])
        )

        return result

    def validate_space(self, text: str, pos: int) -> bool:
        return self.get_prev(text, pos, 1) != " "

    def validate_function(self, text: str, pos: int) -> bool:
        return (
            self.get_prev(text, pos, 1) in ['(', ''] or
            any([key in self.get_prev(text, pos, 2) for key in OPERATORS])
        )

    def validate_parenthesis(self, text: str, op: str, pos: int) -> bool:
        return (
            op == "(" or (
                self.get_prev(text, pos, 2).strip() in OPERATORS
            )
        )

    def validate_operator(self, text: str, op: str, pos: int) -> bool:
        return op == "-" or not (
            self.get_prev(text, pos, 2) == " " or
            self.get_prev(text, pos, 1) == "(" or
            self.get_prev(text, pos, 2).strip() == "("
        )

    def validate_param(self, text: str, pos: int) -> bool:
        if any([key in self.get_next(text, pos, 2) for key in ['x', '(']]):
            return False

        return (
            self.get_prev(text, pos, 1) == "(" or
            self.get_prev(text, pos, 2).strip() in ["(", ""] or
            any([key in self.get_prev(text, pos, 2) for key in OPERATORS])
        )