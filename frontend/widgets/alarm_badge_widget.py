from PySide6.QtCore import Property, Qt, QTimer
from PySide6.QtGui import QBrush, QColor, QFont, QLinearGradient, QPainter, QPen
from PySide6.QtWidgets import QSizePolicy, QWidget

from frontend.app_theme import safe_set_point_size
from frontend.styles._colors import _TEXT_PRI, _WARNING, _DANGER, _DANGER_DIM, _ALARM_LOW_DARK, _ALARM_CRITICAL, _ALARM_CRITICAL_HI
from frontend.ui_tokens import FONT_SIZE_MICRO, RADIUS_MD, SIZE_BADGE_H, SIZE_FIELD_W_SM

_LEVEL_LABELS = {1: "LOW", 2: "MED", 3: "HIGH"}


class AlarmBadgeWidget(QWidget):
    def __init__(self, text="", level=1, parent=None):
        super().__init__(parent)
        self._text = text
        self._level = level
        self._opacity = 1.0
        self._pulse_state = True
        self._pulse_timer = QTimer(self)
        self._pulse_timer.timeout.connect(self._toggle_pulse)
        self.setFixedHeight(SIZE_BADGE_H)
        self.setMinimumWidth(SIZE_FIELD_W_SM)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        if level >= 2:
            self._pulse_timer.start(500)

    def _get_opacity(self):
        return self._opacity

    def _set_opacity(self, val):
        self._opacity = val
        self.update()

    opacity_prop = Property(float, _get_opacity, _set_opacity)

    def _toggle_pulse(self):
        self._pulse_state = not self._pulse_state
        self.update()

    def set_level(self, level):
        self._level = level
        if level >= 2:
            if not self._pulse_timer.isActive():
                self._pulse_timer.start(500)
        else:
            self._pulse_timer.stop()
            self._pulse_state = True
        self.update()

    def set_text(self, text):
        self._text = text
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        base_colors = {
            1: (QColor(_ALARM_LOW_DARK), QColor(_WARNING)),
            2: (QColor(_DANGER_DIM), QColor(_DANGER)),
            3: (QColor(_ALARM_CRITICAL), QColor(_ALARM_CRITICAL_HI)),
        }
        c_dark, c_light = base_colors.get(self._level, base_colors[2])

        if not self._pulse_state:
            c_dark = c_dark.darker(130)
            c_light = c_light.darker(130)

        r = self.rect()
        grad = QLinearGradient(0, 0, 0, r.height())
        grad.setColorAt(0.0, c_light)
        grad.setColorAt(1.0, c_dark)
        painter.setBrush(QBrush(grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(r, RADIUS_MD, RADIUS_MD)

        border_color = c_light.lighter(120) if self._pulse_state else c_dark.lighter(110)
        painter.setPen(QPen(border_color, 1))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(r.adjusted(0, 0, -1, -1), RADIUS_MD, RADIUS_MD)

        painter.setPen(QPen(QColor(_TEXT_PRI)))
        font = QFont("Segoe UI")
        safe_set_point_size(font, FONT_SIZE_MICRO)
        font.setBold(True)
        painter.setFont(font)
        level_label = _LEVEL_LABELS.get(self._level, "")
        painter.drawText(r, Qt.AlignmentFlag.AlignCenter, f"⚠  {self._text}  [{level_label}]")
        painter.end()

    def stop(self):
        self._pulse_timer.stop()
