# gmail_oauth.py (แก้ไขส่วน _create_html_summary และ send_registration_summary)
import os
import pickle
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

SECRETS_DIR = r"C:\secrets"
CREDENTIALS_FILE = os.path.join(SECRETS_DIR, "credentials.json")
TOKEN_FILE = os.path.join(SECRETS_DIR, "token.pickle")

class GmailOAuth:
    def __init__(self, credentials_file=None, token_file=None):
        if credentials_file and os.path.exists(credentials_file):
            self.credentials_file = credentials_file
        else:
            self.credentials_file = CREDENTIALS_FILE

        if token_file and os.path.exists(token_file):
            self.token_file = token_file
        else:
            self.token_file = TOKEN_FILE
        
        if not os.path.exists(self.credentials_file):
            raise FileNotFoundError(
                f"❌ ไม่พบไฟล์ credentials.json ที่ {self.credentials_file}\n"
                "กรุณาวาง credentials.json ไว้ใน C:\\secrets\\"
            )
        
        self.service = self._authenticate()
    
    def _authenticate(self):
        creds = None
                
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        print(f"✅ Gmail API (OAuth) พร้อมใช้งาน")
        print(f"   📁 credentials: {self.credentials_file}")
        print(f"   📁 token: {self.token_file}")
        return build('gmail', 'v1', credentials=creds)
    
    def send_email(self, recipient_email, subject, body, html_body=None):
        try:
            msg = MIMEMultipart('alternative')
            msg['To'] = recipient_email
            msg['Subject'] = subject
            
            text_part = MIMEText(body, 'plain', 'utf-8')
            msg.attach(text_part)
            
            if html_body:
                html_part = MIMEText(html_body, 'html', 'utf-8')
                msg.attach(html_part)
            
            raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode()
            
            self.service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            
            print(f"✅ ส่งอีเมลถึง {recipient_email} สำเร็จ")
            return True
            
        except Exception as e:
            print(f"❌ ส่งอีเมลล้มเหลว: {e}")
            return False
    
    def send_registration_summary(self, recipient_email, summary, user_list, duplicate_report="", fail_report=""):
        subject = f"📊 สรุปผลการสมัครสมาชิก - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        total_all = summary.get("total", 0)
        total_success = summary.get("success", 0)
        total_failed = summary.get("failed", 0)
        total_skipped = summary.get("skipped", 0)
        
        dup_email_count = summary.get("duplicate_email", 0)
        dup_phone_count = summary.get("duplicate_phone", 0)
        dup_both_count = summary.get("duplicate_both", 0)
        fail_email_count = summary.get("fail_email", 0)
        fail_phone_count = summary.get("fail_phone", 0)
        fail_both_count = summary.get("fail_both", 0)
        
        if total_all == 0:
            total_all = total_success + total_failed + total_skipped
        
        body = f"""
{'='*50}
📊 สรุปผลการสมัครสมาชิก
{'='*50}

📋 ข้อมูลทั้งหมด: {total_all} ราย
   ✅ สมัครสำเร็จ: {total_success} ราย
   ❌ สมัครล้มเหลว: {total_failed} ราย
      - 📧 อีเมลล้มเหลว: {fail_email_count} ราย
      - 📱 เบอร์โทรล้มเหลว: {fail_phone_count} ราย
      - 📧📱 อีเมลและเบอร์โทรล้มเหลว: {fail_both_count} ราย
   ⏭️ ถูกข้าม (ซ้ำ): {total_skipped} ราย
      - 📧 อีเมลซ้ำ: {dup_email_count} ราย
      - 📱 เบอร์โทรซ้ำ: {dup_phone_count} ราย
      - 📧📱 อีเมลและเบอร์โทรซ้ำ: {dup_both_count} ราย

{duplicate_report if duplicate_report else '✅ ไม่พบข้อมูลซ้ำ'}
{fail_report if fail_report else '✅ ไม่พบข้อมูลล้มเหลว'}

{'='*50}
📋 รายละเอียดผู้ใช้ที่สมัครสำเร็จ
{'='*50}
"""
        success_count = 0
        for idx, user in enumerate(user_list, start=1):
            if user.get("status") == "SUCCESS":
                success_count += 1
                body += f"""
{success_count}. ✅ {user.get('username')}
   📧 {user.get('email')}
   📱 {user.get('phone')}
"""
        
        body += f"""
{'='*50}
✅ สรุป: สำเร็จ {total_success} ราย | ล้มเหลว {total_failed} ราย | ข้าม {total_skipped} ราย | รวม {total_all} ราย
{'='*50}
"""
        
        html_body = self._create_html_summary(summary, user_list, duplicate_report, fail_report)
        
        return self.send_email(recipient_email, subject, body, html_body)

    def _create_html_summary(self, summary, user_list, duplicate_report="", fail_report=""):
        total_all = summary.get("total", 0)
        total_success = summary.get("success", 0)
        total_failed = summary.get("failed", 0)
        total_skipped = summary.get("skipped", 0)
        dup_email_count = summary.get("duplicate_email", 0)
        dup_phone_count = summary.get("duplicate_phone", 0)
        dup_both_count = summary.get("duplicate_both", 0)
        fail_email_count = summary.get("fail_email", 0)
        fail_phone_count = summary.get("fail_phone", 0)
        fail_both_count = summary.get("fail_both", 0)
        
        dup_display = ""
        if duplicate_report and "ไม่พบข้อมูลซ้ำ" not in duplicate_report:
            dup_display = duplicate_report.replace("\n", "<br>")
        
        fail_display = ""
        if fail_report and "ไม่พบข้อมูลล้มเหลว" not in fail_report:
            fail_display = fail_report.replace("\n", "<br>")
        
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
        .skipped {{ color: #856404; font-weight: bold; }}
        .duplicate {{ background: #fff3cd; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 5px solid #ffc107; }}
        .fail {{ background: #f8d7da; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 5px solid #dc3545; }}
        .dup-list {{ font-family: 'Consolas', monospace; background: #f8f9fa; padding: 10px 15px; border-radius: 5px; white-space: pre-wrap; line-height: 1.8; }}
        .fail-list {{ font-family: 'Consolas', monospace; background: #f8f9fa; padding: 10px 15px; border-radius: 5px; white-space: pre-wrap; line-height: 1.8; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th {{ background: #343a40; color: white; padding: 10px; text-align: left; }}
        td {{ padding: 10px; border-bottom: 1px solid #dee2e6; }}
        .row-success {{ background: #d4edda; }}
        .footer {{ text-align: center; color: #6c757d; margin-top: 20px; font-size: 12px; }}
        .total {{ font-weight: bold; font-size: 16px; }}
    </style>
</head>
<body>
    <div class="header">
        <h2>📊 สรุปผลการสมัครสมาชิก</h2>
        <p>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="summary">
        <h3>📈 สถิติ</h3>
        <p class="total">📋 ข้อมูลทั้งหมด: {total_all} ราย</p>
        <p>✅ <span class="success">สมัครสำเร็จ: {total_success} ราย</span></p>
        <p>❌ <span class="failed">สมัครล้มเหลว: {fail_email_count + fail_phone_count + fail_both_count} ราย</span></p>
        <p>⏭️ <span class="skipped">ถูกข้าม (ซ้ำ): {dup_email_count + dup_phone_count + dup_both_count} ราย</span></p>
        <ul style="margin-left: 20px;">
            <li>📧 อีเมลซ้ำ: <strong>{dup_email_count}</strong> ราย</li>
            <li>📱 เบอร์โทรซ้ำ: <strong>{dup_phone_count}</strong> ราย</li>
            <li>📧📱 อีเมลและเบอร์โทรซ้ำ: <strong>{dup_both_count}</strong> ราย</li>
            <li style="color: #856404;">-----------------------------------------------</li>
            <li>📧 อีเมลล้มเหลว: <strong>{fail_email_count}</strong> ราย</li>
            <li>📱 เบอร์โทรล้มเหลว: <strong>{fail_phone_count}</strong> ราย</li>
            <li>📧📱 อีเมลและเบอร์โทรล้มเหลว: <strong>{fail_both_count}</strong> ราย</li>
        </ul>
    </div>
"""
        
        if dup_display:
            html += f"""
    <div class="duplicate">
        <h3>⚠️ รายงานข้อมูลซ้ำ</h3>
        <div class="dup-list">
{dup_display}
        </div>
    </div>
"""
        
        if fail_display:
            html += f"""
    <div class="fail">
        <h3>❌ รายงานข้อมูลล้มเหลว</h3>
        <div class="fail-list">
{fail_display}
        </div>
    </div>
"""
        
        html += """
    <h3>📋 รายละเอียดผู้ใช้ที่สมัครสำเร็จ</h3>
    <table>
        <tr>
            <th>#</th>
            <th>Username</th>
            <th>Email</th>
            <th>Phone</th>
        </tr>
"""
        success_count = 0
        for user in user_list:
            if user.get("status") == "SUCCESS":
                success_count += 1
                html += f"""
        <tr class="row-success">
            <td>{success_count}</td>
            <td>{user.get('username')}</td>
            <td>{user.get('email')}</td>
            <td>{user.get('phone')}</td>
        </tr>
"""
        
        html += f"""
    </table>
    <div class="footer">
        <p>✅ สรุป: สำเร็จ {total_success} ราย | ล้มเหลว {total_failed} ราย | ข้าม {total_skipped} ราย | รวม {total_all} ราย</p>
        <p>🤖 ส่งจากระบบ RPA อัตโนมัติ</p>
    </div>
</body>
</html>
"""
        return html
    
    def send_error_alert(self, recipient_email, error_message):
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