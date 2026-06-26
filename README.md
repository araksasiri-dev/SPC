🛠️ แผนล้างบาง รีเซ็ตโปรเจกต์ให้เบาหวิวใน 4 สเตป
สเตปที่ 1: กวาดล้างไฟล์ขยะตัวจริง (700 MB ที่เหลือ)
ให้คุณนพสแกนดูโฟลเดอร์ใน C:\spc เช่น .tmp.driveupload (ถ้ามันยังซ่อนอยู่), โฟลเดอร์ results หรือไฟล์ *.gz แล้วกด Shift + Delete ลบทิ้งออกจากเครื่องไปเลยครับ ให้เหลือแต่ไฟล์โค้ด .py, .robot และ index.html จริงๆ

สเตปที่ 2: ระเบิดความทรงจำ Git ทิ้ง
กดคลิกที่โฟลเดอร์ .git บนหน้าจอ Windows Explorer ของคุณนพ แล้วกด Shift + Delete ลบทิ้งถาวรได้เลยครับ (หรือใช้คำสั่ง rmdir /s /q .git ใน Terminal ก็ได้ครับ)

สเตปที่ 3: เริ่มประวัติศาสตร์ใหม่ที่ใสสะอาด
กลับมาที่ Terminal พิมพ์คำสั่ง 3 บรรทัดนี้เพื่อสร้างคลังใหม่ที่เบาหวิว (ขนาดจะเหลือไม่กี่ KB) และแพ็กเฉพาะเนื้องานจริงครับ:
 
git init
git add .
git commit -m "production ready: clean code only"
สเตปที่ 4: บังคับเซิร์ฟเวอร์ให้ลืมของเก่า (Force Push)
เชื่อมต่อกับ GitHub แล้วใช้คำสั่ง Force ทุบประวัติบนคลาวด์ให้สะอาดกริ๊บตรงกับในเครื่องคุณนพครับ:
 
git remote add origin  https://github.com/araksasiri-dev/SPC
git push -f origin master

# SPC - Password Strength Checker

ตรวจสอบความแข็งแรงของรหัสผ่านด้วย Robot Framework และ Python

## วิธีใช้

### ตรวจสอบรหัสผ่านเดียว
```bash
robot -v PASSWORD:MyP@ssw0rd password_checker.robot
"ทดสอบการสร้าง  feature/README" 
"ทดสอบ feature/README" 


C:\SPC\
├── DataProcessor.py              # Python Library
├── register_users_excel.robot    # Robot Test
├── mock_server.py                # Mock Web Server
├── users.xlsx                    # ไฟล์ข้อมูลต้นทาง
├── results.xlsx                  # ไฟล์ผลลัพธ์

โครงสร้างโปรเจค (OAuth Version) 24/6/2026
C:\SPC\
├── DataProcessor_email.py        # Python Library หลัก (ใช้ OAuth)
├── database.py                   # จัดการ SQLite
├── gmail_oauth.py                # Gmail API OAuth 2.0
├── register_users_gmail.robot    # Robot Framework Test Suite
├── mock_server.py                # Mock Web Server
├── generate_test_data.py         # สร้างข้อมูลทดสอบ
├── test_oauth.py                 # ทดสอบ OAuth
├── users.xlsx                    # ไฟล์ข้อมูลต้นทาง
├── credentials.json              # OAuth Client ID (ดาวน์โหลดจาก GCP)
├── token.pickle                  # สร้างอัตโนมัติ (อย่าแชร์)
├── .env                          # ไฟล์ตั้งค่า
└── .gitignore                    # Git ignore
└── requirement_outh.txt          # ติดตั้ง dependencies
└── view_db.py                    # บริหาร database
# 1. ติดตั้ง dependencies
pip install -r requirements_oauth.txt

# 2. ทดสอบ OAuth
python test_oauth.py

# 3. รัน Mock Server (Terminal 1)
python mock_server.py

# 4. รัน Robot (Terminal 2)
robot register_users_gmail.robot    

โครงสร้างโปรเจค (เพิ่ม Dashboard) 25/6/2026
C:\spc\
├── dashboard/
│   ├── app.py                 # Flask Web Server
│   ├── templates/
│   │   └── index.html         # Dashboard UI
│   └── static/
│       └── css/
│           └── style.css      # (optional)
├── DataProcessor_email.py
├── database.py
├── register_users_gmail.robot
└── users.db
🚀 วิธีรัน Dashboard
bash
# 1. ติดตั้ง Flask
pip install flask

# 2. ไปที่โฟลเดอร์ dashboard
cd C:\spc\dashboard

# 3. รัน Flask
python app.py

# 4. เปิด Browser ไปที่ http://localhost:5000

🚀 วิธีรันทั้ง 2 ระบบพร้อมกัน
Terminal 1 (Mock Server)
bash
cd C:\spc
python mock_server.py
Terminal 2 (Dashboard)
bash
cd C:\spc\dashboard
python app.py
🌐 URL ที่ใช้งาน
URL	คำอธิบาย
http://localhost/	หน้า Status
http://localhost/register	ฟอร์มสมัครสมาชิก
http://localhost/dashboard	เปลี่ยนไป Dashboard
http://localhost:5000	Dashboard Web (Flask)