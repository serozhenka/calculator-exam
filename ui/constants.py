from PyQt6.QtCore import Qt


# widgets settings

WINDOW_SIZE = 400, 600  # main window size

BUTTON_SIZE = 75
BUTTON_GAP_SIZE = 2

INPUT_FIELD_HEIGHT = 150
OUTPUT_FIELD_HEIGHT = 90
CREATE_FUNCTION_FIELD_HEIGHT = 200
CREATE_FUNCTION_NAME_FIELD_HEIGHT = 30

OPERATORS = ["+", "-", "*", "/", "^"]

# widgets (input / output / text) settings

ADD_BUTTON_TEXT = "+"
HELPERS_BUTTONS_TEXT = ['f(x)', "←", "→", "⇇"]
COMMON_OPS_BUTTONS_TEXT = ['(', ')', 'sqrt', '^']
NUMBERS_AND_ARITHMETICAL_BUTTONS_TEXT = [
    7, 8, 9, '/',
    4, 5, 6, '*',
    1, 2, 3, '-',
    0, '.', '=', '+',
]

TEXT_FIELDS_ALLOWED_KEYS = [
    key.value for key in
    [
        Qt.Key.Key_Left, Qt.Key.Key_Right,
        Qt.Key.Key_Space, Qt.Key.Key_Backspace, Qt.Key.Key_Period,
        Qt.Key.Key_0, Qt.Key.Key_1, Qt.Key.Key_2, Qt.Key.Key_3, Qt.Key.Key_4,
        Qt.Key.Key_5, Qt.Key.Key_6, Qt.Key.Key_7, Qt.Key.Key_8, Qt.Key.Key_9,
        Qt.Key.Key_ParenLeft, Qt.Key.Key_ParenRight,
        Qt.Key.Key_Plus, Qt.Key.Key_Minus, Qt.Key.Key_Slash, Qt.Key.Key_Asterisk, Qt.Key.Key_AsciiCircum,
    ]
]

LETTERS_KEYS = list(range(0x41, 0x5a + 1))

INPUT_HANDLER_KEYS = [
    *[str(i) for i in range(10)],
    '*', '/', '+', '-',
    "⇇", "←", "→", ".",
    "(", ")", "^", "=",
]

QT_KEY_TO_KEY_TEXT_MAP = {
    Qt.Key.Key_Backspace: "⇇",
    Qt.Key.Key_Left: "←",
    Qt.Key.Key_Right: "→",
}


# styling settings

COLORS = {
    'white': '#FEFEFE',
    'white-hover': '#EFF0F0',
    'gray': '#E1E5E3',
    'gray-hover': '#CBD2D1',
    'dark-gray': '#888',
    'dark-dark-gray': '#555',
    'light-red': '#F0AA8A',
    'light-hover-red': '#E9827C',
    'red': '#DC3C34',
}

DEFAULT_BUTTON_QSS = """
    QPushButton {{
        border: none;
        background-color: {bg_color};
    }}
    QPushButton:hover {{
        background-color: {hover_bg_color};
    }}
"""

DEFAULT_TEXT_FIELD_QSS = \
    f"font-size: 14px;" \
    f"border: none;" \
    f"background-color: {COLORS['white-hover']};"

DASHED_BOTTOM_QSS = f"border-bottom: 3px dashed {COLORS['dark-gray']};"

DEFAULT_V_SCROLLBAR_QSS = f"""
    QScrollBar:vertical {{
        width: 5px;
        background: {COLORS['gray-hover']};
    }}

    QScrollBar::handle:vertical {{
        background: {COLORS['dark-gray']};
    }}

    QScrollBar::add-line:vertical {{
        border: 2px solid gray;
        background: {COLORS['gray-hover']};
    }}

    QScrollBar::sub-line:horizontal {{
        border: 2px solid gray;
        background: {COLORS['gray-hover']};
    }}

    QScrollBar::handle:hover:vertical {{
        background: {COLORS['dark-dark-gray']};
    }}
"""
