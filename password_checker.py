import sys
import re

def check_password_strength(password: str) -> dict:
    """
    ตรวจสอบความแข็งแรงของรหัสผ่าน
    คืนค่า dict พร้อมคะแนนและคำแนะนำ
    """
    score = 0
    feedback = []
    
    # เงื่อนไขการตรวจสอบ
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ ต้องยาวอย่างน้อย 8 ตัวอักษร")
    
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("❌ ต้องมีตัวพิมพ์ใหญ่อย่างน้อย 1 ตัว")
    
    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("❌ ต้องมีตัวพิมพ์เล็กอย่างน้อย 1 ตัว")
    
    if re.search(r'\d', password):
        score += 1
    else:
        feedback.append("❌ ต้องมีตัวเลขอย่างน้อย 1 ตัว")
    
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
    else:
        feedback.append("❌ ควรมีอักขระพิเศษ (!@#$% ฯลฯ)")
    
    # ประเมินระดับ
    if score >= 5:
        level = "🌟🌟🌟🌟🌟 แข็งแรงมาก"
    elif score >= 4:
        level = "🌟🌟🌟🌟 ดี"
    elif score >= 3:
        level = "🌟🌟🌟 พอใช้"
    else:
        level = "🌟 อ่อนแอ ควรปรับปรุง"
    
    return {
        "score": score,
        "level": level,
        "feedback": " | ".join(feedback) if feedback else "✅ ผ่านเกณฑ์ทั้งหมด!"
    }

# ส่วนหลัก: อ่านค่าจาก Power Automate
if __name__ == "__main__":
    # รับ password จาก argument (ส่งผ่าน Power Automate)
    password = sys.argv[1] if len(sys.argv) > 1 else ""
    
    if not password:
        print("ERROR: ไม่ได้รับรหัสผ่าน")
    else:
        result = check_password_strength(password)
        # ส่งผลลัพธ์กลับ Power Automate ผ่าน print()
        print(f"คะแนน: {result['score']}/5 | {result['level']}")
        print(f"รายละเอียด: {result['feedback']}")