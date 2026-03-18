from __future__ import annotations

from frontend.styles._colors import _BG_BASE, _BG_SURFACE, _BORDER_DIM
from frontend.ui_tokens import SPACE_XXXS


def header_bar_style(widget_id: str | None = None, bg: str = _BG_BASE, border: str = _BORDER_DIM) -> str:
    base = f"background: {bg}; border-bottom: {SPACE_XXXS}px solid {border};"
    if widget_id:
        return f"QWidget#{widget_id} {{ {base} }}"
    return base


def toolbar_style(bg: str = _BG_SURFACE, border: str = _BORDER_DIM) -> str:
    return f"background: {bg}; border-bottom: {SPACE_XXXS}px solid {border};"


def splitter_handle_style(color: str = _BORDER_DIM, width: int = SPACE_XXXS) -> str:
    return f"QSplitter::handle {{ background-color: {color}; width: {width}px; }}"


def divider_style(color: str = _BORDER_DIM, height: int = SPACE_XXXS) -> str:
    return f"background: {color}; border: none; max-height: {height}px;"
