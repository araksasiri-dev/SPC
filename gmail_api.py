# gmail_api.py
import os
import pickle
import base64
import mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime

# Gmail API Scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

class GmailAPI:
    def __init__(self, credentials_file="credentials.json", token_file="token.pickle"):
        """
        ตั้งค่า Gmail API
        credentials_file: ไฟล์ OAuth credentials ที่ดาวน์โหลดจาก Google Cloud Console
        token_file: ไฟล์เก็บ token (สร้างอัตโนมัติ)
        """
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Gmail API"""
        creds = None
        
        # โหลด token ที่เก็บไว้
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)
        
        # ถ้าไม่มี token หรือหมดอายุ
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    raise FileNotFoundError(
                        f"❌ ไม่พบไฟล์ {self.credentials_file}\n"
                        "กรุณาดาวน์โหลดจาก Google Cloud Console"
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # บันทึก token
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        print("✅ Gmail API Authentication สำเร็จ")
        return build('gmail', 'v1', credentials=creds)
    
    def send_email(self, recipient_email, subject, body, html_body=None, attachments=None):
        """
        ส่งอีเมล
        - recipient_email: อีเมลผู้รับ
        - subject: หัวข้ออีเมล
        - body: ข้อความ Plain Text
        - html_body: ข้อความ HTML (optional)
        - attachments: list of file paths (optional)
        """
        try:
            message = self._create_message(
                recipient_email, subject, body, html_body, attachments
            )
            
            # ส่งอีเมล
            result = self.service.users().messages().send(
                userId='me',
                body={'raw': message}
            ).execute()
            
            print(f"✅ ส่งอีเมลถึง {recipient_email} สำเร็จ")
            return True
            
        except Exception as e:
            print(f"❌ ส่งอีเมลล้มเหลว: {e}")
            return False
    
    def _create_message(self, recipient_email, subject, body, html_body=None, attachments=None):
        """สร้างข้อความอีเมลในรูปแบบ base64"""
        msg = MIMEMultipart('alternative')
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        # Plain Text
        text_part = MIMEText(body, 'plain', 'utf-8')
        msg.attach(text_part)
        
        # HTML (ถ้ามี)
        if html_body:
            html_part = MIMEText(html_body, 'html', 'utf-8')
            msg.attach(html_part)
        
        # แนบไฟล์ (ถ้ามี)
        if attachments:
            for file_path in attachments:
                if os.path.exists(file_path):
                    self._attach_file(msg, file_path)
        
        # แปลงเป็น base64
        raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        return raw_message
    
    def _attach_file(self, msg, file_path):
        """แนบไฟล์ไปกับอีเมล"""
        content_type, encoding = mimetypes.guess_type(file_path)
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        
        main_type, sub_type = content_type.split('/', 1)
        filename = os.path.basename(file_path)
        
        with open(file_path, 'rb') as f:
            if main_type == 'text':
                attachment = MIMEText(f.read().decode(), _subtype=sub_type)
            elif main_type == 'image':
                attachment = MIMEImage(f.read(), _subtype=sub_type)
            else:
                attachment = MIMEApplication(f.read(), _subtype=sub_type)
        
        attachment.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(attachment)
        print(f"📎 แนบไฟล์: {filename}")
    
    def send_registration_summary(self, recipient_email, summary, user_list):
        """ส่งสรุปผลการสมัครสมาชิก"""
        subject = f"📊 สรุปผลการสมัครสมาชิก - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        # Plain Text
        body = f"""
===============================
📊 สรุปผลการสมัครสมาชิก
===============================

✅ สมัครสำเร็จ: {summary['success']} ราย
❌ สมัครล้มเหลว: {summary['failed']} ราย
📋 รวมทั้งหมด: {summary['total']} ราย

===============================
รายละเอียดผู้ใช้
===============================
"""
        for user in user_list:
            status_emoji = "✅" if user.get("status") == "SUCCESS" else "❌"
            body += f"""
{status_emoji} {user.get('username')}
   📧 {user.get('email')}
   📱 {user.get('phone')}
   สถานะ: {user.get('status')}
"""
        body += "\n================================"
        
        # HTML Version
        html_body = self._create_html_summary(summary, user_list)
        
        return self.send_email(recipient_email, subject, body, html_body)
    
    def _create_html_summary(self, summary, user_list):
        """สร้าง HTML สรุปผล"""
        html = f"""
<html>
<head>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                  color: white; padding: 20px; border-radius: 10px; text-align: center; }}
        .summary {{ background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 20px 0; }}
        .success {{ color: #28a745; font-weight: bold; }}
        .failed {{ color: #dc3545; font-weight: bold; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th {{ background: #343a40; color: white; padding: 10px; text-align: left; }}
        td {{ padding: 10px; border-bottom: 1px solid #dee2e6; }}
        .row-success {{ background: #d4edda; }}
        .row-failed {{ background: #f8d7da; }}
        .footer {{ text-align: center; color: #6c757d; margin-top: 20px; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="header">
        <h2>📊 สรุปผลการสมัครสมาชิก</h2>
        <p>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="summary">
        <h3>📈 สถิติ</h3>
        <p>✅ <span class="success">สมัครสำเร็จ: {summary['success']} ราย</span></p>
        <p>❌ <span class="failed">สมัครล้มเหลว: {summary['failed']} ราย</span></p>
        <p>📋 รวมทั้งหมด: {summary['total']} ราย</p>
    </div>
    
    <h3>📋 รายละเอียดผู้ใช้</h3>
    <table>
        <tr>
            <th>สถานะ</th>
            <th>Username</th>
            <th>Email</th>
            <th>Phone</th>
        </tr>
"""
        for user in user_list:
            status = user.get("status")
            row_class = "row-success" if status == "SUCCESS" else "row-failed"
            status_emoji = "✅" if status == "SUCCESS" else "❌"
            html += f"""
        <tr class="{row_class}">
            <td>{status_emoji} {status}</td>
            <td>{user.get('username')}</td>
            <td>{user.get('email')}</td>
            <td>{user.get('phone')}</td>
        </tr>
"""
        
        html += """
    </table>
    <div class="footer">
        <p>ส่งจากระบบ RPA อัตโนมัติ</p>
    </div>
</body>
</html>
"""
        return html
    
    def send_error_alert(self, recipient_email, error_message):
        """ส่งแจ้งเตือนเมื่อเกิดข้อผิดพลาด"""
        subject = "⚠️ แจ้งเตือน: ระบบสมัครสมาชิกพบปัญหา"
        body = f"""
===============================
⚠️ แจ้งเตือนจากระบบ RPA
===============================

เกิดข้อผิดพลาดขณะทำงาน:

{error_message}

เวลา: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

===============================
กรุณาตรวจสอบระบบ
===============================
"""
        return self.send_email(recipient_email, subject, body)