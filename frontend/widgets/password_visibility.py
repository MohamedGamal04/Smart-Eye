from __future__ import annotations

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QLineEdit

from frontend.icon_theme import themed_icon_path

_EYE_ICON = "frontend/assets/icons/eye.png"
_HIDDEN_ICON = "frontend/assets/icons/hidden.png"


def attach_password_visibility_toggle(edit: QLineEdit):
    """Attach an icon-only trailing action to toggle password visibility."""
    state = {"hidden": True}
    action = edit.addAction(QIcon(), QLineEdit.ActionPosition.TrailingPosition)

    def _apply() -> None:
        if state["hidden"]:
            edit.setEchoMode(QLineEdit.EchoMode.Password)
            action.setIcon(QIcon(themed_icon_path(_EYE_ICON)))
            action.setToolTip("Show password")
        else:
            edit.setEchoMode(QLineEdit.EchoMode.Normal)
            action.setIcon(QIcon(themed_icon_path(_HIDDEN_ICON)))
            action.setToolTip("Hide password")

    def _toggle() -> None:
        pos = edit.cursorPosition()
        state["hidden"] = not state["hidden"]
        _apply()
        edit.setFocus()
        edit.setCursorPosition(pos)

    action.triggered.connect(_toggle)
    _apply()
    return action
