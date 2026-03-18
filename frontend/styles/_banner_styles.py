from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel

from frontend.styles._colors import _ACCENT_BG_10, _ACCENT_HI, _ACCENT_HI_BG_20
from frontend.ui_tokens import FONT_SIZE_CAPTION, FONT_SIZE_TINY, SPACE_SM, SPACE_XL, SPACE_XXXS


EDIT_BANNER_STYLE = (
    "QFrame {"
    f"    background: {_ACCENT_BG_10};"
    f"    border-bottom: {SPACE_XXXS}px solid {_ACCENT_HI_BG_20};"
    "    border-top: none; border-left: none; border-right: none;"
    "}"
)

EDIT_BANNER_DOT_STYLE = f"color: {_ACCENT_HI}; font-size: {FONT_SIZE_TINY}px; background: transparent; border: none;"

EDIT_BANNER_TEXT_STYLE = f"color: {_ACCENT_HI}; font-size: {FONT_SIZE_CAPTION}px; background: transparent; border: none;"


def make_edit_banner(text: str, parent=None) -> QFrame:
    if not text.lower().startswith("editing"):
        text = f"Editing \u2014 {text}"
    banner = QFrame(parent)
    banner.setStyleSheet(EDIT_BANNER_STYLE)
    bi = QHBoxLayout(banner)
    bi.setContentsMargins(SPACE_XL, SPACE_SM, SPACE_XL, SPACE_SM)
    bi.setSpacing(SPACE_SM)
    dot = QLabel("\u25cf")
    dot.setStyleSheet(EDIT_BANNER_DOT_STYLE)
    bi.addWidget(dot)
    lbl = QLabel(text)
    lbl.setStyleSheet(EDIT_BANNER_TEXT_STYLE)
    bi.addWidget(lbl)
    bi.addStretch()
    return banner
