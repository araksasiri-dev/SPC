def check_password_strength(password):
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("At least 8 chars")

    has_upper = False
    for c in password:
        if c.isupper():
            has_upper = True
            break
    if has_upper:
        score += 1
    else:
        feedback.append("Need 1 uppercase")

    has_lower = False
    for c in password:
        if c.islower():
            has_lower = True
            break
    if has_lower:
        score += 1
    else:
        feedback.append("Need 1 lowercase")

    has_digit = False
    for c in password:
        if c.isdigit():
            has_digit = True
            break
    if has_digit:
        score += 1
    else:
        feedback.append("Need 1 number")

    has_special = False
    for c in password:
        if not c.isalnum():
            has_special = True
            break
    if has_special:
        score += 1
    else:
        feedback.append("Need special char")

    if score >= 5:
        level = "Very Strong"
    elif score >= 4:
        level = "Strong"
    elif score >= 3:
        level = "Fair"
    else:
        level = "Weak"

    return score, level, " | ".join(feedback) if feedback else "Passed all criteria!"

# --- ลบ if __name__ == "__main__": ออก เพื่อบังคับให้ PAD รันทำงานทันที ---
try:
    password = '''%UserInput%'''.strip()
    
    if not password :
        print("ERROR: No password received")
    else:
        s, l, f = check_password_strength(password)
       # print("SCORE:{}|LEVEL:{}|FEEDBACK:{}".format(s, l, f))
        #result = check_password_strength(password)
        print("SCORE: {}/5".format(s))
        print("LEVEL: {}".format(l))
        print("FEEDBACK: {}".format(f))  
except Exception as e:
    # หากมีอะไรผิดพลาดระหว่างทาง บังคับให้พิมพ์ Error ออกมาโชว์ที่หน้าจอ
    print("CRASH_REPORT: " + str(e))