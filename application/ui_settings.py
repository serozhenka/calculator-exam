WINDOW_SIZE = 400, 600

BUTTON_SIZE = 75
BUTTON_GAP_SIZE = 2

INPUT_FIELD_HEIGHT = 150
OUTPUT_FIELD_HEIGHT = 90

DEFAULT_BUTTON_QSS = """
    QPushButton {{
        border: none;
        background-color: {bg_color};
    }}
    QPushButton:hover {{
        background-color: {hover_bg_color};
    }}
"""

COLORS = {
    'white': '#FEFEFE',
    'white-hover': '#EFF0F0',
    'gray': '#E1E5E3',
    'gray-hover': '#CBD2D1',
    'dark-gray': '#888',
    'dark-dark-gray': '#555',
}

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
