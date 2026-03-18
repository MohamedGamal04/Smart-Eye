import threading
import time


class EscalationManager:
    def __init__(self):
        self._active_violations = {}
        self._lock = threading.Lock()

    def update(self, triggered_rules):
        now = time.time()
        current_ids = {r["id"] for r in triggered_rules}
        with self._lock:
            expired = [rid for rid in self._active_violations if rid not in current_ids]
            for rid in expired:
                del self._active_violations[rid]
            for rule in triggered_rules:
                rid = rule["id"]
                if rid not in self._active_violations:
                    self._active_violations[rid] = {
                        "start_time": now,
                        "rule": rule,
                    }

    def get_escalation_levels(self, triggered_rules):
        now = time.time()
        levels = {}
        from backend.repository import db

        for rule in triggered_rules:
            rid = rule["id"]
            with self._lock:
                active = self._active_violations.get(rid)
            if not active:
                levels[rid] = 0
                continue
            elapsed = now - active["start_time"]
            actions = db.get_alarm_actions(rule_id=rid)
            level = 0
            for action in sorted(actions, key=lambda a: a["escalation_level"]):
                if elapsed >= action.get("trigger_after_sec", 0):
                    level = action["escalation_level"]
            levels[rid] = level
        return levels

    def get_active_violations(self):
        now = time.time()
        result = []
        with self._lock:
            items = list(self._active_violations.items())
        for rid, info in items:
            level = self.get_escalation_levels([info["rule"]]).get(rid, 0)

            if level <= 0:
                continue
            result.append(
                {
                    "rule_id": rid,
                    "rule_name": info["rule"].get("name", ""),
                    "duration": now - info["start_time"],
                    "level": level,
                }
            )
        return result

    def clear(self):
        with self._lock:
            self._active_violations.clear()


_instance = None


def get_escalation_manager():
    global _instance
    if _instance is None:
        _instance = EscalationManager()
    return _instance
