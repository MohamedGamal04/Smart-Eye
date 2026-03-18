from __future__ import annotations

from typing import Iterable

from frontend.navigation import nav_keys


def build_trusted_user() -> dict:
    return {"email": "local", "is_admin": True, "allowed_tabs": nav_keys()}


def compute_access(account: dict | None) -> tuple[set[str], bool]:
    if not account:
        return set(), False
    allowed_tabs = set(account.get("allowed_tabs") or [])
    is_admin = bool(account.get("is_admin"))
    return allowed_tabs, is_admin


def pick_initial_tab(allowed_tabs: set[str], is_admin: bool, pages: Iterable[str]) -> str | None:
    page_keys = set(pages)
    for key in nav_keys():
        if key in page_keys and (is_admin or key in allowed_tabs):
            return key
    return next(iter(page_keys), None)
