from ui.constants import OPERATORS


class Validator:
    """
    Class that validates different type of characters that might be inserted
    into specified string position. validate_{} functions return True if
    validation is successful else False.
    """

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
    def validate_float(text):  # check if number is float (4.321)
        try:
            float(text)
            return True
        except ValueError:
            return False

    def validate_point(self, text: str, pos: int) -> bool:  # validate decimal point for insertion
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

    def validate_number(self, text: str, pos: int) -> bool:  # validate digit for insertion
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

    def validate_identifier(self, text: str, pos: int) -> bool:  # validate identifier for insertion
        result = self.validate_number(text, pos)  # precondition
        result = result and (
            not self.get_next(text, pos, 1).isalpha() and  # invalid before digit
            not any([key.isdigit() for key in self.get_prev(text, pos, 2)])  # invalid after digit
        )
        return result

    def validate_space(self, text: str, pos: int) -> bool:  # validate space for insertion
        return self.get_prev(text, pos, 1) != " "  # invalid after space

    def validate_function(self, text: str, pos: int) -> bool:  # validate func for insertion
        return (
            self.get_prev(text, pos, 1) in ['(', ''] or  # valid after left par. or at str start
            any([key in self.get_prev(text, pos, 2) for key in OPERATORS])  # valid after operators
        )

    def validate_parenthesis(self, text: str, op: str, pos: int) -> bool:  # validate lr parenthesis
        return (
            (
                op == "("  # left parenthesis is always ok
            ) or
            (
                op == ")" and
                (
                    self.get_prev(text, pos, 1).isdigit() or  # valid before digit
                    self.get_prev(text, pos, 1) in ["(", ")"]  # valid before lr parenthesis
                )
            )
        )

    def validate_operator(self, text: str, op: str, pos: int) -> bool:
        return op == "-" or not (  # minus is always valid
            self.get_prev(text, pos, 1) == " " or  # valid after space
            self.get_prev(text, pos, 1) == "(" or  # valid after l parenthesis
            self.get_prev(text, pos, 2).strip() == "("  # valid after l parenthesis
        )

    # def validate_param(self, text: str, pos: int) -> bool:
    #     if any([key in self.get_next(text, pos, 2) for key in ['x', '(']]):
    #         return False
    #
    #     return (
    #         self.get_prev(text, pos, 1) == "(" or
    #         self.get_prev(text, pos, 2).strip() in ["(", ""] or
    #         any([key in self.get_prev(text, pos, 2) for key in OPERATORS])
    #     )
