import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from utils import config

logger = logging.getLogger(__name__)


def send_email_alert(to_address, subject, body, html=False):
    smtp = config.smtp_config()
    if not smtp["host"] or not to_address:
        return False
    msg = MIMEMultipart()
    msg["From"] = smtp["user"]
    msg["To"] = to_address
    msg["Subject"] = subject
    content_type = "html" if html else "plain"
    msg.attach(MIMEText(body, content_type))
    try:
        server = smtplib.SMTP(smtp["host"], int(smtp["port"]))
        server.ehlo()
        if smtp.get("tls", True):
            server.starttls()
            server.ehlo()
        if smtp["user"] and smtp["password"]:
            server.login(smtp["user"], smtp["password"])
        server.sendmail(smtp["user"], [to_address], msg.as_string())
        server.quit()
        return True
    except Exception:
        logger.exception("Failed to send email to %s", to_address)
        return False


def test_email(to_address):
    return send_email_alert(
        to_address,
        "SmartEye Test Notification",
        "This is a test email from SmartEye.\nIf you received this, email notifications are configured correctly.",
    )
