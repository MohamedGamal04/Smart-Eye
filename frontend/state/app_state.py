from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import QObject, Signal


@dataclass
class SessionUser:
    email: str
    is_admin: bool
    allowed_tabs: set[str]
    avatar_path: str | None = None


class AppState(QObject):
    theme_changed = Signal(str)
    session_changed = Signal(object)
    auth_required_changed = Signal(bool)

    def __init__(self, theme: str, auth_required: bool):
        super().__init__()
        self._theme = theme
        self._auth_required = auth_required
        self._session: SessionUser | None = None

    @property
    def theme(self) -> str:
        return self._theme

    def set_theme(self, value: str) -> None:
        if value == self._theme:
            return
        self._theme = value
        self.theme_changed.emit(value)

    @property
    def auth_required(self) -> bool:
        return self._auth_required

    def set_auth_required(self, value: bool) -> None:
        if value == self._auth_required:
            return
        self._auth_required = value
        self.auth_required_changed.emit(value)

    @property
    def session(self) -> SessionUser | None:
        return self._session

    def set_session(self, session: SessionUser | None) -> None:
        self._session = session
        self.session_changed.emit(session)
