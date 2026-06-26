*** Settings ***
Documentation     ระบบตรวจสอบ Username ของโปรเจกต์ BizSmartERP
# ดึงไฟล์ Python เข้ามาใช้งานตรง ๆ เป็น Library
Library           MySecurityLib.py

*** Variables ***
# ลองเปลี่ยนค่าตัวแปรนี้เพื่อทดสอบเคสต่าง ๆ ครับ (เช่น: 123Nopphawan, Nop, Nop Raksasiri, Annop66)
${TEST_USER}      123Nopphawan

*** Tasks ***
กระบวนการตรวจสอบการตั้งชื่อ Username   
    [Documentation]    เรียกใช้ Python Library มาประมวลผลตรรกะ

    # สั่งเรียกฟังก์ชันจาก Python มาใช้งาน
    ${status}    ${message}=    Verify Username    ${TEST_USER}
    
    IF    ${status} == ${True}
        # เชื่อมตัวแปรทั้งหมดให้กลายเป็นประโยคก้อนเดียวก่อน
        ${output_msg}=    Catenate    \n\n    ${TEST_USER}    ✅ [ผ่านเกณฑ์] ->    ${message}\n
        Log To Console    ${output_msg}
    ELSE
        # ฝั่งไม่ผ่านเกณฑ์ก็ทำแบบเดียวกันเพื่อความปลอดภัยครับ
        ${output_msg}=    Catenate    \n\n    ${TEST_USER}    ❌ [ไม่ผ่านเกณฑ์] ->    ${message}\n
        Log To Console    ${output_msg}
    END