*** Settings ***
Documentation     คลังคู่มือแสดงวิธีใช้งานระบบบอทสำหรับ User
Library           BuiltIn

*** Test Cases ***
📖 MANUAL & HELP GUIDE FOR PASSWORD CHECKER CLI
    Log To Console    \n=====================================================================
    Log To Console    📋 MANUAL & HELP GUIDE FOR PASSWORD CHECKER CLI
    Log To Console    =====================================================================
    Log To Console    วิธีใช้งานสคริปต์และการส่งข้อมูลผ่าน Console (Flags Usage):
    Log To Console    ---------------------------------------------------------------------
    Log To Console    1. โหมดตรวจสอบรหัสผ่านเดี่ยว (กรอกรหัสเทสโดยตรงผ่านคีย์บอร์ด):
    Log To Console    คำสั่ง: robot -v INPUT_PASSWORD:"รหัสที่ต้องการ" test_password_checker.robot
    Log To Console    ---------------------------------------------------------------------
    Log To Console    2. โหมดตรวจสอบรหัสผ่านยกกล่องจากไฟล์ Text (ระบุชื่อไฟล์):
    Log To Console    คำสั่ง: robot -v FILE_PATH:"ชื่อไฟล์.txt" test_password_checker.robot
    Log To Console    ---------------------------------------------------------------------
    Log To Console    3. โหมดผสม (กรอกรหัสเดี่ยว พร้อมเปลี่ยนชื่อไฟล์รายงานส่งออกผล):
    Log To Console    คำสั่ง: robot -v INPUT_PASSWORD:"MyP@ss" -v REPORT_OUT:"mrt_audit.txt" test_password_checker.robot
    Log To Console    =====================================================================