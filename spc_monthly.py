import pandas as pd
import re
import os
import gzip

# 1. ตั้งค่า Path หลัก
base_path = r'c:\spc\04-2026'
folder_name = os.path.basename(base_path)  # '04-2026'
# แปลงเป็นรูปแบบเดือน-ปีที่ต้องการ
if '-' in folder_name:
    month, year = folder_name.split('-')
    output_file = f'SupplyChain_Report_{month}{year}_Final.xlsx'
else:
    output_file = f'SupplyChain_Report_{folder_name}_Final.xlsx'


# 2. Regex สำหรับดึงข้อมูล
log_pattern = r'(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2}).*?- ([\d\.,\s]+) \d+ (.*?):(.*?)\s+(GET|POST)\s+(.*?)\s+\[\]'

def process_folder(folder_name):
    data_list = []
    folder_path = os.path.join(base_path, folder_name)
    
    if not os.path.exists(folder_path):
        print(f"⚠️ ไม่พบ Folder: {folder_path}")
        return []

    files = sorted([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])
    print(f"🚀 กำลังอ่านไฟล์จาก {folder_name} (พบ {len(files)} ไฟล์)...")

    for filename in files:
        file_path = os.path.join(folder_path, filename)
        open_func = gzip.open if filename.endswith('.gz') else open
        mode = 'rt' if filename.endswith('.gz') else 'r'
        
        try:
            with open_func(file_path, mode, encoding='utf-8') as f:
                for line in f:
                    match = re.search(log_pattern, line)
                    if match:
                        date, time, ip, user_raw, role, method, path = match.groups()
                        
                        # Logic: เลือก IP แรก และ Mapping User
                        client_ip = ip.split(',')[0].strip()
                        final_user = role if user_raw == "UNKNOWN" else user_raw
                        
                        data_list.append({
                            'Date:Time': f"{date} {time}",
                            'IP Address': client_ip,
                            'User': final_user,
                            'Command': f"{method} {path}"
                        })
        except Exception as e:
            print(f"❌ Error at {filename}: {e}")
    return data_list

# 3. ประมวลผลแยกแต่ละ Folder
back_data = process_folder('web_back')
front_data = process_folder('web_front')

# 4. บันทึกลง Excel
with pd.ExcelWriter(output_file) as writer:
    if back_data:
        df_back = pd.DataFrame(back_data)
        df_back['Date:Time'] = pd.to_datetime(df_back['Date:Time'])
        df_back.sort_values(by='Date:Time').to_excel(writer, sheet_name='WebBack', index=False)
    
    if front_data:
        df_front = pd.DataFrame(front_data)
        df_front['Date:Time'] = pd.to_datetime(df_front['Date:Time'])
        df_front.sort_values(by='Date:Time').to_excel(writer, sheet_name='WebFront', index=False)

print(f"✅ รายงานฉบับสมบูรณ์สร้างเสร็จแล้ว: {output_file}")