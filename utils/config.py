import threading
import time

from backend.repository import db

_cache: dict = {}
_cache_lock = threading.Lock()
_CACHE_TTL = 3.0


def get(key, default=None):
    with _cache_lock:
        entry = _cache.get(key)
        if entry and (time.time() - entry["ts"]) < _CACHE_TTL:
            return entry["val"]
    val = db.get_setting(key, default)
    with _cache_lock:
        _cache[key] = {"val": val, "ts": time.time()}
    return val


def invalidate_cache():
    with _cache_lock:
        _cache.clear()


def theme():
    return get("theme", "dark")


def gpu_enabled():
    return get("gpu_enabled", True)


def snapshot_on_alarm():
    return get("snapshot_on_alarm", True)


def face_threshold():
    return get("face_similarity_threshold", 0.45)


def liveness_global():
    return get("liveness_check_global", False)


def smtp_config():
    return {
        "host": get("smtp_host", ""),
        "port": get("smtp_port", 587),
        "user": get("smtp_user", ""),
        "password": get("smtp_pass", ""),
        "tls": get("smtp_tls", True),
    }
