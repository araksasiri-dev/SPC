# database.py
import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self.create_table()
    
    def create_table(self):
        """สร้างตาราง users ถ้ายังไม่มี"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT  ,
                email TEXT  ,
                phone TEXT  ,
                status TEXT,
                registered_at DATETIME DEFAULT (datetime('now', 'localtime')),
                error_message TEXT
            )
        """)
        conn.commit()
        conn.close()
        print("✅ Database ready")
    
    def insert_user(self, username, email, phone, status, error_message=""):
        """เพิ่มหรืออัปเดตข้อมูลผู้ใช้"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        registered_at = datetime.now().isoformat()
        
        cursor.execute("""
            INSERT OR REPLACE INTO users 
            (username, email, phone, status, registered_at, error_message)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (username, email, phone, status, registered_at, error_message))
        
        conn.commit()
        conn.close()
        return True
    
    def get_user_by_username(self, username):
        """ค้นหาผู้ใช้ด้วย username"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()
        return result
        
    def get_user_by_email(self, email):
        """
        ค้นหาผู้ใช้ด้วยอีเมล
        
        Args:
            email (str): อีเมลที่ต้องการค้นหา
        
        Returns:
            tuple: ข้อมูลผู้ใช้ หรือ None ถ้าไม่พบ
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        result = cursor.fetchone()
        conn.close()
        return result
    
    def get_user_by_phone(self, phone):
        """
        ค้นหาผู้ใช้ด้วยเบอร์โทรศัพท์
        
        Args:
            phone (str): เบอร์โทรที่ต้องการค้นหา
        
        Returns:
            tuple: ข้อมูลผู้ใช้ หรือ None ถ้าไม่พบ
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE phone = ?", (phone,))
        result = cursor.fetchone()
        conn.close()
        return result    
        
    def get_recent_users(self, limit=10):
        """
        ดึงข้อมูลผู้ใช้ล่าสุด
        
        Args:
            limit (int): จำนวนที่ต้องการ
        
        Returns:
            list: รายการข้อมูลผู้ใช้ล่าสุด
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users ORDER BY id DESC LIMIT ?", (limit,))
        results = cursor.fetchall()
        conn.close()
        return results        
        
    def get_all_users(self):
        """ดึงข้อมูลผู้ใช้ทั้งหมด"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        conn.close()
        return results

    def get_summary(self):
        """
        สรุปสถิติ
        
        Returns:
            dict: {total, success, failed}
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM users")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE status = 'SUCCESS'")
        success = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE status = 'FAIL'")
        failed = cursor.fetchone()[0]
        
        # นับ SKIPPED
        cursor.execute("SELECT COUNT(*) FROM users WHERE status LIKE 'SKIPPED%'")
        skipped = cursor.fetchone()[0]
        
        conn.close()
        return {
            "total": total,
            "success": success,
            "failed": failed,
            "skipped": skipped
        }
    
    def get_daily_stats(self, days=7):
        """
        ดึงสถิติรายวัน
        
        Args:
            days (int): จำนวนวันย้อนหลัง
        
        Returns:
            list: [(date, total, success, failed), ...]
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DATE(registered_at) as date, 
                   COUNT(*) as total,
                   SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) as success,
                   SUM(CASE WHEN status = 'FAIL' THEN 1 ELSE 0 END) as failed
            FROM users 
            WHERE registered_at >= DATE('now', ?)
            GROUP BY DATE(registered_at) 
            ORDER BY date DESC
        """, (f'-{days} days',))
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_status_counts(self):
        """
        ดึงจำนวนแยกตามสถานะ
        
        Returns:
            list: [(status, count), ...]
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT status, COUNT(*) FROM users GROUP BY status")
        results = cursor.fetchall()
        conn.close()
        return results
    
    def clear_all(self):
        """ล้างข้อมูลทั้งหมด (ใช้เฉพาะตอนทดสอบ)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users")
        conn.commit()
        conn.close()
        print("🗑️ ล้าง Database เรียบร้อย")
    
    def delete_user(self, username):
        """
        ลบผู้ใช้ด้วย username
        
        Args:
            username (str): ชื่อผู้ใช้ที่ต้องการลบ
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
        conn.close()
        print(f"🗑️ ลบผู้ใช้ {username} เรียบร้อย")