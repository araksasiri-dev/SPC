# generate_user_dup_100.py
import random
import string
from openpyxl import Workbook

def generate_users_with_duplicates(count=90, duplicate_count=10, fail_count=5):
 
    
    # สร้างข้อมูลปกติ
    users = []
    seen_emails = set()
    seen_phones = set()
    
    while len(users) < count:
        username = ''.join(random.choices(string.ascii_lowercase, k=6)) + str(random.randint(100, 999))
        email = f"{''.join(random.choices(string.ascii_lowercase, k=8))}@test.com"
        phone = f"08{''.join(random.choices(string.digits, k=8))}"
        
        if email not in seen_emails and phone not in seen_phones:
            seen_emails.add(email)
            seen_phones.add(phone)
            users.append({"username": username, "email": email, "phone": phone})
    
    # เพิ่มข้อมูลซ้ำ
    for i in range(duplicate_count):
        dup = random.choice(users)
        
        dup_user = {
            "username": f"dup_{i+1}_{dup['username']}",
            # i % 3 == 0 (ซ้ำแค่อีเมล), i % 3 == 1 (ซ้ำแค่เบอร์), i % 3 == 2 (ซ้ำทั้งคู่)
            "email": dup["email"] if i % 3 in (0, 2) else f"dup_new_{i+1}@test.com",
            "phone": dup["phone"] if i % 3 in (1, 2) else f"08{''.join(random.choices(string.digits, k=8))}"
        }
        users.append(dup_user)
    
    fail_email_count = 0
    fail_phone_count = 0
    fail_both_count = 0
    
    fail_templates = [
        # Email Fail Patterns
        {
            "email": ["invalid_email", "test@", "@test.com", "test@test", "test@.com", "test@test.c"],
            "phone": [f"08{''.join(random.choices(string.digits, k=8))}" for _ in range(6)]
        },
        # Phone Fail Patterns
        {
            "email": [f"{''.join(random.choices(string.ascii_lowercase, k=8))}@test.com" for _ in range(6)],
            "phone": ["1234567890", "081234567", "08123456789", "abcdefghij", "081234567a", "08"]
        },
        # Both Fail
        {
            "email": ["invalid_email", "test@", "@test.com", "test@test", "test@.com", "test@test.c"],
            "phone": ["1234567890", "081234567", "08123456789", "abcdefghij", "081234567a", "08"]
        }
    ]
    
    # เพิ่มข้อมูลล้มเหลว
    for i in range(fail_count):
    # สลับประเภท Fail
        if i % 3 == 0:
            # Email Fail
            fail_user = {
                "username": f"fail_email_{i+1}_{''.join(random.choices(string.ascii_lowercase, k=4))}",
                "email": random.choice(fail_templates[0]["email"]),
                "phone": f"08{''.join(random.choices(string.digits, k=8))}"
            }
            fail_email_count += 1
        elif i % 3 == 1:
            # Phone Fail
            fail_user = {
                "username": f"fail_phone_{i+1}_{''.join(random.choices(string.ascii_lowercase, k=4))}",
                "email": f"{''.join(random.choices(string.ascii_lowercase, k=8))}@test.com",
                "phone": random.choice(fail_templates[1]["phone"])
            }
            fail_phone_count += 1
        else:
            # Both Fail
            fail_user = {
                "username": f"fail_both_{i+1}_{''.join(random.choices(string.ascii_lowercase, k=4))}",
                "email": random.choice(fail_templates[2]["email"]),
                "phone": random.choice(fail_templates[2]["phone"])
            }
            fail_both_count += 1
        
        users.append(fail_user)
        
    return users

if __name__ == "__main__":
    
    # ========== ตั้งค่าตรงนี้! ==========
    NORMAL_COUNT = 500      # จำนวนข้อมูลปกติ
    DUPLICATE_COUNT = 40   # จำนวนข้อมูลซ้ำ
    FAIL_COUNT = 30 # จำนวนข้อมูลล้มเหลว
    # ===================================
    users = generate_users_with_duplicates(NORMAL_COUNT, DUPLICATE_COUNT, FAIL_COUNT)
      
    
    # บันทึก Excel
    wb = Workbook()
    ws = wb.active
    ws.append(["username", "email", "phone"])
    for u in users:
        ws.append([u["username"], u["email"], u["phone"]])
    wb.save("users_dup.xlsx")
    
    print(f"✅ สร้างข้อมูล {len(users)} รายการ (รวมข้อมูลซ้ำ {DUPLICATE_COUNT} ราย) รวมข้อมูลล้มเหลว {FAIL_COUNT} ราย)")
    print("📁 บันทึกใน users_dup.xlsx")