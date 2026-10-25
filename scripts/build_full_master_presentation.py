import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

def generate_master_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    C_NAVY = RGBColor(15, 23, 42)       # #0F172A
    C_BLUE = RGBColor(34, 100, 172)     # #2264AC
    C_TEAL = RGBColor(34, 166, 161)     # #22A6A1
    C_BG = RGBColor(248, 250, 252)      # #F8FAFC
    C_WHITE = RGBColor(255, 255, 255)
    C_DARK = RGBColor(30, 41, 59)       # #1E293B
    C_MUTED = RGBColor(100, 116, 139)   # #64748B
    C_GREEN = RGBColor(22, 163, 74)
    C_RED = RGBColor(220, 38, 38)
    C_BORDER = RGBColor(226, 232, 240)

    LOGO_DNTU = os.path.abspath("assets/logos/dntu_logo.png")
    LOGO_CNTT = os.path.abspath("assets/logos/cntt_dntu_logo.png")
    EVIDENCE_DIR = os.path.abspath("deliverables/evidence")

    def add_header(slide, title_text, category_text, slide_num, speaker_name):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG
        bg.line.fill.background()

        header_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(1.15))
        header_shape.fill.solid()
        header_shape.fill.fore_color.rgb = C_WHITE
        header_shape.line.color.rgb = C_BORDER
        header_shape.line.width = Pt(1)

        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.06))
        line.fill.solid()
        line.fill.fore_color.rgb = C_TEAL
        line.line.fill.background()

        txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(9.5), Inches(0.95))
        tf = txBox.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_left = tf.margin_right = tf.margin_bottom = 0
        
        p1 = tf.paragraphs[0]
        p1.text = category_text.upper()
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = C_TEAL
        p1.font.name = "Segoe UI"

        p2 = tf.add_paragraph()
        p2.text = title_text
        p2.font.size = Pt(19)
        p2.font.bold = True
        p2.font.color.rgb = C_NAVY
        p2.font.name = "Segoe UI"

        if os.path.exists(LOGO_DNTU):
            slide.shapes.add_picture(LOGO_DNTU, Inches(11.4), Inches(0.15), height=Inches(0.85))
        if os.path.exists(LOGO_CNTT):
            slide.shapes.add_picture(LOGO_CNTT, Inches(12.1), Inches(0.15), height=Inches(0.85))

        footer = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(7.05), Inches(13.333), Inches(0.45))
        footer.fill.solid()
        footer.fill.fore_color.rgb = C_WHITE
        footer.line.color.rgb = C_BORDER

        ft_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.1), Inches(11.733), Inches(0.35))
        ft_tf = ft_box.text_frame
        ft_tf.margin_top = ft_tf.margin_left = ft_tf.margin_right = ft_tf.margin_bottom = 0
        fp = ft_tf.paragraphs[0]
        fp.text = f"VISIONARY API – TH71108 Web API (DNTU) | Người trình bày: {speaker_name} | Slide {slide_num}/16"
        fp.font.size = Pt(10)
        fp.font.color.rgb = C_MUTED
        fp.font.name = "Segoe UI"

    # ==========================================
    # SLIDE 1: TRANG BÌA (QUÁCH KHOA ĐỨC)
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = C_NAVY
    bg1.line.fill.background()

    if os.path.exists(LOGO_DNTU):
        s1.shapes.add_picture(LOGO_DNTU, Inches(1.0), Inches(0.8), height=Inches(1.2))
    if os.path.exists(LOGO_CNTT):
        s1.shapes.add_picture(LOGO_CNTT, Inches(2.2), Inches(0.8), height=Inches(1.2))

    tx_uni = s1.shapes.add_textbox(Inches(3.8), Inches(0.85), Inches(8.5), Inches(1.1))
    tf_uni = tx_uni.text_frame
    p_u1 = tf_uni.paragraphs[0]
    p_u1.text = "TRƯỜNG ĐẠI HỌC CÔNG NGHỆ ĐỒNG NAI (DNTU)"
    p_u1.font.size = Pt(14)
    p_u1.font.bold = True
    p_u1.font.color.rgb = C_TEAL
    p_u1.font.name = "Segoe UI"

    p_u2 = tf_uni.add_paragraph()
    p_u2.text = "KHOA CÔNG NGHỆ THÔNG TIN – HỌC PHẦN WEB API (TH71108)"
    p_u2.font.size = Pt(12)
    p_u2.font.color.rgb = C_WHITE
    p_u2.font.name = "Segoe UI"

    tx_title = s1.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.333), Inches(1.8))
    tf_title = tx_title.text_frame
    p_t1 = tf_title.paragraphs[0]
    p_t1.text = "VISIONARY"
    p_t1.font.size = Pt(36)
    p_t1.font.bold = True
    p_t1.font.color.rgb = C_WHITE
    p_t1.font.name = "Segoe UI"

    p_t2 = tf_title.add_paragraph()
    p_t2.text = "HỆ THỐNG QUẢN LÝ HOẠT ĐỘNG HỘI NHẬP & KẾT NỐI SINH VIÊN"
    p_t2.font.size = Pt(20)
    p_t2.font.bold = True
    p_t2.font.color.rgb = C_TEAL
    p_t2.font.name = "Segoe UI"

    p_t3 = tf_title.add_paragraph()
    p_t3.text = "Mô hình Một Web API (ASP.NET Core 8) phục vụ Ba Nền tảng (Web Next.js, Desktop WinForms C#, Android Java)"
    p_t3.font.size = Pt(13)
    p_t3.font.color.rgb = RGBColor(203, 213, 225)
    p_t3.font.name = "Segoe UI"

    box_m = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(4.2), Inches(11.333), Inches(2.0))
    box_m.fill.solid()
    box_m.fill.fore_color.rgb = RGBColor(30, 41, 59)
    box_m.line.color.rgb = RGBColor(51, 65, 85)

    tx_m = s1.shapes.add_textbox(Inches(1.2), Inches(4.3), Inches(10.9), Inches(1.8))
    tf_m = tx_m.text_frame
    pm0 = tf_m.paragraphs[0]
    pm0.text = "NHÓM PHÁT TRIỂN: VISIONARY API (PHÂN CÔNG THUYẾT TRÌNH THEO ĐỘ KHÓ TĂNG DẦN):"
    pm0.font.size = Pt(11)
    pm0.font.bold = True
    pm0.font.color.rgb = C_TEAL
    pm0.font.name = "Segoe UI"

    members_text = [
        "1. Quách Khoa Đức (1923040025) – Trưởng nhóm, Kiến trúc hệ thống & Web Client Next.js [Người bắt đầu: 2'45\"]",
        "2. Đào Trí Khang (1923040156) – Kỹ sư Mobile, Ứng dụng di động Android Native Java [3'15\"]",
        "3. Hồ Đoàng Nguyên Khang (1923040112) – Kỹ sư API, Swagger Contract, JWT & PostgreSQL [4'15\"]",
        "4. Võ Ngọc Minh Đạt (1923040088) – Kỹ sư Desktop, Windows Forms C#, Sự cố & Tổng kết [Người kết thúc: 4'45\"]"
    ]
    for mt in members_text:
        pm = tf_m.add_paragraph()
        pm.text = mt
        pm.font.size = Pt(11)
        pm.font.color.rgb = C_WHITE
        pm.font.name = "Segoe UI"

    tx_urls = s1.shapes.add_textbox(Inches(1.0), Inches(6.35), Inches(11.333), Inches(0.85))
    tf_urls = tx_urls.text_frame
    pu1 = tf_urls.paragraphs[0]
    pu1.text = "🌐 Web: https://visionary-platform.vercel.app  |  ⚡ API & Swagger: https://visionary-api-gb51.onrender.com/swagger"
    pu1.font.size = Pt(10.5)
    pu1.font.bold = True
    pu1.font.color.rgb = C_TEAL
    pu1.font.name = "Segoe UI"

    pu2 = tf_urls.add_paragraph()
    pu2.text = "Khai báo AI: Nhóm sử dụng AI (Google Antigravity) để hỗ trợ rà soát mã nguồn, thiết lập test hồi quy và biên soạn tài liệu; toàn bộ mã nguồn, cấu hình đám mây và kết quả chạy đều do nhóm trực tiếp kiểm chứng."
    pu2.font.size = Pt(9.5)
    pu2.font.color.rgb = RGBColor(148, 163, 184)
    pu2.font.name = "Segoe UI"

    s1.notes_slide.notes_text_frame.text = (
        "LỜI THUYẾT TRÌNH (QUÁCH KHOA ĐỨC - 45s):\n"
        "Kính chào Thầy và các bạn! Em tên là Quách Khoa Đức, đại diện nhóm VISIONARY API gồm 4 thành viên. "
        "Hôm nay nhóm em xin báo cáo đồ án học phần Web API với đề tài: VISIONARY – Hệ thống Quản lý Hoạt động Hội nhập. "
        "Đề tài của nhóm em xây dựng một Web API duy nhất bằng ASP.NET Core 8, phục vụ đồng bộ cho ba ứng dụng: "
        "Website Next.js, Desktop Windows Forms và Mobile Android Native. Sau đây em xin bắt đầu phần giới thiệu bài toán và kiến trúc."
    )

    # ==========================================
    # SLIDE 2: BÀI TOÁN & MỤC TIÊU (QUÁCH KHOA ĐỨC)
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "BÀI TOÁN THỰC TẾ & MỤC TIÊU HỆ THỐNG", "01. Giới thiệu Đề tài", 2, "Quách Khoa Đức")

    card1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2))
    card1.fill.solid()
    card1.fill.fore_color.rgb = C_WHITE
    card1.line.color.rgb = C_BORDER
    tx1 = s2.shapes.add_textbox(Inches(1.1), Inches(1.8), Inches(5.0), Inches(4.6))
    tf1 = tx1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "VẤN ĐỀ THỰC TẾ CỦA CLB & SINH VIÊN"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_RED

    problems = [
        "1. Quản lý thủ công, rời rạc:",
        "   CLB Tiếng Anh DNTU trước đây quản lý qua Google Form và file tính, dễ nhầm lẫn dữ liệu và thất lạc thông tin người tham gia.",
        "2. Thiếu cổng thông tin hội nhập & cơ hội:",
        "   Sinh viên CNTT thiếu kênh tiếp cận học thuật English for IT, Radar công nghệ mở (GitHub/Hugging Face) và các cuộc thi Hackathon.",
        "3. Trải nghiệm không đồng bộ trên các thiết bị:",
        "   Sinh viên dùng điện thoại di động, Ban Chủ Nhiệm quản trị trên máy tính Windows, độc giả truy cập trên trình duyệt Web."
    ]
    for pr in problems:
        p = tf1.add_paragraph()
        p.text = pr
        p.font.size = Pt(11)
        p.font.color.rgb = C_DARK

    card2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.2))
    card2.fill.solid()
    card2.fill.fore_color.rgb = C_WHITE
    card2.line.color.rgb = C_BORDER
    tx2 = s2.shapes.add_textbox(Inches(7.1), Inches(1.8), Inches(5.1), Inches(4.6))
    tf2 = tx2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "MỤC TIÊU GIẢI PHÁP VISIONARY"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    solutions = [
        "1. Xây dựng một Web API trung tâm duy nhất:",
        "   ASP.NET Core 8 Web API làm hạt nhân xử lý toàn bộ logic nghiệp vụ, xác thực JWT và kết nối cơ sở dữ liệu PostgreSQL.",
        "2. Phục vụ ba ứng dụng khách chuyên biệt:",
        "   - Web Next.js: Cổng thông tin công khai, tin tức hội nhập, tra cứu sự kiện, English for IT.",
        "   - Windows Forms C#: Phần mềm quản trị cho BCN CLB: quản lý thành viên, duyệt đơn, điểm danh sự kiện.",
        "   - Android Native Java: Ứng dụng di động cho sinh viên: xem sự kiện, đăng ký tham gia, nhận mã QR check-in.",
        "3. Đảm bảo toàn vẹn dữ liệu (Data Integrity):",
        "   Không dùng dữ liệu mẫu (mock/fallback), bảo vệ bài nháp, phân quyền chặt chẽ theo vai trò (RBAC)."
    ]
    for sol in solutions:
        p = tf2.add_paragraph()
        p.text = sol
        p.font.size = Pt(11)
        p.font.color.rgb = C_DARK

    s2.notes_slide.notes_text_frame.text = (
        "LỜI THUYẾT TRÌNH (QUÁCH KHOA ĐỨC - 1'00\"):\n"
        "Thưa Thầy, lý do nhóm em chọn đề tài xuất phát từ bài toán thực tế của CLB Tiếng Anh và sinh viên DNTU. "
        "Trước đây, việc quản lý thành viên và điểm danh sự kiện làm bằng file tính thủ công. "
        "Sinh viên cũng thiếu cổng thông tin học thuật tiếng Anh chuyên ngành IT và các cuộc thi quốc tế. "
        "Hệ thống VISIONARY giải quyết trọn vẹn bài toán bằng một Web API trung tâm duy nhất trên ASP.NET Core 8, "
        "kết nối cơ sở dữ liệu PostgreSQL. Cả ba ứng dụng Web, Android và Windows Forms đều dùng chung dữ liệu nên không bao giờ bị lệch số liệu."
    )

    # ==========================================
    # SLIDE 3: KIẾN TRÚC MỘT API, BA ỨNG DỤNG (QUÁCH KHOA ĐỨC)
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "KIẾN TRÚC HỆ THỐNG: MỘT WEB API, BA NỀN TẢNG", "02. Kiến trúc Hệ sinh thái", 3, "Quách Khoa Đức")

    b_web = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(3.2), Inches(1.3))
    b_web.fill.solid()
    b_web.fill.fore_color.rgb = C_WHITE
    b_web.line.color.rgb = C_BLUE
    b_web.line.width = Pt(2)
    s3.shapes.add_textbox(Inches(0.9), Inches(1.7), Inches(3.0), Inches(1.1)).text_frame.text = (
        "ỨNG DỤNG WEB (Next.js 14)\nChạy: Trình duyệt (Vercel Cloud)\nCổng: HTTPS 443 (Local: 3000)"
    )

    b_win = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.3), Inches(3.2), Inches(1.3))
    b_win.fill.solid()
    b_win.fill.fore_color.rgb = C_WHITE
    b_win.line.color.rgb = C_TEAL
    b_win.line.width = Pt(2)
    s3.shapes.add_textbox(Inches(0.9), Inches(3.4), Inches(3.0), Inches(1.1)).text_frame.text = (
        "ỨNG DỤNG WINDOWS FORMS (C#)\nChạy: Máy tính Windows (Desktop)\nCổng gọi ra: HTTPS 443"
    )

    b_and = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.0), Inches(3.2), Inches(1.3))
    b_and.fill.solid()
    b_and.fill.fore_color.rgb = C_WHITE
    b_and.line.color.rgb = C_GREEN
    b_and.line.width = Pt(2)
    s3.shapes.add_textbox(Inches(0.9), Inches(5.1), Inches(3.0), Inches(1.1)).text_frame.text = (
        "ỨNG DỤNG ANDROID (Java Native)\nChạy: Máy ảo / Điện thoại thật\nGateway ảo: 10.0.2.2 / HTTPS Cloud"
    )

    b_api = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.4), Inches(2.5), Inches(3.6), Inches(2.9))
    b_api.fill.solid()
    b_api.fill.fore_color.rgb = C_NAVY
    b_api.line.color.rgb = C_TEAL
    b_api.line.width = Pt(2)
    tx_api = s3.shapes.add_textbox(Inches(5.5), Inches(2.6), Inches(3.4), Inches(2.7))
    tf_api = tx_api.text_frame
    tf_api.word_wrap = True
    p = tf_api.paragraphs[0]
    p.text = "ASP.NET CORE 8 WEB API"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    api_items = [
        "Kestrel Web Server (.NET 8)",
        "Swagger UI: /swagger",
        "Middleware: CORS, Exception, JWT",
        "Clean Architecture: Core, Infra, Api",
        "Host Cloud: Render (Port 443)",
        "Host Local: localhost:5000 / 5001"
    ]
    for ai in api_items:
        p = tf_api.add_paragraph()
        p.text = "• " + ai
        p.font.size = Pt(10)
        p.font.color.rgb = C_WHITE

    b_db = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.2), Inches(2.9), Inches(2.3), Inches(2.1))
    b_db.fill.solid()
    b_db.fill.fore_color.rgb = C_WHITE
    b_db.line.color.rgb = RGBColor(59, 130, 246)
    b_db.line.width = Pt(2)
    tx_db = s3.shapes.add_textbox(Inches(10.3), Inches(3.0), Inches(2.1), Inches(1.9))
    tf_db = tx_db.text_frame
    p = tf_db.paragraphs[0]
    p.text = "CƠ SỞ DỮ LIỆU"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_BLUE
    db_items = [
        "PostgreSQL 16.3",
        "Cloud: Supabase",
        "Region: Singapore",
        "Port: 5432 (IPv4 Pooler)",
        "EF Core 8 Npgsql"
    ]
    for dbi in db_items:
        p = tf_db.add_paragraph()
        p.text = "• " + dbi
        p.font.size = Pt(10)
        p.font.color.rgb = C_DARK

    card_exp = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.4), Inches(5.7), Inches(7.1), Inches(1.1))
    card_exp.fill.solid()
    card_exp.fill.fore_color.rgb = C_WHITE
    card_exp.line.color.rgb = C_BORDER
    tx_exp = s3.shapes.add_textbox(Inches(5.5), Inches(5.75), Inches(6.9), Inches(1.0))
    tf_exp = tx_exp.text_frame
    p = tf_exp.paragraphs[0]
    p.text = "TẠI SAO DÙNG CHUNG MỘT API MÀ KHÔNG PHẢI MỖI BÊN MỘT DATABASE?"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p2 = tf_exp.add_paragraph()
    p2.text = "1. Toàn vẹn dữ liệu: Không bao giờ xảy ra lệch dữ liệu giữa các nền tảng.\n2. Bảo mật tập trung: Toàn bộ quy tắc kiểm tra quyền JWT thực thi trên server.\n3. Android dùng 10.0.2.2 vì máy ảo coi 127.0.0.1 là chính nó; 10.0.2.2 là gateway trỏ về máy tính host."
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = C_MUTED

    s3.notes_slide.notes_text_frame.text = (
        "LỜI THUYẾT TRÌNH (QUÁCH KHOA ĐỨC - 1'00\"):\n"
        "Đây là sơ đồ kiến trúc tổng thể của hệ thống. "
        "Ở trung tâm là máy chủ ASP.NET Core 8 Web API chạy trên Kestrel. "
        "Cả ba ứng dụng đều giao tiếp với API qua giao thức HTTP/HTTPS chuẩn RESTful. "
        "Website Next.js chạy trên trình duyệt gọi qua cổng 443 hoặc qua BFF route handler. "
        "Ứng dụng Windows Forms chạy trực tiếp trên máy tính Windows gọi tới API bằng HttpClient. "
        "Còn ứng dụng Android khi chạy máy ảo sử dụng địa chỉ 10.0.2.2 để kết nối vào máy chủ, "
        "vì máy ảo Android xem localhost là chính nó; khi lên production, Android gọi thẳng vào tên miền cloud https của Render. "
        "Phía sau API là cơ sở dữ liệu PostgreSQL lưu trữ trên Supabase Singapore thông qua cổng 5432. "
        "Việc dùng chung một API giúp hệ thống kiểm soát toàn vẹn dữ liệu và phân quyền một nơi duy nhất."
    )

    # ==========================================
    # SLIDE 4: WEB CLIENT (QUÁCH KHOA ĐỨC)
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "ỨNG DỤNG WEB: NEXT.JS 14 APP ROUTER", "03. Ứng dụng Khách (Web)", 4, "Quách Khoa Đức")

    img_web = os.path.join(EVIDENCE_DIR, "02_web_events.png")
    if os.path.exists(img_web):
        s4.shapes.add_picture(img_web, Inches(0.8), Inches(1.5), width=Inches(5.8))

    table_shape = s4.shapes.add_table(5, 3, Inches(6.9), Inches(1.5), Inches(5.6), Inches(1.8))
    t = table_shape.table
    t.columns[0].width = Inches(1.6)
    t.columns[1].width = Inches(1.8)
    t.columns[2].width = Inches(2.2)
    for i, h in enumerate(["Tên điều khiển", "Loại điều khiển", "Vai trò nghiệp vụ"]):
        cell = t.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_WHITE

    ctrl_rows = [
        ("txtSearch", "<input type='text'>", "Nhập từ khóa tìm kiếm sự kiện"),
        ("btnSearch", "<button>", "Kích hoạt tìm kiếm hoặc xóa từ khóa"),
        ("cboStatus", "<select> / Pills", "Lọc sự kiện Sắp diễn ra / Đã qua"),
        ("grdEvents", "<div className='grid'>", "Hiển thị danh sách card sự kiện")
    ]
    for row_idx, r in enumerate(ctrl_rows, start=1):
        for col_idx, val in enumerate(r):
            cell = t.cell(row_idx, col_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_WHITE
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(9.5)
            p.font.color.rgb = C_DARK

    code_box = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.9), Inches(3.5), Inches(5.6), Inches(3.2))
    code_box.fill.solid()
    code_box.fill.fore_color.rgb = C_NAVY
    code_box.line.color.rgb = C_TEAL
    tx_c = s4.shapes.add_textbox(Inches(7.0), Inches(3.55), Inches(5.4), Inches(3.1))
    tf_c = tx_c.text_frame
    tf_c.word_wrap = True
    p = tf_c.paragraphs[0]
    p.text = "// frontend/src/app/events/page.tsx (Mã nguồn thật):"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    code_lines = [
        "const query = new URLSearchParams();",
        "query.set('pageIndex', '1'); query.set('pageSize', '12');",
        "if (searchQuery.trim()) query.set('search', searchQuery.trim());",
        "const res = await fetch(`/api/events?${query.toString()}`, {",
        "  signal: abortController.signal,",
        "  headers: { 'Content-Type': 'application/json' }",
        "});",
        "const data: ApiResponse<PagedResponse<EventItem>> = await res.json();",
        "if (res.ok && data.success) setEvents(data.data.items);"
    ]
    for cl in code_lines:
        p = tf_c.add_paragraph()
        p.text = cl
        p.font.size = Pt(9)
        p.font.color.rgb = RGBColor(226, 232, 240)
        p.font.name = "Consolas"

    s4.notes_slide.notes_text_frame.text = (
        "LỜI THUYẾT TRÌNH (QUÁCH KHOA ĐỨC - 1'00\"):\n"
        "Đây là giao diện Web của nhóm được xây dựng bằng Next.js 14 App Router. "
        "Màn hình hiển thị danh sách các sự kiện CLB. "
        "Các điều khiển tuân thủ đúng quy ước: ô nhập từ khóa là txtSearch, nút bấm là btnSearch, danh sách hiển thị là grdEvents. "
        "Đoạn mã bên phải lấy trực tiếp từ file events/page.tsx. "
        "Khi người dùng gõ từ khóa, hàm gửi request GET tới /api/events kèm phân trang pageIndex và pageSize. "
        "Điểm kỹ thuật quan trọng ở đây là nhóm dùng AbortController để tự động hủy request cũ khi người dùng gõ nhanh, "
        "tránh lỗi bất đồng bộ race condition. Khi nhận kết quả thành công, hàm setEvents sẽ đổ dữ liệu thật vào giao diện. "
        "Sau đây, em xin kính mời bạn Đào Trí Khang tiếp tục trình bày về ứng dụng di động Android Native."
    )

    # ==========================================
    # SLIDE 5: ANDROID NATIVE JAVA (ĐÀO TRÍ KHANG)
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "ỨNG DỤNG DI ĐỘNG: ANDROID NATIVE JAVA", "04. Ứng dụng Khách (Mobile)", 5, "Đào Trí Khang")

    img_and = os.path.join(EVIDENCE_DIR, "11_android_events.png")
    if os.path.exists(img_and):
        s5.shapes.add_picture(img_and, Inches(1.5), Inches(1.4), height=Inches(5.3))

    table_shape5 = s5.shapes.add_table(5, 3, Inches(4.5), Inches(1.4), Inches(8.0), Inches(1.8))
    t5 = table_shape5.table
    t5.columns[0].width = Inches(2.0)
    t5.columns[1].width = Inches(2.4)
    t5.columns[2].width = Inches(3.6)
    for i, h in enumerate(["Tên điều khiển", "Loại điều khiển", "Vai trò nghiệp vụ"]):
        cell = t5.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_WHITE

    ctrl_rows5 = [
        ("lstEvents", "RecyclerView", "Danh sách cuộn các sự kiện CLB"),
        ("btnRegister", "Button", "Đăng ký tham gia sự kiện trực tiếp"),
        ("swpRefresh", "SwipeRefreshLayout", "Vuốt xuống để tải lại dữ liệu mới nhất"),
        ("txtSearch", "EditText", "Ô tìm kiếm sự kiện theo từ khóa")
    ]
    for row_idx, r in enumerate(ctrl_rows5, start=1):
        for col_idx, val in enumerate(r):
            cell = t5.cell(row_idx, col_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_WHITE
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(9.5)
            p.font.color.rgb = C_DARK

    code_box5 = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.5), Inches(3.4), Inches(8.0), Inches(3.3))
    code_box5.fill.solid()
    code_box5.fill.fore_color.rgb = C_NAVY
    code_box5.line.color.rgb = C_GREEN
    tx_c5 = s5.shapes.add_textbox(Inches(4.6), Inches(3.45), Inches(7.8), Inches(3.2))
    tf_c5 = tx_c5.text_frame
    tf_c5.word_wrap = True
    p = tf_c5.paragraphs[0]
    p.text = "// EventsFragment.java – Gọi API bất đồng bộ qua Retrofit (Mã nguồn thật):"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_GREEN

    code_lines5 = [
        "ApiClient.getService(getContext()).getEvents(1, 20)",
        "    .enqueue(new Callback<ApiResponse<PagedResponse<EventItem>>>() {",
        "        @Override",
        "        public void onResponse(@NonNull Call<ApiResponse<PagedResponse<EventItem>>> call,",
        "                               @NonNull Response<ApiResponse<PagedResponse<EventItem>>> res) {",
        "            swipeRefresh.setRefreshing(false);",
        "            if (res.isSuccessful() && res.body() != null && res.body().isSuccess()) {",
        "                adapter.setEvents(res.body().getData().getItems());",
        "            }",
        "        }",
        "    });"
    ]
    for cl in code_lines5:
        p = tf_c5.add_paragraph()
        p.text = cl
        p.font.size = Pt(9)
        p.font.color.rgb = RGBColor(226, 232, 240)
        p.font.name = "Consolas"

    s5.notes_slide.notes_text_frame.text = (
        "LỜI THUYẾT TRÌNH (ĐÀO TRÍ KHANG - 1'00\"):\n"
        "Kính chào Thầy và các bạn! Em tên là Đào Trí Khang, phụ trách ứng dụng di động Android Native bằng Java. "
        "Ứng dụng Android được thiết kế cho sinh viên DNTU để theo dõi hoạt động CLB và đăng ký sự kiện ngay trên điện thoại. "
        "Bên trái là ảnh chụp thật từ ứng dụng Android. "
        "Các điều khiển tuân thủ đúng quy ước đặt tên: danh sách cuộn là lstEvents (RecyclerView), nút đăng ký là btnRegister, vuốt làm mới là swpRefresh. "
        "Đoạn mã bên phải thể hiện hàm loadEvents gọi tới Web API thông qua thư viện Retrofit 2. "
        "Hàm getEvents(1, 20) được đẩy vào phương thức enqueue để thực thi trên luồng nền của OkHttp, "
        "khi có kết quả onResponse sẽ tự động đưa về luồng chính để cập nhật adapter cho RecyclerView."
    )

    # ==========================================
    # SLIDE 6: ANDROID NETWORK & THREADING (ĐÀO TRÍ KHANG)
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "ANDROID GỌI API: LUỒNG NỀN & LUỒNG GIAO DIỆN", "05. Cơ chế Mạng Android", 6, "Đào Trí Khang")

    box_f1 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(3.6), Inches(5.2))
    box_f1.fill.solid()
    box_f1.fill.fore_color.rgb = C_WHITE
    box_f1.line.color.rgb = C_BLUE
    tx_f1 = s6.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(3.2), Inches(4.8))
    tf_f1 = tx_f1.text_frame
    tf_f1.word_wrap = True
    p = tf_f1.paragraphs[0]
    p.text = "1. LUỒNG CHÍNH (UI THREAD)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_BLUE
    items_f1 = [
        "Người dùng tương tác trên màn hình (Bấm Đăng ký / Vuốt làm mới).",
        "KHÔNG ĐƯỢC gọi mạng trực tiếp tại đây! Nếu gọi đồng bộ (execute), Android ném ngoại lệ: NetworkOnMainThreadException và dừng ứng dụng ngay.",
        "Nhiệm vụ: Chỉ gọi enqueue() và hiển thị thanh tiến trình prgLoading."
    ]
    for it in items_f1:
        p = tf_f1.add_paragraph()
        p.text = "• " + it
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_DARK

    box_f2 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.8), Inches(1.5), Inches(3.6), Inches(5.2))
    box_f2.fill.solid()
    box_f2.fill.fore_color.rgb = C_WHITE
    box_f2.line.color.rgb = C_TEAL
    tx_f2 = s6.shapes.add_textbox(Inches(5.0), Inches(1.7), Inches(3.2), Inches(4.8))
    tf_f2 = tx_f2.text_frame
    tf_f2.word_wrap = True
    p = tf_f2.paragraphs[0]
    p.text = "2. LUỒNG NỀN (WORKER THREAD)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    items_f2 = [
        "OkHttp tạo luồng ngầm thực hiện kết nối Socket TCP, bắt tay TLS/HTTPS.",
        "Gửi HTTP Request qua mạng tới API Server (Kestrel 443).",
        "Nhận chuỗi phản hồi JSON UTF-8 từ Server.",
        "Gson Deserialize chuỗi JSON thành Java Object (EventItem).",
        "KHÔNG ĐƯỢC cập nhật View tại đây! Nếu sửa View từ luồng nền, Android sẽ báo lỗi: CalledFromWrongThreadException."
    ]
    for it in items_f2:
        p = tf_f2.add_paragraph()
        p.text = "• " + it
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_DARK

    box_f3 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.5), Inches(3.7), Inches(5.2))
    box_f3.fill.solid()
    box_f3.fill.fore_color.rgb = C_WHITE
    box_f3.line.color.rgb = C_GREEN
    tx_f3 = s6.shapes.add_textbox(Inches(9.0), Inches(1.7), Inches(3.3), Inches(4.8))
    tf_f3 = tx_f3.text_frame
    tf_f3.word_wrap = True
    p = tf_f3.paragraphs[0]
    p.text = "3. ĐẨY VỀ UI THREAD (HANDLER)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_GREEN
    items_f3 = [
        "Retrofit tự động sử dụng Handler gắn với Looper.getMainLooper().",
        "Đưa hàm callback onResponse() chạy trở lại trên Luồng Chính.",
        "Ẩn thanh tiến trình ProgressBar.",
        "Đổ danh sách dữ liệu vào Adapter và gọi notifyDataSetChanged().",
        "Màn hình điện thoại hiển thị thẻ sự kiện mượt mà, không bị khựng đơ."
    ]
    for it in items_f3:
        p = tf_f3.add_paragraph()
        p.text = "• " + it
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_DARK

    s6.notes_slide.notes_text_frame.text = (
        "LỜI THUYẾT TRÌNH (ĐÀO TRÍ KHANG - 1'00\"):\n"
        "Thưa Thầy, một trong những khó khăn lớn nhất khi lập trình ứng dụng di động Android kết nối Web API "
        "là cơ chế điều phối đa luồng. "
        "Hệ điều hành Android có hai quy tắc nghiêm ngặt: "
        "Thứ nhất: Tuyệt đối không được gọi mạng trên Luồng Chính (UI Thread). Nếu vi phạm, hệ điều hành sẽ ném ngoại lệ NetworkOnMainThreadException và tắt app ngay. "
        "Thứ hai: Tuyệt đối không được chạm vào giao diện View từ luồng nền. Nếu vi phạm, sẽ gặp lỗi CalledFromWrongThreadException. "
        "Để giải quyết triệt để, nhóm em sử dụng phương thức enqueue() của Retrofit. "
        "OkHttp sẽ mở luồng nền chạy ngầm gửi request và nhận JSON. Sau đó Retrofit dùng Handler với MainLooper "
        "để chuyển kết quả đã parse xong về lại Luồng Chính an toàn, giúp giao diện người dùng luôn mượt mà."
    )

    # ==========================================
    # SLIDE 7: DEMO ANDROID TRỰC TIẾP (ĐÀO TRÍ KHANG)
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "DEMO TRỰC TIẾP: ANDROID ĐĂNG KÝ THAM GIA SỰ KIỆN", "06. Demo Nghiệp vụ Di động", 7, "Đào Trí Khang")

    img_reg = os.path.join(EVIDENCE_DIR, "12_android_registration.png")
    if os.path.exists(img_reg):
        s7.shapes.add_picture(img_reg, Inches(1.5), Inches(1.4), height=Inches(5.3))

    box_steps7 = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.5), Inches(1.4), Inches(8.0), Inches(5.3))
    box_steps7.fill.solid()
    box_steps7.fill.fore_color.rgb = C_WHITE
    box_steps7.line.color.rgb = C_BORDER
    tx_st7 = s7.shapes.add_textbox(Inches(4.8), Inches(1.7), Inches(7.4), Inches(4.8))
    tf_st7 = tx_st7.text_frame
    tf_st7.word_wrap = True
    p = tf_st7.paragraphs[0]
    p.text = "QUY TRÌNH THAO TÁC DEMO TRÊN THIẾT BỊ THẬT / MÁY ẢO:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    demo_steps = [
        ("Bước 1: Khởi động & Đăng nhập Sinh viên", "Mở app Visionary Connect -> Đăng nhập tài khoản sinh viên daotrikhang@visionary.dntu.edu.vn -> Nhận JWT Token lưu vào SharedPreferences."),
        ("Bước 2: Gọi API tải danh sách sự kiện CLB", "Màn hình tự động gọi GET /api/events?pageIndex=1&pageSize=20. Hiển thị sự kiện 'Workshop: Master Git, GitHub & CI/CD Actions'."),
        ("Bước 3: Thực hiện thao tác Đăng ký tham gia", "Nhấn nút 'ĐĂNG KÝ NGAY' -> App gửi POST /api/events/{id}/register kèm Header 'Authorization: Bearer <token>'."),
        ("Bước 4: Nhận phản hồi thành công & Mã QR", "Server lưu đăng ký vào bảng EventRegistrations trong PostgreSQL và cấp mã check-in VIS-QR-E4B2A8C1. Giao diện đổi sang trạng thái 'ĐÃ ĐĂNG KÝ'."),
        ("Bước 5: Chuyển giao dữ liệu sang WinForms", "Ngay sau khi Android đăng ký, Ban Chủ Nhiệm mở Windows Forms sẽ thấy tên sinh viên xuất hiện tức thì trong danh sách chờ điểm danh.")
    ]
    for title, desc in demo_steps:
        p = tf_st7.add_paragraph()
        p.text = title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_TEAL
        p2 = tf_st7.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = C_DARK

    s7.notes_slide.notes_text_frame.text = (
        "LỜI THUYẾT TRÌNH (ĐÀO TRÍ KHANG - 1'15\"):\n"
        "Bây giờ em xin thực hiện thao tác demo trực tiếp trên ứng dụng Android đã biên dịch sẵn file app-debug.apk. "
        "Đầu tiên em đăng nhập bằng tài khoản sinh viên. Sau khi đăng nhập thành công, app nhận chuỗi JWT và lưu vào bộ nhớ an toàn SharedPreferences. "
        "Ở màn hình sự kiện, em chọn workshop 'Master Git, GitHub & CI/CD Actions' và bấm nút Đăng ký. "
        "Ứng dụng sẽ gửi HTTP POST tới endpoint /api/events/register kèm mã token. "
        "Server xác thực thành công và trả về mã QR check-in như trên màn hình. "
        "Đồng thời, dữ liệu này đã được ghi nhận ngay lập tức vào cơ sở dữ liệu chung. "
        "Tiếp theo, em xin kính mời bạn Hồ Đoàng Nguyên Khang trình bày chi tiết về máy chủ Web API, Swagger và cơ chế xác thực JWT."
    )

    # ==========================================
    # SLIDE 8: SWAGGER & HỢP ĐỒNG API (HỒ ĐOÀNG NGUYÊN KHANG)
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "SWAGGER UI VÀ HỢP ĐỒNG API NHÓM TIÊU THỤ", "07. Hợp đồng API & Swagger", 8, "Hồ Đoàng Nguyên Khang")

    img_sw = os.path.join(EVIDENCE_DIR, "04_swagger_overview.png")
    if os.path.exists(img_sw):
        s8.shapes.add_picture(img_sw, Inches(0.8), Inches(1.5), width=Inches(5.0))

    table_shape8 = s8.shapes.add_table(7, 4, Inches(6.0), Inches(1.5), Inches(6.5), Inches(5.2))
    t8 = table_shape8.table
    t8.columns[0].width = Inches(1.1)
    t8.columns[1].width = Inches(2.2)
    t8.columns[2].width = Inches(1.4)
    t8.columns[3].width = Inches(1.8)
    for i, h in enumerate(["Method", "Endpoint Route", "Quyền truy cập", "Khuôn phản hồi JSON"]):
        cell = t8.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_WHITE

    api_contract_rows = [
        ("POST", "/api/auth/login", "Công khai (Mở)", "{ token, user }"),
        ("GET", "/api/events", "Công khai (Mở)", "{ items, totalCount }"),
        ("GET", "/api/events/{slug}", "Công khai (Mở)", "{ eventDetail }"),
        ("POST", "/api/events", "Admin, Committee", "{ eventCreated }"),
        ("POST", "/api/events/{id}/register", "Cần đăng nhập", "{ success, message }"),
        ("POST", "/api/events/{id}/attendance", "Admin, Committee", "{ checkInSuccess }")
    ]
    for row_idx, r in enumerate(api_contract_rows, start=1):
        for col_idx, val in enumerate(r):
            cell = t8.cell(row_idx, col_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_WHITE
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(9.5)
            if col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = C_TEAL if val == "GET" else C_BLUE
            elif col_idx == 2:
                p.font.color.rgb = C_RED if "Admin" in val else C_GREEN
            else:
                p.font.color.rgb = C_DARK

    s8.notes_slide.notes_text_frame.text = (
        "LỜI THUYẾT TRÌNH (HỒ ĐOÀNG NGUYÊN KHANG - 1'00\"):\n"
        "Kính chào Thầy và các bạn! Em tên là Hồ Đoàng Nguyên Khang, phụ trách phát triển Web API, tài liệu Swagger và cơ sở dữ liệu. "
        "Bên trái là giao diện Swagger UI thực tế đang chạy trực tuyến tại địa chỉ https://visionary-api-gb51.onrender.com/swagger. "
        "Bảng bên phải là hợp đồng API chính thức mà cả ba ứng dụng đều tuân thủ từng ký tự. "
        "Hợp đồng phân định rõ ràng các mức quyền: "
        "Các endpoint công khai như đăng nhập và xem danh sách sự kiện ai cũng gọi được. "
        "Endpoint đăng ký tham gia sự kiện yêu cầu người dùng phải đăng nhập có JWT token. "
        "Còn các thao tác tạo sự kiện hoặc điểm danh học viên bắt buộc phải có vai trò Admin hoặc Committee. "
        "Mọi tên trường trong JSON đều dùng quy ước camelCase đồng bộ như totalCount, pageIndex, pageSize và items."
    )

    # ==========================================
    # SLIDE 9: XUYÊN SUỐT MỘT YÊU CẦU (HỒ ĐOÀNG NGUYÊN KHANG)
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "XUYÊN SUỐT MỘT YÊU CẦU: TỪ CÚ NHẤP CHUỘT TỚI DATABASE", "08. Luồng Dữ liệu Xuyên suốt", 9, "Hồ Đoàng Nguyên Khang")

    stages = [
        ("Chặng 1: Thao tác Giao diện (UI Event)", "Người dùng nhấn nút Đăng ký (btnRegister) trên Android hoặc Xem chi tiết trên Web.", C_BLUE),
        ("Chặng 2: Client đóng gói Yêu cầu (Network Request)", "Hàm UI gọi lớp ApiClient: Web dùng fetch(), Android dùng Retrofit enqueue(), WinForms dùng HttpClient.SendAsync().", C_TEAL),
        ("Chặng 3: Truyền tải qua Mạng (Network Transfer)", "Gói tin HTTP đi qua Internet tới máy chủ Kestrel cổng 443 kèm Header 'Authorization: Bearer <token>'.", C_NAVY),
        ("Chặng 4: Server tiếp nhận & Xử lý (Controller & DB)", "Middleware xác thực JWT, đọc UserId từ Claims -> Controller gọi EF Core truy vấn và lưu bản ghi vào PostgreSQL.", C_BLUE),
        ("Chặng 5: Đóng gói Phản hồi JSON (Serialization)", "Server bọc kết quả vào ApiResponse<T>, tuần tự hóa JSON UTF-8 camelCase, trả mã HTTP 200 OK (hoặc 201 Created).", C_TEAL),
        ("Chặng 6: Nhận kết quả & Hiển thị (UI Rendering)", "Client nhận JSON, deserialize thành Model DTO, chuyển về Luồng Chính để cập nhật điều khiển giao diện.", C_GREEN)
    ]
    y_pos = 1.45
    for title, desc, color in stages:
        box = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(y_pos), Inches(11.733), Inches(0.82))
        box.fill.solid()
        box.fill.fore_color.rgb = C_WHITE
        box.line.color.rgb = color
        box.line.width = Pt(1.5)

        tx = s9.shapes.add_textbox(Inches(1.0), Inches(y_pos+0.05), Inches(11.3), Inches(0.72))
        tf = tx.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = color
        p1.font.name = "Segoe UI"

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = C_DARK
        p2.font.name = "Segoe UI"

        y_pos += 0.9

    s9.notes_slide.notes_text_frame.text = (
        "LỜI THUYẾT TRÌNH (HỒ ĐOÀNG NGUYÊN KHANG - 1'00\"):\n"
        "Thưa Thầy, để minh họa một chu trình request hoàn chỉnh, nhóm em chọn endpoint GET /api/events và POST /api/events/register "
        "đi qua đủ 6 chặng kỹ thuật: "
        "Chặng 1: Bắt đầu từ cú nhấp chuột của người dùng. "
        "Chặng 2: Client gọi hàm mạng bất đồng bộ tương ứng ở từng ngôn ngữ. "
        "Chặng 3: Gói tin HTTP mang header Authorization gửi tới cổng 443 của máy chủ Kestrel. "
        "Chặng 4: Server xác thực token, kiểm tra hạn chót sự kiện và gọi Entity Framework Core ghi vào PostgreSQL. "
        "Chặng 5: Server đóng gói kết quả dạng JSON UTF-8 trả về cho client. "
        "Chặng 6: Client giải mã JSON, đưa về Luồng Chính và đổ dữ liệu lên màn hình. "
        "Cả ba nền tảng đều đi qua đúng 6 chặng này một cách nhất quán."
    )

    # ==========================================
    # SLIDE 10: XÁC THỰC VÀ PHÂN QUYỀN JWT (HỒ ĐOÀNG NGUYÊN KHANG)
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "XÁC THỰC & PHÂN QUYỀN: VÒNG ĐỜI JWT VÀ BẢO MẬT SERVER", "09. Bảo mật & Xác thực", 10, "Hồ Đoàng Nguyên Khang")

    img_401 = os.path.join(EVIDENCE_DIR, "13_401_response.png")
    if os.path.exists(img_401):
        s10.shapes.add_picture(img_401, Inches(0.8), Inches(1.5), width=Inches(5.6))

    img_403 = os.path.join(EVIDENCE_DIR, "14_403_response.png")
    if os.path.exists(img_403):
        s10.shapes.add_picture(img_403, Inches(6.8), Inches(1.5), width=Inches(5.7))

    card_jwt = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(5.1), Inches(11.733), Inches(1.75))
    card_jwt.fill.solid()
    card_jwt.fill.fore_color.rgb = C_WHITE
    card_jwt.line.color.rgb = C_BORDER
    tx_jwt = s10.shapes.add_textbox(Inches(1.0), Inches(5.15), Inches(11.3), Inches(1.65))
    tf_jwt = tx_jwt.text_frame
    tf_jwt.word_wrap = True
    p = tf_jwt.paragraphs[0]
    p.text = "CÁC NGUYÊN TẮC BẢO MẬT CỐT LÕI ĐƯỢC CHỨNG MINH THỰC TẾ:"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    jwt_principles = [
        "1. JWT không phải là chuỗi mã hóa: Phần Header và Payload chỉ mã hóa Base64URL, ai cũng đọc được nội dung bên trong.",
        "2. Toàn vẹn nhờ Chữ ký số (HMAC-SHA256): Chữ ký được sinh từ Secret Key chỉ Server nắm giữ. Người dùng đổi role sẽ làm sai chữ ký và bị từ chối.",
        "3. Phân biệt 401 vs 403: Mã 401 (Unauthorized) xảy ra khi thiếu token hoặc token hết hạn. Mã 403 (Forbidden) xảy ra khi người dùng hợp lệ nhưng không đủ quyền Admin.",
        "4. Server không bao giờ tin Client: Khi đăng ký sự kiện, Server tự trích xuất UserId từ Claims (ClaimTypes.NameIdentifier) trong token, client không thể mạo danh."
    ]
    for jp in jwt_principles:
        p = tf_jwt.add_paragraph()
        p.text = jp
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_DARK

    s10.notes_slide.notes_text_frame.text = (
        "LỜI THUYẾT TRÌNH (HỒ ĐOÀNG NGUYÊN KHANG - 1'15\"):\n"
        "Về cơ chế xác thực, nhóm em sử dụng JSON Web Token (JWT) theo chuẩn RFC 7519. "
        "Có hai bức ảnh chụp kết quả kiểm thử thực tế trên slide: "
        "Bên trái là mã HTTP 401 Unauthorized khi người dùng gọi endpoint quản trị mà chưa đăng nhập hoặc không gửi kèm Bearer token. "
        "Bên phải là mã HTTP 403 Forbidden: trường hợp này người dùng đã đăng nhập thành công với tài khoản Sinh viên, "
        "nhưng cố tình gọi vào endpoint phân quyền của Admin thì server từ chối ngay. "
        "Điểm mấu chốt: JWT không phải chuỗi mã hóa bí mật mà là chuỗi được ký số. "
        "Nếu người dùng tự ý chỉnh sửa vai trò trong payload, chữ ký số sẽ không khớp và server lập tức chặn lại. "
        "Đồng thời, server luôn tự đọc danh tính người gọi từ token chứ không tin vào tham số client gửi lên."
    )

    # ==========================================
    # SLIDE 11: JSON & DATABASE (HỒ ĐOÀNG NGUYÊN KHANG)
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "JSON, CƠ SỞ DỮ LIỆU & QUYẾT ĐỊNH KỸ THUẬT", "10. Quản lý Dữ liệu & Kiến trúc", 11, "Hồ Đoàng Nguyên Khang")

    # 3 Cards
    cards11 = [
        ("VAI TRÒ CỦA DTO TRONG HỆ THỐNG", [
            "• Không bao giờ trả Entity trực tiếp ra ngoài.",
            "• Che giấu thông tin nhạy cảm: PasswordHash, thông tin nội bộ.",
            "• Tránh lỗi đệ quy vòng lặp JSON (Cyclic Reference) giữa các bảng có quan hệ 1-N trong Entity Framework.",
            "• Giảm tải băng thông mạng: Chỉ truyền những trường giao diện thực sự cần."
        ], C_BLUE),
        ("PHÂN TRANG PHÍA SERVER (PAGEDRESPONSE)", [
            "• Không bao giờ tải hàng nghìn bản ghi vào RAM server.",
            "• Câu lệnh SQL thực thi trực tiếp OFFSET và LIMIT trên PostgreSQL.",
            "• Trả về vỏ phân trang chuẩn gồm: totalCount, pageIndex, pageSize, totalPages và mảng items.",
            "• Sắp xếp ổn định (Tie-breaker): OrderBy(Date).ThenBy(Id) chống trùng bản ghi giữa các trang."
        ], C_TEAL),
        ("CƠ SỞ DỮ LIỆU CLOUD POSTGRESQL", [
            "• Đám mây Supabase PostgreSQL 16.3 tại trung tâm dữ liệu Singapore (ap-southeast-1).",
            "• Kết nối qua IPv4 Connection Pooler cổng 5432 để Render container kết nối ổn định.",
            "• Sử dụng AsNoTracking() cho tất cả truy vấn chỉ đọc để tăng tốc độ phản hồi.",
            "• Toàn bộ dữ liệu 4 danh mục và sự kiện đều là dữ liệu thật, không có mock data."
        ], C_GREEN)
    ]
    cx = 0.8
    for title, items, color in cards11:
        box = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(cx), Inches(1.5), Inches(3.7), Inches(5.2))
        box.fill.solid()
        box.fill.fore_color.rgb = C_WHITE
        box.line.color.rgb = color
        box.line.width = Pt(1.5)

        tx = s11.shapes.add_textbox(Inches(cx+0.15), Inches(1.7), Inches(3.4), Inches(4.8))
        tf = tx.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = color

        for it in items:
            p = tf.add_paragraph()
            p.text = it
            p.font.size = Pt(10)
            p.font.color.rgb = C_DARK
            p.space_after = Pt(8)

        cx += 4.0

    s11.notes_slide.notes_text_frame.text = (
        "LỜI THUYẾT TRÌNH (HỒ ĐOÀNG NGUYÊN KHANG - 1'00\"):\n"
        "Ở tầng dữ liệu, nhóm em đưa ra ba quyết định kỹ thuật quan trọng: "
        "Thứ nhất: Luôn sử dụng DTO (Data Transfer Object) để tách biệt hoàn toàn giữa cơ sở dữ liệu và giao diện. "
        "DTO giúp bảo mật trường mật khẩu đã băm và triệt tiêu lỗi vòng lặp tuần tự hóa JSON. "
        "Thứ hai: Cơ chế phân trang PagedResponse bắt buộc thực thi ở cấp cơ sở dữ liệu qua Skip và Take, "
        "kèm tiêu chí sắp xếp phụ tie-breaker để đảm bảo dữ liệu không bị trùng giữa các trang. "
        "Thứ ba: Cơ sở dữ liệu PostgreSQL đặt tại Singapore kết nối qua Connection Pooler IPv4 "
        "đảm bảo thời gian phản hồi dưới 100ms. "
        "Sau đây, em xin kính mời bạn Võ Ngọc Minh Đạt trình bày ứng dụng Windows Forms và tổng kết bài báo cáo."
    )

    # ==========================================
    # SLIDE 12: WINDOWS FORMS C# (VÕ NGỌC MINH ĐẠT)
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "ỨNG DỤNG DESKTOP: WINDOWS FORMS C# (.NET 8)", "11. Ứng dụng Khách (Desktop)", 12, "Võ Ngọc Minh Đạt")

    img_win = os.path.join(EVIDENCE_DIR, "08_winforms_dashboard.png")
    if os.path.exists(img_win):
        s12.shapes.add_picture(img_win, Inches(0.8), Inches(1.5), width=Inches(5.8))

    table_shape12 = s12.shapes.add_table(5, 3, Inches(6.9), Inches(1.5), Inches(5.6), Inches(1.8))
    t12 = table_shape12.table
    t12.columns[0].width = Inches(1.6)
    t12.columns[1].width = Inches(1.8)
    t12.columns[2].width = Inches(2.2)
    for i, h in enumerate(["Tên điều khiển", "Loại điều khiển", "Vai trò nghiệp vụ"]):
        cell = t12.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_WHITE

    ctrl_rows12 = [
        ("_dgvEvents", "DataGridView", "Hiển thị danh sách sự kiện và số lượng đăng ký"),
        ("_dgvRegistrations", "DataGridView", "Danh sách sinh viên đăng ký để điểm danh"),
        ("btnCheckIn", "Button", "Xác nhận điểm danh sinh viên tham gia"),
        ("btnRefresh", "Button", "Tải lại dữ liệu mới nhất từ Web API")
    ]
    for row_idx, r in enumerate(ctrl_rows12, start=1):
        for col_idx, val in enumerate(r):
            cell = t12.cell(row_idx, col_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_WHITE
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(9.5)
            p.font.color.rgb = C_DARK

    code_box12 = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.9), Inches(3.5), Inches(5.6), Inches(3.2))
    code_box12.fill.solid()
    code_box12.fill.fore_color.rgb = C_NAVY
    code_box12.line.color.rgb = C_TEAL
    tx_c12 = s12.shapes.add_textbox(Inches(7.0), Inches(3.55), Inches(5.4), Inches(3.1))
    tf_c12 = tx_c12.text_frame
    tf_c12.word_wrap = True
    p = tf_c12.paragraphs[0]
    p.text = "// MainForm.cs – Tải danh sách đăng ký bằng async/await (Mã nguồn thật):"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    code_lines12 = [
        "private async Task LoadEventRegistrationsAsync(Guid eventId)",
        "{",
        "    var list = await ApiClient.GetEventRegistrationsAsync(eventId);",
        "    _dgvRegistrations.DataSource = null;",
        "    _dgvRegistrations.DataSource = list.Select(r => new {",
        "        MSSV = r.StudentId ?? 'N/A',",
        "        SinhVien = r.FullName, Email = r.Email,",
        "        TrangThai = r.IsAttended ? 'Đã điểm danh' : 'Chưa điểm danh'",
        "    }).ToList();",
        "}"
    ]
    for cl in code_lines12:
        p = tf_c12.add_paragraph()
        p.text = cl
        p.font.size = Pt(9)
        p.font.color.rgb = RGBColor(226, 232, 240)
        p.font.name = "Consolas"

    s12.notes_slide.notes_text_frame.text = (
        "LỜI THUYẾT TRÌNH (VÕ NGỌC MINH ĐẠT - 1'00\"):\n"
        "Kính chào Thầy và các bạn! Em tên là Võ Ngọc Minh Đạt, phụ trách ứng dụng Windows Forms C# trên .NET 8. "
        "Đây là phần mềm chuyên dụng dành riêng cho Ban Chủ Nhiệm CLB để quản lý thành viên và điểm danh sự kiện trên máy tính văn phòng. "
        "Giao diện sử dụng các điều khiển DataGridView tiêu chuẩn. "
        "Đoạn mã bên phải thể hiện hàm nạp danh sách đăng ký sự kiện. "
        "Trong C#, nhóm em sử dụng từ khóa async và await kết hợp với HttpClient tĩnh duy nhất. "
        "Từ khóa await giúp nhường quyền điều khiển cho luồng giao diện trong lúc chờ máy chủ phản hồi, "
        "và tự động quay về đúng SynchronizationContext của UI khi có dữ liệu. "
        "Nhờ vậy, cửa sổ ứng dụng không bao giờ bị đơ (Not Responding) và tuyệt đối tránh lỗi Deadlock do gọi .Result."
    )

    # ==========================================
    # SLIDE 13: DEMO WINFORMS TRỰC TIẾP (VÕ NGỌC MINH ĐẠT)
    # ==========================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "DEMO TRỰC TIẾP: WINFORMS ĐIỂM DANH SỰ KIỆN", "12. Demo Nghiệp vụ Desktop", 13, "Võ Ngọc Minh Đạt")

    img_wev = os.path.join(EVIDENCE_DIR, "09_winforms_events.png")
    if os.path.exists(img_wev):
        s13.shapes.add_picture(img_wev, Inches(0.8), Inches(1.5), width=Inches(6.8))

    box_steps13 = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.9), Inches(1.5), Inches(4.6), Inches(5.2))
    box_steps13.fill.solid()
    box_steps13.fill.fore_color.rgb = C_WHITE
    box_steps13.line.color.rgb = C_BORDER
    tx_st13 = s13.shapes.add_textbox(Inches(8.1), Inches(1.7), Inches(4.2), Inches(4.8))
    tf_st13 = tx_st13.text_frame
    tf_st13.word_wrap = True
    p = tf_st13.paragraphs[0]
    p.text = "KỊCH BẢN ĐIỂM DANH ĐỒNG BỘ 3 NỀN TẢNG:"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    demo_steps13 = [
        ("1. BCN Đăng nhập hệ thống", "Đăng nhập tài khoản BCN vongocminhdat@visionary.dntu.edu.vn."),
        ("2. Chọn Sự kiện cần kiểm tra", "Bấm chọn workshop 'Master Git, GitHub & CI/CD Actions' trên grid _dgvEvents."),
        ("3. Tải danh sách Sinh viên đăng ký", "Grid _dgvRegistrations hiển thị ngay sinh viên vừa đăng ký từ ứng dụng Android ở Slide 7."),
        ("4. Thực hiện Điểm danh (Check-in)", "Chọn sinh viên và bấm 'Xác nhận Điểm danh'. Ứng dụng gửi POST /api/events/{id}/attendance."),
        ("5. Đồng bộ tức thời lên Web", "Trạng thái đổi thành 'Đã điểm danh'. Khi mở Web hoặc Android xem lại, trạng thái đã được cập nhật đồng bộ 100%.")
    ]
    for title, desc in demo_steps13:
        p = tf_st13.add_paragraph()
        p.text = title
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = C_TEAL
        p2 = tf_st13.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = C_DARK

    s13.notes_slide.notes_text_frame.text = (
        "LỜI THUYẾT TRÌNH (VÕ NGỌC MINH ĐẠT - 1'15\"):\n"
        "Sau khi bạn Trí Khang vừa bấm đăng ký sự kiện trên ứng dụng Android, "
        "bây giờ em mở bản chạy thật của ứng dụng Windows Forms đã biên dịch sẵn trong thư mục Release. "
        "Em đăng nhập bằng tài khoản Ban Chủ Nhiệm và chuyển sang tab 'Sự kiện & Điểm danh'. "
        "Khi em bấm vào workshop Git, bảng đăng ký phía dưới hiển thị ngay thông tin sinh viên vừa đăng ký từ điện thoại di động. "
        "Em bấm nút 'Xác nhận Điểm danh'. Ứng dụng gửi yêu cầu POST tới Web API. "
        "Server kiểm tra quyền của em và ghi nhận thời gian điểm danh vào cơ sở dữ liệu. "
        "Ngay lập tức, cột trạng thái chuyển sang 'Đã điểm danh'. "
        "Điều này chứng minh ba ứng dụng tương tác hoàn hảo trên cùng một nguồn dữ liệu thông qua Web API duy nhất."
    )

    # ==========================================
    # SLIDE 14: BA CHỖ BUỘC PHẢI KHÁC NHAU (VÕ NGỌC MINH ĐẠT)
    # ==========================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "BA CHỖ BUỘC PHẢI KHÁC NHAU GIỮA BA NỀN TẢNG", "13. So sánh Đa Nền tảng", 14, "Võ Ngọc Minh Đạt")

    table_shape14 = s14.shapes.add_table(5, 4, Inches(0.8), Inches(1.5), Inches(11.733), Inches(3.6))
    t14 = table_shape14.table
    t14.columns[0].width = Inches(2.733)
    t14.columns[1].width = Inches(3.0)
    t14.columns[2].width = Inches(3.0)
    t14.columns[3].width = Inches(3.0)
    for i, h in enumerate(["Tiêu chí Kỹ thuật", "Web (Next.js / TS)", "Windows Forms (C#)", "Android (Java Native)"]):
        cell = t14.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_WHITE

    diff_rows = [
        ("1. Thư viện Mạng & Mô hình Bất đồng bộ", "fetch() + async/await\n(Promise-based, Event Loop)", "HttpClient + async/await\n(Task<T>, State Machine)", "Retrofit 2 + OkHttp 3\n(enqueue() Callback trên Worker Thread)"),
        ("2. Cơ chế Điều phối Luồng Giao diện", "Trình duyệt tự xử lý\n(Single-threaded Event Loop)", "SynchronizationContext\n(Tự quay về UI thread sau await)", "Handler(Looper.getMainLooper())\n(Bắt buộc chuyển luồng thủ công)"),
        ("3. Lưu trữ Token & Kết nối", "localStorage / Cookie\n(Chặn CORS, dùng relative /api)", "AppState tĩnh trong RAM\n(Không bị ảnh hưởng bởi CORS)", "SharedPreferences mã hóa\n(Dùng 10.0.2.2 máy ảo / Cloud HTTPS)"),
        ("ĐIỀU BUỘC PHẢI GIỐNG HỆT NHAU", "Cùng gọi chung một hợp đồng Web API: Đường dẫn endpoint, Phương thức HTTP (GET, POST, PUT, DELETE), Khuôn JSON DTO và Mã trạng thái HTTP (200, 201, 204, 400, 401, 403, 404, 500).", "", "")
    ]
    for row_idx, r in enumerate(diff_rows, start=1):
        if row_idx == 4:
            cell = t14.cell(row_idx, 0)
            cell.text = r[0]
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_NAVY
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = C_TEAL

            cell_span = t14.cell(row_idx, 1)
            cell_span.text = r[1]
            cell_span.fill.solid()
            cell_span.fill.fore_color.rgb = C_WHITE
            p = cell_span.text_frame.paragraphs[0]
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = C_DARK
            # fill rest of row
            for ci in [2, 3]:
                t14.cell(row_idx, ci).fill.solid()
                t14.cell(row_idx, ci).fill.fore_color.rgb = C_WHITE
        else:
            for col_idx, val in enumerate(r):
                cell = t14.cell(row_idx, col_idx)
                cell.text = val
                cell.fill.solid()
                cell.fill.fore_color.rgb = C_WHITE
                p = cell.text_frame.paragraphs[0]
                p.font.size = Pt(9.5)
                p.font.color.rgb = C_DARK

    card_diff_note = s14.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(5.35), Inches(11.733), Inches(1.5))
    card_diff_note.fill.solid()
    card_diff_note.fill.fore_color.rgb = C_WHITE
    card_diff_note.line.color.rgb = C_BORDER
    tx_dn = s14.shapes.add_textbox(Inches(1.0), Inches(5.4), Inches(11.3), Inches(1.4))
    tf_dn = tx_dn.text_frame
    p = tf_dn.paragraphs[0]
    p.text = "KẾT LUẬN QUAN TRỌNG VỀ TÁCH TẦNG WEB API:"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p2 = tf_dn.add_paragraph()
    p2.text = "Sự khác biệt về cú pháp, tên hàm và thư viện mạng là do đặc thù ngôn ngữ và hệ điều hành bắt buộc. " \
              "Web API hoàn toàn độc lập và không quan tâm bên kia là trình duyệt, máy tính hay điện thoại. " \
              "Chỉ cần client tuân thủ đúng hợp đồng API, hệ thống sẽ hoạt động đồng nhất."
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = C_MUTED

    s14.notes_slide.notes_text_frame.text = (
        "LỜI THUYẾT TRÌNH (VÕ NGỌC MINH ĐẠT - 1'00\"):\n"
        "Thưa Thầy, một câu hỏi cốt lõi của học phần là: Điều gì buộc phải giống nhau và điều gì buộc phải khác nhau giữa ba ứng dụng? "
        "Nhóm em đã tổng hợp rõ trong bảng đối chiếu: "
        "Ba chỗ buộc phải khác nhau: "
        "Thứ nhất là thư viện mạng: JavaScript dùng fetch, C# dùng HttpClient, Java dùng Retrofit và OkHttp. "
        "Thứ hai là cơ chế điều phối luồng: Android bắt buộc dùng Handler để đưa về Luồng Chính, "
        "trong khi C# có async/await tự động quay về UI context, và trình duyệt chạy theo mô hình Event Loop. "
        "Thứ ba là lưu trữ token: Web dùng localStorage, WinForms dùng RAM tĩnh, Android dùng SharedPreferences. "
        "Ngược lại, điều bắt buộc phải giống nhau tuyệt đối là Hợp đồng API: "
        "đường dẫn, phương thức HTTP, khuôn JSON và mã trạng thái. "
        "Đây chính là sức mạnh của kiến trúc tách tầng Web API."
    )

    # ==========================================
    # SLIDE 15: SỰ CỐ THẬT VÀ KHẮC PHỤC (VÕ NGỌC MINH ĐẠT)
    # ==========================================
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "SỰ CỐ THẬT VÀ QUY TRÌNH CHẨN ĐOÁN – SỬA LỖI", "14. Xử lý Sự cố Kỹ thuật", 15, "Võ Ngọc Minh Đạt")

    img_err = os.path.join(EVIDENCE_DIR, "15_real_error_log.png")
    if os.path.exists(img_err):
        s15.shapes.add_picture(img_err, Inches(0.8), Inches(1.5), width=Inches(5.6))

    img_fix = os.path.join(EVIDENCE_DIR, "16_error_fixed_test.png")
    if os.path.exists(img_fix):
        s15.shapes.add_picture(img_fix, Inches(6.8), Inches(1.5), width=Inches(5.7))

    card_diag = s15.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(5.1), Inches(11.733), Inches(1.75))
    card_diag.fill.solid()
    card_diag.fill.fore_color.rgb = C_WHITE
    card_diag.line.color.rgb = C_BORDER
    tx_dg = s15.shapes.add_textbox(Inches(1.0), Inches(5.15), Inches(11.3), Inches(1.65))
    tf_dg = tx_dg.text_frame
    p = tf_dg.paragraphs[0]
    p.text = "QUY TRÌNH 4 BƯỚC KHẮC PHỤC SỰ CỐ THEO ĐÚNG CHUẨN KỸ THUẬT:"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    fix_steps = [
        "1. Đọc thông điệp lỗi nguyên văn: error NETSDK1100: To build a project targeting Windows on this operating system, set the EnableWindowsTargeting property to true.",
        "2. Xác định nguyên nhân gốc rễ: File solution gốc backend/Visionary.sln bao gồm cả dự án WinForms (.NET 8 Windows Desktop), khi chạy trên GitHub Actions runner Ubuntu Linux thì bị từ chối biên dịch.",
        "3. Thực hiện sửa đổi kiến trúc: Tách thành backend/Visionary.Backend.sln độc lập chỉ chứa Core, Infrastructure, Api và Tests. Cấu hình pipeline riêng desktop.yml trên máy ảo windows-latest.",
        "4. Kiểm chứng hồi quy: Chạy lại toàn bộ 15 bài kiểm thử xUnit và CI pipeline -> Kết quả Build Succeeded 0 Warning, 0 Error, Passed 15/15 Tests (Ảnh bên phải)."
    ]
    for fs in fix_steps:
        p = tf_dg.add_paragraph()
        p.text = fs
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_DARK

    s15.notes_slide.notes_text_frame.text = (
        "LỜI THUYẾT TRÌNH (VÕ NGỌC MINH ĐẠT - 1'00\"):\n"
        "Trong quá trình xây dựng pipeline CI/CD tự động, nhóm em đã gặp một sự cố thật rất điển hình. "
        "Bên trái là log lỗi nguyên văn từ GitHub Actions: NETSDK1100. "
        "Lỗi xảy ra vì file solution chung chứa cả dự án Windows Forms, khi đưa lên máy ảo Ubuntu Linux của GitHub Actions để build API, "
        "hệ điều hành Linux từ chối biên dịch các thư viện giao diện Windows. "
        "Nhóm em đã tự phân tích và khắc phục triệt để bằng cách tách riêng một solution Visionary.Backend.sln độc lập cho backend, "
        "còn dự án Windows Forms được biên dịch trong workflow riêng chạy trên máy ảo Windows. "
        "Sau khi sửa, toàn bộ 15 bài test tự động đều vượt qua 100% như hình bên phải."
    )

    # ==========================================
    # SLIDE 16: GIỚI HẠN & HƯỚNG PHÁT TRIỂN (VÕ NGỌC MINH ĐẠT)
    # ==========================================
    s16 = prs.slides.add_slide(blank_layout)
    add_header(s16, "GIỚI HẠN THỰC TẾ, HƯỚNG PHÁT TRIỂN & KẾT LUẬN", "15. Đánh giá & Hướng phát triển", 16, "Võ Ngọc Minh Đạt")

    card_lim = s16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(4.2))
    card_lim.fill.solid()
    card_lim.fill.fore_color.rgb = C_WHITE
    card_lim.line.color.rgb = C_BORDER
    tx_lim = s16.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(3.8))
    tf_lim = tx_lim.text_frame
    p = tf_lim.paragraphs[0]
    p.text = "BA GIỚI HẠN THỰC TẾ CỦA HỆ THỐNG HIỆN TẠI"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_RED

    lims = [
        "1. Chưa có thông báo đẩy thời gian thực (Push Notification):",
        "   Khi BCN điểm danh hoặc có sự kiện mới, sinh viên chưa nhận được thông báo qua Firebase Cloud Messaging (FCM) hoặc SignalR.",
        "2. Chưa hỗ trợ Offline Caching hoàn chỉnh trên Android:",
        "   Khi mất kết nối Internet, ứng dụng Android chưa lưu đệm danh sách sự kiện vào SQLite cục bộ (Room Database).",
        "3. Một chỗ mã nguồn chưa tối ưu:",
        "   Cơ chế Refresh Token tự động khi JWT 4 giờ hết hạn chưa được triển khai hoàn chỉnh, người dùng vẫn phải đăng nhập lại."
    ]
    for lm in lims:
        p = tf_lim.add_paragraph()
        p.text = lm
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_DARK

    card_plan = s16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(4.2))
    card_plan.fill.solid()
    card_plan.fill.fore_color.rgb = C_WHITE
    card_plan.line.color.rgb = C_BORDER
    tx_plan = s16.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.3), Inches(3.8))
    tf_plan = tx_plan.text_frame
    p = tf_plan.paragraphs[0]
    p.text = "KẾ HOẠCH NẾU CÓ THÊM 2 TUẦN NỮA"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    plans = [
        "1. Tích hợp SignalR Hub vào ASP.NET Core:",
        "   Cập nhật danh sách điểm danh thời gian thực giữa Windows Forms và Android mà không cần người dùng bấm làm mới.",
        "2. Triển khai Room Database trên Android:",
        "   Lưu trữ ngoại tuyến danh sách tài liệu English for IT và sự kiện đã tải để sinh viên xem lại khi không có mạng.",
        "3. Hoàn thiện quy trình Refresh Token với HttpOnly Cookie:",
        "   Tự động cấp lại token mới khi token cũ hết hạn, nâng cao trải nghiệm người dùng."
    ]
    for pl in plans:
        p = tf_plan.add_paragraph()
        p.text = pl
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_DARK

    box_end = s16.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(5.85), Inches(11.733), Inches(1.05))
    box_end.fill.solid()
    box_end.fill.fore_color.rgb = C_NAVY
    tx_end = s16.shapes.add_textbox(Inches(1.0), Inches(5.95), Inches(11.3), Inches(0.85))
    tf_end = tx_end.text_frame
    p_end = tf_end.paragraphs[0]
    p_end.alignment = PP_ALIGN.CENTER
    p_end.text = "CHÂN THÀNH CẢM ƠN THẦY VÀ CÁC BẠN ĐÃ LẮNG NGHE BÀI BÁO CÁO CỦA NHÓM VISIONARY API!"
    p_end.font.size = Pt(13)
    p_end.font.bold = True
    p_end.font.color.rgb = C_TEAL
    p_end.font.name = "Segoe UI"

    p_end2 = tf_end.add_paragraph()
    p_end2.alignment = PP_ALIGN.CENTER
    p_end2.text = "Nhóm chúng em rất mong nhận được những câu hỏi phản biện và đóng góp quý báu từ Thầy để hoàn thiện sản phẩm."
    p_end2.font.size = Pt(10)
    p_end2.font.color.rgb = C_WHITE
    p_end2.font.name = "Segoe UI"

    s16.notes_slide.notes_text_frame.text = (
        "LỜI THUYẾT TRÌNH (VÕ NGỌC MINH ĐẠT - 45s):\n"
        "Kính thưa Thầy, biết mình chưa làm được gì là một dạng hiểu biết chứ không phải lời thú tội. "
        "Dù hệ thống đã chạy tốt các chức năng chính, nhóm em thẳng thắn nhìn nhận ba hạn chế thực tế: "
        "chưa có thông báo đẩy thời gian thực, chưa có bộ nhớ đệm offline Room DB trên Android, "
        "và cơ chế refresh token cần được tự động hóa tốt hơn. "
        "Nếu có thêm hai tuần, nhóm em sẽ ưu tiên tích hợp SignalR và Room DB để nâng cao độ bền vững của ứng dụng. "
        "Đến đây, nhóm VISIONARY API xin kết thúc bài thuyết trình. "
        "Chúng em xin chân thành cảm ơn Thầy và các bạn đã chú ý lắng nghe. "
        "Nhóm chúng em sẵn sàng bước vào phần trả lời câu hỏi phản biện ạ!"
    )

    output_path = "deliverables/VISIONARY_TH71108_FINAL_PRESENTATION.pptx"
    prs.save(output_path)
    print(f"Master 16-Slide Presentation generated successfully at: {output_path}")

generate_master_presentation()
