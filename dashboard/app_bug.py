# dashboard/app.py
from flask import Flask, render_template, jsonify
import sqlite3
import os
import sys

# เพิ่ม path หลักเพื่อ import database.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import DatabaseManager

app = Flask(__name__)

def get_db_stats():
    """ดึงสถิติจาก Database"""
    db = DatabaseManager(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'users.db'))
    summary = db.get_summary()
    
    # ดึงข้อมูลรายละเอียด
    conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'users.db'))
    cursor = conn.cursor()
    
    # ดูข้อมูลล่าสุด 10 รายการ
    cursor.execute("SELECT username, email, phone, status, registered_at FROM users ORDER BY id DESC LIMIT 10")
    recent_users = cursor.fetchall()
    
    # สถิติรายวัน
    cursor.execute("""
        SELECT DATE(registered_at) as date, 
               COUNT(*) as total,
               SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) as success,
               SUM(CASE WHEN status = 'FAIL' THEN 1 ELSE 0 END) as failed
        FROM users 
        GROUP BY DATE(registered_at) 
        ORDER BY date DESC 
        LIMIT 7
    """)
    daily_stats = cursor.fetchall()
    
    # สถิติแยกตามสถานะ
    cursor.execute("SELECT status, COUNT(*) FROM users GROUP BY status")
    status_counts = cursor.fetchall()
    
    conn.close()
    
    return {
        "summary": summary,
        "recent_users": recent_users,
        "daily_stats": daily_stats,
        "status_counts": status_counts
    }

@app.route('/')
def index():
    """หน้า Dashboard"""
    return render_template('index.html')

@app.route('/api/stats')
def api_stats():
    """API สำหรับข้อมูลสถิติ (AJAX)"""
    stats = get_db_stats()
    return jsonify(stats)

@app.route('/api/refresh')
def api_refresh():
    """API สำหรับรีเฟรชข้อมูล (เรียกทุก 5 วินาที)"""
    stats = get_db_stats()
    return jsonify(stats)
    
@app.route('/api/skipped_breakdown')
def api_skipped_breakdown():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # นับแยกตามประเภท
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