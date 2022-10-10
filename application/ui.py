from functools import partial
import application.ui_settings as settings

from PyQt6.QtCore import QSize, QVariantAnimation, QAbstractAnimation, pyqtSlot, QObject
from PyQt6.uic.properties import QtGui
from PyQt6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QTextEdit,
    QScrollBar,
    QFrame,
)

from evaluating.constants import STR_FUNC_TO_FUNC_MAP


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # initializing attributes
        self.layout = None
        self.input_field = None
        self.output_field = None
        self.buttons_section = None
        self.helpers = None
        self.advanced_functions = None
        self.common_section = None
        self.common_ops = None
        self.numbers_and_arithmetic_buttons = None
        self.advanced_functions_visible = False

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Calculator")  # set windows title
        self.setFixedSize(QSize(*settings.WINDOW_SIZE))  # set program window size
        self.setCentralWidget(QWidget(self))  # necessary operation

        self.setup_input_field()
        self.setup_output_field()

        self.layout = QVBoxLayout()  # layout for main window
        self.layout.setContentsMargins(*[0] * 4)  # remove padding inside main window

        self.buttons_section = QVBoxLayout()  # section of clickable buttons (child of 'layout')

        self.setup_helpers()  # child of 'buttons_section'

        self.setup_advanced_functions()  # child of 'buttons_section'
        self.advanced_functions.hide()
        self.setup_common_section()
        common_section_layout = QHBoxLayout()  # child of 'buttons_section'
        common_section_layout.setContentsMargins(0, 0, 0, 0)
        common_section_layout.setSpacing(settings.BUTTON_GAP_SIZE)

        # setup children of 'common_section'
        self.setup_common_ops()
        self.setup_numbers_and_arithmetic_buttons()
        common_section_layout.addLayout(self.common_ops, 1)
        common_section_layout.addLayout(self.numbers_and_arithmetic_buttons, 5)
        self.common_section.setLayout(common_section_layout)

        self.buttons_section.addLayout(self.helpers)
        self.buttons_section.addWidget(self.advanced_functions)
        self.buttons_section.addWidget(self.common_section)

        self.layout.addWidget(self.input_field)
        self.layout.addWidget(self.output_field)

        self.layout.addLayout(self.buttons_section)
        self.layout.addStretch()
        self.centralWidget().setLayout(self.layout)

    def button_clicked(self, value):
        print(value)

    def setup_input_field(self):
        self.input_field = QTextEdit()
        self.input_field.setFixedHeight(settings.INPUT_FIELD_HEIGHT)
        self.input_field.setStyleSheet(
            f"font-size: 14px;"
            f"border: none;"
            f"background-color: {settings.COLORS['white-hover']};"
            f"border-bottom: 3px dashed {settings.COLORS['dark-gray']};"
        )
        self.input_field.verticalScrollBar().setStyleSheet(settings.DEFAULT_V_SCROLLBAR_QSS)

    def setup_output_field(self):
        self.output_field = QTextEdit()
        self.output_field.setFixedHeight(settings.OUTPUT_FIELD_HEIGHT)
        self.output_field.setEnabled(False)
        self.output_field.setStyleSheet(
            f"font-size: 14px;"
            f"border: none;"
            f"background-color: {settings.COLORS['white-hover']};"
        )
        self.output_field.verticalScrollBar().setStyleSheet(settings.DEFAULT_V_SCROLLBAR_QSS)

    def setup_helpers(self):
        self.helpers = QHBoxLayout()  # child of 'buttons_section'
        helpers_bar = ['f(x)', "←", "→", "⇇"]

        for name in helpers_bar:
            button = QPushButton(name)
            button.setStyleSheet(
                settings.DEFAULT_BUTTON_QSS.format(
                    bg_color=settings.COLORS['gray'],
                    hover_bg_color=settings.COLORS['gray-hover'],
                )
            )
            button.setMinimumHeight(settings.BUTTON_SIZE // 2)
            button.setMinimumWidth(settings.BUTTON_SIZE)

            match name:
                case "f(x)":
                    button.clicked.connect(self.additional_functions_click)

            self.helpers.addWidget(button)

    def setup_advanced_functions(self):
        self.advanced_functions = QFrame()
        advanced_functions_layout = QGridLayout()
        advanced_functions_layout.setContentsMargins(0, 0, 0, 0)
        advanced_functions_layout.setSpacing(settings.BUTTON_GAP_SIZE)

        advanced_functions = STR_FUNC_TO_FUNC_MAP
        advanced_functions.pop('sqrt')
        button_names = [key for key in advanced_functions.keys()]

        positions = [(i, j) for i in range(4) for j in range(5)]

        for name, position in zip(button_names, positions):
            button = QPushButton(name)

            button.setStyleSheet(
                settings.DEFAULT_BUTTON_QSS.format(
                    bg_color=settings.COLORS['gray'],
                    hover_bg_color=settings.COLORS['gray-hover'],
                )
            )
            button.setMinimumSize(settings.BUTTON_SIZE, settings.BUTTON_SIZE)
            advanced_functions_layout.addWidget(button, *position)

        self.advanced_functions.setLayout(advanced_functions_layout)

    def setup_common_section(self):
        self.common_section = QFrame()

    def setup_common_ops(self):
        self.common_ops = QVBoxLayout()  # child of 'common_section'
        self.common_ops.setSpacing(settings.BUTTON_GAP_SIZE)
        common_ops = ['(', ')', 'sqrt', '^']

        for name in common_ops:
            button = QPushButton(name)
            button.clicked.connect(partial(self.button_clicked, name))
            button.setStyleSheet(
                settings.DEFAULT_BUTTON_QSS.format(
                    bg_color=settings.COLORS['gray'],
                    hover_bg_color=settings.COLORS['gray-hover'],
                ))
            button.setMinimumSize(settings.BUTTON_SIZE, settings.BUTTON_SIZE)
            self.common_ops.addWidget(button)

    def setup_numbers_and_arithmetic_buttons(self):
        self.numbers_and_arithmetic_buttons = QGridLayout()  # child of 'common_section'
        self.numbers_and_arithmetic_buttons.setSpacing(settings.BUTTON_GAP_SIZE)

        button_names = [
            '7', '8', '9', '÷',
            '4', '5', '6', '×',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
        ]

        positions = [(i, j) for i in range(4) for j in range(4)]

        for name, position in zip(button_names, positions):
            button = QPushButton(name)
            button.clicked.connect(partial(self.button_clicked, name))

            try:
                int(name)
                bg_color = settings.COLORS['white']
                hover_bg_color = settings.COLORS['white-hover']
            except ValueError:
                bg_color = settings.COLORS['gray']
                hover_bg_color = settings.COLORS['gray-hover']

            button.setStyleSheet(
                settings.DEFAULT_BUTTON_QSS.format(
                    bg_color=bg_color,
                    hover_bg_color=hover_bg_color,
                )
            )
            button.setMinimumSize(settings.BUTTON_SIZE, settings.BUTTON_SIZE)
            self.numbers_and_arithmetic_buttons.addWidget(button, *position)

    def additional_functions_click(self):
        to_hide = self.advanced_functions if self.advanced_functions_visible else self.common_section
        to_show = self.common_section if self.advanced_functions_visible else self.advanced_functions
        to_hide.hide()
        to_show.show()

        self.advanced_functions_visible = not self.advanced_functions_visible

