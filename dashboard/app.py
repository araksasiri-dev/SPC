# dashboard/app.py
from flask import Flask, render_template, jsonify
import sqlite3
import os
import sys
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import DatabaseManager

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "users.db")

def get_db_stats():
    """ดึงสถิติจาก Database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # สรุปสถิติ
    cursor.execute("SELECT COUNT(*) FROM users")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE status = 'SUCCESS'")
    success = cursor.fetchone()[0]
    
    # ✅ แก้ไข: นับ FAIL ทั้งหมด
    cursor.execute("SELECT COUNT(*) FROM users WHERE status LIKE 'FAILED%'")
    failed = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE status LIKE 'SKIPPED%'")
    skipped = cursor.fetchone()[0]
    
    # ✅ ดึงจำนวน FAIL แยกประเภท
    cursor.execute("SELECT COUNT(*) FROM users WHERE status = 'FAILED_EMAIL'")
    failed_email = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE status = 'FAILED_PHONE'")
    failed_phone = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE status = 'FAILED_BOTH'")
    failed_both = cursor.fetchone()[0]
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    # ✅ 1. ดึงสถิติรายวัน ย้อนหลัง 7 วัน
    cursor.execute("""
        SELECT DATE(registered_at) as date, 
               COUNT(*) as total,
               SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) as success,
               SUM(CASE WHEN status LIKE 'FAILED%' THEN 1 ELSE 0 END) as failed
        FROM users 
        WHERE DATE(registered_at) < ?
          AND registered_at >= DATE('now', '-7 days')
        GROUP BY DATE(registered_at) 
        ORDER BY date ASC
    """, (today,))
    daily_stats = cursor.fetchall()
    
    # ✅ 2. ดึงสถิติรายชั่วโมงของวันนี้ (แยกตามสถานะ)
    cursor.execute("""
        SELECT strftime('%H:00', registered_at) as hour,
               COUNT(*) as total,
               SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) as success,
               SUM(CASE WHEN status LIKE 'FAILED%' THEN 1 ELSE 0 END) as failed,
               SUM(CASE WHEN status LIKE 'SKIPPED%' THEN 1 ELSE 0 END) as skipped
        FROM users 
        WHERE DATE(registered_at) = ?
        GROUP BY strftime('%H:00', registered_at)
        ORDER BY hour ASC
    """, (today,))
    hourly_stats = cursor.fetchall()
    
    # ✅ 3. ดึงข้อมูลสถานะ
    cursor.execute("SELECT status, COUNT(*) FROM users GROUP BY status")
    status_counts = cursor.fetchall()
    
    # ✅ 4. ดึงผู้ใช้ล่าสุด 10 ราย
    cursor.execute("SELECT username, email, phone, status, registered_at FROM users ORDER BY id DESC LIMIT 10")
    recent_users = cursor.fetchall()
    
    conn.close()
    
    return {
        "summary": {
            "total": total,
            "success": success,
            "failed": failed,
            "skipped": skipped
        },
        "failed_breakdown": {
            "failed_email": failed_email,
            "failed_phone": failed_phone,
            "failed_both": failed_both
        },
        "daily_stats": daily_stats,
        "hourly_stats": hourly_stats,
        "status_counts": status_counts,
        "recent_users": recent_users
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stats')
def api_stats():
    stats = get_db_stats()
    return jsonify(stats)

@app.route('/api/skipped_breakdown')
def api_skipped_breakdown():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            COUNT(CASE WHEN status = 'SKIPPED (Duplicate Email)' THEN 1 END) as dup_email,
            COUNT(CASE WHEN status = 'SKIPPED (Duplicate Phone)' THEN 1 END) as dup_phone,
            COUNT(CASE WHEN status = 'SKIPPED (Duplicate Both)' THEN 1 END) as dup_both,
            COUNT(CASE WHEN status = 'SKIPPED (Duplicate)' THEN 1 END) as dup_general
        FROM users
    """)
    row = cursor.fetchone()
    conn.close()
    
    return jsonify({
        "duplicate_email": row[0] or 0,
        "duplicate_phone": row[1] or 0,
        "duplicate_both": row[2] or 0,
        "duplicate_general": row[3] or 0
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)