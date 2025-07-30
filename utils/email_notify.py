import smtplib
import os
from email.message import EmailMessage

def send_email_notification(subject, body):
    host = os.getenv("EMAIL_HOST")
    port = int(os.getenv("EMAIL_PORT", 587))
    user = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    to = os.getenv("EMAIL_TO")

    if not all([host, port, user, password, to]):
        print("❌ 缺少 Email 環境變數，無法發送通知")
        return

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = user
    msg["To"] = to
    msg.set_content(body)

    try:
        with smtplib.SMTP(host, port) as server:
            server.starttls()
            server.login(user, password)
            server.send_message(msg)
            print("✅ Email 通知已發送")
    except Exception as e:
        print(f"❌ 發送 Email 失敗：{e}")
