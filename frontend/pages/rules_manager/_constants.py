from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QWidget,
)

from frontend.styles._btn_styles import _TEXT_BTN_BLUE, _TEXT_BTN_GHOST, _TEXT_BTN_RED, _TEXT_BTN_RED_CONFIRM, _PRIMARY_BTN
from frontend.app_theme import page_base_styles

from frontend.styles._colors import (
    _BG_SURFACE,
    _BG_RAISED,
    _BG_OVERLAY,
    _BORDER,
    _BORDER_DIM,
    _TEXT_PRI,
    _TEXT_SEC,
    _TEXT_MUTED,
    _ACCENT,
    _ACCENT_HI,
    _ACCENT_MID,
    _ACCENT_MID_DARK,
    _ACCENT_MID_HOVER,
    _ACCENT_BG_12,
    _ACCENT_BG_22,
    _ACCENT_HI_BG_03,
    _ACCENT_HI_BG_10,
    _ACCENT_HI_BG_12,
    _ACCENT_HI_BG_28,
    _ACCENT_HI_BG_45,
    _ACCENT_HI_BG_55,
    _ACCENT_HI_BG_70,
    _ACCENT_TINT,
    _ACCENT_TINT_STRONG,
    _WARNING,
    _WARNING_DIM,
    _WARNING_BG_14,
    _DANGER,
    _DANGER_DIM,
    _DANGER_BG_14,
    _DANGER_BORDER_45,
    _DANGER_TINT,
    _DANGER_TINT_STRONG,
    _DANGER_TINT_CONFIRM,
    _DANGER_TINT_HOVER,
    _DANGER_TINT_PRESSED,
    _SUCCESS,
    _BG_BASE,
    _TEXT_ON_ACCENT,
)
from frontend.ui_tokens import (
    FONT_SIZE_BODY,
    FONT_SIZE_CAPTION,
    FONT_SIZE_LABEL,
    FONT_SIZE_MICRO,
    FONT_WEIGHT_BOLD,
    FONT_WEIGHT_HEAVY,
    FONT_WEIGHT_NORMAL,
    FONT_WEIGHT_SEMIBOLD,
    RADIUS_MD,
    RADIUS_LG,
    RADIUS_SM,
    RADIUS_XS,
    SIZE_BTN_W_XS,
    SIZE_ITEM_SM,
    SIZE_LABEL_W,
    SIZE_PILL_H,
    SPACE_10,
    SPACE_14,
    SPACE_20,
    SPACE_28,
    SPACE_5,
    SPACE_6,
    SPACE_LG,
    SPACE_MD,
    SPACE_SM,
    SPACE_XL,
    SPACE_XS,
    SPACE_XXL,
    SPACE_XXS,
    SPACE_XXXS,
)
from frontend.styles._input_styles import _FORM_INPUTS, _FORM_COMBO

_ACTION_BTN_W = SIZE_BTN_W_XS
_ACTION_BTN_H = SIZE_ITEM_SM

_ACTION_META = {
    "alarm": (_DANGER, _DANGER_BG_14, _DANGER_BORDER_45, "ALARM"),
    "suppress": (_WARNING, _WARNING_BG_14, _WARNING_DIM, "SUPPRESS"),
    "log_only": (_ACCENT_HI, _ACCENT_BG_12, _ACCENT, "LOG ONLY"),
}


_STYLESHEET = (
    page_base_styles()
    + f"""
QPushButton {{
    background-color: {_BG_OVERLAY};
    border: {SPACE_XXXS}px solid {_BORDER};
    border-radius: {RADIUS_MD}px;
    padding: 0 {SPACE_LG}px;
    color: {_TEXT_PRI};
    font-weight: {FONT_WEIGHT_SEMIBOLD};
    min-height: {SPACE_XXL}px;
}}
QPushButton:hover {{ background-color: {_BORDER}; border-color: {_TEXT_SEC}; }}
QPushButton:disabled {{ color: {_TEXT_MUTED}; border-color: {_TEXT_MUTED}; background-color: {_BG_RAISED}; }}
QPushButton[class="secondary"] {{
    background-color: transparent;
    border: {SPACE_XXXS}px solid {_BORDER};
    color: {_TEXT_SEC};
}}
QPushButton[class="secondary"]:hover {{ background-color: {_BG_OVERLAY}; color: {_TEXT_PRI}; }}
{_FORM_INPUTS}
{_FORM_COMBO}
QScrollArea {{ border: none; background-color: transparent; }}
QScrollBar:vertical {{ border: none; background: transparent; width: {SPACE_6}px; margin: {SPACE_XXS}px {SPACE_XS}px; }}
QScrollBar::handle:vertical {{
    background: {_ACCENT_HI_BG_28};
    min-height: {SPACE_28}px; border-radius: {RADIUS_XS}px;
}}
QScrollBar::handle:vertical:hover {{ background: {_ACCENT_HI_BG_55}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QScrollBar:horizontal {{ border: none; background: transparent; height: {SPACE_6}px; margin: {SPACE_XXS}px {SPACE_XXS}px; }}
QScrollBar::handle:horizontal {{
    background: {_ACCENT_HI_BG_28}; min-width: {SPACE_28}px; border-radius: {RADIUS_XS}px;
}}
QScrollBar::handle:horizontal:hover {{ background: {_ACCENT_HI_BG_55}; }}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; }}
QCheckBox {{ color: {_TEXT_PRI}; spacing: {SPACE_SM}px; }}
QCheckBox::indicator {{
    width: {SPACE_LG}px; height: {SPACE_LG}px;
    border: {SPACE_XXXS}px solid {_BORDER};
    border-radius: {RADIUS_SM}px;
    background-color: {_BG_RAISED};
    image: none;
}}
QCheckBox::indicator:checked {{
    background-color: {_ACCENT}; border-color: {_ACCENT};
    image: url(frontend/assets/icons/checkmark.png);
}}
QCheckBox::indicator:hover {{ border-color: {_ACCENT_HI}; }}
QLabel {{ background: transparent; }}
QFormLayout QLabel {{ color: {_TEXT_SEC}; font-size: {FONT_SIZE_LABEL}px; font-weight: {FONT_WEIGHT_NORMAL}; }}
QDialog {{ background-color: {_BG_SURFACE}; }}
"""
)

_ADD_BTN_BLUE = f"""
QPushButton {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {_ACCENT_MID}, stop:1 {_ACCENT_MID_DARK});
    border: {SPACE_XXXS}px solid {_ACCENT_HI_BG_45};
    border-radius: {RADIUS_MD}px;
    color: {_TEXT_ON_ACCENT};
    font-size: {FONT_SIZE_LABEL}px;
    font-weight: {FONT_WEIGHT_BOLD};
    padding: 0 {SPACE_LG}px;
    min-height: {SPACE_XXL}px;
}}
QPushButton:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {_ACCENT_MID_HOVER}, stop:1 {_ACCENT});
    border-color: {_ACCENT_HI_BG_70};
}}
QPushButton:pressed {{
    background: {_ACCENT_MID_DARK};
}}
"""

_EDIT_BTN_SS = _TEXT_BTN_BLUE

_DEL_DEFAULT_SS = _TEXT_BTN_RED

_DEL_CONFIRM_SS = _TEXT_BTN_RED_CONFIRM


def _get_attributes():
    return ["identity", "object", "objects"]


def _input_ss(radius: int = RADIUS_MD) -> str:
    return _FORM_INPUTS


def _combo_ss() -> str:
    return _FORM_COMBO


def _spin_ss() -> str:
    return _FORM_INPUTS


def _make_separator() -> QFrame:
    sep = QFrame()
    sep.setFrameShape(QFrame.Shape.HLine)
    sep.setStyleSheet(f"background-color: {_BORDER}; border: none; max-height: {SPACE_XXXS}px; margin: {SPACE_XXS}px 0;")
    return sep


def _pill(text: str, fg: str, bg: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setFixedHeight(SIZE_PILL_H)
    lbl.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
    lbl.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
    lbl.setStyleSheet(f"""
        color: {fg};
        background-color: {bg};
        border: none;
        border-radius: {RADIUS_LG}px;
        padding: 0 {SPACE_10}px;
        font-size: {FONT_SIZE_MICRO}px;
        font-weight: {FONT_WEIGHT_BOLD};
        letter-spacing: 0.{SPACE_5}px;
    """)
    return lbl


def _make_sdiv(title: str) -> QFrame:
    fr = QFrame()
    fr.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    fr.setStyleSheet(
        f"QFrame {{ background: {_BG_RAISED}; border-top: {SPACE_XXXS}px solid {_BORDER};"
        f" border-bottom: {SPACE_XXXS}px solid {_BORDER}; border-left: none; border-right: none; }}"
    )
    row = QHBoxLayout(fr)
    row.setContentsMargins(SPACE_LG, SPACE_6, SPACE_MD, SPACE_6)
    lbl = QLabel(title.upper())
    lbl.setStyleSheet(
        f"color: {_TEXT_SEC}; font-size: {FONT_SIZE_MICRO}px; font-weight: {FONT_WEIGHT_HEAVY};"
        f" letter-spacing: {SPACE_XXS}px; background: transparent; border: none;"
    )
    row.addWidget(lbl)
    row.addStretch()
    return fr


def _srow(label_text: str, widget: QWidget, height: int = 52) -> QFrame:
    fr = QFrame()
    fr.setFixedHeight(height)
    fr.setStyleSheet(f"""
        QFrame {{
            background:transparent;
            border:none;
            border-bottom:{SPACE_XXXS}px solid {_BORDER_DIM};
        }}
        QFrame:hover {{ background:{_ACCENT_HI_BG_03}; }}
    """)
    row = QHBoxLayout(fr)
    row.setContentsMargins(SPACE_XL, 0, SPACE_XL, 0)
    row.setSpacing(SPACE_20)
    lb = QLabel(label_text)
    lb.setFixedWidth(SIZE_LABEL_W)
    lb.setAlignment(Qt.AlignmentFlag.AlignVCenter)
    lb.setStyleSheet(
        f"color:{_TEXT_SEC}; font-size:{FONT_SIZE_LABEL}px; font-weight:{FONT_WEIGHT_NORMAL};background:transparent; border:none;"
    )
    row.addWidget(lb)
    row.addWidget(widget, stretch=1)
    return fr
