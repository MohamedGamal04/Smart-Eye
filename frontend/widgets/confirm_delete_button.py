from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QPushButton, QSizePolicy

from frontend.styles._colors import (
    _DANGER,
    _DANGER_BG_10,
    _DANGER_BG_11,
    _DANGER_BG_14,
    _DANGER_BG_22,
    _DANGER_BORDER_45,
    _DANGER_BORDER_55,
    _DANGER_BORDER_75,
)
from frontend.ui_tokens import (
    FONT_SIZE_LABEL,
    FONT_WEIGHT_SEMIBOLD,
    RADIUS_MD,
    SPACE_28,
    SPACE_SM,
    SPACE_XXXS,
)


_DEL_BTN_DEFAULT = (
    "QPushButton {"
    f"    border: {SPACE_XXXS}px solid {_DANGER_BORDER_45};"
    f"    background: {_DANGER_BG_10};"
    f"    color: {_DANGER};"
    f"    border-radius: {RADIUS_MD}px;"
    f"    font-size: {FONT_SIZE_LABEL}px;"
    f"    font-weight: {FONT_WEIGHT_SEMIBOLD};"
    f"    padding: 0 {SPACE_SM}px;"
    f"    min-height: {SPACE_28}px;"
    "}"
    "QPushButton:hover {"
    f"    border: {SPACE_XXXS}px solid {_DANGER_BORDER_45};"
    f"    background: {_DANGER_BG_11};"
    "}"
    "QPushButton:pressed {"
    f"    border: {SPACE_XXXS}px solid {_DANGER_BORDER_55};"
    f"    background: {_DANGER_BG_14};"
    "}"
)

_DEL_BTN_CONFIRM = (
    "QPushButton {"
    f"    border: {SPACE_XXXS}px solid {_DANGER_BORDER_55};"
    f"    background: {_DANGER_BG_14};"
    f"    color: {_DANGER};"
    f"    border-radius: {RADIUS_MD}px;"
    f"    font-size: {FONT_SIZE_LABEL}px;"
    f"    font-weight: {FONT_WEIGHT_SEMIBOLD};"
    f"    padding: 0 {SPACE_SM}px;"
    f"    min-height: {SPACE_28}px;"
    "}"
    "QPushButton:hover {"
    f"    border: {SPACE_XXXS}px solid {_DANGER_BORDER_75};"
    f"    background: {_DANGER_BG_22};"
    "}"
)


class ConfirmDeleteButton(QPushButton):
    def __init__(self, text: str = "Delete", confirm_text: str = "Sure?", parent=None):
        super().__init__(text, parent)
        self._base_text = text
        self._confirm_text = confirm_text
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.setInterval(3000)
        self._timer.timeout.connect(self._reset_state)
        self._default_style = _DEL_BTN_DEFAULT
        self._confirm_style = _DEL_BTN_CONFIRM
        self.setStyleSheet(self._default_style)
        self.setCursor(Qt.PointingHandCursor)
        self._confirming = False
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

    def set_confirm_callback(self, fn):
        def _on_click():
            if self._confirming:
                self._timer.stop()
                self._reset_state()
                fn()
            else:
                self._confirming = True
                self.setText(self._confirm_text)
                self.setStyleSheet(self._confirm_style)
                self._timer.start()

        self.clicked.connect(_on_click)

    def set_button_styles(self, default_style: str, confirm_style: str):
        self._default_style = default_style
        self._confirm_style = confirm_style
        self.setStyleSheet(self._confirm_style if self._confirming else self._default_style)

    def _reset_state(self):
        self._confirming = False
        self.setText(self._base_text)
        self.setStyleSheet(self._default_style)
