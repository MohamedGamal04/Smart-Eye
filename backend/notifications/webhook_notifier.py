import logging
import requests

logger = logging.getLogger(__name__)


def send_webhook(url, payload, auth_token=None):
    if not url:
        return False
    headers = {"Content-Type": "application/json"}
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code < 400
    except Exception:
        logger.exception("Failed to send webhook to %s", url)
        return False


def test_webhook(url, auth_token=None):
    payload = {
        "source": "SmartEye",
        "type": "test",
        "message": "This is a test webhook from SmartEye.",
    }
    return send_webhook(url, payload, auth_token)
