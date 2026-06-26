import sys

def check_password_strength(password):

    score = 0
    feedback = []

    # Length
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("ต้องยาวอย่างน้อย 8 ตัวอักษร")

    # Uppercase
    has_upper = False
    for c in password:
        if c.isupper():
            has_upper = True
            break

    if has_upper:
        score += 1
    else:
        feedback.append("ต้องมีตัวพิมพ์ใหญ่อย่างน้อย 1 ตัว")

    # Lowercase
    has_lower = False
    for c in password:
        if c.islower():
            has_lower = True
            break

    if has_lower:
        score += 1
    else:
        feedback.append("ต้องมีตัวพิมพ์เล็กอย่างน้อย 1 ตัว")

    # Number
    has_digit = False
    for c in password:
        if c.isdigit():
            has_digit = True
            break

    if has_digit:
        score += 1
    else:
        feedback.append("ต้องมีตัวเลขอย่างน้อย 1 ตัว")

    # Special Character
    has_special = False
    for c in password:
        if not c.isalnum():
            has_special = True
            break

    if has_special:
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


# Main
# ส่วนหลัก
if __name__ == "__main__":
    password = sys.argv[1] if len(sys.argv) > 1 else ""
    
    if not password:
        print("ERROR: ไม่ได้รับรหัสผ่าน")
    else:
        result = check_password_strength(password)
        print(f"คะแนน: {result['score']}/5 | {result['level']}")
        print(f"รายละเอียด: {result['feedback']}")