from __future__ import annotations

from PySide6.QtWidgets import QComboBox


class NoWheelComboBox(QComboBox):
    """QComboBox that ignores wheel events unless the popup view is open.

    Ignoring the wheel event allows the parent scroll area to handle scrolling
    when the user scrolls over the combo box.
    """

    def wheelEvent(self, event) -> None:  # type: ignore[override]
        try:
            popup_visible = self.view().isVisible()
        except Exception:
            popup_visible = False

        if popup_visible:
            super().wheelEvent(event)
        else:
            event.ignore()
