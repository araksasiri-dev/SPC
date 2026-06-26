# generate_user_clear_100.py
import random
import string
from openpyxl import Workbook

def generate_username():
    """สร้างชื่อผู้ใช้แบบสุ่ม"""
    prefixes = ["user", "test", "dev", "qa", "demo", "client", "staff", "member", "guest", "tester"]
    suffix = ''.join(random.choices(string.digits, k=4))
    return f"{random.choice(prefixes)}_{suffix}"

def generate_email():
    """สร้างอีเมลแบบสุ่ม"""
    domains = ["test.com", "demo.com", "example.com", "sample.com", "mail.com", "web.com", "app.com"]
    local = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(6, 12)))
    return f"{local}@{random.choice(domains)}"

def generate_phone():
    """สร้างเบอร์โทรศัพท์แบบสุ่ม (ขึ้นต้นด้วย 08 หรือ 09)"""
    prefix = random.choice(["08", "09"])
    number = ''.join(random.choices(string.digits, k=8))
    return f"{prefix}{number}"

def generate_users(count=100):
    """สร้างข้อมูลผู้ใช้ตามจำนวนที่กำหนด"""
    users = []
    seen_emails = set()
    seen_phones = set()
    
    while len(users) < count:
        username = generate_username()
        email = generate_email()
        phone = generate_phone()
        
        # ตรวจสอบไม่ให้ซ้ำ
        if email not in seen_emails and phone not in seen_phones:
            seen_emails.add(email)
            seen_phones.add(phone)
            users.append({
                "username": username,
                "email": email,
                "phone": phone
            })
    
    return users

def save_to_excel(users, filename="users_clear.xlsx"):
    """บันทึกข้อมูลลงไฟล์ Excel"""
    wb = Workbook()
    ws = wb.active
    ws.title = "Users"
    
    # Header
    ws.append(["username", "email", "phone"])
    
    # Data
    for user in users:
        ws.append([user["username"], user["email"], user["phone"]])
    
    wb.save(filename)
    print(f"✅ บันทึกข้อมูล {len(users)} รายการลง {filename} เรียบร้อย")

def save_to_csv(users, filename="users_clear.csv"):
    """บันทึกข้อมูลลงไฟล์ CSV"""
    import csv
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["username", "email", "phone"])
        for user in users:
            writer.writerow([user["username"], user["email"], user["phone"]])
    print(f"✅ บันทึกข้อมูล {len(users)} รายการลง {filename} เรียบร้อย")

if __name__ == "__main__":
    # สร้างข้อมูล 100 รายการ
    users = generate_users(100)
    
    # แสดงตัวอย่าง 5 รายการแรก
    print("\n📋 ตัวอย่างข้อมูล 5 รายการแรก:")
    print("-" * 50)
    for i, user in enumerate(users[:5], 1):
        print(f"{i}. {user['username']} | {user['email']} | {user['phone']}")
    print("-" * 50)
    
    # บันทึกเป็น Excel
    save_to_excel(users, "users_clear.xlsx")
    
    # บันทึกเป็น CSV (เผื่อใช้)
    save_to_csv(users, "users_clear.csv")
    
    print("\n🎉 พร้อมใช้งานแล้ว!")