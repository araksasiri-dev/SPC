*** Settings ***
Documentation     ระบบสมัครสมาชิกอัตโนมัติ (อ่าน Excel + กรอกฟอร์มเว็บจริง)
...               ใช้ SeleniumLibrary ควบคุมเบราว์เซอร์
Library           DataProcessor.py    WITH NAME    Processor
Library           SeleniumLibrary
Library           Collections

*** Variables ***
${EXCEL_INPUT}      users_dup.xlsx
${EXCEL_OUTPUT}     results_dup.xlsx
${REGISTER_URL}     http://localhost/register
${BROWSER}          chrome
@{CLEAN_USERS}      # ตัวแปรเก็บผู้ใช้ที่ผ่านการตรวจสอบ
@{RESULTS}          # ตัวแปรเก็บผลลัพธ์การสมัคร

*** Test Cases ***
สมัครสมาชิกอัตโนมัติจาก Excel
    [Documentation]    อ่าน Excel -> ตรวจสอบ -> กรอกฟอร์มเว็บ -> เขียนผลลัพธ์
    
    # 1. ประมวลผลข้อมูล
    ${result}=    Processor.Process Data
    @{CLEAN_USERS}=    Set Variable    ${result["clean_data"]}
    ${dup_email}=    Set Variable    ${result["duplicate_email"]}
    ${dup_phone}=    Set Variable    ${result["duplicate_phone"]}
    
    # 2. รายงานข้อมูล
    Log To Console    \n📊 อ่านข้อมูลจาก ${EXCEL_INPUT}
    Log To Console    ✅ ข้อมูลผ่าน: ${CLEAN_USERS.__len__()} ราย
    Log To Console    ⚠️ อีเมลซ้ำ: ${dup_email.__len__()} ราย
    Log To Console    ⚠️ เบอร์โทรซ้ำ: ${dup_phone.__len__()} ราย
    
    # 3. เปิดเบราว์เซอร์
    Open Browser    ${REGISTER_URL}    ${BROWSER}
    Maximize Browser Window
    
    # 4. กรอกฟอร์มเฉพาะผู้ใช้ที่ผ่านการตรวจสอบ
    FOR    ${user}    IN    @{CLEAN_USERS}
        ${status}=    Fill Registration Form    ${user}
        ${username}=    Set Variable    ${user["username"]}
        ${result_entry}=    Create Dictionary    username=${username}    status=${status}
        Append To List    ${RESULTS}    ${result_entry}
    END
    
    # 5. ปิดเบราว์เซอร์
    Close Browser
    
    # 6. เขียนผลลัพธ์กลับ Excel
    Processor.Write Results To Excel    ${RESULTS}    ${EXCEL_OUTPUT}
    
    # 7. สรุปผล
    Log To Console    ================================
    Log To Console    🎉 สมัครสำเร็จ: ${RESULTS.count("SUCCESS")} ราย
    Log To Console    ❌ สมัครล้มเหลว: ${RESULTS.count("FAIL")} ราย
    Log To Console    📁 ผลลัพธ์ถูกบันทึกใน ${EXCEL_OUTPUT}
    Log To Console    ================================

*** Keywords ***
Fill Registration Form
    [Arguments]    ${user_data}
    [Documentation]    กรอกฟอร์มด้วยข้อมูลผู้ใช้
    ${username}=    Set Variable    ${user_data["username"]}
    ${email}=       Set Variable    ${user_data["email"]}
    ${phone}=       Set Variable    ${user_data["phone"]}
    
    # ตรวจสอบอีเมล
    ${email_valid}=    Processor.Validate Email    ${email}
    IF    ${email_valid} == False
        Log To Console    ❌ ${username} - อีเมลไม่ถูกต้อง
        RETURN    FAIL
    END
    
    # กรอกฟอร์ม
    Input Text    id:username    ${username}
    Input Text    id:email       ${email}
    Input Text    id:phone       ${phone}
    Click Button    id:register_btn
    
    # รอผลลัพธ์
    Wait Until Page Contains    Registration successful!    timeout=5s
    
    Log To Console    ✅ ${username} - สมัครสำเร็จ
    RETURN    Success