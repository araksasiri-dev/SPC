import re
import hashlib
import os
from datetime import datetime

class PasswordChecker:
    """Python Library สำหรับตรวจสอบความแข็งแรงของรหัสผ่าน"""
    
    def __init__(self):
        self.score = 0
        self.feedback = []
    
    def check_password(self, password):
        self.score = 0
        self.feedback = []    
        
        # 🛡️ สเตปแรก: ใช้กลยุทธ์เตะตัดบท (Short-Circuit) ตรวจสอบรหัสยอดนิยมจากฟังก์ชันย่อย
        if self.is_common_password(password):
            return {
                "score": 0,
                "level": "0 รหัสผ่านยอดนิยม ห้ามใช้เด็ดขาด",
                "feedback": "⚠️ รหัสผ่านนี้เป็นรหัสผ่านที่นิยมใช้เดาง่ายมาก ห้ามใช้งานเด็ดขาด",
                "strength": 0,
                "is_common": True,
                "criteria": {"length": "❌ ตกเกณฑ์", "upper": "❌ ไม่มี", "lower": "✅ มี", "number": "❌ ไม่มี", "special": "❌ ไม่มี"}
            }            
        # ตรวจสอบเกณฑ์และบันทึกสถานะ Checklist รายข้อ
        length_status = "✅ ผ่าน" if len(password) >= 8 else "❌ ตกเกณฑ์"
        upper_status = "✅ มี" if re.search(r'[A-Z]', password) else "❌ ไม่มี"
        lower_status = "✅ มี" if re.search(r'[a-z]', password) else "❌ ไม่มี"
        number_status = "✅ มี" if re.search(r'\d', password) else "❌ ไม่มี"
        special_status = "✅ มี" if re.search(r'[^a-zA-Z0-9]', password) else "❌ ไม่มี"
        # -------------------------------------------------------------
        # 🟢 ถ้ารอดพ้นมาได้ ให้คำนวณเกณฑ์ความแข็งแรงตามปกติ
        # 1. ตรวจสอบความยาว
        if len(password) >= 8:
            self.score += 1
        else:
            self.feedback.append(f"ต้องยาวอย่างน้อย 8 ตัวอักษร (ปัจจุบัน {len(password)} ตัว)")
        
        # 2. ตรวจสอบตัวพิมพ์ใหญ่
        if re.search(r'[A-Z]', password):
            self.score += 1
        else:
            self.feedback.append("ต้องมีตัวพิมพ์ใหญ่อย่างน้อย 1 ตัว")
        
        # 3. ตรวจสอบตัวพิมพ์เล็ก
        if re.search(r'[a-z]', password):
            self.score += 1
        else:
            self.feedback.append("ต้องมีตัวพิมพ์เล็กอย่างน้อย 1 ตัว")
        
        # 4. ตรวจสอบตัวเลข
        if re.search(r'\d', password):
            self.score += 1
        else:
            self.feedback.append("ต้องมีตัวเลขอย่างน้อย 1 ตัว")
        
        # 5. ตรวจสอบอักขระพิเศษ
        if re.search(r'[^a-zA-Z0-9]', password):
            self.score += 1
        else:
            self.feedback.append("ควรมีอักขระพิเศษ เช่น !@#$%")
        
        # กำหนดระดับตามคะแนนจริงที่ได้
        if self.score >= 5:
            level = "🌟🌟🌟🌟🌟 แข็งแรงมาก"
        elif self.score >= 4:
            level = "🌟🌟🌟🌟 ดี"
        elif self.score >= 3:
            level = "🌟🌟🌟 พอใช้"
        else:
            level = "🌟 อ่อนแอ ควรปรับปรุง"
 
        return {
            "score": self.score,
            "level": level,
            "feedback": " | ".join(self.feedback) if self.feedback else "✅ ผ่านเกณฑ์ทั้งหมด!",
            "strength": self.get_strength_percentage(),
            "is_common": False,
            "criteria": {
                "length": length_status,
                "upper": upper_status,
                "lower": lower_status,
                "number": number_status,
                "special": special_status
            }
        }
    
    def get_strength_percentage(self):
        """คืนค่าเปอร์เซ็นต์ความแข็งแรง"""
        return int((self.score / 5) * 100)
    
    def is_common_password(self, password):
        """โหลดคลังข้อมูลจากไฟล์ Dictionary ภายนอกเพื่อทำ Dictionary Attack"""
        import os
        
        # ค้นหาพิกัดไฟล์ common_passwords.txt ที่อยู่ในโฟลเดอร์เดียวกัน
        current_dir = os.path.dirname(os.path.abspath(__file__))
        dict_file_path = os.path.join(current_dir, "common_passwords.txt")
        
        # ตรวจสอบก่อนว่าไฟล์ Dictionary มีอยู่จริงไหม ป้องกันระบบแครช
        if not os.path.exists(dict_file_path):
            print(f"⚠️ Warning: Dictionary file not found at {dict_file_path}")
            return False
            
        # เปิดอ่านไฟล์และดึงคำออกมาล้างช่องว่าง ทำเป็น Set เพื่อความเร็วสูงสุดในการค้นหา (O(1))
        with open(dict_file_path, 'r', encoding='utf-8') as f:
            common_set = {line.strip().lower() for line in f if line.strip()}
            
        # ตรวจสอบว่าคำที่ส่งเข้ามาสแกน อยู่ในคลังข้อมูลความเสี่ยงหรือไม่
        return password.strip().lower() in common_set
    
    def hash_password(self, password):
        """แปลงรหัสผ่านเป็น SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def generate_strong_password(self, length=12):
        """สร้างรหัสผ่านที่แข็งแรงอัตโนมัติ"""
        import random
        import string
        
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(random.choice(chars) for _ in range(length))
        
        while not (re.search(r'[A-Z]', password) and 
                   re.search(r'[a-z]', password) and 
                   re.search(r'\d', password) and 
                   re.search(r'[^a-zA-Z0-9]', password)):
            password = ''.join(random.choice(chars) for _ in range(length))
        
        return password
    
    def read_passwords_from_file(self, file_path):
        if not os.path.exists(file_path):
            return []
        with open(file_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    
# 🟢 ฟังก์ชันใหม่: ทำหน้าที่สร้างและบันทึกรายงานสรุปผลการเทสลงไฟล์ภายนอก
    def export_report_to_file(self, file_prefix, report_data_list):
        """เขียนรายงานผลลัพธ์แยกทีละรายการลงไฟล์ Text ภายนอกพร้อม Timestamp"""
        # สร้างตัวแปรเวลาปัจจุบันต่อท้ายชื่อไฟล์
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        actual_filename = f"{file_prefix}_{timestamp}.txt"
        
        with open(actual_filename, 'w', encoding='utf-8') as f:
            f.write("========================================================================\n")
            f.write("                DETAILED PASSWORD SECURITY AUDIT REPORT                \n")
            f.write(f"                Generated At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("========================================================================\n\n")
            
            # วนลูปนำ List รายการที่ส่งมาจาก Robot Framework มาเขียนลงไฟล์ทีละบรรทัด
            for record in report_data_list:
                f.write(f"{record}\n")
                
            f.write("\n========================================================================\n")
            f.write("Status: Complete Audit Session Successfully.\n")
            
        print(f"Robot successfully exported: {actual_filename}")

    def export_report_to_pdf(self, file_prefix, password_results_list):
        """รับอาร์กิวเมนต์ผลลัพธ์ดิกชันนารีมาจัดหน้ากระดาษพ่นเป็น PDF คลีน ๆ พร้อมระบุตำแหน่งที่แน่นอน"""
        from datetime import datetime
        import os
        from weasyprint import HTML

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 🟢 ป้องกันไฟล์หลงทาง: บังคับให้สร้างไฟล์ไว้ในโฟลเดอร์เดียวกับสคริปต์ Python ตัวนี้ทันที
        current_dir = os.path.dirname(os.path.abspath(__file__))
        pdf_filename = f"{file_prefix}_{timestamp}.pdf"
        full_output_path = os.path.join(current_dir, pdf_filename)
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        total = len(password_results_list)
        critical = sum(1 for p in password_results_list if p["is_common"])
        weak = sum(1 for p in password_results_list if not p["is_common"] and p["score"] < 3)
        good = sum(1 for p in password_results_list if not p["is_common"] and (p["score"] == 3 or p["score"] == 4))
        excellent = sum(1 for p in password_results_list if p["score"] == 5)

        # 📄 ปรับดีไซน์ CSS ขยายช่องคอลุมน์ และแก้ปัญหาภาษาไทยทะลุขอบตาราง
        # 📄 ปรับดีไซน์ CSS ห้ามฉีกแถวตารางเมื่อขึ้นหน้าใหม่ (Fix Page-Break Bug)
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                @page {{
                    size: A4; margin: 15mm 15mm;
                    @bottom-right {{ content: "Page " counter(page) " of " counter(pages); font-family: 'Tahoma', 'Segoe UI', sans-serif; font-size: 8pt; color: #718096; }}
                    @bottom-left {{ content: "PASSWORD SECURITY AUDIT REPORT • CONFIDENTIAL"; font-family: 'Tahoma', 'Segoe UI', sans-serif; font-size: 8pt; color: #a0aec0; font-weight: bold; }}
                }}
                body {{ font-family: 'Tahoma', 'Segoe UI', Arial, sans-serif; color: #2d3748; line-height: 1.5; margin: 0; padding: 0; }}
                .header {{ border-bottom: 3px solid #2b6cb0; padding-bottom: 12px; margin-bottom: 15px; }}
                .title {{ font-size: 20pt; color: #2b6cb0; font-weight: bold; margin: 0; }}
                .subtitle {{ font-size: 10pt; color: #4a5568; margin: 4px 0 0 0; }}
                .meta-container {{ width: 100%; margin-bottom: 15px; border-collapse: collapse; }}
                .meta-container td {{ padding: 4px 0; font-size: 9.5pt; }}
                .meta-label {{ font-weight: bold; color: #4a5568; width: 15%; }}
                
                /* EXECUTIVE DASHBOARD DESIGN */
                .dashboard {{ width: 100%; margin-bottom: 20px; border-collapse: separate; border-spacing: 8px 0; }}
                .stat-card {{ padding: 12px; text-align: center; border-radius: 6px; background-color: #f7fafc; border: 1px solid #e2e8f0; }}
                .stat-val {{ font-size: 16pt; font-weight: bold; margin: 0; }}
                .stat-lbl {{ font-size: 8.5pt; color: #718096; margin: 2px 0 0 0; }}
                .section-title {{ font-size: 12pt; color: #2c5282; border-left: 4px solid #2b6cb0; padding-left: 8px; margin-top: 20px; margin-bottom: 12px; font-weight: bold; }}
                
                /* 🟢 MAIN FIX 1: บังคับให้ส่วนสรุปผู้บริหารและแดชบอร์ดอยู่หน้าแรกเสมอ และห้ามตารางดีดขึ้นมาเบียด */
                .summary-page {{
                    page-break-after: always; /* 🟢 รันสรุปแดชบอร์ดเสร็จแล้ว ให้ตัดขึ้นหน้าใหม่เพื่อขึ้นตารางทันที */
                    break-after: always;
                }}
                
                /* AUDIT TABLE LAYOUT */
                .audit-table {{ 
                    width: 100%; 
                    border-collapse: collapse; 
                    margin-bottom: 20px; 
                }}
                
                /* 🟢 MAIN FIX 2: ล็อกหัวตารางให้แสดงซ้ำทุกครั้งที่ขึ้นหน้าใหม่ (ป้องกันตารางไม่มีหัว) */
                .audit-table thead {{
                    display: table-header-group;
                }}
                
                .audit-table th {{ background-color: #2b6cb0; color: white; font-weight: bold; padding: 10px 8px; font-size: 9.5pt; text-align: left; }}
                
                .audit-table td {{ 
                    padding: 12px 8px; 
                    border-bottom: 1px solid #e2e8f0; 
                    font-size: 9pt; 
                    vertical-align: top; 
                    word-break: break-all;
                    white-space: normal;
                }}
                
                /* 🟢 MAIN FIX 3: คลายสิทธิ์ล็อกตารางให้ยืดหยุ่นขึ้น เพื่อให้เนื้อหาไหลข้ามหน้าได้โดยไม่ดีดตัวกลับ */
                .audit-table tr {{ 
                    page-break-inside: avoid !important;
                    break-inside: avoid !important;
                }} 
                .audit-table tr:nth-child(even) {{ background-color: #f8fafc; }}
                
                /* CRITERIA BOX DESIGN */
                .criteria-box {{ 
                    font-size: 8pt; 
                    color: #4a5568; 
                    background-color: #ffffff; 
                    padding: 6px; 
                    border-radius: 4px; 
                    border: 1px solid #edf2f7;
                }}
                .criteria-item {{
                    display: inline-block;
                    width: 46%;
                    margin-bottom: 3px;
                    margin-right: 4%;
                }}
                
                .badge {{ display: inline-block; padding: 3px 6px; border-radius: 4px; font-weight: bold; font-size: 7.5pt; text-align: center; width: 90%; }}
                .status-critical {{ background-color: #fff5f5; color: #c53030; border: 1px solid #feb2b2; }}
                .status-weak {{ background-color: #fffaf0; color: #dd6b20; border: 1px solid #fbd38d; }}
                .status-good {{ background-color: #f7fafc; color: #4a5568; border: 1px solid #cbd5e0; }}
                .status-excellent {{ background-color: #f0fff4; color: #38a169; border: 1px solid #9ae6b4; }}
                
                .remediation-text {{
                    color: #4a5568; 
                    font-size: 8.5pt; 
                    line-height: 1.5; 
                    word-break: break-all;
                    white-space: normal;
                    display: block;
                    padding-bottom: 5px;
                }}
            </style>
        </head>
        <body>
            <div class="summary-page">
                <div class="header">
                    <h1 class="title">Password Security Audit Report</h1>
                    <p class="subtitle">Automated Password Strength Analysis & Evaluation Report</p>
                </div>
                <table class="meta-container">
                    <tr><td class="meta-label">Execution Time:</td><td class="meta-value">{current_time}</td><td class="meta-label">Classification:</td><td class="meta-value" style="color:#c53030; font-weight:bold;">CONFIDENTIAL</td></tr>
                </table>
                <div class="section-title">📊 Risk Assessment Summary (Executive Dashboard)</div>
                <table class="dashboard">
                    <tr>
                        <td><div class="stat-card"><div class="stat-val">{total}</div><div class="stat-lbl">Total</div></div></td>
                        <td><div class="stat-card" style="background-color:#fff5f5;"><div class="stat-val" style="color:#e53e3e;">{critical}</div><div class="stat-lbl">Critical</div></div></td>
                        <td><div class="stat-card" style="background-color:#fffaf0;"><div class="stat-val" style="color:#ed8936;">{weak}</div><div class="stat-lbl">Weak</div></div></td>
                        <td><div class="stat-card" style="background-color:#f7fafc;"><div class="stat-val" style="color:#4a5568;">{good}</div><div class="stat-lbl">Good</div></div></td>
                        <td><div class="stat-card" style="background-color:#f0fff4;"><div class="stat-val" style="color:#38a169;">{excellent}</div><div class="stat-lbl">Excellent</div></div></td>
                    </tr>
                </table>
            </div>

            <div class="section-title">🔍 Detailed Password List Audit</div>
            <table class="audit-table">
                <thead>
                    <tr>
                        <th style="width: 18%;">Password</th>
                        <th style="width: 32%;">Criteria Checklist</th>
                        <th style="width: 10%; text-align:center;">Score</th>
                        <th style="width: 13%; text-align:center;">Status</th>
                        <th style="width: 27%;">Remediation & Feedback</th>
                    </tr>
                </thead>
                <tbody>
        """
        for item in password_results_list:
            status_class = "status-critical" if item["is_common"] else ("status-excellent" if item["score"] == 5 else ("status-good" if item["score"] >= 3 else "status-weak"))
            status_text = "CRITICAL" if item["is_common"] else item["level"].upper()
            
            html_content += f"""
                    <tr>
                        <td style="font-family:monospace; font-weight:bold; color:#2d3748; padding-top:14px; word-break:break-all;">{item['password']}</td>
                        <td>
                            <div class="criteria-box">
                                <div class="criteria-item">Length: {item['criteria']['length']}</div>
                                <div class="criteria-item">Upper: {item['criteria']['upper']}</div>
                                <div class="criteria-item">Lower: {item['criteria']['lower']}</div>
                                <div class="criteria-item">Number: {item['criteria']['number']}</div>
                                <div class="criteria-item" style="width:100%;">Special: {item['criteria']['special']}</div>
                            </div>
                        </td>
                        <td style="font-weight:bold; font-size:11pt; text-align:center; color:#2b6cb0; padding-top:14px;">{item['score']}/5</td>
                        <td style="text-align:center; padding-top:14px;"><span class="badge {status_class}">{status_text}</span></td>
                        <td style="padding-top:14px;"><span class="remediation-text">{item['feedback']}</span></td>
                    </tr>
            """
        html_content += "</tbody></table></body></html>"
        
        HTML(string=html_content).write_pdf(full_output_path)
        print(f"--- PDF Generated Successfully at: {full_output_path} ---")