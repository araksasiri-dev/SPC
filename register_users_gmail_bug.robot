*** Settings ***
Documentation     ระบบสมัครสมาชิกอัตโนมัติ (Excel + Web + Database + Gmail OAuth)
...               วิธีใช้: robot register_users_gmail.robot
...               ต้องการ: credentials.json, token.pickle, users_dup.xlsx
Library           DataProcessor_email.py    WITH NAME    Processor
Library           SeleniumLibrary
Library           Collections
Library           OperatingSystem

*** Variables ***
${EXCEL_INPUT}      users_dup.xlsx
${EXCEL_OUTPUT}     results_gmail.xlsx
${REGISTER_URL}     http://localhost/register
${BROWSER}          chrome
@{DB_RESULTS}

*** Test Cases ***
สมัครสมาชิกและส่งรายงานทาง Gmail OAuth
    [Documentation]    อ่าน Excel -> ตรวจสอบ -> กรอกฟอร์ม -> บันทึก DB -> ส่ง Gmail
    
    # ============================================================
    # 1. สร้าง instance และเริ่มต้น Gmail OAuth
    # ============================================================
    ${processor}=    Evaluate    __import__("DataProcessor_email").DataProcessor("${EXCEL_INPUT}")
    ${gmail}=    Call Method    ${processor}    init_gmail    credentials.json    token.pickle
    
    # ============================================================
    # 2. ประมวลผลข้อมูล (แยก clean / duplicate)
    # ============================================================
    ${result}=    Call Method    ${processor}    process_data
    @{CLEAN_USERS}=    Set Variable    ${result["clean_data"]}
    @{DUP_EMAIL_USERS}=    Set Variable    ${result["duplicate_email"]}
    @{DUP_PHONE_USERS}=    Set Variable    ${result["duplicate_phone"]}
    @{DUP_BOTH_USERS}=    Set Variable    ${result["duplicate_both"]}
    
    # ============================================================
    # 3. รายงานข้อมูลบน Console
    # ============================================================
    Log To Console    \n📊 อ่านข้อมูลจาก ${EXCEL_INPUT}
    Log To Console    ✅ ข้อมูลผ่าน: ${CLEAN_USERS.__len__()} ราย
    Log To Console    ⚠️ อีเมลซ้ำ: ${DUP_EMAIL_USERS.__len__()} ราย
    Log To Console    ⚠️ เบอร์โทรซ้ำ: ${DUP_PHONE_USERS.__len__()} ราย
    Log To Console    ⚠️ ซ้ำทั้งคู่: ${DUP_BOTH_USERS.__len__()} ราย
    
    # ============================================================
    # 4. เปิดเบราว์เซอร์และกรอกฟอร์ม (เฉพาะ clean users)
    # ============================================================
    Open Browser    ${REGISTER_URL}    ${BROWSER}
    Maximize Browser Window
    
    @{DB_RESULTS}=    Create List
    FOR    ${user}    IN    @{CLEAN_USERS}
        ${status}=    Fill Registration Form    ${user}
        ${entry}=    Create Dictionary
        ...    username=${user["username"]}
        ...    email=${user["email"]}
        ...    phone=${user["phone"]}
        ...    status=${status}
        Append To List    ${DB_RESULTS}    ${entry}
    END
    
    Close Browser
    
    # ============================================================
    # 5. บันทึก Database (รวมข้อมูลซ้ำทุกประเภท)
    # ============================================================
    ${db_summary}=    Call Method    ${processor}    save_all_results_to_db
    ...    ${DB_RESULTS}
    ...    ${DUP_EMAIL_USERS}
    ...    ${DUP_PHONE_USERS}
    ...    ${DUP_BOTH_USERS}
    Log To Console    📊 บันทึก DB สำเร็จ: ${db_summary}
    
    # ============================================================
    # 6. เขียน Excel (บันทึกเฉพาะที่สมัคร)
    # ============================================================
    Call Method    ${processor}    write_results_to_excel    ${DB_RESULTS}    ${EXCEL_OUTPUT}
    Log To Console    📁 บันทึก Excel: ${EXCEL_OUTPUT}
    
    # ============================================================
    # 7. ดึงสรุปผลเต็ม (รวมข้อมูลซ้ำ)
    # ============================================================
    ${full_summary}=    Call Method    ${processor}    get_full_summary_with_duplicates
    Log To Console    📊 สรุปผลทั้งหมด: ${full_summary}
    Log To Console    📧 อีเมลซ้ำ: ${full_summary["duplicate_email"]} ราย
    Log To Console    📱 เบอร์โทรซ้ำ: ${full_summary["duplicate_phone"]} ราย
    Log To Console    ⚠️ ซ้ำทั้งคู่: ${full_summary["duplicate_both"]} ราย
    
    # ============================================================
    # 8. ดึงรายงานข้อมูลซ้ำ
    # ============================================================
    ${duplicate_report}=    Call Method    ${processor}    get_duplicate_report
    Log To Console    📋 รายงานข้อมูลซ้ำ:\n${duplicate_report}
    
    # ============================================================
    # 9. ส่ง Email (ใช้ข้อมูลจาก Excel + duplicate_report)
    # ============================================================
    ${recipient}=    Get Environment Variable    RECIPIENT_EMAIL    default=araksasiri@gmail.com
    ${email_result}=    Call Method    ${processor}    send_email_report    ${recipient}    ${full_summary}    ${DB_RESULTS}    ${duplicate_report}
    
    IF    ${email_result} == True
        Log To Console    📧 ส่งอีเมลสำเร็จถึง: ${recipient}
    ELSE
        Log To Console    ⚠️ ส่งอีเมลล้มเหลว (ตรวจสอบ credentials.json)
    END
    
    # ============================================================
    # 10. สรุปผล
    # ============================================================
    Log To Console    ================================
    Log To Console    🎉 เสร็จสิ้น!
    Log To Console    📁 ${EXCEL_OUTPUT}
    Log To Console    📊 SQLite: users.db
    Log To Console    ================================

*** Keywords ***
Fill Registration Form
    [Arguments]    ${user_data}
    [Documentation]    กรอกฟอร์มด้วยข้อมูลผู้ใช้
    ${username}=    Set Variable    ${user_data["username"]}
    ${email}=       Set Variable    ${user_data["email"]}
    ${phone}=       Set Variable    ${user_data["phone"]}
    
    Input Text    id:username    ${username}
    Input Text    id:email       ${email}
    Input Text    id:phone       ${phone}
    Click Button    id:register_btn
    
    Wait Until Page Contains    Registration successful!    timeout=5s
    Log To Console    ✅ ${username} - สมัครสำเร็จ
    RETURN    SUCCESS