# test_oauth.py
from gmail_oauth import GmailOAuth

gmail = GmailOAuth("credentials.json", "token.pickle")

result = gmail.send_email(
    recipient_email="ar0816250183@gmail.com",  # เปลี่ยนเป็นอีเมลคุณ
    subject="📧 ทดสอบ OAuth 2.0",
    body="สวัสดี! การทดสอบ OAuth 2.0 ทำงานสำเร็จ 🎉"
)

print("✅ สำเร็จ" if result else "❌ ล้มเหลว")