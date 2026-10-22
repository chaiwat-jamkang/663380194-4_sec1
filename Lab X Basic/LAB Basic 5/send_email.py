import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# 1. โหลดค่าจากไฟล์ .env โดยอิงจากตำแหน่งของไฟล์นี้
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, '.env')
load_dotenv(dotenv_path=env_path)

# 2. ดึงค่าจาก .env
sender_email = os.getenv("SENDER_EMAIL")
sender_password = os.getenv("SENDER_APP_PASSWORD")

# 3. ตั้งค่าข้อมูลอีเมลที่จะส่ง
receiver_email = "Chaiwat.jam@kkumail.com"
subject = "แจ้งเตือนการรันโค้ด Python - ข้อมูลนักศึกษา"

# ข้อมูลนักศึกษา
std_name = "ไชยวัฒน์"      
std_surname = "แจ่มกลาง"    # 👈 อย่าลืมเปลี่ยนนามสกุลตรงนี้นะครับ
std_id = "663380194-4"    

# นำตัวแปรมาใส่ในเนื้อหาอีเมลให้สั้นกระชับ (เพื่อให้ขึ้นพรีวิวสวยงามแบบในภาพ)
body = f"{std_name} {std_surname} รหัสนักศึกษา {std_id}"

# 4. สร้างโครงสร้างอีเมล (MIME)
msg = MIMEMultipart()
msg["From"] = sender_email
msg["To"] = receiver_email
msg["Subject"] = subject
msg.attach(MIMEText(body, 'plain', 'utf-8'))

try:
    print("กำลังเชื่อมต่อกับ Gmail SMTP over SSL (port 465)...")
    # 5. เชื่อมต่อเซิร์ฟเวอร์และส่งอีเมล (ใช้ตัวแปรพิมพ์เล็กให้ตรงกับด้านบน)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        print("กำลังล็อกอิน...")
        server.login(sender_email, sender_password)
        print("ล็อกอินสำเร็จ! กำลังส่งอีเมล...")
        
        # ส่งอีเมล
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print(f"ส่งอีเมลสำเร็จแล้ว ไปยัง: {receiver_email} 🎉")

except Exception as e:
    print(f"เกิดข้อผิดพลาดในการส่งอีเมล: {e}")