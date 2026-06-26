# setup_gmail_api.py
"""
ขั้นตอนการตั้งค่า Gmail API:
1. ไปที่ https://console.cloud.google.com/
2. สร้าง Project ใหม่ (หรือเลือกที่มี)
3. เปิดใช้งาน Gmail API
4. สร้าง Credentials (OAuth 2.0 Client ID)
5. ดาวน์โหลด credentials.json
6. วางในโฟลเดอร์ C:\SPC
7. รันสคริปต์นี้
"""

import os
from gmail_api import GmailAPI

if __name__ == "__main__":
    # ถ้าไม่มี credentials.json ระบบจะให้ Login ผ่าน Browser
    gmail = GmailAPI("credentials.json", "token.pickle")
    
    # ทดสอบส่งอีเมล
    result = gmail.send_email(
        recipient_email="your-email@gmail.com",  # เปลี่ยนเป็นอีเมลของคุณ
        subject="Test from Gmail API",
        body="Hello! This is a test email from Gmail API."
    )
    
    print("✅ ทดสอบสำเร็จ" if result else "❌ ทดสอบล้มเหลว")