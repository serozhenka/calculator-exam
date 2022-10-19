from PyQt6 import QtGui
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtCore import Qt

from .constants import TEXT_FIELDS_ALLOWED_KEYS
from .input_handler import InputHandler
from .constants import QT_KEY_TO_KEY_TEXT_MAP, LETTERS_KEYS


class TextEdit(QTextEdit):
    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() not in TEXT_FIELDS_ALLOWED_KEYS + LETTERS_KEYS:
            return

        text: str = QT_KEY_TO_KEY_TEXT_MAP.get(event.key(), event.text())
        input_handler = InputHandler(self)
        input_handler.handle(text.lower())


class LettersOnlyTextEdit(QTextEdit):
    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() not in LETTERS_KEYS + [Qt.Key.Key_Backspace, Qt.Key.Key_Left, Qt.Key.Key_Right]:
            return
        super(LettersOnlyTextEdit, self).keyPressEvent(event)