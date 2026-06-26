# generate_user_dup_100.py
import random
import string
from openpyxl import Workbook

def generate_users_with_duplicates(count=90, duplicate_count=10):
 
    
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
    
    return users

if __name__ == "__main__":
    
    # ========== ตั้งค่าตรงนี้! ==========
    NORMAL_COUNT = 20      # จำนวนข้อมูลปกติ
    DUPLICATE_COUNT = 5    # จำนวนข้อมูลซ้ำ
    # ===================================
    users = generate_users_with_duplicates(NORMAL_COUNT, DUPLICATE_COUNT)
      
    
    # บันทึก Excel
    wb = Workbook()
    ws = wb.active
    ws.append(["username", "email", "phone"])
    for u in users:
        ws.append([u["username"], u["email"], u["phone"]])
    wb.save("users_dup.xlsx")
    
    print(f"✅ สร้างข้อมูล {len(users)} รายการ (รวมข้อมูลซ้ำ {DUPLICATE_COUNT} ราย)")
    print("📁 บันทึกใน users_dup.xlsx")