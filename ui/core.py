import random
import re

from functools import partial
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QInputDialog,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from calculator import Calculator
from parsing.exceptions import ParserException
from evaluating.constants import CUSTOM_FUNC_TO_STR_MAP
from evaluating.exceptions import EvaluatorException
from .input_handler.validator import Validator

from ui import constants
from ui.widgets import TextEdit, LettersOnlyTextEdit
from ui.input_handler.handler import InputHandler
from evaluating.constants import STR_FUNC_TO_FUNC_MAP


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # initializing attributes
        self.layout = None
        self.text_section = None
        self.text_section_layout = None
        self.input_field = None
        self.output_field = None
        self.create_function_section = None
        self.create_function_section_layout = None
        self.create_function_field = None
        self.create_function_buttons = None
        self.create_function_name_field = None
        self.add_identifiers_section = None
        self.add_identifiers_section_layout = None
        self.add_identifiers_field = None
        self.buttons_section = None
        self.helpers = None
        self.advanced_functions = None
        self.advanced_functions_layout = None
        self.common_section = None
        self.common_section_layout = None
        self.common_ops = None
        self.numbers_and_arithmetic_buttons = None
        self.advanced_functions_visible = False

        self.adding_function = False
        self.save_cursor_position = False
        self.identifiers = {}
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Calculator")  # set windows title
        self.setWindowIcon(QIcon("static/icon.png"))
        self.setFixedSize(QSize(*constants.WINDOW_SIZE))  # set program window size
        self.setCentralWidget(QWidget(self))  # necessary operation

        self.layout = QVBoxLayout()  # layout for main window
        self.layout.setContentsMargins(0, 0, 0, 0)  # remove padding inside main window

        self.setup_text_section()
        self.setup_add_function_section()
        self.buttons_section = QVBoxLayout()  # section of clickable buttons (child of 'layout')

        self.setup_helpers()  # child of 'buttons_section'
        self.setup_advanced_functions()  # child of 'buttons_section'
        self.setup_common_section()  # child of 'buttons_section'

        self.buttons_section.addLayout(self.helpers)
        self.buttons_section.addWidget(self.advanced_functions)
        self.buttons_section.addWidget(self.common_section)

        self.layout.addWidget(self.text_section)
        self.layout.addWidget(self.create_function_section)
        self.layout.addLayout(self.buttons_section)
        self.layout.addStretch()
        self.centralWidget().setLayout(self.layout)

    def setup_text_section(self):
        self.text_section = QFrame()
        self.text_section_layout = QVBoxLayout()
        self.text_section_layout.setContentsMargins(3, 3, 3, 3)
        self.setup_input_field()
        self.setup_output_field()
        self.text_section_layout.addWidget(self.input_field)
        self.text_section_layout.addWidget(self.output_field)
        self.text_section.setLayout(self.text_section_layout)

    def setup_input_field(self):
        self.input_field = TextEdit()
        self.input_field.setPlaceholderText("Type an expression...")
        self.input_field.setFixedHeight(constants.INPUT_FIELD_HEIGHT)
        self.input_field.setStyleSheet(
            constants.DEFAULT_TEXT_FIELD_QSS + constants.DASHED_BOTTOM_QSS
        )
        self.input_field.verticalScrollBar().setStyleSheet(constants.DEFAULT_V_SCROLLBAR_QSS)

    def setup_output_field(self):
        self.output_field = QTextEdit()
        self.output_field.setEnabled(False)
        self.output_field.setFixedHeight(constants.OUTPUT_FIELD_HEIGHT)
        self.output_field.setStyleSheet(constants.DEFAULT_TEXT_FIELD_QSS)
        self.output_field.verticalScrollBar().setStyleSheet(constants.DEFAULT_V_SCROLLBAR_QSS)

    def setup_add_function_section(self):
        self.create_function_section = QFrame()
        self.create_function_section_layout = QVBoxLayout()
        self.create_function_section_layout.setContentsMargins(3, 3, 3, 3)

        self.setup_add_function_field()
        self.setup_add_function_buttons()
        self.setup_add_function_name_field()
        self.create_function_section_layout.addWidget(self.create_function_field)
        self.create_function_section_layout.addWidget(self.create_function_name_field)
        self.create_function_section_layout.addLayout(self.create_function_buttons)

        self.create_function_section.setLayout(self.create_function_section_layout)
        self.create_function_section.hide()

    def setup_add_function_field(self):
        self.create_function_field = TextEdit()
        self.create_function_field.setPlaceholderText(
            "Type a function...\n"
            "Hint: use x as a parameter (sin(x) * cos(x) + 1)"
        )
        self.create_function_field.setFixedHeight(constants.CREATE_FUNCTION_FIELD_HEIGHT)
        self.create_function_field.setStyleSheet(
            constants.DEFAULT_TEXT_FIELD_QSS + constants.DASHED_BOTTOM_QSS
        )
        self.create_function_field.verticalScrollBar().setStyleSheet(constants.DEFAULT_V_SCROLLBAR_QSS)

    def setup_add_function_name_field(self):
        self.create_function_name_field = LettersOnlyTextEdit()
        self.create_function_name_field.setPlaceholderText("Name your function")
        self.create_function_name_field.setFixedHeight(constants.CREATE_FUNCTION_NAME_FIELD_HEIGHT)
        self.create_function_name_field.setStyleSheet(constants.DEFAULT_TEXT_FIELD_QSS)
        self.create_function_name_field.verticalScrollBar().setStyleSheet(constants.DEFAULT_V_SCROLLBAR_QSS)

    def setup_add_function_buttons(self):
        self.create_function_buttons = QHBoxLayout()
        add_function_buttons = ['Save', 'Cancel']

        for name in add_function_buttons:
            button = QPushButton(name)
            button.setStyleSheet(
                constants.DEFAULT_BUTTON_QSS.format(
                    bg_color=constants.COLORS['gray'],
                    hover_bg_color=constants.COLORS['gray-hover'],
                )
            )
            button.setMinimumHeight(constants.BUTTON_SIZE // 2)
            button.setMinimumWidth(constants.BUTTON_SIZE)
            if name == 'Cancel':
                button.clicked.connect(self.add_custom_function_click)
            elif name == 'Save':
                button.clicked.connect(self.save_new_function)

            self.create_function_buttons.addWidget(button)

    def setup_add_identifiers_section(self):
        self.add_identifiers_section = QFrame()
        self.add_identifiers_section_layout = QVBoxLayout()
        self.add_identifiers_section_layout.setContentsMargins(3, 3, 3, 3)

        self.setup_add_identifiers_field()
        self.setup_add_function_buttons()
        self.add_identifiers_section_layout.addWidget(self.add_identifiers_field)
        self.add_identifiers_section_layout.addLayout(self.create_function_buttons)

        self.create_function_section.setLayout(self.add_identifiers_section_layout)
        self.create_function_section.hide()

    def setup_add_identifiers_field(self):
        self.add_identifiers_field = TextEdit()
        self.add_identifiers_field.setFixedHeight(constants.CREATE_FUNCTION_FIELD_HEIGHT)
        self.add_identifiers_field.setStyleSheet(
            constants.DEFAULT_TEXT_FIELD_QSS + constants.DASHED_BOTTOM_QSS
        )
        self.add_identifiers_field.verticalScrollBar().setStyleSheet(constants.DEFAULT_V_SCROLLBAR_QSS)

    def setup_helpers(self):
        self.helpers = QHBoxLayout()
        helpers_bar = constants.HELPERS_BUTTONS_TEXT

        for name in helpers_bar:
            button = QPushButton(name)
            button.setStyleSheet(
                constants.DEFAULT_BUTTON_QSS.format(
                    bg_color=constants.COLORS['gray'],
                    hover_bg_color=constants.COLORS['gray-hover'],
                )
            )
            button.setMinimumHeight(constants.BUTTON_SIZE // 2)
            button.setMinimumWidth(constants.BUTTON_SIZE)
            button.clicked.connect(partial(self.button_clicked, name))

            self.helpers.addWidget(button)

    def setup_advanced_functions(self):
        self.advanced_functions = QFrame()

        self.advanced_functions_layout = QGridLayout()
        self.advanced_functions_layout.setContentsMargins(0, 0, 0, 0)
        self.advanced_functions_layout.setSpacing(constants.BUTTON_GAP_SIZE)

        button_names = [constants.ADD_BUTTON_TEXT] + [key for key in STR_FUNC_TO_FUNC_MAP.keys() if key != 'sqrt']
        positions = [(i, j) for i in range(4) for j in range(5)]

        for name, position in zip(button_names, positions):
            button = QPushButton(name)
            if not name == constants.ADD_BUTTON_TEXT:
                button.clicked.connect(partial(self.button_clicked, name))
                button.setStyleSheet(
                    constants.DEFAULT_BUTTON_QSS.format(
                        bg_color=constants.COLORS['gray'],
                        hover_bg_color=constants.COLORS['gray-hover'],
                    )
                )
            else:
                button.clicked.connect(self.add_custom_function_click)
                button.setStyleSheet(
                    constants.DEFAULT_BUTTON_QSS.format(
                        bg_color=constants.COLORS['light-red'],
                        hover_bg_color=constants.COLORS['light-hover-red'],
                    )
                )
            button.setMinimumSize(constants.BUTTON_SIZE, constants.BUTTON_SIZE)
            self.advanced_functions_layout.addWidget(button, *position)

        self.advanced_functions.setLayout(self.advanced_functions_layout)
        self.advanced_functions.hide()

    def setup_common_section(self):
        self.common_section = QFrame()

        self.common_section_layout = QHBoxLayout()
        self.common_section_layout.setContentsMargins(0, 0, 0, 0)
        self.common_section_layout.setSpacing(constants.BUTTON_GAP_SIZE)

        self.setup_common_ops()  # child of 'common_section'
        self.setup_numbers_and_arithmetic_buttons()  # child of 'common_section'

        self.common_section_layout.addLayout(self.common_ops, 1)
        self.common_section_layout.addLayout(self.numbers_and_arithmetic_buttons, 4)
        self.common_section.setLayout(self.common_section_layout)

    def setup_common_ops(self):
        self.common_ops = QVBoxLayout()  # child of 'common_section'
        self.common_ops.setSpacing(constants.BUTTON_GAP_SIZE)
        common_ops = constants.COMMON_OPS_BUTTONS_TEXT

        for name in common_ops:
            button = QPushButton(name)
            button.clicked.connect(partial(self.button_clicked, name))
            button.setStyleSheet(
                constants.DEFAULT_BUTTON_QSS.format(
                    bg_color=constants.COLORS['gray'],
                    hover_bg_color=constants.COLORS['gray-hover'],
                ))
            button.setMinimumSize(constants.BUTTON_SIZE, constants.BUTTON_SIZE)
            self.common_ops.addWidget(button)

    def setup_numbers_and_arithmetic_buttons(self):
        self.numbers_and_arithmetic_buttons = QGridLayout()  # child of 'common_section'
        self.numbers_and_arithmetic_buttons.setSpacing(constants.BUTTON_GAP_SIZE)

        button_names = constants.NUMBERS_AND_ARITHMETICAL_BUTTONS_TEXT
        positions = [(i, j) for i in range(4) for j in range(4)]

        for name, position in zip(button_names, positions):
            button = QPushButton(str(name))
            button.clicked.connect(partial(self.button_clicked, str(name)))

            if isinstance(name, int):
                bg_color = constants.COLORS['white']
                hover_bg_color = constants.COLORS['white-hover']
            else:
                bg_color = constants.COLORS['gray']
                hover_bg_color = constants.COLORS['gray-hover']

            button.setStyleSheet(
                constants.DEFAULT_BUTTON_QSS.format(
                    bg_color=bg_color,
                    hover_bg_color=hover_bg_color,
                )
            )
            button.setMinimumSize(constants.BUTTON_SIZE, constants.BUTTON_SIZE)
            self.numbers_and_arithmetic_buttons.addWidget(button, *position)

    def show_error(self, message, msg_type):
        dialog = QMessageBox()
        dialog.setWindowIcon(QIcon('static/error.png'))
        dialog.setIcon(QMessageBox.Icon.NoIcon)
        dialog.setText(message)
        dialog.setWindowTitle(msg_type)
        dialog.exec()

    def additional_functions_click(self):
        to_hide = self.advanced_functions if self.advanced_functions_visible else self.common_section
        to_show = self.common_section if self.advanced_functions_visible else self.advanced_functions
        to_hide.hide()
        to_show.show()

        self.advanced_functions_visible = not self.advanced_functions_visible

    def add_custom_function_button(self, name):
        button = QPushButton(name)
        button.clicked.connect(partial(self.button_clicked, name))
        button.setStyleSheet(
            constants.DEFAULT_BUTTON_QSS.format(
                bg_color=constants.COLORS['gray'],
                hover_bg_color=constants.COLORS['gray-hover'],
            )
        )
        button.setMinimumSize(constants.BUTTON_SIZE, constants.BUTTON_SIZE)
        self.advanced_functions_layout.addWidget(button)

    def add_custom_function_click(self):
        to_hide = self.create_function_section if self.adding_function else self.text_section
        to_show = self.text_section if self.adding_function else self.create_function_section
        to_hide.hide()
        to_show.show()

        if to_show == self.create_function_section:
            self.additional_functions_click()

        self.adding_function = not self.adding_function

    def save_new_function(self):
        text = self.create_function_field.toPlainText()
        name = self.create_function_name_field.toPlainText()

        if not (name and text):
            return

        try:
            Calculator.calculate(text.replace('x', str(random.random())))
            if name in CUSTOM_FUNC_TO_STR_MAP:
                self.show_error('Function with name already exists', 'Integrity error')
                return

            CUSTOM_FUNC_TO_STR_MAP[name] = text
            self.add_custom_function_button(name)
            self.add_custom_function_click()
        except Exception:
            pass

    def preprocess_calculation(self, text):
        functions = re.findall(r"[A-Za-z_]{2,}", text)

        for function in functions:
            if function not in [*STR_FUNC_TO_FUNC_MAP.keys(), *CUSTOM_FUNC_TO_STR_MAP.keys()]:
                self.show_error(f"{function} not defined", "Undefined literals")
                return False

        identifiers = set(re.findall(r"[A-Za-z_][0-9_]*", text))

        for identifier in identifiers:
            text, accepted = QInputDialog.getText(self, 'Input dialog', f'{identifier}')
            if not (accepted and Validator.validate_float(text)):
                return False

            self.identifiers[identifier] = text

        return True

    def button_clicked(self, inp):
        input_field = self.create_function_field if self.adding_function else self.input_field
        text = input_field.toPlainText()
        self.save_cursor_position = 0
        self.identifiers = {}

        if inp == "f(x)":
            self.additional_functions_click()

        elif inp == "=":
            if (
                not text or
                input_field == self.create_function_field or
                not self.preprocess_calculation(text)
            ):
                return

            for identifier in self.identifiers:
                text = text.replace(identifier, self.identifiers[identifier])

            try:
                result = Calculator.calculate(str(text))
                self.output_field.setText(str(result))
            except (ParserException, EvaluatorException) as e:
                self.save_cursor_position = True
                self.show_error(e.message, e.type)
            except Exception as e:
                print(e)

        elif inp in [*constants.INPUT_HANDLER_KEYS, *STR_FUNC_TO_FUNC_MAP.keys(), *CUSTOM_FUNC_TO_STR_MAP.keys()]:
            input_handler = InputHandler(input_field)
            input_handler.handle(inp)

        if self.save_cursor_position:
            input_field.setFocus()
            cursor = input_field.textCursor()
            cursor.setPosition(self.save_cursor_position)
            input_field.setTextCursor(cursor)
