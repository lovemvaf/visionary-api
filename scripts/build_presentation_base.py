import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # Blank layout

    # Colors
    C_NAVY = RGBColor(15, 23, 42)       # #0F172A
    C_BLUE = RGBColor(34, 100, 172)     # #2264AC
    C_TEAL = RGBColor(34, 166, 161)     # #22A6A1
    C_BG = RGBColor(248, 250, 252)      # #F8FAFC
    C_WHITE = RGBColor(255, 255, 255)
    C_DARK = RGBColor(30, 41, 59)       # #1E293B
    C_MUTED = RGBColor(100, 116, 139)   # #64748B
    C_LIGHT_BG = RGBColor(241, 245, 249) # #F1F5F9
    C_GREEN = RGBColor(22, 163, 74)
    C_RED = RGBColor(220, 38, 38)

    LOGO_DNTU = os.path.abspath("assets/logos/dntu_logo.png")
    LOGO_CNTT = os.path.abspath("assets/logos/cntt_dntu_logo.png")
    EVIDENCE_DIR = os.path.abspath("deliverables/evidence")

    def add_header(slide, title_text, category_text, slide_num, speaker_name):
        # Background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG
        bg.line.fill.background()

        # Header bar
        header_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(1.15))
        header_shape.fill.solid()
        header_shape.fill.fore_color.rgb = C_WHITE
        header_shape.line.color.rgb = RGBColor(226, 232, 240)
        header_shape.line.width = Pt(1)

        # Teal top accent line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.06))
        line.fill.solid()
        line.fill.fore_color.rgb = C_TEAL
        line.line.fill.background()

        # Category & Title text
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
        p2.font.size = Pt(20)
        p2.font.bold = True
        p2.font.color.rgb = C_NAVY
        p2.font.name = "Segoe UI"

        # Logos at header right
        if os.path.exists(LOGO_DNTU):
            slide.shapes.add_picture(LOGO_DNTU, Inches(11.4), Inches(0.15), height=Inches(0.85))
        if os.path.exists(LOGO_CNTT):
            slide.shapes.add_picture(LOGO_CNTT, Inches(12.1), Inches(0.15), height=Inches(0.85))

        # Footer
        footer = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(7.05), Inches(13.333), Inches(0.45))
        footer.fill.solid()
        footer.fill.fore_color.rgb = C_WHITE
        footer.line.color.rgb = RGBColor(226, 232, 240)

        ft_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.1), Inches(11.733), Inches(0.35))
        ft_tf = ft_box.text_frame
        ft_tf.margin_top = ft_tf.margin_left = ft_tf.margin_right = ft_tf.margin_bottom = 0
        fp = ft_tf.paragraphs[0]
        fp.text = f"VISIONARY API – TH71108 Web API (DNTU) | Người trình bày: {speaker_name} | Slide {slide_num}/16"
        fp.font.size = Pt(10)
        fp.font.color.rgb = C_MUTED
        fp.font.name = "Segoe UI"

    # ==========================================
    # SLIDE 1: TRANG BÌA (COVER)
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = C_NAVY
    bg1.line.fill.background()

    # Logos on cover
    if os.path.exists(LOGO_DNTU):
        s1.shapes.add_picture(LOGO_DNTU, Inches(1.0), Inches(0.8), height=Inches(1.2))
    if os.path.exists(LOGO_CNTT):
        s1.shapes.add_picture(LOGO_CNTT, Inches(2.2), Inches(0.8), height=Inches(1.2))

    # University & Department text
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

    # Project Title
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

    # Members card
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

    # AI Declaration & URLs Footer
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
        "Kính chào Thầy và các bạn! Em tên là Quách Khoa Đức, đại diện nhóm VISIONARY API gồm 4 thành viên: "
        "em, bạn Đào Trí Khang, bạn Hồ Đoàng Nguyên Khang và bạn Võ Ngọc Minh Đạt. "
        "Hôm nay nhóm em xin báo cáo đồ án học phần Web API với đề tài: VISIONARY – Hệ thống Quản lý Hoạt động Hội nhập. "
        "Đề tài của nhóm em xây dựng một Web API duy nhất bằng ASP.NET Core 8, phục vụ đồng bộ cho ba ứng dụng: "
        "Website Next.js, Desktop Windows Forms và Mobile Android Native. Sau đây em xin bắt đầu phần giới thiệu bài toán và kiến trúc."
    )

    # ==========================================
    # SLIDE 2: BÀI TOÁN & MỤC TIÊU
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "BÀI TOÁN THỰC TẾ & MỤC TIÊU HỆ THỐNG", "01. Giới thiệu Đề tài", 2, "Quách Khoa Đức")

    # Card 1: Vấn đề thực tế
    card1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2))
    card1.fill.solid()
    card1.fill.fore_color.rgb = C_WHITE
    card1.line.color.rgb = RGBColor(226, 232, 240)
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
        "   CLB Tiếng Anh và các hoạt động hội nhập tại DNTU trước đây chủ yếu quản lý qua Google Form/Sheets, dễ nhầm lẫn và thất lạc dữ liệu.",
        "2. Thiếu cổng thông tin công nghệ & cơ hội:",
        "   Sinh viên CNTT thiếu kênh tiếp cận học thuật English for IT, Radar công nghệ mở (GitHub/Hugging Face) và các cuộc thi Hackathon quốc tế.",
        "3. Trải nghiệm không đồng bộ trên các thiết bị:",
        "   Sinh viên dùng điện thoại di động, Ban Chủ Nhiệm quản trị trên laptop Windows, khách truy cập tra cứu trên Web."
    ]
    for pr in problems:
        p = tf1.add_paragraph()
        p.text = pr
        p.font.size = Pt(11)
        p.font.color.rgb = C_DARK

    # Card 2: Mục tiêu giải pháp
    card2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.2))
    card2.fill.solid()
    card2.fill.fore_color.rgb = C_WHITE
    card2.line.color.rgb = RGBColor(226, 232, 240)
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
        "   Sử dụng ASP.NET Core 8 Web API làm hạt nhân xử lý toàn bộ logic nghiệp vụ, xác thực JWT và kết nối PostgreSQL.",
        "2. Phục vụ ba ứng dụng khách (Clients) chuyên biệt:",
        "   - Web Next.js: Cổng thông tin công khai, tin tức hội nhập, tra cứu sự kiện, English for IT.",
        "   - Windows Forms C#: Phần mềm quản trị dành cho BCN CLB: quản lý thành viên, duyệt đơn, điểm danh sự kiện.",
        "   - Android Native Java: Ứng dụng di động sinh viên: xem sự kiện, đăng ký tham gia, nhận mã QR check-in.",
        "3. Đảm bảo toàn vẹn dữ liệu (Data Integrity):",
        "   Không dùng dữ liệu mẫu (mock/fallback), bảo mật bản nháp, phân quyền chặt chẽ theo vai trò (RBAC)."
    ]
    for sol in solutions:
        p = tf2.add_paragraph()
        p.text = sol
        p.font.size = Pt(11)
        p.font.color.rgb = C_DARK

    s2.notes_slide.notes_text_frame.text = (
        "LỜI THUYẾT TRÌNH (QUÁCH KHOA ĐỨC - 1'00\"):\n"
        "Thưa Thầy, lý do nhóm em chọn đề tài VISIONARY xuất phát từ nhu cầu rất thực tế của Câu lạc bộ Tiếng Anh và sinh viên DNTU. "
        "Trước đây, việc quản lý thành viên, duyệt đơn đăng ký và điểm danh sự kiện hoàn toàn làm thủ công qua file tính. "
        "Sinh viên cũng thiếu một cổng tập trung để học tiếng Anh chuyên ngành IT và cập nhật các cuộc thi quốc tế. "
        "Mục tiêu của dự án VISIONARY là xây dựng một Web API trung tâm duy nhất trên ASP.NET Core 8 kết nối cơ sở dữ liệu PostgreSQL. "
        "Từ API này, hệ thống phục vụ đồng bộ cho ba giao diện: Web Next.js cho sinh viên tra cứu, Android di động để đăng ký sự kiện tiện lợi, "
        "và Windows Forms để Ban Chủ Nhiệm quản trị và điểm danh nhanh chóng. Tất cả dùng chung dữ liệu nên không bao giờ bị lệch số liệu."
    )

    # ==========================================
    # SLIDE 3: KIẾN TRÚC MỘT API, BA ỨNG DỤNG
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "KIẾN TRÚC HỆ THỐNG: MỘT WEB API, BA NỀN TẢNG", "02. Kiến trúc Hệ sinh thái", 3, "Quách Khoa Đức")

    # Architecture Boxes & Arrows
    # Client 1: Web
    b_web = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(3.2), Inches(1.3))
    b_web.fill.solid()
    b_web.fill.fore_color.rgb = C_WHITE
    b_web.line.color.rgb = C_BLUE
    b_web.line.width = Pt(2)
    s3.shapes.add_textbox(Inches(0.9), Inches(1.7), Inches(3.0), Inches(1.1)).text_frame.text = (
        "ỨNG DỤNG WEB (Next.js 14)\nChạy: Trình duyệt (Vercel Cloud)\nCổng: HTTPS 443 (Local: 3000)"
    )

    # Client 2: WinForms
    b_win = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.3), Inches(3.2), Inches(1.3))
    b_win.fill.solid()
    b_win.fill.fore_color.rgb = C_WHITE
    b_win.line.color.rgb = C_TEAL
    b_win.line.width = Pt(2)
    s3.shapes.add_textbox(Inches(0.9), Inches(3.4), Inches(3.0), Inches(1.1)).text_frame.text = (
        "ỨNG DỤNG WINDOWS FORMS (C#)\nChạy: Máy tính Windows (Desktop)\nCổng gọi ra: HTTPS 443"
    )

    # Client 3: Android
    b_and = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.0), Inches(3.2), Inches(1.3))
    b_and.fill.solid()
    b_and.fill.fore_color.rgb = C_WHITE
    b_and.line.color.rgb = C_GREEN
    b_and.line.width = Pt(2)
    s3.shapes.add_textbox(Inches(0.9), Inches(5.1), Inches(3.0), Inches(1.1)).text_frame.text = (
        "ỨNG DỤNG ANDROID (Java Native)\nChạy: Máy ảo / Điện thoại thật\nGateway ảo: 10.0.2.2 / HTTPS Cloud"
    )

    # Center: Backend API
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

    # Database: Supabase PostgreSQL
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

    # Explanation Card below
    card_exp = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.4), Inches(5.7), Inches(7.1), Inches(1.1))
    card_exp.fill.solid()
    card_exp.fill.fore_color.rgb = C_WHITE
    card_exp.line.color.rgb = RGBColor(226, 232, 240)
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
        "Đây là sơ đồ kiến trúc tổng thể của hệ thống VISIONARY. "
        "Ở trung tâm là máy chủ ASP.NET Core 8 Web API chạy trên Kestrel. "
        "Cả ba ứng dụng khách đều giao tiếp với API qua giao thức HTTP/HTTPS chuẩn RESTful. "
        "Website Next.js chạy trên trình duyệt gọi qua cổng 443 hoặc qua BFF route handler. "
        "Ứng dụng Windows Forms chạy trực tiếp trên máy tính Windows gọi tới API bằng HttpClient. "
        "Còn ứng dụng Android khi chạy máy ảo sử dụng địa chỉ 10.0.2.2 để kết nối vào máy chủ, "
        "vì máy ảo Android xem localhost là chính nó; khi lên production, Android gọi thẳng vào tên miền cloud https của Render. "
        "Phía sau API là cơ sở dữ liệu PostgreSQL lưu trữ trên Supabase Singapore thông qua cổng 5432. "
        "Việc dùng chung một API giúp hệ thống kiểm soát toàn vẹn dữ liệu và phân quyền một nơi duy nhất."
    )

    # ==========================================
    # SLIDE 4: WEB CLIENT (NEXT.JS)
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "ỨNG DỤNG WEB: NEXT.JS 14 APP ROUTER", "03. Ứng dụng Khách (Web)", 4, "Quách Khoa Đức")

    # Left: Screenshot
    img_web = os.path.join(EVIDENCE_DIR, "02_web_events.png")
    if os.path.exists(img_web):
        s4.shapes.add_picture(img_web, Inches(0.8), Inches(1.5), width=Inches(5.8))

    # Right: Controls Table & Code
    # Table of controls
    table_shape = s4.shapes.add_table(5, 3, Inches(6.9), Inches(1.5), Inches(5.6), Inches(1.8))
    t = table_shape.table
    t.columns[0].width = Inches(1.6)
    t.columns[1].width = Inches(1.8)
    t.columns[2].width = Inches(2.2)
    headers = ["Tên điều khiển", "Loại điều khiển", "Vai trò nghiệp vụ"]
    for i, h in enumerate(headers):
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

    # Code Box (<= 10 lines)
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
        "Các điều khiển tuân thủ đúng quy ước đặt tên: ô nhập từ khóa là txtSearch, nút bấm là btnSearch, danh sách hiển thị dạng lưới grdEvents. "
        "Đoạn mã bên phải lấy trực tiếp từ file events/page.tsx. "
        "Khi người dùng gõ từ khóa, hàm gửi request GET tới /api/events kèm phân trang pageIndex và pageSize. "
        "Điểm kỹ thuật quan trọng ở đây là nhóm dùng AbortController để tự động hủy request cũ khi người dùng gõ nhanh, "
        "tránh lỗi bất đồng bộ race condition. Khi nhận kết quả thành công, hàm setEvents sẽ đổ dữ liệu thật vào giao diện. "
        "Sau đây, em xin kính mời bạn Đào Trí Khang tiếp tục trình bày về ứng dụng di động Android Native."
    )

    # Save initial presentation structure
    prs.save("deliverables/VISIONARY_TH71108_FINAL_PRESENTATION.pptx")
    print("Base PPTX created with first 4 slides.")

build_presentation()
