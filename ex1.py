import pandas as pd

# 1. โหลดไฟล์ Excel โดยระบุชื่อ Sheet
file_path = 'SupplyChain_Report_042026_Final.xlsx'
df_back = pd.read_excel(file_path, sheet_name='WebBack')
df_front = pd.read_excel(file_path, sheet_name='WebFront')

# 2. รวมข้อมูลจากทั้ง 2 Sheet เข้าด้วยกันก่อนเพื่อหาภาพรวมทั้งระบบ
df_total = pd.concat([df_back, df_front])

# 3. คำนวณหา Unique IP และ Unique User
unique_ips = df_total['IP Address'].nunique()
unique_users = df_total['User'].nunique()

print(f"--- สรุปภาพรวมระบบ (Total) ---")
print(f"จำนวน Unique IP ทั้งหมด: {unique_ips} รายการ")
print(f"จำนวน Unique User ทั้งหมด: {unique_users} คน")


# 2. กรองเอาเฉพาะ User ที่ไม่ใช่ BATCH
# เราใช้ != เพื่อบอกว่า "ไม่เท่ากับ"
df_human_only = df_total[df_total['User'] != 'BATCH']

# 3. หา Unique IP และ Unique User จากข้อมูลที่กรองแล้ว
unique_ips = df_human_only['IP Address'].nunique()
unique_users = df_human_only['User'].nunique()

print(f"--- สรุปสถิติ (เฉพาะใช้งานจริง) ---")
print(f"จำนวน Unique IP: {unique_ips}")
print(f"จำนวน Unique User: {unique_users}")

# นับจำนวนรายการ BATCH
batch_count = len(df_total[df_total['User'] == 'BATCH'])

# นับจำนวนรายการที่ไม่ใช่ BATCH
human_count = len(df_total[df_total['User'] != 'BATCH'])
print(f"--- สรุปสถิติ (เActions) ---")
print(f"System Actions (Batch): {batch_count}")
print(f"User Actions (Users): {human_count}")



def analyze_sheet(sheet_name):
    # 1. อ่านข้อมูล
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    # กรองเอาเฉพาะมนุษย์ (ไม่เอา BATCH)
    df_human = df[df['User'] != 'BATCH'].copy()
    
    # 2. จัดอันดับ User 10 อันดับ
    top_users = df_human['User'].value_counts().head(10)
    
    # 3. วิเคราะห์เวลา โดยใช้ชื่อคอลัมน์ 'Date:Time' ตามใน Excel
    time_col = 'Date:Time' 
    
    if time_col in df_human.columns:
        # แปลงเป็น datetime (Pandas จะฉลาดพอที่จะแยกวันที่และเวลาให้เอง)
        df_human[time_col] = pd.to_datetime(df_human[time_col])
        # ดึงเฉพาะ "ชั่วโมง" ออกมา
        df_human['Hour'] = df_human[time_col].dt.hour
        # นับความถี่ของชั่วโมง
        peak_hours = df_human['Hour'].value_counts().sort_values(ascending=False).head(10)
    else:
        peak_hours = pd.Series()
        print(f"⚠️ ไม่พบคอลัมน์ชื่อ '{time_col}'")

    # แสดงผล
    print(f"\n========================================")
    print(f"📊 ผลวิเคราะห์ Sheet: {sheet_name}")
    print(f"========================================")
    print(f"--- 🏆 Top 10 Active Users ---")
    print(top_users if not top_users.empty else "ไม่มีข้อมูลใช้งาน")
    
    print(f"\n--- ⏰ Top 10 Peak Usage Hours ---")
    if not peak_hours.empty:
        for hour, count in peak_hours.items():
            print(f"ช่วงเวลา {int(hour):02d}:00 - {int(hour):02d}:59 | จำนวน: {count} ครั้ง")
    else:
        print("ไม่มีข้อมูลเวลา")

# รันการวิเคราะห์ทีละ Sheet
analyze_sheet('WebBack')
analyze_sheet('WebFront')

