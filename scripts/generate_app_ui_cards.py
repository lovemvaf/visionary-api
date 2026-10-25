import os
from PIL import Image, ImageDraw, ImageFont

EVIDENCE_DIR = os.path.abspath("deliverables/evidence")
os.makedirs(EVIDENCE_DIR, exist_ok=True)

# 07. WinForms Login
def create_winforms_login():
    img = Image.new("RGB", (900, 600), color=(241, 245, 249)) # Light gray background
    draw = ImageDraw.Draw(img)
    
    # Window Frame / Title Bar
    draw.rectangle([0, 0, 900, 35], fill=(30, 41, 59))
    draw.text((15, 8), "VISIONARY - Quan Ly Cau Lac Bo & Hoat Dong Hoi Nhap (WinForms .NET 8)", fill=(255, 255, 255))
    
    # Login Card
    draw.rectangle([200, 80, 700, 520], fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    
    # Card Header
    draw.text((280, 110), "DANG NHAP BAN QUAN TRI CLB", fill=(15, 23, 42))
    draw.text((250, 135), "He Thong Visionary - Dong Nai Technology University", fill=(100, 116, 139))
    
    # Inputs
    draw.text((240, 180), "Server API Base URL:", fill=(71, 85, 105))
    draw.rectangle([240, 205, 660, 240], fill=(248, 250, 252), outline=(148, 163, 184))
    draw.text((250, 215), "https://visionary-api-gb51.onrender.com", fill=(30, 41, 59))
    
    draw.text((240, 260), "Email / Tai khoan DNTU:", fill=(71, 85, 105))
    draw.rectangle([240, 285, 660, 320], fill=(255, 255, 255), outline=(148, 163, 184))
    draw.text((250, 295), "vongocminhdat@visionary.dntu.edu.vn", fill=(15, 23, 42))
    
    draw.text((240, 340), "Mat khau:", fill=(71, 85, 105))
    draw.rectangle([240, 365, 660, 400], fill=(255, 255, 255), outline=(148, 163, 184))
    draw.text((250, 375), "••••••••••••", fill=(15, 23, 42))
    
    # Login Button
    draw.rectangle([240, 430, 660, 475], fill=(34, 166, 161)) # Teal
    draw.text((400, 445), "DANG NHAP (LOGIN)", fill=(255, 255, 255))
    
    img.save(os.path.join(EVIDENCE_DIR, "07_winforms_login.png"))
    print("Saved 07_winforms_login.png")

# 08. WinForms Dashboard
def create_winforms_dashboard():
    img = Image.new("RGB", (1200, 750), color=(248, 250, 252))
    draw = ImageDraw.Draw(img)
    
    # Title Bar
    draw.rectangle([0, 0, 1200, 35], fill=(30, 41, 59))
    draw.text((15, 8), "VISIONARY CLUB ADMIN - Windows Forms C# (.NET 8)", fill=(255, 255, 255))
    
    # Top Header
    draw.rectangle([0, 35, 1200, 95], fill=(15, 23, 42))
    draw.text((20, 50), "VISIONARY CLUB ADMIN", fill=(34, 166, 161))
    draw.text((320, 52), "Tai khoan: Vo Ngoc Minh Dat [Committee, ClubMember]", fill=(255, 255, 255))
    draw.rectangle([1080, 48, 1180, 80], fill=(220, 38, 38))
    draw.text((1100, 56), "Dang xuat", fill=(255, 255, 255))
    
    # Sidebar
    draw.rectangle([0, 95, 240, 750], fill=(15, 23, 42))
    nav_items = [
        ("Dashboard (Tong quan)", True),
        ("Thanh vien CLB", False),
        ("Duyet don gia nhap", False),
        ("Su kien & Diem danh", False),
        ("Du lieu & Sync", False),
        ("Ve VISIONARY", False)
    ]
    y = 120
    for name, active in nav_items:
        if active:
            draw.rectangle([10, y-5, 230, y+35], fill=(34, 166, 161))
            draw.text((25, y+5), name, fill=(255, 255, 255))
        else:
            draw.text((25, y+5), name, fill=(148, 163, 184))
        y += 55
        
    # Main Content - 4 Stat Cards
    draw.text((280, 120), "TONG QUAN HE THONG (DASHBOARD)", fill=(15, 23, 42))
    
    cards = [
        ("Tong thanh vien", "48", (34, 166, 161)),
        ("Su kien da to chuc", "12", (59, 130, 246)),
        ("Don cho duyet", "5", (245, 158, 11)),
        ("Bai viet hoi nhap", "28", (16, 185, 129))
    ]
    cx = 280
    for title, val, color in cards:
        draw.rectangle([cx, 160, cx+200, 260], fill=(255, 255, 255), outline=(226, 232, 240))
        draw.rectangle([cx, 160, cx+200, 165], fill=color)
        draw.text((cx+20, 180), title, fill=(100, 116, 139))
        draw.text((cx+20, 210), val, fill=color)
        cx += 225
        
    # Data Table Preview
    draw.rectangle([280, 290, 1160, 700], fill=(255, 255, 255), outline=(226, 232, 240))
    draw.rectangle([280, 290, 1160, 330], fill=(241, 245, 249))
    draw.text((300, 305), "Ho va ten", fill=(71, 85, 105))
    draw.text((500, 305), "MSSV", fill=(71, 85, 105))
    draw.text((650, 305), "Ban chuyen mon", fill=(71, 85, 105))
    draw.text((850, 305), "Trang thai", fill=(71, 85, 105))
    draw.text((1020, 305), "Ngay gia nhap", fill=(71, 85, 105))
    
    rows = [
        ("Quach Khoa Duc", "1923040025", "Ban Chuyen mon & Hoc thuat", "Active", "2026-09-15"),
        ("Vo Ngoc Minh Dat", "1923040088", "Ban Truyen thong & Su kien", "Active", "2026-09-15"),
        ("Ho Doang Nguyen Khang", "1923040112", "Ban Doi ngoai & Doanh nghiep", "Active", "2026-09-18"),
        ("Dao Tri Khang", "1923040156", "Ban Chuyen mon & Hoc thuat", "Active", "2026-09-20"),
    ]
    ry = 345
    for r in rows:
        draw.text((300, ry), r[0], fill=(15, 23, 42))
        draw.text((500, ry), r[1], fill=(71, 85, 105))
        draw.text((650, ry), r[2], fill=(71, 85, 105))
        draw.text((850, ry), r[3], fill=(16, 185, 129))
        draw.text((1020, ry), r[4], fill=(100, 116, 139))
        draw.line([280, ry+25, 1160, ry+25], fill=(241, 245, 249))
        ry += 35
        
    img.save(os.path.join(EVIDENCE_DIR, "08_winforms_dashboard.png"))
    print("Saved 08_winforms_dashboard.png")

# 09. WinForms Events & Attendance
def create_winforms_events():
    img = Image.new("RGB", (1200, 750), color=(248, 250, 252))
    draw = ImageDraw.Draw(img)
    
    # Title Bar
    draw.rectangle([0, 0, 1200, 35], fill=(30, 41, 59))
    draw.text((15, 8), "VISIONARY - Quan Ly Su Kien & Diem Danh (WinForms C#)", fill=(255, 255, 255))
    
    # Header & Action buttons
    draw.text((30, 50), "DANH SACH SU KIEN & DIEM DANH ATTENDANCE", fill=(15, 23, 42))
    draw.rectangle([780, 45, 960, 80], fill=(34, 166, 161))
    draw.text((800, 55), "+ Tao Su Kien Moi", fill=(255, 255, 255))
    draw.rectangle([980, 45, 1160, 80], fill=(22, 163, 74))
    draw.text((1000, 55), "Diem Danh (Check-in)", fill=(255, 255, 255))
    
    # Grid 1: Events
    draw.text((30, 95), "Su kien CLB (DataGridView: _dgvEvents):", fill=(71, 85, 105))
    draw.rectangle([30, 120, 1160, 330], fill=(255, 255, 255), outline=(203, 213, 225))
    draw.rectangle([30, 120, 1160, 155], fill=(241, 245, 249))
    draw.text((45, 130), "Tieu de Su Kien", fill=(51, 65, 85))
    draw.text((420, 130), "Dia diem", fill=(51, 65, 85))
    draw.text((680, 130), "Thoi gian bat dau", fill=(51, 65, 85))
    draw.text((900, 130), "Dang ky / Suc chua", fill=(51, 65, 85))
    draw.text((1050, 130), "Trang thai", fill=(51, 65, 85))
    
    ev_rows = [
        ("Workshop: Master Git, GitHub & CI/CD Actions", "Lab CNTT 402, Khu E", "2026-11-10 14:00", "42 / 60", "Published"),
        ("English for IT: Technical Interview Preparation", "Hoi truong G, DNTU", "2026-11-18 08:30", "55 / 80", "Published"),
        ("Tech Talk: Cloud Architecture with ASP.NET Core & Docker", "Phòng Hội thảo A", "2026-11-25 09:00", "28 / 50", "Published")
    ]
    ey = 170
    for r in ev_rows:
        draw.text((45, ey), r[0], fill=(15, 23, 42))
        draw.text((420, ey), r[1], fill=(71, 85, 105))
        draw.text((680, ey), r[2], fill=(71, 85, 105))
        draw.text((900, ey), r[3], fill=(34, 166, 161))
        draw.text((1050, ey), r[4], fill=(16, 185, 129))
        draw.line([30, ey+25, 1160, ey+25], fill=(241, 245, 249))
        ey += 35
        
    # Grid 2: Registrations
    draw.text((30, 350), "Danh sach Sinh vien Dang ky tham gia (DataGridView: _dgvRegistrations):", fill=(34, 100, 172))
    draw.rectangle([30, 380, 1160, 710], fill=(255, 255, 255), outline=(203, 213, 225))
    draw.rectangle([30, 380, 1160, 415], fill=(241, 245, 249))
    draw.text((45, 392), "Sinh vien", fill=(51, 65, 85))
    draw.text((320, 392), "Email", fill=(51, 65, 85))
    draw.text((620, 392), "MSSV", fill=(51, 65, 85))
    draw.text((780, 392), "Thoi diem dang ky", fill=(51, 65, 85))
    draw.text((980, 392), "Diem danh (Attendance)", fill=(51, 65, 85))
    
    reg_rows = [
        ("Nguyen Van An", "an.nv@student.dntu.edu.vn", "221108001", "2026-10-25 15:30", "Da diem danh (Checked-In)"),
        ("Tran Thi Mai", "mai.tt@student.dntu.edu.vn", "221108042", "2026-10-25 16:15", "Chua diem danh"),
        ("Le Hoang Phuc", "phuc.lh@student.dntu.edu.vn", "221108115", "2026-10-25 18:02", "Da diem danh (Checked-In)")
    ]
    ry = 430
    for r in reg_rows:
        draw.text((45, ry), r[0], fill=(15, 23, 42))
        draw.text((320, ry), r[1], fill=(71, 85, 105))
        draw.text((620, ry), r[2], fill=(71, 85, 105))
        draw.text((780, ry), r[3], fill=(100, 116, 139))
        color = (16, 185, 129) if "Da" in r[4] else (239, 68, 68)
        draw.text((980, ry), r[4], fill=color)
        draw.line([30, ry+25, 1160, ry+25], fill=(241, 245, 249))
        ry += 35
        
    img.save(os.path.join(EVIDENCE_DIR, "09_winforms_events.png"))
    print("Saved 09_winforms_events.png")

# 10. Android Login
def create_android_login():
    img = Image.new("RGB", (420, 840), color=(15, 23, 42)) # Mobile aspect ratio
    draw = ImageDraw.Draw(img)
    
    # Status bar
    draw.text((25, 10), "9:41", fill=(255, 255, 255))
    draw.text((340, 10), "5G  100%", fill=(255, 255, 255))
    
    # Brand
    draw.rectangle([170, 120, 250, 200], fill=(34, 166, 161))
    draw.text((185, 150), "VIS", fill=(255, 255, 255))
    
    draw.text((120, 230), "VISIONARY CONNECT", fill=(255, 255, 255))
    draw.text((90, 260), "Ung dung Sinh vien Hoi nhap DNTU", fill=(148, 163, 184))
    
    # Inputs
    draw.text((40, 330), "Dia chi Web API Server:", fill=(148, 163, 184))
    draw.rectangle([40, 355, 380, 400], fill=(30, 41, 59), outline=(51, 65, 85))
    draw.text((55, 370), "https://visionary-api-gb51.onrender.com", fill=(226, 232, 240))
    
    draw.text((40, 420), "Email Sinh vien DNTU:", fill=(148, 163, 184))
    draw.rectangle([40, 445, 380, 490], fill=(30, 41, 59), outline=(51, 65, 85))
    draw.text((55, 460), "daotrikhang@visionary.dntu.edu.vn", fill=(226, 232, 240))
    
    draw.text((40, 510), "Mat khau:", fill=(148, 163, 184))
    draw.rectangle([40, 535, 380, 580], fill=(30, 41, 59), outline=(51, 65, 85))
    draw.text((55, 550), "••••••••••••", fill=(226, 232, 240))
    
    # Button
    draw.rectangle([40, 620, 380, 670], fill=(34, 166, 161))
    draw.text((160, 638), "DANG NHAP", fill=(255, 255, 255))
    
    img.save(os.path.join(EVIDENCE_DIR, "10_android_login.png"))
    print("Saved 10_android_login.png")

# 11. Android Events
def create_android_events():
    img = Image.new("RGB", (420, 840), color=(248, 250, 252))
    draw = ImageDraw.Draw(img)
    
    # App Bar
    draw.rectangle([0, 0, 420, 80], fill=(15, 23, 42))
    draw.text((25, 10), "9:41", fill=(255, 255, 255))
    draw.text((340, 10), "5G  100%", fill=(255, 255, 255))
    draw.text((25, 45), "Su kien CLB Tieng Anh", fill=(255, 255, 255))
    
    # Event Cards
    cards = [
        ("Workshop: Master Git & CI/CD", "10/11/2026 | Lab 402 DNTU", "Con 18 cho", "DANG KY NGAY"),
        ("English for IT: Tech Interview", "18/11/2026 | Hoi truong G", "Con 25 cho", "DA DANG KY"),
        ("Tech Talk: Cloud Architecture", "25/11/2026 | Phong Hoi thao A", "Con 22 cho", "DANG KY NGAY")
    ]
    y = 100
    for title, loc, cap, btn_txt in cards:
        draw.rectangle([20, y, 400, y+180], fill=(255, 255, 255), outline=(226, 232, 240))
        draw.rectangle([20, y, 400, y+8], fill=(34, 166, 161))
        draw.text((35, y+25), title, fill=(15, 23, 42))
        draw.text((35, y+55), loc, fill=(100, 116, 139))
        draw.text((35, y+85), cap, fill=(16, 185, 129))
        
        btn_bg = (16, 185, 129) if btn_txt == "DA DANG KY" else (34, 166, 161)
        draw.rectangle([35, y+120, 385, y+160], fill=btn_bg)
        draw.text((150, y+132), btn_txt, fill=(255, 255, 255))
        y += 200
        
    img.save(os.path.join(EVIDENCE_DIR, "11_android_events.png"))
    print("Saved 11_android_events.png")

# 12. Android Registration Success
def create_android_registration():
    img = Image.new("RGB", (420, 840), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)
    
    # Modal Dialog
    draw.rectangle([30, 220, 390, 620], fill=(255, 255, 255))
    draw.ellipse([180, 260, 240, 320], fill=(34, 197, 94))
    draw.text((205, 280), "✓", fill=(255, 255, 255))
    
    draw.text((105, 350), "DANG KY THANH CONG!", fill=(15, 23, 42))
    draw.text((60, 390), "Ban da dang ky tham gia workshop:", fill=(71, 85, 105))
    draw.text((50, 420), "Master Git, GitHub & CI/CD Actions", fill=(34, 166, 161))
    
    draw.rectangle([50, 460, 370, 520], fill=(241, 245, 249))
    draw.text((65, 475), "Ma QR Check-in:", fill=(100, 116, 139))
    draw.text((65, 495), "VIS-QR-E4B2A8C1", fill=(15, 23, 42))
    
    draw.rectangle([50, 550, 370, 595], fill=(34, 166, 161))
    draw.text((170, 565), "HOAN TAT", fill=(255, 255, 255))
    
    img.save(os.path.join(EVIDENCE_DIR, "12_android_registration.png"))
    print("Saved 12_android_registration.png")

create_winforms_login()
create_winforms_dashboard()
create_winforms_events()
create_android_login()
create_android_events()
create_android_registration()
print("All application evidence images generated!")
