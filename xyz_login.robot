*** Settings ***
Documentation     บอทล็อกอิน https://bizpotential.xyz/ ออฟฟิศอัตโนมัติประจำเช้าวันทำงาน
Library           SeleniumLibrary

*** Variables ***
${LOGIN_URL}     https://bizpotential.xyz/    # ใส่ URL https://bizpotential.xyz/ ของออฟฟิศ 
${XYZ_USER}      AR             # ใส่ Username ออฟฟิศของคุณนพ
${XYZ_PASS}      0946851426    # ใส่ Password ออฟฟิศของคุณนพ

# --- ตรงนี้คือจุดชี้เป้า (Locators) ที่ต้องไปดูมาจากหน้าเว็บจริงของออฟฟิศครับ ---
#${TXT_USERNAME}   id=USER_NAME    # เปลี่ยนเป็น id หรือ name ของช่องกรอกชื่อ
${TXT_USERNAME}   xpath=//input[@type='text' and contains(@name, 'USER')]
#${TXT_PASSWORD}   id=USER_PASSWORD    # เปลี่ยนเป็น id หรือ name ของช่องกรอกรหัสผ่าน
${TXT_PASSWORD}   xpath=//input[@type='password' and contains(@name, 'PASS')]
#${BTN_LOGIN}      id=login_submit      # เปลี่ยนเป็น id, name หรือ xpath ของปุ่มล็อกอิน
#${BTN_LOGIN}      xpath=//button[contains(text(), 'เข้าสู่ระบบ')]
${BTN_LOGIN}      css=button.btn-block[type='submit']
*** Tasks ***
กระบวนการเข้าสู่ระบบ Bizpotential
    # 1. สร้าง Option สั่งให้เบราว์เซอร์แยกตัวเป็นอิสระ (Detach) หลังบอททำงานจบ
    ${options}=    Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys, selenium
    Call Method    ${options}    add_experimental_option    detach    ${True}
    
    # 2. สั่งเปิดเบราว์เซอร์พร้อมยัด Option ปลดแอกเข้าไปด้วย
    Open Browser    ${LOGIN_URL}    chrome    options=${options}
    Maximize Browser Window
    
    # รอจนกว่าช่องกรอก Username จะโผล่มา
    Wait Until Page Contains Element    ${TXT_USERNAME}    timeout=10s
    
    # พิมพ์ข้อมูลและกดเข้าสู่ระบบ
    Input Text      ${TXT_USERNAME}    ${XYZ_USER}
    Input Text      ${TXT_PASSWORD}    ${XYZ_PASS}
    Click Element   ${BTN_LOGIN}
    
    # พ่นข้อความยืนยันการทำงานลง Console และปล่อยบอทจบการทำงาน (Chrome จะยังคงเปิดอยู่)
    Log To Console    \n✅ ล็อกอินสำเร็จ! ปล่อยเบราว์เซอร์ทิ้งไว้ให้ผู้ใช้งานทำงานต่อครับ
 