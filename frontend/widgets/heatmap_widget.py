import cv2
import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QLabel, QSizePolicy

from frontend.styles._colors import _BG_HEATMAP_90, _TEXT_FAINT, _WHITE_04
from frontend.ui_tokens import FONT_SIZE_SUBHEAD, RADIUS_LG, SPACE_XXXS


class HeatmapWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(320, 240)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setStyleSheet(
            f"""
            QLabel {{
                background-color: {_BG_HEATMAP_90};
                border: {SPACE_XXXS}px solid {_WHITE_04};
                border-radius: {RADIUS_LG}px;
            }}
            """
        )

    def set_heatmap(self, heatmap_img):
        if heatmap_img is None:
            self.clear()
            return
        if isinstance(heatmap_img, np.ndarray):
            rgb = cv2.cvtColor(heatmap_img, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb.shape
            qimg = QImage(rgb.data, w, h, ch * w, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qimg)
        elif isinstance(heatmap_img, QPixmap):
            pixmap = heatmap_img
        else:
            return
        scaled = pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.setPixmap(scaled)

    def clear_heatmap(self):
        self.clear()
        self.setText("No Heatmap Data")
        self.setStyleSheet(
            f"""
            QLabel {{
                background-color: {_BG_HEATMAP_90};
                color: {_TEXT_FAINT};
                font-size: {FONT_SIZE_SUBHEAD}px;
                border: {SPACE_XXXS}px solid {_WHITE_04};
                border-radius: {RADIUS_LG}px;
            }}
            """
        )
