*** Settings ***
Documentation     ตรวจสอบความแข็งแรงของรหัสผ่านจากไฟล์ CSV
...               วิธีใช้: robot password_checker_bulk.robot
Library           Collections
Library           String
Library           OperatingSystem

*** Variables ***
${CSV_FILE}       passwords.csv
${OUTPUT_FILE}    password_report.csv

*** Tasks ***
ตรวจสอบรหัสผ่านทั้งหมดจากไฟล์ CSV
    [Documentation]    อ่าน CSV และตรวจสอบรหัสผ่านทุกแถว
    
    ${file_exists}=    Run Keyword And Return Status    File Should Exist    ${CSV_FILE}
    IF    not ${file_exists}
        Log To Console    \n❌ ERROR: ไม่พบไฟล์ ${CSV_FILE}
        Log To Console    ================================
        Fatal Error    Missing CSV file
    END
    
    # อ่านไฟล์ CSV แบบ manual
    ${content}=    Get File    ${CSV_FILE}
    @{lines}=    Split To Lines    ${content}
    ${row_count}=    Get Length    ${lines}
    Log To Console    \n📂 พบข้อมูล ${row_count-1} รายการในไฟล์ ${CSV_FILE}
    Log To Console    ================================
    
    # สร้างไฟล์ผลลัพธ์
    Create File    ${OUTPUT_FILE}    \uFEFFusername,password,score,level,feedback\n    UTF-8
    
    # ข้าม header (บรรทัดแรก)
    FOR    ${index}    IN RANGE    1    ${row_count}
        ${line}=    Set Variable    ${lines}[${index}]
        @{columns}=    Split String    ${line}    ,
        ${username}=    Set Variable    ${columns}[0]
        ${password}=    Set Variable    ${columns}[1]
        
        Log To Console    \n🔍 กำลังตรวจสอบ: ${username}
        ${result}=    Evaluate Password Strength    ${password}
        Log To Console    📊 ${username} (${password}): ${result.score}/5 | ${result.level}
        Log To Console    💬 ข้อแนะนำ: ${result.feedback}
        
        Append To File    ${OUTPUT_FILE}    ${username},${password},${result.score},${result.level},"${result.feedback}"\n
    END
    
    Log To Console    \n================================
    Log To Console    ✅ เสร็จสิ้น! ผลลัพธ์ถูกบันทึกใน ${OUTPUT_FILE}
    Log To Console    ================================

*** Keywords ***
Evaluate Password Strength
    [Arguments]    ${password}
    ${score}=      Set Variable    ${0}
    ${feedback}=   Create List
    
    ${length}=    Get Length    ${password}
    IF    ${length} >= 8
        ${score}=    Evaluate    ${score} + 1
    ELSE
        Append To List    ${feedback}    ต้องยาวอย่างน้อย 8 ตัวอักษร (ปัจจุบัน ${length} ตัว)
    END
    
    ${has_upper}=    Run Keyword And Return Status    Should Match Regexp    ${password}    [A-Z]
    IF    ${has_upper}
        ${score}=    Evaluate    ${score} + 1
    ELSE
        Append To List    ${feedback}    ต้องมีตัวพิมพ์ใหญ่อย่างน้อย 1 ตัว
    END
    
    ${has_lower}=    Run Keyword And Return Status    Should Match Regexp    ${password}    [a-z]
    IF    ${has_lower}
        ${score}=    Evaluate    ${score} + 1
    ELSE
        Append To List    ${feedback}    ต้องมีตัวพิมพ์เล็กอย่างน้อย 1 ตัว
    END
    
    ${has_digit}=    Run Keyword And Return Status    Should Match Regexp    ${password}    [0-9]
    IF    ${has_digit}
        ${score}=    Evaluate    ${score} + 1
    ELSE
        Append To List    ${feedback}    ต้องมีตัวเลขอย่างน้อย 1 ตัว
    END
    
    ${has_special}=    Run Keyword And Return Status    Should Match Regexp    ${password}    [^a-zA-Z0-9]
    IF    ${has_special}
        ${score}=    Evaluate    ${score} + 1
    ELSE
        Append To List    ${feedback}    ควรมีอักขระพิเศษ
    END
    
    IF    ${score} >= 5
        ${level}=    Set Variable    🌟🌟🌟🌟🌟 แข็งแรงมาก
    ELSE IF    ${score} >= 4
        ${level}=    Set Variable    🌟🌟🌟🌟 ดี
    ELSE IF    ${score} >= 3
        ${level}=    Set Variable    🌟🌟🌟 พอใช้
    ELSE
        ${level}=    Set Variable    🌟 อ่อนแอ ควรปรับปรุง
    END
    
    ${feedback_len}=    Get Length    ${feedback}
    IF    ${feedback_len} > 0
        ${feedback_text}=    Evaluate    " | ".join($feedback)
    ELSE
        ${feedback_text}=    Set Variable    ✅ ผ่านเกณฑ์ทั้งหมด!
    END
    
    &{result}=    Create Dictionary    score=${score}    level=${level}    feedback=${feedback_text}
    RETURN  ${result}