# test_send_email.py
from gmail_oauth import GmailOAuth

gmail = GmailOAuth("credentials.json", "token.pickle")

result = gmail.send_email(
    recipient_email="ar0816250183@gmail.com",  # ส่งหาตัวเอง
    subject="✅ ทดสอบ Gmail API สำเร็จ!",
    body="""สวัสดี!

การทดสอบ Gmail API ทำงานสำเร็จแล้ว 🎉

ระบบพร้อมใช้งานกับ Robot Framework แล้วครับ.
"""
)

print("✅ ส่งสำเร็จ" if result else "❌ ส่งไม่สำเร็จ")