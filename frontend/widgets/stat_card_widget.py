from PySide6.QtGui import QFont
from PySide6.QtWidgets import QFrame, QLabel, QSizePolicy, QVBoxLayout

from frontend.app_theme import safe_set_point_size
from frontend.styles._colors import _ACCENT, _TEXT_PRI, _TEXT_MUTED
from frontend.styles._card_styles import _CARD_BASE
from frontend.ui_tokens import (
    FONT_SIZE_LABEL,
    FONT_SIZE_LARGE,
    FONT_SIZE_MICRO,
    RADIUS_LG,
    SPACE_14,
    SPACE_MD,
    SPACE_SM,
    SIZE_MIN_W_SM,
    SIZE_PANEL_H_SM,
)


class StatCardWidget(QFrame):
    def __init__(self, title="", value="0", subtitle="", color=_ACCENT, parent=None):
        super().__init__(parent)
        self.setObjectName("StatCard")
        self.setFixedHeight(SIZE_PANEL_H_SM)
        self.setMinimumWidth(SIZE_MIN_W_SM)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setStyleSheet(
            f"""
            {_CARD_BASE}
            QFrame:hover {{ border-color: {color}; }}
            """
        )

        root = QVBoxLayout(self)
        root.setContentsMargins(SPACE_14, SPACE_MD, SPACE_14, SPACE_MD)
        root.setSpacing(SPACE_SM)

        title_lbl = QLabel(title)
        title_font = QFont()
        safe_set_point_size(title_font, FONT_SIZE_LABEL)
        title_font.setBold(True)
        title_lbl.setFont(title_font)
        title_lbl.setStyleSheet(f"color: {color}; background: transparent; border: none;")
        root.addWidget(title_lbl)

        self._value_label = QLabel(str(value))
        val_font = QFont()
        safe_set_point_size(val_font, FONT_SIZE_LARGE)
        val_font.setBold(True)
        self._value_label.setFont(val_font)
        self._value_label.setStyleSheet(f"color: {_TEXT_PRI}; background: transparent; border: none;")
        root.addWidget(self._value_label)

        self._sub_label = QLabel(subtitle)
        self._sub_label.setStyleSheet(f"color: {_TEXT_MUTED}; font-size: {FONT_SIZE_MICRO}px; background: transparent; border: none;")
        root.addWidget(self._sub_label)

    def set_value(self, value):
        self._value_label.setText(str(value))

    def set_subtitle(self, text):
        self._sub_label.setText(text)
