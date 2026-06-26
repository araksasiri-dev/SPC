# view_db.py
import sqlite3
import os
import csv
from datetime import datetime

# ตัวแปร global สำหรับชื่อ database
DB_NAME = "users.db"

def clear_screen():
    """ล้างหน้าจอ"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_connection():
    """สร้าง connection ไปยัง database ปัจจุบัน"""
    return sqlite3.connect(DB_NAME)

def select_database():
    """เลือกหรือสร้าง database ใหม่"""
    global DB_NAME
    
    print("\n" + "="*50)
    print("🗄️  เลือกฐานข้อมูล")
    print("="*50)
    print(f"📁 ฐานข้อมูลปัจจุบัน: {DB_NAME}")
    print("1. ใช้ฐานข้อมูลเดิม")
    print("2. เปลี่ยน/สร้างฐานข้อมูลใหม่")
    
    choice = input("\n👉 เลือก (1-2): ").strip()
    
    if choice == "2":
        new_db = input("📝 ป้อนชื่อฐานข้อมูลใหม่ (ไม่ต้องใส่ .db): ").strip()
        if not new_db:
            print("❌ ไม่ได้ป้อนชื่อ ใช้ค่าเดิม")
            return
        
        if not new_db.endswith('.db'):
            new_db += '.db'
        
        DB_NAME = new_db
        print(f"✅ เปลี่ยนเป็นฐานข้อมูล: {DB_NAME}")
        
        # สร้างตารางถ้ายังไม่มี
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                email TEXT UNIQUE,
                phone TEXT UNIQUE,
                status TEXT,
                registered_at TEXT,
                error_message TEXT
            )
        """)
        conn.commit()
        conn.close()
        print(f"✅ สร้างตาราง users ใน {DB_NAME} เรียบร้อย")
    
    input("\nกด Enter เพื่อกลับเมนู...")

def view_all_users():
    """แสดงข้อมูลผู้ใช้ทั้งหมด"""
    conn = get_connection()
    cursor = conn.cursor()
    
    print("\n" + "="*90)
    print(f"📊 ข้อมูลผู้ใช้ทั้งหมดใน Database: {DB_NAME}")
    print("="*90)
    
    cursor.execute("SELECT * FROM users ORDER BY id")
    rows = cursor.fetchall()
    
    if not rows:
        print("⚠️ ไม่มีข้อมูลใน Database")
        conn.close()
        return
    
    print(f"{'ID':<5} {'Username':<15} {'Email':<30} {'Phone':<15} {'Status':<20} {'Registered At':<25}")
    print("-"*90)
    
    for row in rows:
        registered_at = row[5][:19] if row[5] else "N/A"
        print(f"{row[0]:<5} {row[1]:<15} {row[2]:<30} {row[3]:<15} {row[4]:<20} {registered_at:<25}")
    
    # สรุปสถิติ
    cursor.execute("SELECT COUNT(*) FROM users")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE status = 'SUCCESS'")
    success = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE status = 'FAIL'")
    failed = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE status LIKE 'SKIPPED%'")
    skipped = cursor.fetchone()[0]
    
    print("-"*90)
    print(f"📋 รวม: {total} ราย")
    print(f"   ✅ SUCCESS: {success} ราย")
    print(f"   ❌ FAIL: {failed} ราย")
    print(f"   ⏭️ SKIPPED: {skipped} ราย")
    print("="*90)
    
    conn.close()

def view_duplicates():
    """แสดงเฉพาะข้อมูลที่ซ้ำ"""
    conn = get_connection()
    cursor = conn.cursor()
    
    print("\n" + "="*90)
    print(f"⚠️ ข้อมูลที่ถูกข้าม (Duplicate) ใน: {DB_NAME}")
    print("="*90)
    
    cursor.execute("SELECT * FROM users WHERE status LIKE 'SKIPPED%'")
    rows = cursor.fetchall()
    
    if not rows:
        print("✅ ไม่มีข้อมูลที่ถูกข้าม")
        conn.close()
        return
    
    print(f"{'ID':<5} {'Username':<15} {'Email':<30} {'Phone':<15} {'Status':<25}")
    print("-"*90)
    
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<15} {row[2]:<30} {row[3]:<15} {row[4]:<25}")
    
    print("="*90)
    conn.close()

def view_summary_by_status():
    """แสดงสรุปแยกตามสถานะ"""
    conn = get_connection()
    cursor = conn.cursor()
    
    print("\n" + "="*50)
    print(f"📊 สรุปแยกตามสถานะใน: {DB_NAME}")
    print("="*50)
    
    cursor.execute("""
        SELECT status, COUNT(*) 
        FROM users 
        GROUP BY status 
        ORDER BY status
    """)
    rows = cursor.fetchall()
    
    if not rows:
        print("⚠️ ไม่มีข้อมูลใน Database")
        conn.close()
        return
    
    print(f"{'Status':<30} {'Count':<10}")
    print("-"*50)
    
    for row in rows:
        status = row[0] if row[0] else "NULL"
        print(f"{status:<30} {row[1]:<10}")
    
    print("="*50)
    conn.close()

def view_by_username():
    """ค้นหาผู้ใช้ด้วย username"""
    username = input("🔍 ป้อน Username ที่ต้องการค้นหา: ").strip()
    
    if not username:
        print("❌ ไม่ได้ป้อน Username")
        return
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    
    if row:
        print(f"\n✅ พบผู้ใช้: {username}")
        print(f"   📧 Email: {row[2]}")
        print(f"   📱 Phone: {row[3]}")
        print(f"   📊 Status: {row[4]}")
        print(f"   📅 Registered: {row[5]}")
    else:
        print(f"\n❌ ไม่พบผู้ใช้: {username}")
    
    conn.close()

def view_by_status():
    """ค้นหาผู้ใช้ตามสถานะ พร้อมแสดงจำนวน"""
    print("\n📊 สถานะที่ค้นหาได้:")
    print("   1. SUCCESS")
    print("   2. FAIL")
    print("   3. SKIPPED (ทั้งหมด)")
    print("   4. SKIPPED (Duplicate Email)")
    print("   5. SKIPPED (Duplicate Phone)")
    print("   6. ทั้งหมด (ทุกสถานะ)")
    
    choice = input("\n👉 เลือกสถานะ (1-6): ").strip()
    
    status_map = {
        "1": "SUCCESS",
        "2": "FAIL",
        "3": "SKIPPED%",
        "4": "SKIPPED (Duplicate Email)",
        "5": "SKIPPED (Duplicate Phone)",
        "6": "%"
    }
    
    status = status_map.get(choice)
    if not status:
        print("❌ เลือกไม่ถูกต้อง")
        return
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # ✅ นับจำนวนก่อน
    if status == "%":
        cursor.execute("SELECT COUNT(*) FROM users")
    else:
        cursor.execute("SELECT COUNT(*) FROM users WHERE status LIKE ?", (status,))
    total_count = cursor.fetchone()[0]
    
    if total_count == 0:
        print(f"\n⚠️ ไม่มีข้อมูลที่มีสถานะ: {status}")
        conn.close()
        return
    
    # ดึงข้อมูล
    if status == "%":
        cursor.execute("SELECT * FROM users ORDER BY id")
    else:
        cursor.execute("SELECT * FROM users WHERE status LIKE ? ORDER BY id", (status,))
    rows = cursor.fetchall()
    
    # แสดงผล
    status_display = "ทั้งหมด (ทุกสถานะ)" if status == "%" else status
    print("\n" + "="*100)
    print(f"📊 ข้อมูลที่มีสถานะ: {status_display} (จำนวน {total_count} ราย)")
    print("="*100)
    print(f"{'ID':<5} {'Username':<15} {'Email':<30} {'Phone':<15} {'Status':<25} {'Registered At':<20}")
    print("-"*100)
    
    for row in rows:
        registered_at = row[5][:16] if row[5] else "N/A"
        print(f"{row[0]:<5} {row[1]:<15} {row[2]:<30} {row[3]:<15} {row[4]:<25} {registered_at:<20}")
    
    print("-"*100)
    print(f"📋 รวมทั้งหมด: {total_count} ราย")
    print("="*100)
    
    conn.close()

def view_status_summary():
    """แสดงสรุปสถานะทั้งหมดพร้อมจำนวน"""
    conn = get_connection()
    cursor = conn.cursor()
    
    print("\n" + "="*50)
    print("📊 สรุปสถานะทั้งหมด")
    print("="*50)
    
    cursor.execute("""
        SELECT status, COUNT(*) as count 
        FROM users 
        GROUP BY status 
        ORDER BY count DESC
    """)
    rows = cursor.fetchall()
    
    if not rows:
        print("⚠️ ไม่มีข้อมูลใน Database")
        conn.close()
        return
    
    total = 0
    print(f"{'Status':<35} {'Count':<10}")
    print("-"*50)
    
    for row in rows:
        status = row[0] if row[0] else "NULL"
        count = row[1]
        total += count
        print(f"{status:<35} {count:<10}")
    
    print("-"*50)
    print(f"{'รวมทั้งหมด':<35} {total:<10}")
    print("="*50)
    
    conn.close()

def export_to_csv():
    """ส่งออกข้อมูลเป็น CSV"""
    filename = input("📁 ป้อนชื่อไฟล์ CSV (default: users_export.csv): ").strip()
    if not filename:
        filename = "users_export.csv"
    
    if not filename.endswith('.csv'):
        filename += '.csv'
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    
    if not rows:
        print("⚠️ ไม่มีข้อมูลที่จะส่งออก")
        conn.close()
        return
    
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'username', 'email', 'phone', 'status', 'registered_at', 'error_message'])
        for row in rows:
            writer.writerow(row)
    
    print(f"✅ ส่งออกข้อมูล {len(rows)} รายการ ไปยัง {filename} เรียบร้อย")
    conn.close()

def clear_database():
    """ล้างข้อมูลทั้งหมด"""
    confirm = input(f"⚠️ ต้องการล้างข้อมูลทั้งหมดใน {DB_NAME}? (yes/no): ").strip().lower()
    if confirm == 'yes':
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users")
        conn.commit()
        conn.close()
        print(f"🗑️ ล้าง Database {DB_NAME} เรียบร้อย")
    else:
        print("❌ ยกเลิก")

def show_db_info():
    """แสดงข้อมูลของ database ปัจจุบัน"""
    conn = get_connection()
    cursor = conn.cursor()
    
    print("\n" + "="*50)
    print(f"📁 ข้อมูล Database: {DB_NAME}")
    print("="*50)
    
    if os.path.exists(DB_NAME):
        size = os.path.getsize(DB_NAME)
        if size < 1024:
            size_str = f"{size} bytes"
        elif size < 1024 * 1024:
            size_str = f"{size / 1024:.2f} KB"
        else:
            size_str = f"{size / (1024 * 1024):.2f} MB"
        print(f"📦 ขนาดไฟล์: {size_str}")
    else:
        print("📦 ขนาดไฟล์: 0 bytes (ยังไม่มีไฟล์)")
    
    cursor.execute("SELECT COUNT(*) FROM users")
    total = cursor.fetchone()[0]
    print(f"📋 จำนวนข้อมูล: {total} รายการ")
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"📊 ตาราง: {', '.join([t[0] for t in tables]) if tables else 'ไม่มี'}")
    
    print("="*50)
    conn.close()

def main():
    """โปรแกรมหลัก - เมนูวนลูป"""
    global DB_NAME
    
    # ตรวจสอบว่ามี database หรือไม่
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                email TEXT UNIQUE,
                phone TEXT UNIQUE,
                status TEXT,
                registered_at TEXT,
                error_message TEXT
            )
        """)
        conn.commit()
        conn.close()
        print(f"✅ สร้างฐานข้อมูล {DB_NAME} เรียบร้อย")
    
    while True:
        print("\n" + "="*50)
        print(f"🔍 ระบบตรวจสอบ SQLite Database: {DB_NAME}")
        print("="*50)
        print("1. ดูข้อมูลทั้งหมด")
        print("2. ดูข้อมูลที่ซ้ำ (SKIPPED)")
        print("3. ดูสรุปแยกตามสถานะ")
        print("4. ค้นหาด้วย Username")
        print("5. ค้นหาด้วย Status (พร้อมแสดงจำนวน)")
        print("6. ส่งออกข้อมูลเป็น CSV")
        print("7. ล้างข้อมูลทั้งหมด (ระวัง!)")
        print("8. เปลี่ยน/สร้างฐานข้อมูลใหม่")
        print("9. แสดงข้อมูล Database")
        print("10. สรุปสถานะทั้งหมด")
        print("0. ออกจากโปรแกรม")
        print("="*50)
        
        choice = input("👉 เลือกเมนู (0-10): ").strip()
        
        if choice == "1":
            view_all_users()
            input("\nกด Enter เพื่อกลับเมนู...")
        elif choice == "2":
            view_duplicates()
            input("\nกด Enter เพื่อกลับเมนู...")
        elif choice == "3":
            view_summary_by_status()
            input("\nกด Enter เพื่อกลับเมนู...")
        elif choice == "4":
            view_by_username()
            input("\nกด Enter เพื่อกลับเมนู...")
        elif choice == "5":
            view_by_status()
            input("\nกด Enter เพื่อกลับเมนู...")
        elif choice == "6":
            export_to_csv()
            input("\nกด Enter เพื่อกลับเมนู...")
        elif choice == "7":
            clear_database()
            input("\nกด Enter เพื่อกลับเมนู...")
        elif choice == "8":
            select_database()
        elif choice == "9":
            show_db_info()
            input("\nกด Enter เพื่อกลับเมนู...")
        elif choice == "10":
            view_status_summary()
            input("\nกด Enter เพื่อกลับเมนู...")
        elif choice == "0":
            print("\n👋 ออกจากโปรแกรม...")
            break
        else:
            print("❌ เลือกเมนูไม่ถูกต้อง กรุณาเลือก 0-10")
            input("\nกด Enter เพื่อกลับเมนู...")

if __name__ == "__main__":
    main()