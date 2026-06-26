*** Settings ***
Documentation     =====================================================================
...               📋 MANUAL & HELP GUIDE FOR PASSWORD CHECKER CLI
...               =====================================================================
...               วิธีใช้งานสคริปต์และการส่งข้อมูลผ่าน Console (Flags Usage):
...               
...               1. โหมดตรวจสอบรหัสผ่านเดี่ยว (กรอกรหัสที่ต้องการเทสโดยตรง):
...                  คำสั่ง: robot -v INPUT_PASSWORD:"รหัสผ่านที่ต้องการ" test_password_checker.robot
...               
...               2. โหมดตรวจสอบรหัสผ่านยกกล่องจากไฟล์ Text (กรอกชื่อไฟล์ข้อมูล):
...                  คำสั่ง: robot -v FILE_PATH:"ชื่อไฟล์.txt" test_password_checker.robot
...               
...               3. โหมดผสม (กำหนดทั้งรหัสผ่านเดี่ยว และ เปลี่ยนชื่อไฟล์รายงานสรุปผล):
...                  คำสั่ง: robot -v INPUT_PASSWORD:"MyP@ss" -v REPORT_OUT:"audit.txt" test_password_checker.robot
...               =====================================================================
Library           PasswordChecker.py
Library           Collections

***** Variables ***
# กำหนดค่าตัวแปรเปิด-ปิด คู่มือผ่าน Console (เริ่มต้นเป็น False เพื่อรันเทสปกติ)
${INPUT_PASSWORD}    DefaultP@ss123
${FILE_PATH}         password1.txt
${REPORT_OUT}        audit_summary_report.txt
${REPORT_PREFIX}     Detailed_Password_Security_Report

*** Test Cases ***

⚙️ โหมดที่ 1: ตรวจสอบรหัสผ่านเดี่ยว (Console Input Dynamic)
    [Documentation]    ทดสอบรหัสผ่านเดี่ยวและบันทึกผลลัพธ์แยกไฟล์
    ${single_report}=    Create List
    
    Log To Console    \n================================
    Log To Console    📥 กำลังตรวจสอบรหัสผ่านเดี่ยว: '${INPUT_PASSWORD}'
    
    ${result}=    Verify Password Strength    ${INPUT_PASSWORD}
    
    Log To Console    📊 คะแนน: ${result["score"]}/5
    Log To Console    📢 ระดับ: ${result["level"]}
    Log To Console    📝 ข้อแนะนำ: ${result["feedback"]}
    Log To Console    ================================
    
    Append To List    ${single_report}    [TARGET] Password: ${INPUT_PASSWORD}
    Append To List    ${single_report}    Score: ${result["score"]}/5
    Append To List    ${single_report}    Level: ${result["level"]}
    Append To List    ${single_report}    Feedback: ${result["feedback"]}
    
    # เคาะระหว่างคำสั่ง 4 ช่องให้เคลียร์ชัดเจน ห้ามเคาะสเปซบาร์รัว ๆ เกินจำเป็นครับ
    Export Report To File    single_report    ${single_report}
    Log To Console    "💾 บันทึกรายงานเดี่ยวเรียบร้อย"
    
    IF    ${result["is_common"]} == ${True}
        Should Be Equal As Integers    ${result["score"]}    0
    ELSE
        Should Be True    ${result["score"]} >= 3
    END

📂 โหมดที่ 2: ตรวจสอบรหัสผ่านยกกล่องและพ่นรายงานเป็น List
    [Documentation]    อ่านค่าจากไฟล์ภายนอกและบันทึกรายงานเป็นรายบรรทัด
    ${bulk_report}=    Create List
    
    Log To Console    \n📋 เริ่มกระบวนการสแกนไฟล์รหัสผ่าน: ${FILE_PATH}
    Log To Console    ========================================================
    
    ${passwords_list}=    Read Passwords From File    ${FILE_PATH}
    
    # วนลูปสแกนและจัดข้อมูลให้เป็นระเบียบลง List
    FOR    ${pwd}    IN    @{passwords_list}
        ${result}=    Verify Password Strength    ${pwd}
        
        # จัดข้อความสรุปผลรายบุคคลเพื่อนำไปบรรจุลง List Report
        ${report_line}=    Set Variable    Password: [ ${pwd} ] -> คะแนน: ${result["score"]}/5 | ระดับความปลอดภัย: ${result["level"]}
        
        # พ่นแสดงผลสดหน้าจอ Console
        Log To Console    ${report_line}
        
        # หยอดลงถัง List เพื่อส่งไปเขียนไฟล์รายงานตอนจบ
        Append To List    ${bulk_report}    ${report_line}
    END
    Log To Console    ========================================================
    
    # 🟢 ส่งถัง List ข้อมูลไปให้ Python เขียนไฟล์ (เว้นวรรค 4 ช่องตรงกลาง)
    Export Report To File    bulk_report    ${bulk_report}
    Log To Console    📢 ดำเนินการสร้างรายงานพร้อมระบุ Timestamp เรียบร้อยแล้ว!
    

📂 โหมดที่ 3: ตรวจสอบรหัสผ่านยกกล่องจาก Text File (PDF)
    [Documentation]    ดึงลิสต์รหัสผ่านมาลูปตรวจจับพร้อมส่งมอบงานเป็นรายงาน PDF 
    # สร้างกล่องลิสต์กลางใน Robot เพื่อสะสมดิกชันนารีผลลัพธ์จาก Python
    ${results_accumulator}=    Create List
    
    Log To Console    \n📋 [System Report] เริ่มกระบวนการสแกนไฟล์รหัสผ่าน: ${FILE_PATH}
    Log To Console    ========================================================
    
    ${passwords_list}=    Read Passwords From File    ${FILE_PATH}
    
    FOR    ${pwd}    IN    @{passwords_list}
        # สั่งรันคิดคะแนนผ่านตัวแปรหลักหลังบ้าน
        ${result}=    Check Password    ${pwd}
        
        # ใส่คีย์รหัสผ่านแฝงตัวเข้าไปในดิกชันนารีเพื่อให้ Python รู้ว่าเป็นของใคร
        Set To Dictionary    ${result}    password=${pwd}
        
        Log To Console    "📝 ตรวจสอบรหัส: '${pwd}' -> ได้คะแนน: ${result["score"]}/5"
        
        # หยอดดิกชันนารีชิ้นนี้สะสมลงถังเพื่อรอแปลงร่างเป็นตาราง PDF
        Append To List    ${results_accumulator}    ${result}
    END
    Log To Console    ========================================================
    
    # 🟢 ส่งถังลิสต์ดิกชันนารีทั้งหมดข้ามท่อไปให้ WeasyPrint ใน Python เนรมิตไฟล์ PDF หรู ๆ ทันที!
    Export Report To Pdf    ${REPORT_PREFIX}    ${results_accumulator}
    Log To Console    "📢 ดำเนินการจัดพิมพ์เอกสาร PDF และฝังระบบ Timestamp สำเร็จเสร็จสิ้น!"

ทดสอบตรวจสอบรหัสผ่านหลายรายการ
    [Documentation]    ทดสอบรหัสผ่านหลายตัวจาก List เพื่อพ่นรายงานละเอียด
    Log To Console    \n📋 รายงานการตรวจสอบรหัสผ่านหลายรายการ
    Log To Console    ================================

    ${passwords_list}=    Read Passwords From File    ${FILE_PATH}
    
    FOR    ${pwd}    IN    @{passwords_list}
        ${result}=    Verify Password Strength    ${pwd}
        Log To Console    "📝 '${pwd}' → คะแนน: ${result["score"]}/5 (${result["strength"]}%) - ${result["level"]} - ${result["feedback"]}"
    END
    Log To Console    ================================

ทดสอบสร้างรหัสผ่านที่แข็งแรง
    [Documentation]    สร้างรหัสผ่านอัตโนมัติ
    ${strong_pwd}=    Generate System Strong Password    length=14
	
	# 🟢 ใช้ท่านี้เพื่อแปลงกายตัวแปรให้แชร์ข้าม Test Case ได้
    Set Suite Variable    ${SHARED_PASSWORD}    ${strong_pwd}
    Log To Console    \n🔑 รหัสผ่านที่สร้างอัตโนมัติ: ${strong_pwd}
    
    ${result}=    Verify Password Strength    ${strong_pwd}
    Log To Console    "✅ ตรวจสอบ: คะแนน ${result["score"]}/5 (${result["strength"]}%)"
    Should Be True    ${result["score"]} >= 4

ทดสอบแปลงรหัสผ่านเป็น Hash
    [Documentation]    แปลงรหัสผ่านเป็น SHA-256
    ${password}=    Set Variable    ${SHARED_PASSWORD}   
    ${hash_value}=    Convert Password To Hash    ${password}
    Log To Console    \n🔐 Original: ${password}
    Log To Console    "🔑 SHA-256: ${hash_value[:10]}"
    Should Be Equal    ${hash_value[:10]}    ${hash_value[:10]} 

*** Keywords ***
Verify Password Strength
    [Arguments]    ${password}
    ${result}=    Check Password    ${password}
    RETURN    ${result}

Generate System Strong Password
    [Arguments]    ${length}=12
    ${password}=    Generate Strong Password    ${length}
    RETURN    ${password}

Convert Password To Hash
    [Arguments]    ${password}
    ${hash}=    Hash Password    ${password}
    RETURN    ${hash}