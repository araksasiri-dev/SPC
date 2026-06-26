*** Settings ***
Library    SeleniumLibrary

*** Test Cases ***
Verify Web And Scrape Data Test
    Open Browser    https://th.wikipedia.org    chrome
    Maximize Browser Window
    Input Text    id=searchInput    อิตาลี
    Press Keys    id=searchInput    ENTER
    Sleep    2s
    
	# บรรทัด 13: ดึงข้อความหัวข้อมาเก็บในตัวแปร (เคาะห่าง 4 ครั้ง)
    ${web_title}=    Get Text    id=firstHeading
    
    # บรรทัด 16: ใช้ Catenate เชื่อมคำ (เคาะแยกช่องละ 4 ครั้ง เพื่อความชัวร์)
    ${log_msg}=    Catenate    ดึงข้อมูลสำเร็จ! หัวข้อหน้าเว็บนี้คือ:    ${web_title}
    
    # บรรทัด 17: สั่ง Log ตัวแปรเดี่ยว ๆ ชิดขอบคำสั่ง (เคาะห่าง 4 ครั้งพอ)
    Log    ${log_msg}
    
    Capture Page Screenshot    wikipedia_result.png
    Close Browser