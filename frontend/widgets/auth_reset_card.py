from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from frontend.styles._colors import (
    _ACCENT,
    _ACCENT_ALT_BG_08,
    _ACCENT_HI,
    _BG_SURFACE,
    _BORDER,
    _BORDER_DIM,
    _DANGER,
    _TEXT_PRI,
    _TEXT_SEC,
    _TEXT_MUTED,
    _TEXT_ON_ACCENT,
)
from frontend.styles._input_styles import _AUTH_INPUT_LG, _AUTH_INPUT_MD
from frontend.styles._btn_styles import _PRIMARY_BTN, _SECONDARY_BTN
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
    RADIUS_MD,
    SIZE_CONTROL_38,
    SIZE_CONTROL_MID,
    SIZE_DIALOG_W_XL,
    SPACE_10,
    SPACE_14,
    SPACE_20,
    SPACE_28,
    SPACE_36,
    SPACE_6,
    SPACE_LG,
    SPACE_MD,
    SPACE_SM,
    SPACE_XL,
    SPACE_XXL,
    SPACE_XXXS,
)


class AuthResetCard(QFrame):
    load_requested = Signal(str)
    submit_requested = Signal(str, list, str, str)
    back = Signal()

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
        form.setContentsMargins(SPACE_36, SPACE_XXL, SPACE_36, SPACE_XXL)
        form.setSpacing(0)

        title = QLabel("Reset password")
        f = QFont()
        safe_set_point_size(f, FONT_SIZE_XXL)
        f.setBold(True)
        title.setFont(f)
        title.setStyleSheet(f"QLabel {{ color: {_TEXT_PRI}; background: transparent; border: none; }}")
        form.addWidget(title)

        form.addSpacing(SPACE_6)

        subtitle = QLabel("Answer your security questions to reset your password.")
        subtitle.setStyleSheet(f"QLabel {{ color: {_TEXT_SEC}; background: transparent; border: none; font-size: {FONT_SIZE_BODY}px; }}")
        form.addWidget(subtitle)

        form.addSpacing(SPACE_20)

        self._error_lbl = QLabel("")
        self._error_lbl.setStyleSheet(
            f"QLabel {{ color: {_DANGER}; background: transparent; border: none; font-size: {FONT_SIZE_BODY}px; }}"
        )
        self._error_lbl.setWordWrap(True)
        self._error_lbl.setVisible(False)
        form.addWidget(self._error_lbl)

        email_label = QLabel("Email")
        email_label.setStyleSheet(
            f"QLabel {{ color: {_TEXT_SEC}; background: transparent; border: none; font-size: {FONT_SIZE_BODY}px; font-weight: {FONT_WEIGHT_SEMIBOLD}; }}"
        )
        form.addWidget(email_label)

        form.addSpacing(SPACE_6)

        self._email = QLineEdit()
        self._email.setPlaceholderText("your@email.com")
        self._email.setFixedHeight(SIZE_CONTROL_MID)
        self._email.setStyleSheet(_AUTH_INPUT_LG)
        form.addWidget(self._email)

        form.addSpacing(SPACE_20)

        self._q_labels = []
        self._a_edits = []
        for i in range(3):
            q = QLabel(f"Security question {i + 1}")
            q.setStyleSheet(
                f"QLabel {{ color: {_TEXT_SEC}; background: transparent; border: none; font-size: {FONT_SIZE_LABEL}px; font-weight: {FONT_WEIGHT_SEMIBOLD}; }}"
            )
            form.addWidget(q)
            self._q_labels.append(q)

            form.addSpacing(SPACE_6)

            a = QLineEdit()
            a.setEchoMode(QLineEdit.EchoMode.Password)
            a.setPlaceholderText("Your answer")
            a.setFixedHeight(SIZE_CONTROL_38)
            a.setStyleSheet(_AUTH_INPUT_MD)
            self._a_edits.append(a)
            form.addWidget(a)

            form.addSpacing(SPACE_MD)

        form.addSpacing(SPACE_SM)

        new_pw_label = QLabel("New Password")
        new_pw_label.setStyleSheet(
            f"QLabel {{ color: {_TEXT_SEC}; background: transparent; border: none; font-size: {FONT_SIZE_BODY}px; font-weight: {FONT_WEIGHT_SEMIBOLD}; }}"
        )
        form.addWidget(new_pw_label)

        form.addSpacing(SPACE_6)

        self._new_pw = QLineEdit()
        self._new_pw.setEchoMode(QLineEdit.EchoMode.Password)
        self._new_pw.setPlaceholderText("Enter new password")
        self._new_pw.setFixedHeight(SIZE_CONTROL_MID)
        self._new_pw.setStyleSheet(_AUTH_INPUT_LG)
        form.addWidget(self._new_pw)

        form.addSpacing(SPACE_MD)

        self._new_pw2 = QLineEdit()
        self._new_pw2.setEchoMode(QLineEdit.EchoMode.Password)
        self._new_pw2.setPlaceholderText("Confirm new password")
        self._new_pw2.setFixedHeight(SIZE_CONTROL_MID)
        self._new_pw2.setStyleSheet(_AUTH_INPUT_LG)
        form.addWidget(self._new_pw2)

        form.addSpacing(SPACE_XL)

        button_row = QHBoxLayout()
        button_row.setSpacing(SPACE_10)
        load_btn = QPushButton("Load questions")
        load_btn.setFixedHeight(SIZE_CONTROL_MID)
        load_btn.setStyleSheet(_SECONDARY_BTN)
        load_btn.clicked.connect(lambda: self.load_requested.emit(self.reset_email()))
        button_row.addWidget(load_btn)

        back_btn = QPushButton("Back to login")
        back_btn.setFixedHeight(SIZE_CONTROL_MID)
        back_btn.setStyleSheet(_SECONDARY_BTN)
        back_btn.clicked.connect(self.back.emit)
        button_row.addWidget(back_btn)

        button_row.addStretch()

        submit = QPushButton("Reset password")
        submit.setFixedHeight(SIZE_CONTROL_MID)
        submit.setStyleSheet(_PRIMARY_BTN)
        submit.clicked.connect(self._emit_submit)
        button_row.addWidget(submit)

        form.addLayout(button_row)

    def set_questions(self, questions: list[str]):
        for i, lbl in enumerate(self._q_labels):
            lbl.setText(questions[i] if i < len(questions) and questions[i] else f"Security question {i + 1}")

    def set_error(self, msg: str):
        self._error_lbl.setText(msg or "")
        self._error_lbl.setVisible(bool(msg))
        self.adjustSize()

    def reset_email(self) -> str:
        return self._email.text().strip()

    def set_email(self, val: str):
        self._email.setText(val or "")

    def answers(self) -> list[str]:
        return [a.text() for a in self._a_edits]

    def new_password(self) -> str:
        return self._new_pw.text()

    def confirm_password(self) -> str:
        return self._new_pw2.text()

    def clear_answers(self):
        for a in self._a_edits:
            a.clear()
        self._new_pw.clear()
        self._new_pw2.clear()

    def _emit_submit(self):
        self.submit_requested.emit(self.reset_email(), self.answers(), self.new_password(), self.confirm_password())
