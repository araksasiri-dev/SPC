*** Settings ***
Documentation     ระบบตรวจสอบความแข็งแรงของรหัสผ่านสไตล์โมเดิร์น
Library           Collections
Library           String

*** Variables ***
# ประกาศตัวแปรรับค่ารหัสผ่านเริ่มต้น (ดักกรณีผู้ใช้ลืมใส่ผ่านคอมมานด์ไลน์)
${PASSWORD}       ${EMPTY}
# ใช้ ${} สำหรับการอ้างอิงตัวแปร Dictionary ทั่วไปในขั้นตอนการทำงาน
&{RESULT}         score=${0}    level=Unknown    feedback=None

*** Tasks ***
กระบวนการตรวจสอบรหัสผ่าน
    [Documentation]    ตรวจสอบรหัสผ่านที่ส่งมาจาก Arguments
    # 1. ดักจับกรณีผู้ใช้ไม่ได้ส่งตัวแปร PASSWORD มาเลย
    IF  "${PASSWORD}" == "${EMPTY}"
        Log To Console    \n❌ ERROR: กรุณาส่งรหัสผ่านผ่านคำสั่ง -v PASSWORD:yourpassword
        Log To Console    ================================
        Fatal Error    Missing required argument PASSWORD
    END

    # 2. เริ่มประมวลผลตรรกะ
    Evaluate Password Strength    ${PASSWORD}
    Display Result

*** Keywords ***
Evaluate Password Strength
    [Arguments]    ${password}
    ${score}=      Set Variable    ${0}
    ${feedback}=   Create List
    
    # Check 1: Length (ตรวจสอบความยาว)
    ${length}=    Get Length    ${password}
    IF    ${length} >= 8
        ${score}=    Evaluate    ${score} + 1
    ELSE
        Append To List    ${feedback}    ต้องยาวอย่างน้อย 8 ตัวอักษร (ปัจจุบัน ${length} ตัว)
    END
    
    # Check 2: Uppercase (ตัวพิมพ์ใหญ่)
    ${has_upper}=    Run Keyword And Return Status    Should Match Regexp    ${password}    [A-Z]
    IF    ${has_upper}
        ${score}=    Evaluate    ${score} + 1
    ELSE
        Append To List    ${feedback}    ต้องมีตัวพิมพ์ใหญ่อย่างน้อย 1 ตัว
    END
    
    # Check 3: Lowercase (ตัวพิมพ์เล็ก)
    ${has_lower}=    Run Keyword And Return Status    Should Match Regexp    ${password}    [a-z]
    IF    ${has_lower}
        ${score}=    Evaluate    ${score} + 1
    ELSE
        Append To List    ${feedback}    ต้องมีตัวพิมพ์เล็กอย่างน้อย 1 ตัว
    END
    
    # Check 4: Number (ตัวเลข)
    ${has_digit}=    Run Keyword And Return Status    Should Match Regexp    ${password}    [0-9]
    IF    ${has_digit}
        ${score}=    Evaluate    ${score} + 1
    ELSE
        Append To List    ${feedback}    ต้องมีตัวเลขอย่างน้อย 1 ตัว
    END
    
    # Check 5: Special Character (อักขระพิเศษ)
    ${has_special}=    Run Keyword And Return Status    Should Match Regexp    ${password}    [^a-zA-Z0-9]
    IF    ${has_special}
        ${score}=    Evaluate    ${score} + 1
    ELSE
        Append To List    ${feedback}    ควรมีอักขระพิเศษ
    END
    
    # Evaluation Level (ประเมินระดับตามคะแนนจริงที่ได้)
    IF    ${score} >= 5
        ${level}=    Set Variable    🌟🌟🌟🌟🌟 แข็งแรงมาก
    ELSE IF    ${score} >= 4
        ${level}=    Set Variable    🌟🌟🌟🌟 ดี
    ELSE IF    ${score} >= 3
        ${level}=    Set Variable    🌟🌟🌟 พอใช้
    ELSE
        ${level}=    Set Variable    🌟 อ่อนแอ ควรปรับปรุง
    END
    
    # การใช้ Python .join ร่วมกับตัวแปรของ Robot ที่ถูกต้อง (ใช้ $ นำหน้าเพื่อส่งผ่านแบบ Object)
    ${feedback_len}=    Get Length    ${feedback}
    IF    ${feedback_len} > 0
        ${feedback_text}=    Evaluate    " | ".join($feedback)
    ELSE
        ${feedback_text}=    Set Variable    ✅ ผ่านเกณฑ์ทั้งหมด!
    END
    
    # อัปเดตค่าลง Dictionary Global ให้ถูกต้องตามหลักโครงสร้างข้อมูล
    Set To Dictionary    ${RESULT}    score=${score}    level=${level}    feedback=${feedback_text}

Display Result
    Log To Console    \n================================
    Log To Console    คะแนน: ${RESULT}[score]/5 | ${RESULT}[level]
    Log To Console    ข้อแนะนำ: ${RESULT}[feedback]
    Log To Console    ================================"csv_export_enabled = True" 
