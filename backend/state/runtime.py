
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class RuntimeState:

    camera_manager: Any | None = None
    pipeline_service: Any | None = None
    notifier: Any | None = None
    extras: dict[str, Any] = field(default_factory=dict)

    def set(self, name: str, value: Any) -> None:
        if hasattr(self, name):
            setattr(self, name, value)
        else:
            self.extras[name] = value

    def get(self, name: str, default: Any = None) -> Any:
        if hasattr(self, name):
            return getattr(self, name)
        return self.extras.get(name, default)

    def clear(self) -> None:
        self.camera_manager = None
        self.pipeline_service = None
        self.notifier = None
        self.extras.clear()


_state = RuntimeState()


def set_runtime(name: str, value: Any) -> None:
    _state.set(name, value)


def get_runtime(name: str, default: Any = None) -> Any:
    return _state.get(name, default)


def get_state() -> RuntimeState:
    return _state


def clear_runtime() -> None:
    _state.clear()
