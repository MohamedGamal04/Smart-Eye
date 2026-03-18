from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSlider,
    QVBoxLayout,
)

from frontend.app_theme import safe_set_point_size
from frontend.styles._colors import _TEXT_SEC, _TEXT_MUTED, _DANGER, _WARNING, _SUCCESS
from frontend.styles._card_styles import _CARD_BASE, _CARD_HOVER
from frontend.widgets.confirm_delete_button import ConfirmDeleteButton
from frontend.ui_tokens import (
    FONT_SIZE_BODY,
    FONT_SIZE_LABEL,
    FONT_SIZE_SUBHEAD,
    FONT_SIZE_CAPTION,
    FONT_WEIGHT_NORMAL,
    FONT_WEIGHT_SEMIBOLD,
    FONT_WEIGHT_BOLD,
    RADIUS_XL,
    SPACE_6,
    SPACE_SM,
    SPACE_MD,
    SPACE_LG,
    SIZE_CONTROL_30,
    SIZE_PANEL_H_MD,
    SIZE_ROW_MD,
)


class ModelCardWidget(QFrame):
    toggled = Signal(int, bool)
    confidence_changed = Signal(int, float)
    delete_clicked = Signal(int)
    configure_clicked = Signal(int)
    retry_clicked = Signal(int)

    def __init__(self, plugin_data, parent=None):
        super().__init__(parent)
        self._plugin = plugin_data
        self._plugin_id = plugin_data.get("id", 0)
        self.setStyleSheet(f"{_CARD_BASE}{_CARD_HOVER}")
        self.setFixedHeight(SIZE_PANEL_H_MD)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACE_LG, SPACE_MD, SPACE_LG, SPACE_MD)
        layout.setSpacing(SPACE_SM)
        top_row = QHBoxLayout()
        name_label = QLabel(plugin_data.get("name", "Plugin"))
        name_font = QFont()
        safe_set_point_size(name_font, FONT_SIZE_SUBHEAD)
        name_font.setBold(True)
        name_label.setFont(name_font)
        top_row.addWidget(name_label)
        top_row.addStretch()
        self._enable_check = QCheckBox("Enabled")
        self._enable_check.setChecked(plugin_data.get("enabled", True))
        self._enable_check.toggled.connect(lambda v: self.toggled.emit(self._plugin_id, v))
        top_row.addWidget(self._enable_check)
        layout.addLayout(top_row)
        type_label = QLabel(f"Type: {plugin_data.get('model_type', 'onnx')}  |  v{plugin_data.get('version', '1.0')}")
        type_label.setStyleSheet(f"color: {_TEXT_SEC}; font-size: {FONT_SIZE_CAPTION}px; background: transparent;")
        layout.addWidget(type_label)

        status_row = QHBoxLayout()
        status_text, status_style = self._status_badge(plugin_data)
        status_lbl = QLabel(status_text)
        status_lbl.setStyleSheet(status_style)
        status_lbl.setMargin(2)
        status_row.addWidget(status_lbl)

        err = plugin_data.get("last_error")
        if err:
            err_lbl = QLabel("Failed")
            err_lbl.setStyleSheet(f"color: {_DANGER}; font-weight: {FONT_WEIGHT_SEMIBOLD}; font-size: {FONT_SIZE_CAPTION}px;")
            err_lbl.setToolTip(err)
            status_row.addWidget(err_lbl)
        status_row.addStretch()
        layout.addLayout(status_row)

        desc = plugin_data.get("description", "")
        if desc:
            desc_label = QLabel(desc)
            desc_label.setStyleSheet(f"color: {_TEXT_SEC}; font-size: {FONT_SIZE_LABEL}px; background: transparent;")
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)
        conf_row = QHBoxLayout()
        conf_label = QLabel("Confidence:")
        conf_label.setStyleSheet("background: transparent;")
        conf_row.addWidget(conf_label)
        self._conf_slider = QSlider(Qt.Orientation.Horizontal)
        self._conf_slider.setRange(10, 100)
        self._conf_slider.setValue(int(plugin_data.get("confidence", 0.6) * 100))
        self._conf_slider.valueChanged.connect(self._on_conf_changed)
        conf_row.addWidget(self._conf_slider)
        self._conf_value = QLabel(f"{self._conf_slider.value()}%")
        self._conf_value.setFixedWidth(SIZE_ROW_MD)
        self._conf_value.setStyleSheet("background: transparent;")
        conf_row.addWidget(self._conf_value)
        layout.addLayout(conf_row)
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        retry_btn = QPushButton("Retry load")
        retry_btn.setFixedHeight(SIZE_CONTROL_30)
        retry_btn.clicked.connect(lambda: self.retry_clicked.emit(self._plugin_id))
        btn_row.addWidget(retry_btn)
        config_btn = QPushButton("Configure")
        config_btn.setProperty("class", "secondary")
        config_btn.setFixedHeight(SIZE_CONTROL_30)
        config_btn.clicked.connect(lambda: self.configure_clicked.emit(self._plugin_id))
        btn_row.addWidget(config_btn)
        del_btn = ConfirmDeleteButton("Delete", "Sure?")
        del_btn.setFixedHeight(SIZE_CONTROL_30)
        del_btn.set_confirm_callback(lambda: self.delete_clicked.emit(self._plugin_id))
        btn_row.addWidget(del_btn)
        layout.addLayout(btn_row)

    def _on_conf_changed(self, val):
        self._conf_value.setText(f"{val}%")
        self.confidence_changed.emit(self._plugin_id, val / 100.0)

    def _status_badge(self, plugin):
        provider = (plugin.get("last_provider") or "").lower()
        last_error = plugin.get("last_error")
        if last_error:
            return ("Load failed", f"color: {_DANGER}; background: transparent; font-weight: {FONT_WEIGHT_BOLD};")
        if provider.startswith("cpu"):
            return ("CPU (fallback)", f"color: {_WARNING}; background: transparent; font-weight: {FONT_WEIGHT_SEMIBOLD};")
        if provider.startswith("dml"):
            return ("GPU (DML)", f"color: {_SUCCESS}; background: transparent; font-weight: {FONT_WEIGHT_SEMIBOLD};")
        return ("Provider: auto", f"color: {_TEXT_SEC}; background: transparent; font-weight: {FONT_WEIGHT_NORMAL};")
