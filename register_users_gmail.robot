*** Settings ***
Documentation     ระบบสมัครสมาชิกอัตโนมัติ (Excel + Web + Database + Gmail OAuth)
...               วิธีใช้: robot register_users_gmail.robot
...               ต้องการ: credentials.json, token.pickle, users.xlsx
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
${SUCCESS_COUNT}    ${0}
${FAILED_COUNT}     ${0}

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
    
    # ============================================================
    # 3. รายงานข้อมูลบน Console
    # ============================================================
    Log To Console    \n📊 อ่านข้อมูลจาก ${EXCEL_INPUT}
    Log To Console    ✅ ข้อมูลผ่าน: ${CLEAN_USERS.__len__()} ราย
    Log To Console    ⚠️ อีเมลซ้ำ: ${DUP_EMAIL_USERS.__len__()} ราย
    Log To Console    ⚠️ เบอร์โทรซ้ำ: ${DUP_PHONE_USERS.__len__()} ราย
    
    # ============================================================
    # 4. เปิดเบราว์เซอร์และกรอกฟอร์ม (เฉพาะ clean users) พร้อมดักจับ Exception
    # ============================================================
    Open Browser    ${REGISTER_URL}    ${BROWSER}
    Maximize Browser Window
    
    @{DB_RESULTS}=    Create List
    
    # 🟢 เพิ่มตัวแปรนับยอดฝั่งเว็บเพื่อใช้ Reconcile ท้ายงาน
    ${SUCCESS_COUNT}=    Set Variable    ${0}
    ${FAILED_COUNT}=     Set Variable    ${0}
    
    FOR    ${user}    IN    @{CLEAN_USERS}
        # 🟢 ครอบด้วย TRY...EXCEPT เพื่อป้องกันกรณีหน้าเว็บค้างหรือสมัครไม่ผ่าน
        TRY
            ${status}=    Fill Registration Form    ${user}
            ${SUCCESS_COUNT}=    Evaluate    ${SUCCESS_COUNT} + 1
            
        EXCEPT    AS    ${error}
            Log To Console    \n🚨 [WEB ERROR] สมัครสมาชิกล้มเหลวสำหรับคุณ ${user["username"]}: ${error}
            ${status}=    Set Variable    FAILED
            ${FAILED_COUNT}=     Evaluate    ${FAILED_COUNT} + 1
            
            # บังคับให้เบราว์เซอร์กลับมาหน้าแรกเพื่อรอรับคิวถัดไป (ป้องกันลูปค้าง)
            Go To    ${REGISTER_URL}
        END
        
        # บันทึกสถานะจริง (ไม่ว่าจะ SUCCESS หรือ FAILED) ลงในดีบีลิสต์
        ${entry}=    Create Dictionary
        ...    username=${user["username"]}
        ...    email=${user["email"]}
        ...    phone=${user["phone"]}
        ...    status=${status}
        Append To List    ${DB_RESULTS}    ${entry}
    END
    
    Close Browser
 
    
    # ============================================================
    # 5. บันทึก Database (รวมข้อมูลซ้ำ)
    # ============================================================
    ${db_summary}=    Call Method    ${processor}    save_all_results_to_db    ${DB_RESULTS}    ${DUP_EMAIL_USERS}    ${DUP_PHONE_USERS}
    Log To Console    📊 บันทึก DB สำเร็จ: ${db_summary}
    
    # ============================================================
    # 6. เขียน Excel (บันทึกเฉพาะที่สมัคร)
    # ============================================================
    Call Method    ${processor}    write_results_to_excel    ${DB_RESULTS}    ${EXCEL_OUTPUT}
    Log To Console    📁 บันทึก Excel: ${EXCEL_OUTPUT}
    
	# ============================================================
    # 7. สรุปผลจาก Excel โดยตรง (ป้องกันข้อมูลไม่ตรง)
    # ============================================================
    ${excel_summary}=    Call Method    ${processor}    get_summary_from_excel    ${EXCEL_OUTPUT}
    
    # 🟢 แก้ไขให้ถูกต้อง: ดึงค่าด้วย $ และห้ามใส่เครื่องหมายวงเล็บ [] ครอบเด็ดขาด!
    ${email_dup_count}=   Get Length    ${DUP_EMAIL_USERS}
    ${phone_dup_count}=   Get Length    ${DUP_PHONE_USERS}
    
    # นำตัวเลขจำนวนที่นับได้มาบวกกันผ่าน Evaluate
    ${skipped_total}=    Evaluate    ${email_dup_count} + ${phone_dup_count}
    
    ${full_summary}=    Create Dictionary
    ...    total=${excel_summary["total"]}
    ...    success=${excel_summary["success"]}
    ...    failed=${excel_summary["failed"]}
    ...    skipped=${skipped_total}
    ...    duplicate_email=${email_dup_count}
    ...    duplicate_phone=${phone_dup_count}
    
    Log To Console    \n📊 สรุปผลทั้งหมด: ${full_summary}
    Log To Console    📧 อีเมลซ้ำ: ${full_summary["duplicate_email"]} ราย
    Log To Console    📱 เบอร์โทรซ้ำ: ${full_summary["duplicate_phone"]} ราย
    
    # ============================================================
    # 8. ดึงรายงานข้อมูลซ้ำ
    # ============================================================
    ${duplicate_report}=    Call Method    ${processor}    get_duplicate_report
    Log To Console    📋 รายงานข้อมูลซ้ำ:\n${duplicate_report}
    
    # ============================================================
    # 9. ส่ง Email (ใช้ข้อมูลจาก Excel + duplicate_report)
    # ============================================================
    ${recipient}=    Get Environment Variable    RECIPIENT_EMAIL    default=ar0816250183@gmail.com
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