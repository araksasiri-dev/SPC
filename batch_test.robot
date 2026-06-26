*** Settings ***
Documentation     ระบบอ่านไฟล์ภายนอกเพื่อตรวจสอบ Username อัตโนมัติ (File-Driven Testing)
Library           MySecurityLib.py
# Library สำคัญสำหรับสั่งบอทให้จัดการไฟล์ในเครื่อง
Library           OperatingSystem
Library           String

*** Variables ***
${FILE_PATH}      user_data.txt

*** Tasks ***
กระบวนการอ่านไฟล์และตรวจสอบแบบ Batch
    [Documentation]    สั่งบอทอ่านไฟล์ .txt แยกรายบรรทัด แล้ววนลูปส่งตรวจสอบ
    
    Log To Console    \n=========================================
    Log To Console    เริ่มระบบดึงข้อมูลจากไฟล์: ${FILE_PATH}
    Log To Console    =========================================

    # 1. สั่งบอทไปดึงข้อความทั้งหมดจากไฟล์ออกมาเก็บในใจ
    ${file_content}=    Get File    ${FILE_PATH}    encoding=utf-8
    
    # 2. แปลงข้อความยาวๆ ให้กลายเป็นลิสต์แยกตามบรรทัด (Split Line)
    @{usernames}=       Split To Lines    ${file_content}

    # 3. วนลูปตรวจสอบข้อมูลทีละชื่อเหมือนเดิม
    FOR    ${user}    IN    @{usernames}
        # ดักจับกรณีบรรทัดว่างในไฟล์
        IF    "${user}" == "${EMPTY}"    CONTINUE
        
        # ส่งข้อมูลเข้าท่อประมวลผล Python หลังบ้าน
        ${status}    ${message}=    Verify Username    ${user}
        
        # มัดรวมข้อความเพื่อแสดงผล
        IF    ${status} == ${True}
            ${output}=    Catenate    👤 จากไฟล์:    ${user}    ->    ✅ [ผ่าน]: ${message}
        ELSE
            ${output}=    Catenate    👤 จากไฟล์:    ${user}    ->    ❌ [ไม่ผ่าน]: ${message}
        END
        
        Log To Console    ${output}
    END

    Log To Console    =========================================
    Log To Console    จบการทำงาน ตรวจสอบไฟล์เรียบร้อยแล้ว!
    Log To Console    =========================================