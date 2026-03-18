from frontend.styles._colors import (
    _ACCENT,
    _ACCENT_GRAD_START,
    _BG_CHECK,
    _BORDER,
    _TEXT_DIM,
    _TEXT_PRI,
)
from frontend.ui_tokens import RADIUS_SM, SPACE_LG, SPACE_SM, SPACE_XXXS

CHECKBOX_STYLE = f"""
QCheckBox {{
    spacing: {SPACE_SM}px;
    color: {_TEXT_PRI};
}}
QCheckBox::indicator {{
    width: {SPACE_LG}px;
    height: {SPACE_LG}px;
    border: {SPACE_XXXS}px solid {_BORDER};
    border-radius: {RADIUS_SM}px;
    background: {_BG_CHECK};
    image: none;
}}
QCheckBox::indicator:hover {{ border-color: {_TEXT_DIM}; }}
QCheckBox::indicator:checked {{
    background: {_ACCENT_GRAD_START};
    border-color: {_ACCENT};
    image: url(frontend/assets/icons/checkmark.png);
}}
"""
