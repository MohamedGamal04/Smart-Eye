import json
import os
import time
import logging
from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtMultimedia import QSoundEffect

from backend.repository import db
from backend.notifications.email_notifier import send_email_alert
from backend.notifications.webhook_notifier import send_webhook
from utils import config
from utils.image_utils import save_snapshot


class AlarmHandler:
    def __init__(self, data_dir="data"):
        self._data_dir = data_dir
        self._log = logging.getLogger(__name__)

        self._alarm = QSoundEffect()

        self._alarm.setLoopCount(-2)
        self._alarm.setVolume(0.8)

        self._alarm_playing = False
        self._last_trigger_ts = 0.0
        self._alarm_grace_seconds = 0.35

        self._last_action_times = {}

        self._last_log_ts: dict = {}

    def handle_alarms(self, triggered_rules, escalation_levels, state, frame=None):
        now = time.time()
        should_play_alarm = False

        executed = []
        for rule in triggered_rules:
            if not rule.get("enabled", 1):
                continue
            rule_id = rule["id"]
            level = escalation_levels.get(rule_id, 0)
            if level <= 0:
                continue
            actions = db.get_alarm_actions(rule_id=rule_id, escalation_level=level)
            for action in actions:
                if action.get("action_type") == "sound":
                    should_play_alarm = True
                cooldown = action.get("cooldown_sec", 10)
                key = (rule_id, action["id"])
                last = self._last_action_times.get(key, 0)
                if now - last < cooldown:
                    continue
                self._execute_action(action, state, frame)
                self._last_action_times[key] = now
                executed.append(action)

            log_key = (rule_id, state.get("camera_id"), state.get("identity"))
            if now - self._last_log_ts.get(log_key, 0) < 30.0:
                continue
            self._last_log_ts[log_key] = now

            snapshot_path = ""
            if frame is not None and config.snapshot_on_alarm():
                snapshot_path = save_snapshot(
                    frame,
                    Path(self._data_dir) / "snapshots",
                )
            db.add_detection_log(
                camera_id=state.get("camera_id"),
                zone_id=state.get("zone_id"),
                identity=state.get("identity"),
                face_confidence=state.get("face_confidence", 0),
                detections=state.get("detections", {}),
                rules_triggered=[rule["name"]],
                alarm_level=level,
                snapshot_path=snapshot_path,
            )

        if should_play_alarm:
            self._last_trigger_ts = now
            if not self._alarm_playing:
                self._start_alarm()
        else:
            if self._alarm_playing and (now - self._last_trigger_ts > self._alarm_grace_seconds):
                self._stop_alarm()

        return executed

    def _execute_action(self, action, state, frame):
        atype = action["action_type"]
        avalue = action.get("action_value", "")

        if atype == "email":
            self._send_email(avalue, state)
        elif atype == "webhook":
            self._send_webhook(avalue, state)

        return False

    def _start_alarm(self):
        if self._alarm_playing:
            return
        sound_path = Path("frontend/assets/sounds/alarm_level_1.wav").resolve()
        if not sound_path.is_file():
            self._log.warning("Alarm sound not found: %s", sound_path)
            return

        if os.name == "nt":
            try:
                import winsound

                winsound.PlaySound(
                    str(sound_path),
                    winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP,
                )
                self._alarm_playing = True
                self._log.info("Alarm STARTED (winsound) -> %s", sound_path)
                return
            except Exception:
                self._log.exception("winsound start failed; falling back to QSoundEffect")

        if self._alarm is None:
            return
        self._alarm.setSource(QUrl.fromLocalFile(str(sound_path)))
        self._alarm.play()
        self._alarm_playing = True
        self._log.info("Alarm STARTED (qt) -> %s", sound_path)

    def _stop_alarm(self):
        if not self._alarm_playing:
            return
        if os.name == "nt":
            try:
                import winsound

                winsound.PlaySound(None, winsound.SND_PURGE)
            except Exception:
                self._log.exception("winsound stop failed")
        if self._alarm is None:
            self._alarm_playing = False
            return
        self._alarm.stop()
        self._alarm_playing = False
        self._log.info("Alarm STOPPED")

    def _send_email(self, address, state):
        try:
            subject = f"SmartEye Alert: {state.get('identity', 'Unknown')}"
            body = json.dumps(state.get("detections", {}), indent=2)
            send_email_alert(address, subject, body)
        except Exception:
            self._log.exception("Email send failed")

    def _send_webhook(self, url, state):
        try:
            payload = {
                "identity": state.get("identity"),
                "detections": state.get("detections", {}),
                "camera_id": state.get("camera_id"),
                "zone": state.get("zone"),
                "timestamp": time.time(),
            }
            send_webhook(url, payload)
        except Exception:
            self._log.exception("Webhook send failed")


_instance = None


def get_handler(data_dir="data"):
    global _instance
    if _instance is None:
        try:
            _instance = AlarmHandler(data_dir)
        except Exception:
            logging.getLogger(__name__).exception("Failed to initialize AlarmHandler; using silent fallback")
            _instance = AlarmHandler.__new__(AlarmHandler)
            _instance._data_dir = data_dir
            _instance._log = logging.getLogger(__name__)
            _instance._alarm = None
            _instance._alarm_playing = False
            _instance._last_trigger_ts = 0.0
            _instance._alarm_grace_seconds = 2.0
            _instance._last_action_times = {}
    return _instance


def stop_all_sounds():
    get_handler()._stop_alarm()
