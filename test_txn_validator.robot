*** Settings ***
Documentation     ระบบตรวจรับและตัดยอดเงินจำลอง (Transaction File Validator)
Library           OperatingSystem
Library           String
Library           Collections
# 🟢 ดึงเอนจิ้น Python ที่เราเขียนไว้มาสแตนด์บาย
Library           TxnValidator.py

*** Variables ***
${FILE_PATH}      transactions.txt

*** Test Cases ***
TC001: ลุยสแกนธุรกรรมและดักจับข้อยกเว้นระดับ Enterprise
    # 1. ดึงไฟล์ข้อความดิบ
    ${file_content}=    Get File    ${FILE_PATH}    encoding=utf-8
    
    # 2. 🟢 แปลงข้อความก้อนใหญ่เป็นลิสต์รายบรรทัด (ตัดปัญหาเรื่องเครื่องหมายขึ้นบรรทัดใหม่ \n)
    @{lines}=    Split To Lines    ${file_content}
    
    # ตัวแปรสำหรับเก็บยอดรวมเงินธุรกรรมที่ SUCCESS
    ${TOTAL_SUCCESS_AMOUNT}=    Set Variable    ${0.0}
    Set Suite Variable    ${TOTAL_SUCCESS_AMOUNT}

    Log To Console    \n--- START TRANSACTION AUDIT ---

    # 3. เริ่มทำการลูปเจาะข้อมูลทีละบรรทัด
    FOR    ${line}    IN    @{lines}
        # ข้ามบรรทัดว่างเปล่าเพื่อป้องกันระบบรวน
        IF    '${line.strip()}' == '${EMPTY}'    CONTINUE
        
        # 4. 🟢 ท่าไม้ตายดักจับ Exception (TRY...EXCEPT) ห้ามให้แถวพังทำระบบหยุดรัน
        TRY
            # ส่งข้อมูลไปประมวลผลที่ Python ได้เป็น Dictionary
            ${result}=    Validate Transaction Line    ${line}
            
            Log To Console    [PASS] ID: ${result['txn_id']} | User: ${result['user_name']} | Risk: ${result['risk_level']} | Tag: ${result['vip_tag']}
            
            # ถ้าสถานะเป็น SUCCESS ให้บวกยอดเงินรวมสะสม
            IF    '${result['status']}' == 'SUCCESS' and '${result['risk_level']}' != 'REJECTED_NEGATIVE_AMOUNT'
                ${TOTAL_SUCCESS_AMOUNT}=    Evaluate    ${TOTAL_SUCCESS_AMOUNT} + ${result['amount']}
            END

        EXCEPT    INVALID_FORMAT
            Log To Console    [ERROR] บรรทัดนี้รูปแบบพัง (INVALID_FORMAT): "${line}"
            
        EXCEPT    INVALID_AMOUNT_TYPE
            Log To Console    [ERROR] ตัวเลขจำนวนเงินมีค่าผิดปกติ: "${line}"
            
        EXCEPT    ValueError: EMPTY_LINE
            # ข้ามกรณีบรรทัดว่างเปล่าแฝง
            CONTINUE
			
		# ดักจับกรณีพังอื่น ๆ ที่คาดไม่ถึง เพื่อไม่ให้สคริปต์ตายเด็ดขาด
        EXCEPT    AS    ${err}
            Log To Console    [CRITICAL ERROR] เจอบั๊กที่ไม่คาดคิด: ${err}
        END
    END

    Log To Console    \n--- AUDIT SUMMARY ---
    Log To Console    ยอดรวมเงินธุรกรรม SUCCESS ทั้งหมด: ${TOTAL_SUCCESS_AMOUNT} บาท
    Log To Console    --- END PROCESS ---