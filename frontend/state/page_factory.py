from __future__ import annotations

from typing import Callable

from frontend.pages.analytics import AnalyticsPage
from frontend.pages.camera_manager import CameraManagerPage
from frontend.pages.dashboard import DashboardPage
from frontend.pages.face_manager import FaceManagerPage
from frontend.pages.logs import LogsViewerPage
from frontend.pages.models import ModelsPage
from frontend.pages.notifications_manager import NotificationsConfigPage
from frontend.pages.playback import PlaybackPage
from frontend.pages.rules_manager import RulesManagerPage
from frontend.pages.settings import SettingsPage
from frontend.services.rules_service import RulesService


def create_page(key: str, rules_service: RulesService) -> object | None:
    factories = {
        "dashboard": DashboardPage,
        "detectors": CameraManagerPage,
        "rules": lambda: RulesManagerPage(rules_service=rules_service),
        "models": ModelsPage,
        "faces": FaceManagerPage,
        "analytics": AnalyticsPage,
        "logs": LogsViewerPage,
        "playback": PlaybackPage,
        "notifications": NotificationsConfigPage,
        "settings": SettingsPage,
    }
    factory = factories.get(key)
    return factory() if factory else None


def build_pages(preload_fn: Callable[[str], bool], rules_service: RulesService) -> dict[str, object | None]:
    def _preload(key: str, always: bool = False) -> bool:
        return always or preload_fn(key)

    return {
        "dashboard": DashboardPage() if _preload("dashboard", True) else None,
        "detectors": CameraManagerPage() if _preload("detectors") else None,
        "rules": RulesManagerPage(rules_service=rules_service) if _preload("rules") else None,
        "models": ModelsPage() if _preload("models") else None,
        "faces": FaceManagerPage() if _preload("faces") else None,
        "analytics": AnalyticsPage() if _preload("analytics") else None,
        "logs": LogsViewerPage() if _preload("logs") else None,
        "playback": PlaybackPage() if _preload("playback") else None,
        "notifications": NotificationsConfigPage() if _preload("notifications") else None,
        "settings": SettingsPage() if _preload("settings", True) else None,
    }
