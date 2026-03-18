from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from frontend.styles._colors import (
    _ACCENT,
    _ACCENT_HI,
    _BG_OVERLAY,
    _BG_SURFACE,
    _BORDER,
    _BORDER_DIM,
    _DANGER,
    _TEXT_PRI,
    _TEXT_SEC,
    _TEXT_MUTED,
    _TEXT_ON_ACCENT,
)
from frontend.styles._btn_styles import _PRIMARY_BTN, _TEXT_BTN_GHOST
from frontend.styles._input_styles import _AUTH_INPUT_LG
from frontend.app_theme import safe_set_point_size
from frontend.ui_tokens import (
    FONT_SIZE_BODY,
    FONT_SIZE_LABEL,
    FONT_SIZE_SUBHEAD,
    FONT_SIZE_XXL,
    FONT_WEIGHT_BOLD,
    FONT_WEIGHT_SEMIBOLD,
    RADIUS_16,
    RADIUS_LG,
    RADIUS_SM,
    SIZE_CONTROL_LG,
    SIZE_CONTROL_SM,
    SIZE_DIALOG_W_XL,
    SIZE_ICON_TINY,
    SPACE_20,
    SPACE_28,
    SPACE_6,
    SPACE_LG,
    SPACE_MD,
    SPACE_SM,
    SPACE_XXXS,
)


class AuthLoginCard(QFrame):
    submit = Signal(str, str)
    reset_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(SIZE_DIALOG_W_XL)

        self.setStyleSheet(
            f"QFrame {{ background: {_BG_SURFACE}; border: {SPACE_XXXS}px solid {_BORDER_DIM}; border-radius: {RADIUS_16}px; }}"
        )
        self._build()
        self.adjustSize()

    def _build(self):
        form = QVBoxLayout(self)
        form.setContentsMargins(SPACE_28, SPACE_LG, SPACE_28, SPACE_20)
        form.setSpacing(0)

        title = QLabel("Sign in")
        f = QFont()
        safe_set_point_size(f, FONT_SIZE_XXL)
        f.setBold(True)
        title.setFont(f)
        title.setStyleSheet(f"QLabel {{ color: {_TEXT_PRI}; background: transparent; border: none; }}")
        form.addWidget(title)

        form.addSpacing(SPACE_6)

        subtitle = QLabel("Use an account created in Settings > Accounts.")
        subtitle.setStyleSheet(f"QLabel {{ color: {_TEXT_SEC}; background: transparent; border: none; font-size: {FONT_SIZE_BODY}px; }}")
        form.addWidget(subtitle)

        form.addSpacing(SPACE_SM)

        self._error_lbl = QLabel("")
        self._error_lbl.setStyleSheet(
            f"QLabel {{ color: {_DANGER}; background: transparent; border: none; font-size: {FONT_SIZE_BODY}px; }}"
        )
        self._error_lbl.setWordWrap(True)
        self._error_lbl.setVisible(False)
        form.addWidget(self._error_lbl)

        self._email = QLineEdit()
        self._email.setPlaceholderText("Email")
        self._email.setFixedHeight(SIZE_CONTROL_LG)
        self._email.setStyleSheet(_AUTH_INPUT_LG)
        form.addWidget(self._email)

        form.addSpacing(SPACE_SM)

        self._password = QLineEdit()
        self._password.setPlaceholderText("Password")
        self._password.setEchoMode(QLineEdit.EchoMode.Password)
        self._password.setFixedHeight(SIZE_CONTROL_LG)
        self._password.setStyleSheet(_AUTH_INPUT_LG)
        form.addWidget(self._password)

        form.addSpacing(SPACE_SM)

        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(SPACE_SM)
        self._remember = QCheckBox("Remember me")
        self._remember.setStyleSheet(
            f"QCheckBox {{ color: {_TEXT_SEC}; font-size: {FONT_SIZE_BODY}px; background: transparent; border: none; spacing: {SPACE_6}px; }}"
            f"QCheckBox::indicator {{ width: {SIZE_ICON_TINY}px; height: {SIZE_ICON_TINY}px; border-radius: {RADIUS_SM}px; border: {SPACE_XXXS}px solid {_BORDER}; background: {_BG_OVERLAY}; }}"
            f"QCheckBox::indicator:checked {{ background: {_ACCENT}; border-color: {_ACCENT}; }}"
        )
        row.addWidget(self._remember)
        row.addStretch()
        reset_btn = QPushButton("Reset password")
        reset_btn.setFixedHeight(SIZE_CONTROL_SM)
        reset_btn.setStyleSheet(_TEXT_BTN_GHOST)
        reset_btn.clicked.connect(self.reset_requested.emit)
        row.addWidget(reset_btn)
        form.addLayout(row)

        form.addSpacing(SPACE_6)

        self._hint_lbl = QLabel("")
        self._hint_lbl.setWordWrap(True)
        self._hint_lbl.setStyleSheet(
            f"QLabel {{ color: {_TEXT_MUTED}; background: transparent; border: none; font-size: {FONT_SIZE_LABEL}px; }}"
        )
        self._hint_lbl.setVisible(False)
        form.addWidget(self._hint_lbl)

        form.addSpacing(SPACE_MD)

        login_btn = QPushButton("Sign in")
        login_btn.setFixedHeight(SIZE_CONTROL_LG)
        login_btn.setStyleSheet(_PRIMARY_BTN)
        login_btn.clicked.connect(lambda: self.submit.emit(self.email(), self.password()))
        form.addWidget(login_btn)

    def email(self) -> str:
        return self._email.text().strip()

    def password(self) -> str:
        return self._password.text()

    def remember_me(self) -> bool:
        return self._remember.isChecked()

    def set_email(self, val: str):
        self._email.setText(val or "")

    def set_error(self, msg: str):
        self._error_lbl.setText(msg or "")
        self._error_lbl.setVisible(bool(msg))
        self.adjustSize()

    def set_hint(self, msg: str):
        self._hint_lbl.setText(msg or "")
        self._hint_lbl.setVisible(bool(msg))
        self.adjustSize()

    def set_remember(self, checked: bool):
        self._remember.setChecked(bool(checked))

    def clear_password(self):
        self._password.clear()

    def focus_email(self):
        self._email.setFocus()
