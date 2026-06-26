*** Settings ***
Documentation     ระบบตรวจสอบ Username แบบวนลูปอัตโนมัติ (Data-Driven)
Library           MySecurityLib.py
Library           Collections

*** Variables ***
# --- ท่าใหม่: ประกาศตัวแปรแบบ List (@ นำหน้า) รวมชื่อที่เราต้องการจะทดสอบ ---
@{USERNAME_LIST}    123Nopphawan    Nop    Nop Raksasiri    Annop66    SuperAdmin2026    araksasiri    ทดสอบ    test1234

*** Tasks ***
กระบวนการตรวจสอบกลุ่ม Username อัตโนมัติ
    [Documentation]    อ่านค่าจาก List แล้วสั่งให้บอททำงานซ้ำ ๆ จนกว่าจะครบ
    
    Log To Console    =========================================
    Log To Console    เริ่มระบบตรวจสอบอัตโนมัติ (Batch Processing)
    Log To Console    =========================================

    # --- ใช้คำสั่ง FOR Loop เพื่อดึงชื่ออกมาทีละชื่อ ---
    FOR    ${user}    IN    @{USERNAME_LIST}
        
        # ส่งชื่อแต่ละตัวในลูปวิ่งไปให้หลังบ้าน Python ตรวจสอบ
        ${status}    ${message}=    Verify Username    ${user}
        
        # มัดรวมข้อความผลลัพธ์เพื่อเตรียมพ่นออกจอ Console
        IF    ${status} == ${True}
            ${output}=    Catenate    👤 Username:    ${user}    ->    ✅ [ผ่านเกณฑ์]: ${message}
        ELSE
            ${output}=    Catenate    👤 Username:    ${user}    ->    ❌ [ไม่ผ่านเกณฑ์]: ${message}
        END
        
        Log To Console    ${output}
        
    END
    
    Log To Console    =========================================
    Log To Console    สิ้นสุดการทำงาน ตรวจสอบครบทุกรายชื่อแล้ว!
    Log To Console    =========================================
 