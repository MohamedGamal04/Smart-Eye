from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QFont, QPixmap, QTextCharFormat, QColor
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QFileDialog,
    QHBoxLayout,
    QFrame,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from backend.analytics import report_generator, stats_engine
from backend.analytics.heatmap_generator import HeatmapGenerator
from backend.repository import db
from frontend.app_theme import safe_set_point_size
from frontend.widgets.chart_widget import ChartWidget
from frontend.widgets.heatmap_widget import HeatmapWidget
from frontend.widgets.stat_card_widget import StatCardWidget


from frontend.styles._colors import (
    _ACCENT,
    _ACCENT_BG_22,
    _ACCENT_HI_BG_28,
    _ACCENT_HI_BG_55,
    _BG_BASE,
    _BG_OVERLAY,
    _BG_RAISED,
    _BG_SURFACE,
    _BORDER,
    _BORDER_DIM,
    _DANGER_DIM,
    _PURPLE_DIM,
    _SUCCESS_DIM,
    _TEXT_MUTED,
    _TEXT_ON_ACCENT,
    _TEXT_PRI,
    _TEXT_SEC,
    _TEXT_SOFT,
)
from frontend.styles.page_styles import header_bar_style, toolbar_style
from frontend.ui_tokens import (
    FONT_SIZE_BODY,
    FONT_SIZE_CAPTION,
    FONT_SIZE_LABEL,
    FONT_SIZE_LARGE,
    FONT_SIZE_MICRO,
    FONT_SIZE_SUBHEAD,
    FONT_WEIGHT_BOLD,
    FONT_WEIGHT_HEAVY,
    RADIUS_6,
    RADIUS_LG,
    RADIUS_MD,
    RADIUS_SM,
    SPACE_10,
    SPACE_20,
    SPACE_14,
    SPACE_LG,
    SPACE_MD,
    SPACE_28,
    SPACE_6,
    SPACE_SM,
    SPACE_XS,
    SPACE_XXS,
    SPACE_XXXS,
    SPACE_XL,
    SIZE_BADGE_H,
    SIZE_BTN_W_LG,
    SIZE_CONTROL_LG,
    SIZE_CONTROL_MD,
    SIZE_FIELD_W,
    SIZE_FIELD_W_LG,
    SIZE_HEADER_H,
    SIZE_ICON_LG,
    SIZE_ICON_MD,
    SIZE_ITEM_SM,
    SIZE_ROW_MD,
    SIZE_ROW_SM,
)
from frontend.styles._btn_styles import (
    _PRIMARY_BTN,
    _SECONDARY_BTN,
    _TAB_BTN as _A_TAB_BTN,
    _TAB_BTN_ACTIVE as _A_TAB_BTN_ACTIVE,
)

_STYLESHEET = f"""
QWidget {{
    color: {_TEXT_PRI}; background-color: transparent;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    font-size: {FONT_SIZE_BODY}px;
}}
QLabel {{ background: transparent; }}
QComboBox, QDateEdit {{
    background-color: {_BG_RAISED}; border: {SPACE_XXXS}px solid {_BORDER};
    border-radius: {RADIUS_MD}px; padding: {SPACE_XS}px {SPACE_10}px; color: {_TEXT_PRI}; min-height: {SIZE_BADGE_H}px;
}}
QComboBox:focus, QDateEdit:focus {{ border-color: {_ACCENT}; }}
QDateEdit::drop-down {{ border: none; background: transparent; width: {SPACE_20}px; }}
QDateEdit::down-arrow {{ image: url(frontend/assets/icons/arrow_down.png); width: {SPACE_10}px; height: {SPACE_10}px; }}
QComboBox::drop-down {{ border: none; width: {SPACE_20}px; background: transparent; }}
QComboBox::down-arrow {{
    image: url(frontend/assets/icons/arrow_down.png); width: {SPACE_MD}px; height: {SPACE_MD}px;
}}
QComboBox QAbstractItemView {{
    background-color: {_BG_OVERLAY}; border: {SPACE_XXXS}px solid {_BORDER};
    selection-background-color: {_ACCENT_BG_22}; color: {_TEXT_PRI}; padding: {SPACE_XS}px;
}}
QScrollBar:vertical {{ border: none; background: transparent; width: {SPACE_SM}px; margin: {SPACE_XXS}px {SPACE_XXXS}px; }}
QScrollBar::handle:vertical {{
    background: {_ACCENT_HI_BG_28}; min-height: {SPACE_28}px; border-radius: {RADIUS_SM}px;
}}
QScrollBar::handle:vertical:hover {{ background: {_ACCENT_HI_BG_55}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QCalendarWidget QWidget {{
    background-color: {_BG_RAISED};
    color: {_TEXT_PRI};
    alternate-background-color: {_BG_SURFACE};
}}
QCalendarWidget QToolButton {{
    background-color: {_BG_RAISED}; color: {_TEXT_PRI};
    border: none; border-radius: {RADIUS_6}px;
    font-size: {FONT_SIZE_LABEL}px; font-weight: {FONT_WEIGHT_BOLD};
    padding: {SPACE_XS}px {SPACE_SM}px; min-height: {SIZE_ITEM_SM}px;
}}
QCalendarWidget QToolButton:hover {{ background-color: {_BG_OVERLAY}; }}
QCalendarWidget QMenu {{
    background-color: {_BG_OVERLAY}; color: {_TEXT_PRI};
    border: {SPACE_XXXS}px solid {_BORDER};
}}
QCalendarWidget QSpinBox {{
    background-color: {_BG_RAISED}; color: {_TEXT_PRI};
    border: {SPACE_XXXS}px solid {_BORDER_DIM}; border-radius: {RADIUS_SM}px;
    padding: {SPACE_XXS}px {SPACE_XS}px;
    selection-background-color: {_ACCENT}; selection-color: {_TEXT_ON_ACCENT};
}}
QCalendarWidget QAbstractItemView {{
    background-color: {_BG_SURFACE}; color: {_TEXT_PRI};
    selection-background-color: {_ACCENT}; selection-color: {_TEXT_ON_ACCENT};
    outline: none;
}}
QCalendarWidget QAbstractItemView:disabled {{ color: {_TEXT_MUTED}; }}
QCalendarWidget #qt_calendar_navigationbar {{
    background-color: {_BG_RAISED};
    border-bottom: {SPACE_XXXS}px solid {_BORDER_DIM};
    padding: {SPACE_XXS}px {SPACE_6}px;
}}
"""


class AnalyticsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(_STYLESHEET)
        self._heatmap_gen = HeatmapGenerator()

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        header_w = QWidget()
        header_w.setFixedHeight(SIZE_HEADER_H)
        header_w.setObjectName("analytics_header")
        header_w.setStyleSheet(header_bar_style(widget_id="analytics_header", bg=_BG_BASE, border=_BORDER_DIM))
        hl = QHBoxLayout(header_w)
        hl.setContentsMargins(SPACE_XL, 0, SPACE_XL, 0)
        hl.setSpacing(SPACE_MD)

        icon_lbl = QLabel()
        icon_lbl.setFixedSize(SIZE_ICON_LG, SIZE_ICON_LG)
        _pix = QPixmap("frontend/assets/icons/analytics.png")
        if not _pix.isNull():
            icon_lbl.setPixmap(
                _pix.scaled(SIZE_ICON_LG, SIZE_ICON_LG, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            )
        hl.addWidget(icon_lbl)

        title = QLabel("Analytics")
        title_font = QFont()
        safe_set_point_size(title_font, FONT_SIZE_LARGE)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet(f"color: {_TEXT_PRI}; border: none; padding: 0;")
        hl.addWidget(title)
        hl.addStretch()
        root.addWidget(header_w)

        today = QDate.currentDate()
        filter_bar = QWidget()
        filter_bar.setFixedHeight(SIZE_HEADER_H)
        filter_bar.setStyleSheet(toolbar_style(bg=_BG_SURFACE, border=_BORDER_DIM))
        fl = QHBoxLayout(filter_bar)
        fl.setContentsMargins(SPACE_20, 0, SPACE_20, 0)
        fl.setSpacing(0)

        _fl_from_lbl = QLabel("From")
        _fl_from_lbl.setStyleSheet(f"color: {_TEXT_MUTED}; font-size: {FONT_SIZE_CAPTION}px; font-weight: {FONT_WEIGHT_BOLD};")
        fl.addWidget(_fl_from_lbl)
        fl.addSpacing(SPACE_SM)

        self._date_from = QDateEdit()
        self._date_from.setCalendarPopup(True)
        self._date_from.setDisplayFormat("yyyy-MM-dd")
        self._date_from.setDate(today.addDays(-30))
        self._date_from.setFixedHeight(SIZE_CONTROL_MD)
        self._date_from.setMinimumWidth(SIZE_FIELD_W)
        _cal_from = self._date_from.calendarWidget()
        _cal_from.setMinimumSize(400, 300)
        _cal_from.setGridVisible(False)
        _cal_from.setHorizontalHeaderFormat(_cal_from.HorizontalHeaderFormat.SingleLetterDayNames)
        _wknd_fmt = QTextCharFormat()
        _wknd_fmt.setForeground(QColor(_TEXT_SOFT))
        _cal_from.setWeekdayTextFormat(Qt.DayOfWeek.Saturday, _wknd_fmt)
        _cal_from.setWeekdayTextFormat(Qt.DayOfWeek.Sunday, _wknd_fmt)
        fl.addWidget(self._date_from)

        _fl_arr = QLabel("→")
        _fl_arr.setStyleSheet(f"color: {_TEXT_MUTED}; background: transparent; font-size: {FONT_SIZE_LABEL}px;")
        _fl_arr.setFixedWidth(SIZE_ICON_MD)
        _fl_arr.setAlignment(Qt.AlignmentFlag.AlignCenter)
        fl.addWidget(_fl_arr)

        self._date_to = QDateEdit()
        self._date_to.setCalendarPopup(True)
        self._date_to.setDate(today)
        self._date_to.setDisplayFormat("yyyy-MM-dd")
        self._date_to.setFixedHeight(SIZE_CONTROL_MD)
        self._date_to.setMinimumWidth(SIZE_FIELD_W)
        _cal_to = self._date_to.calendarWidget()
        _cal_to.setMinimumSize(400, 300)
        _cal_to.setGridVisible(False)
        _cal_to.setHorizontalHeaderFormat(_cal_to.HorizontalHeaderFormat.SingleLetterDayNames)
        _wknd_fmt2 = QTextCharFormat()
        _wknd_fmt2.setForeground(QColor(_TEXT_SOFT))
        _cal_to.setWeekdayTextFormat(Qt.DayOfWeek.Saturday, _wknd_fmt2)
        _cal_to.setWeekdayTextFormat(Qt.DayOfWeek.Sunday, _wknd_fmt2)
        fl.addWidget(self._date_to)

        fl.addSpacing(SPACE_14)
        _fls1 = QWidget()
        _fls1.setFixedSize(SPACE_XXXS, SPACE_XL)
        _fls1.setStyleSheet(f"background: {_BORDER_DIM};")
        fl.addWidget(_fls1)
        fl.addSpacing(SPACE_14)

        self._camera_combo = QComboBox()
        self._camera_combo.addItem("All Cameras", None)
        self._camera_combo.setFixedHeight(SIZE_CONTROL_MD)
        self._camera_combo.setMinimumWidth(SIZE_FIELD_W_LG)
        fl.addWidget(self._camera_combo)

        fl.addStretch()

        fl.addSpacing(SPACE_14)
        _fls2 = QWidget()
        _fls2.setFixedSize(SPACE_XXXS, SPACE_XL)
        _fls2.setStyleSheet(f"background: {_BORDER_DIM};")
        fl.addWidget(_fls2)
        fl.addSpacing(SPACE_10)

        apply_btn = QPushButton("Apply")
        apply_btn.setFixedSize(SIZE_BTN_W_LG, SIZE_CONTROL_MD)
        apply_btn.setStyleSheet(_PRIMARY_BTN)
        apply_btn.clicked.connect(self._refresh)
        fl.addWidget(apply_btn)

        fl.addSpacing(SPACE_6)
        pdf_btn = QPushButton("Export PDF")
        pdf_btn.setFixedSize(SIZE_BTN_W_LG, SIZE_CONTROL_MD)
        pdf_btn.setStyleSheet(_SECONDARY_BTN)
        pdf_btn.clicked.connect(self._export_pdf)
        fl.addWidget(pdf_btn)
        root.addWidget(filter_bar)

        content_w = QWidget()
        content_w.setStyleSheet(f"background: {_BG_BASE};")
        layout = QVBoxLayout(content_w)
        layout.setContentsMargins(SPACE_20, SPACE_LG, SPACE_20, SPACE_LG)
        layout.setSpacing(SPACE_LG)
        root.addWidget(content_w, stretch=1)

        stats_row = QHBoxLayout()
        stats_row.setSpacing(SPACE_10)
        self._stat_total = StatCardWidget("Total Events", "0", "detections", _ACCENT)
        self._stat_violations = StatCardWidget("Violations", "0", "total", _DANGER_DIM)
        self._stat_compliance = StatCardWidget("Compliance", "100%", "rate", _SUCCESS_DIM)
        self._stat_faces = StatCardWidget("Identified", "0", "faces", _PURPLE_DIM)
        stats_row.addWidget(self._stat_total)
        stats_row.addWidget(self._stat_violations)
        stats_row.addWidget(self._stat_compliance)
        stats_row.addWidget(self._stat_faces)
        layout.addLayout(stats_row)

        tab_card = QWidget()
        tab_card.setStyleSheet(f"background: {_BG_RAISED}; border-radius: {RADIUS_LG}px;")
        tab_card_vbox = QVBoxLayout(tab_card)
        tab_card_vbox.setContentsMargins(0, 0, 0, 0)
        tab_card_vbox.setSpacing(0)

        tab_bar_w = QWidget()
        tab_bar_w.setFixedHeight(SIZE_CONTROL_LG)
        tab_bar_w.setStyleSheet("background: transparent;")
        tb = QHBoxLayout(tab_bar_w)
        tb.setContentsMargins(SPACE_SM, 0, SPACE_SM, 0)
        tb.setSpacing(0)
        self._a_tab_btns: list[QPushButton] = []
        for i, label in enumerate(["Compliance Trend", "Hourly Violations", "Camera Activity", "Heatmap", "Top Violators"]):
            btn = QPushButton(label)
            btn.setStyleSheet(_A_TAB_BTN)
            btn.clicked.connect(lambda _, idx=i: self._switch_analytics_tab(idx))
            tb.addWidget(btn)
            self._a_tab_btns.append(btn)
        tb.addStretch()
        tab_card_vbox.addWidget(tab_bar_w)

        _tab_sep = QWidget()
        _tab_sep.setFixedHeight(SPACE_XXXS)
        _tab_sep.setStyleSheet(f"background: {_BORDER_DIM};")
        tab_card_vbox.addWidget(_tab_sep)

        self._a_stack = QStackedWidget()
        self._a_stack.setStyleSheet("background: transparent;")

        self._compliance_chart = ChartWidget("Compliance Trend")
        _cc_wrap = QWidget()
        _cc_wrap.setStyleSheet("background: transparent;")
        _cc_wl = QVBoxLayout(_cc_wrap)
        _cc_wl.setContentsMargins(SPACE_LG, SPACE_MD, SPACE_LG, SPACE_MD)
        _cc_wl.setSpacing(0)
        _cc_wl.addWidget(self._compliance_chart)
        self._a_stack.addWidget(_cc_wrap)

        self._violation_chart = ChartWidget("Hourly Violations")
        _vc_wrap = QWidget()
        _vc_wrap.setStyleSheet("background: transparent;")
        _vc_wl = QVBoxLayout(_vc_wrap)
        _vc_wl.setContentsMargins(SPACE_LG, SPACE_MD, SPACE_LG, SPACE_MD)
        _vc_wl.setSpacing(0)
        _vc_wl.addWidget(self._violation_chart)
        self._a_stack.addWidget(_vc_wrap)

        self._camera_chart = ChartWidget("Camera Activity")
        _cam_wrap = QWidget()
        _cam_wrap.setStyleSheet("background: transparent;")
        _cam_wl = QVBoxLayout(_cam_wrap)
        _cam_wl.setContentsMargins(SPACE_LG, SPACE_MD, SPACE_LG, SPACE_MD)
        _cam_wl.setSpacing(0)
        _cam_wl.addWidget(self._camera_chart)
        self._a_stack.addWidget(_cam_wrap)

        self._heatmap_widget = HeatmapWidget()
        heatmap_container = QWidget()
        heatmap_container.setStyleSheet("background: transparent;")
        heatmap_layout = QVBoxLayout(heatmap_container)
        heatmap_layout.setContentsMargins(0, 0, 0, 0)
        heatmap_layout.setSpacing(0)
        hm_hdr_w = QWidget()
        hm_hdr_w.setFixedHeight(SIZE_CONTROL_LG)
        hm_hdr_w.setStyleSheet("background: transparent;")
        hm_hdr_l = QHBoxLayout(hm_hdr_w)
        hm_hdr_l.setContentsMargins(SPACE_LG, 0, SPACE_LG, 0)
        hm_hdr_l.setSpacing(SPACE_10)
        hm_title_lbl = QLabel("DETECTION HEATMAP")
        hm_title_lbl.setStyleSheet(
            f"color: {_TEXT_MUTED}; font-size: {FONT_SIZE_MICRO}px; font-weight: {FONT_WEIGHT_HEAVY}; letter-spacing: {SPACE_XXXS}px;"
        )
        hm_hdr_l.addWidget(hm_title_lbl)
        hm_hdr_l.addStretch()
        reset_hm_btn = QPushButton("Reset Heatmap")
        reset_hm_btn.setFixedSize(SIZE_BTN_W_LG, SIZE_CONTROL_MD)
        reset_hm_btn.setStyleSheet(_SECONDARY_BTN)
        reset_hm_btn.clicked.connect(self._reset_heatmap)
        hm_hdr_l.addWidget(reset_hm_btn)
        _hm_sep = QWidget()
        _hm_sep.setFixedHeight(SPACE_XXXS)
        _hm_sep.setStyleSheet(f"background: {_BORDER_DIM};")
        heatmap_layout.addWidget(hm_hdr_w)
        heatmap_layout.addWidget(_hm_sep)
        heatmap_layout.addWidget(self._heatmap_widget, stretch=1)
        self._a_stack.addWidget(heatmap_container)

        top_violators_widget = QWidget()
        top_violators_widget.setStyleSheet("background: transparent;")
        tv_layout = QVBoxLayout(top_violators_widget)
        tv_layout.setContentsMargins(SPACE_LG, SPACE_MD, SPACE_LG, SPACE_MD)
        tv_layout.setSpacing(SPACE_SM)
        self._top_violators_area = QScrollArea()
        self._top_violators_area.setWidgetResizable(True)
        self._top_violators_area.setStyleSheet("border: none; background: transparent;")
        self._tv_container = QWidget()
        self._tv_container.setStyleSheet("background: transparent;")
        self._tv_layout = QVBoxLayout(self._tv_container)
        self._tv_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._tv_layout.setSpacing(SPACE_SM)
        self._top_violators_area.setWidget(self._tv_container)
        tv_layout.addWidget(self._top_violators_area)
        self._a_stack.addWidget(top_violators_widget)

        tab_card_vbox.addWidget(self._a_stack, stretch=1)
        layout.addWidget(tab_card, stretch=1)
        self._switch_analytics_tab(0)

    def _switch_analytics_tab(self, idx: int) -> None:
        self._a_stack.setCurrentIndex(idx)
        for i, btn in enumerate(self._a_tab_btns):
            btn.setStyleSheet(_A_TAB_BTN_ACTIVE if i == idx else _A_TAB_BTN)

    def on_activated(self):
        self._refresh_cameras()
        self._refresh()

    def _refresh_cameras(self):
        self._camera_combo.clear()
        self._camera_combo.addItem("All Cameras", None)
        cameras = db.get_cameras()
        for cam in cameras:
            self._camera_combo.addItem(cam["name"], cam["id"])

    def _refresh(self):
        date_from = self._date_from.date().toString("yyyy-MM-dd")
        date_to = self._date_to.date().toString("yyyy-MM-dd")
        camera_id = self._camera_combo.currentData()
        summary = stats_engine.get_summary(date_from, date_to, camera_id)
        total = summary.get("total_detections", 0) or 0
        violations = summary.get("violations", 0) or 0
        compliant = total - violations
        rate = (compliant / total * 100) if total > 0 else 100.0
        identified = 0
        self._stat_total.set_value(str(total))
        self._stat_violations.set_value(str(violations))
        self._stat_compliance.set_value(f"{rate:.0f}%")
        self._stat_faces.set_value(str(identified))
        self._compliance_chart.clear_data()
        trend = stats_engine.get_compliance_trend(date_from=date_from, date_to=date_to)
        if trend:
            x_idx = list(range(len(trend)))
            values = [float(t["rate"]) for t in trend]
            self._compliance_chart.set_line_data(x_idx, values, "Compliance %", color=_SUCCESS_DIM)
            self._compliance_chart.set_x_ticks([t["date"] for t in trend])

        self._violation_chart.clear_data()
        hourly = stats_engine.get_hourly_violation_chart(date_from, date_to)
        if hourly:
            x_idx = list(range(len(hourly)))
            counts = [float(h["count"]) for h in hourly]
            self._violation_chart.set_bar_data(x_idx, counts, color=_DANGER_DIM)
            self._violation_chart.set_x_ticks([f"{int(h['hour']):02d}:00" for h in hourly])

        self._camera_chart.clear_data()
        cam_data = stats_engine.get_camera_activity_data(date_from, date_to)
        if cam_data:
            cam_idx = list(range(len(cam_data)))
            cam_counts = [float(c["count"]) for c in cam_data]
            self._camera_chart.set_bar_data(cam_idx, cam_counts, color=_ACCENT)
            self._camera_chart.set_x_ticks([c["camera_name"] for c in cam_data])
        heatmap = self._heatmap_gen.generate()
        if heatmap is not None:
            self._heatmap_widget.set_heatmap(heatmap)
        while self._tv_layout.count():
            item = self._tv_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        top = stats_engine.get_person_violations(date_from, date_to, limit=10)
        for rank, person in enumerate(top, 1):
            card = QFrame()
            card.setStyleSheet(f"""
                QFrame {{
                    background-color: {_BG_RAISED};
                    border: {SPACE_XXXS}px solid {_BORDER_DIM};
                    border-radius: {RADIUS_MD}px;
                }}
            """)
            card.setFixedHeight(SIZE_ROW_SM)
            row = QHBoxLayout(card)
            row.setContentsMargins(SPACE_MD, SPACE_XS, SPACE_MD, SPACE_XS)
            rank_label = QLabel(f"#{rank}")
            rank_label.setStyleSheet(
                f"color: {_TEXT_SEC}; font-weight: {FONT_WEIGHT_BOLD}; font-size: {FONT_SIZE_SUBHEAD}px; background: transparent;"
            )
            rank_label.setFixedWidth(SIZE_ROW_MD)
            row.addWidget(rank_label)
            name_label = QLabel(person.get("identity", "Unknown"))
            name_label.setStyleSheet(f"font-weight: {FONT_WEIGHT_BOLD}; font-size: {FONT_SIZE_BODY}px; background: transparent;")
            row.addWidget(name_label, stretch=1)
            count_label = QLabel(f"{person.get('count', 0)} violations")
            count_label.setStyleSheet(f"color: {_DANGER_DIM}; font-weight: {FONT_WEIGHT_BOLD}; background: transparent;")
            row.addWidget(count_label)
            self._tv_layout.addWidget(card)

    def _reset_heatmap(self):
        self._heatmap_gen.reset()
        self._heatmap_widget.clear_heatmap()

    def _export_pdf(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export PDF Report", "report.pdf", "PDF Files (*.pdf)")
        if not path:
            return
        date_from = self._date_from.date().toString("yyyy-MM-dd")
        date_to = self._date_to.date().toString("yyyy-MM-dd")
        camera_id = self._camera_combo.currentData()
        try:
            report_generator.generate_report(path, date_from, date_to, camera_id)
            QMessageBox.information(self, "PDF Exported", f"Report saved to {path}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to export PDF:\n{e}")
