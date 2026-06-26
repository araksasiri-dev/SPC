# email_notify.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class EmailNotifier:
    def __init__(self, smtp_server, smtp_port, sender_email, sender_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
    
    def send_email(self, recipient_email, subject, body, html_body=None):
        """ส่งอีเมลแบบ Plain Text หรือ HTML"""
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.sender_email
            msg["To"] = recipient_email
            
            text_part = MIMEText(body, "plain", "utf-8")
            msg.attach(text_part)
            
            if html_body:
                html_part = MIMEText(html_body, "html", "utf-8")
                msg.attach(html_part)
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient_email, msg.as_string())
            
            print(f"✅ ส่งอีเมลถึง {recipient_email} สำเร็จ")
            return True
            
        except Exception as e:
            print(f"❌ ส่งอีเมลล้มเหลว: {e}")
            return False
    
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
        html_body = f"""
<html>
<head>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; }}
        .summary {{ background: #f0f8ff; padding: 15px; border-radius: 8px; }}
        .success {{ color: green; }}
        .failed {{ color: red; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background: #2c3e50; color: white; }}
        .row-success {{ background: #e8f5e9; }}
        .row-failed {{ background: #ffebee; }}
    </style>
</head>
<body>
    <h2>📊 สรุปผลการสมัครสมาชิก</h2>
    <div class="summary">
        <p>✅ <span class="success">สมัครสำเร็จ: {summary['success']} ราย</span></p>
        <p>❌ <span class="failed">สมัครล้มเหลว: {summary['failed']} ราย</span></p>
        <p>📋 รวมทั้งหมด: {summary['total']} ราย</p>
    </div>
    <h3>📋 รายละเอียดผู้ใช้</h3>
    <table>
        <tr><th>สถานะ</th><th>Username</th><th>Email</th><th>Phone</th></tr>
"""
        for user in user_list:
            status = user.get("status")
            row_class = "row-success" if status == "SUCCESS" else "row-failed"
            status_emoji = "✅" if status == "SUCCESS" else "❌"
            html_body += f"""
        <tr class="{row_class}">
            <td>{status_emoji} {status}</td>
            <td>{user.get('username')}</td>
            <td>{user.get('email')}</td>
            <td>{user.get('phone')}</td>
        </tr>
"""
        
        html_body += """
    </table>
    <p><i>ส่งจากระบบ RPA อัตโนมัติ</i></p>
</body>
</html>
"""
        
        return self.send_email(recipient_email, subject, body, html_body)
    
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