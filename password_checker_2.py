import sys

def check_password_strength(password: str) -> dict:
    score = 0
    feedback = []
    
    # ความยาว
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("ต้องยาวอย่างน้อย 8 ตัวอักษร")
    
    # ตัวพิมพ์ใหญ่
    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("ต้องมีตัวพิมพ์ใหญ่อย่างน้อย 1 ตัว")
    
    # ตัวพิมพ์เล็ก
    if any(c.islower() for c in password):
        score += 1
    else:
        feedback.append("ต้องมีตัวพิมพ์เล็กอย่างน้อย 1 ตัว")
    
    # ตัวเลข
    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("ต้องมีตัวเลขอย่างน้อย 1 ตัว")
    
    # อักขระพิเศษ (แก้ไขให้ถูกต้อง)
    special_chars = '!@#$%^&*(),.?":{}|<>'
    if any(c in special_chars for c in password):
        score += 1
    else:
        feedback.append("ควรมีอักขระพิเศษ")
    
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

# ส่วนหลัก
if __name__ == "__main__":
    password = sys.argv[1] if len(sys.argv) > 1 else ""
    
    if not password:
        print("ERROR: ไม่ได้รับรหัสผ่าน")
    else:
        result = check_password_strength(password)
        print(f"คะแนน: {result['score']}/5 | {result['level']}")
        print(f"รายละเอียด: {result['feedback']}")