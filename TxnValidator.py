import os

class TxnValidator:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def validate_transaction_line(self, line: str) -> dict:
        """
        วิเคราะห์และตรวจสอบข้อมูลธุรกรรมรายบรรทัดตาม Business Rules
        """
        # ล้างช่องว่างหัวท้ายบรรทัด
        clean_line = line.strip()
        if not clean_line:
            raise ValueError("EMPTY_LINE")

        # แยกคอลัมน์ด้วยเครื่องหมาย Pipe (|)
        parts = clean_line.split('|')
        
        # 🟢 Rule 1: Format Validation (ถ้าคอลัมน์ไม่ครบ 4 ช่อง ให้ดีด Error ทันที)
        if len(parts) != 4:
            raise ValueError("INVALID_FORMAT")

        txn_id = parts[0].strip()
        user_name = parts[1].strip()
        status = parts[3].strip()

        # แปลงค่าจำนวนเงินเป็น Float เพื่อคำนวณทางคณิตศาสตร์
        try:
            amount = float(parts[2].strip())
        except ValueError:
            raise ValueError("INVALID_AMOUNT_TYPE")

        # กำหนดสถานะเริ่มต้นของผลลัพธ์
        risk_level = "NORMAL"
        vip_tag = "STANDARD"

        # 🟢 Rule 2: Amount Validation (ห้ามติดลบ และ ตรวจจับวงเงินสูง)
        if amount < 0:
            risk_level = "REJECTED_NEGATIVE_AMOUNT"
        elif amount > 500000.00:
            risk_level = "HIGH_RISK"

        # 🟢 Rule 3: Data Cleaning & VIP Identification
        if user_name.lower() == "annop raksasiri":
            vip_tag = "VIP_TRANSACTION"

        # ส่งค่ากลับไปให้ Robot Framework ในรูปแบบ Dictionary
        return {
            "txn_id": txn_id,
            "user_name": user_name,
            "amount": amount,
            "status": status,
            "risk_level": risk_level,
            "vip_tag": vip_tag
        }