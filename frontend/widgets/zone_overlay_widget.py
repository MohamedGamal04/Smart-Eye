from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QBrush, QColor, QFont, QPainter, QPen
from PySide6.QtWidgets import QSizePolicy, QWidget

from frontend.styles._colors import _ACCENT, _ZONE_COLOR_DEFAULT
from frontend.ui_tokens import FONT_SIZE_MICRO


class ZoneOverlayWidget(QWidget):
    zone_created = Signal(float, float, float, float)
    zone_selected = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._background = None
        self._zones = []
        self._drawing = False
        self._start_pos = None
        self._current_pos = None
        self._selected_zone = -1

    def set_background(self, pixmap):
        self._background = pixmap
        self.update()

    def set_zones(self, zones):
        self._zones = zones
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self._background:
            scaled = self._background.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            x = (self.width() - scaled.width()) // 2
            y = (self.height() - scaled.height()) // 2
            painter.drawPixmap(x, y, scaled)

        w, h = self.width(), self.height()
        for i, zone in enumerate(self._zones):
            x1 = int(zone.get("x1", 0) * w)
            y1 = int(zone.get("y1", 0) * h)
            x2 = int(zone.get("x2", 0) * w)
            y2 = int(zone.get("y2", 0) * h)
            color_hex = zone.get("color", _ZONE_COLOR_DEFAULT)
            r = int(color_hex[1:3], 16)
            g = int(color_hex[3:5], 16)
            b = int(color_hex[5:7], 16)
            painter.setBrush(QBrush(QColor(r, g, b, 60)))
            painter.setPen(QPen(QColor(r, g, b, 200), 2 if i != self._selected_zone else 3))
            painter.drawRect(x1, y1, x2 - x1, y2 - y1)
            painter.setPen(QPen(QColor(255, 255, 255, 220)))
            painter.setFont(QFont("Segoe UI", FONT_SIZE_MICRO, QFont.Weight.Bold))
            painter.drawText(x1 + 6, y1 + 18, zone.get("name", f"Zone {i + 1}"))

        if self._drawing and self._start_pos and self._current_pos:
            accent = QColor(_ACCENT)
            accent.setAlpha(40)
            painter.setBrush(QBrush(accent))
            painter.setPen(QPen(QColor(_ACCENT), 2, Qt.PenStyle.DashLine))
            x1 = min(self._start_pos.x(), self._current_pos.x())
            y1 = min(self._start_pos.y(), self._current_pos.y())
            x2 = max(self._start_pos.x(), self._current_pos.x())
            y2 = max(self._start_pos.y(), self._current_pos.y())
            painter.drawRect(int(x1), int(y1), int(x2 - x1), int(y2 - y1))

        painter.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position()
            for i, zone in enumerate(self._zones):
                x1 = zone.get("x1", 0) * self.width()
                y1 = zone.get("y1", 0) * self.height()
                x2 = zone.get("x2", 0) * self.width()
                y2 = zone.get("y2", 0) * self.height()
                if x1 <= pos.x() <= x2 and y1 <= pos.y() <= y2:
                    self._selected_zone = i
                    self.zone_selected.emit(i)
                    self.update()
                    return
            self._drawing = True
            self._start_pos = pos
            self._current_pos = pos

    def mouseMoveEvent(self, event):
        if self._drawing:
            self._current_pos = event.position()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self._drawing:
            self._drawing = False
            if self._start_pos and self._current_pos:
                w, h = self.width(), self.height()
                x1 = min(self._start_pos.x(), self._current_pos.x()) / w
                y1 = min(self._start_pos.y(), self._current_pos.y()) / h
                x2 = max(self._start_pos.x(), self._current_pos.x()) / w
                y2 = max(self._start_pos.y(), self._current_pos.y()) / h
                if abs(x2 - x1) > 0.02 and abs(y2 - y1) > 0.02:
                    self.zone_created.emit(x1, y1, x2, y2)
            self._start_pos = None
            self._current_pos = None
            self.update()
