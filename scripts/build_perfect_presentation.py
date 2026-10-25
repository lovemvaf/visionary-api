import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

def generate_perfect_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Harmonious Academic Tech Palette
    C_NAVY = RGBColor(15, 23, 42)       # #0F172A
    C_BLUE = RGBColor(34, 100, 172)     # #2264AC
    C_TEAL = RGBColor(34, 166, 161)     # #22A6A1
    C_BG = RGBColor(248, 250, 252)      # #F8FAFC
    C_WHITE = RGBColor(255, 255, 255)
    C_DARK = RGBColor(30, 41, 59)       # #1E293B
    C_MUTED = RGBColor(100, 116, 139)   # #64748B
    C_GREEN = RGBColor(22, 163, 74)     # #16A34A
    C_RED = RGBColor(220, 38, 38)       # #DC2626
    C_BORDER = RGBColor(226, 232, 240) # #E2E8F0
    C_LIGHT_BLUE = RGBColor(239, 246, 255) # #EFF6FF
    C_LIGHT_TEAL = RGBColor(240, 253, 250) # #F0FDFA
    C_LIGHT_RED = RGBColor(254, 242, 242)  # #FEF2F2

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
        fp.font.size = Pt(9.5)
        fp.font.color.rgb = C_MUTED
        fp.font.name = "Segoe UI"

    # ==========================================
    # SLIDE 1: BÌA & PHÂN CÔNG (QUÁCH KHOA ĐỨC)
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = C_BG
    bg1.line.fill.background()

    top_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.15))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = C_BLUE
    top_bar.line.fill.background()

    if os.path.exists(LOGO_DNTU):
        s1.shapes.add_picture(LOGO_DNTU, Inches(0.8), Inches(0.45), height=Inches(1.1))
    if os.path.exists(LOGO_CNTT):
        s1.shapes.add_picture(LOGO_CNTT, Inches(11.3), Inches(0.45), height=Inches(1.1))

    tx_header = s1.shapes.add_textbox(Inches(2.2), Inches(0.5), Inches(8.8), Inches(1.1))
    tf_h = tx_header.text_frame
    tf_h.word_wrap = True
    p = tf_h.paragraphs[0]
    p.text = "TRƯỜNG ĐẠI HỌC CÔNG NGHỆ ĐỒNG NAI (DNTU)\nKHOA CÔNG NGHỆ THÔNG TIN – HỌC PHẦN WEB API (TH71108)"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = C_BLUE
    p.alignment = PP_ALIGN.CENTER
    p.font.name = "Segoe UI"

    tx_title = s1.shapes.add_textbox(Inches(0.8), Inches(1.65), Inches(11.733), Inches(1.4))
    tf_t = tx_title.text_frame
    tf_t.word_wrap = True
    p = tf_t.paragraphs[0]
    p.text = "VISIONARY"
    p.font.size = Pt(30)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.alignment = PP_ALIGN.CENTER
    p.font.name = "Segoe UI"
    
    p2 = tf_t.add_paragraph()
    p2.text = "HỆ THỐNG QUẢN LÝ HOẠT ĐỘNG HỘI NHẬP & KẾT NỐI SINH VIÊN"
    p2.font.size = Pt(15)
    p2.font.bold = True
    p2.font.color.rgb = C_TEAL
    p2.alignment = PP_ALIGN.CENTER
    p2.font.name = "Segoe UI"

    p3 = tf_t.add_paragraph()
    p3.text = "Mô hình Một Web API (ASP.NET Core 8) – Ba Ứng dụng Khách (Web Next.js, Desktop WinForms, Mobile Android)"
    p3.font.size = Pt(11)
    p3.font.color.rgb = C_MUTED
    p3.alignment = PP_ALIGN.CENTER
    p3.font.name = "Segoe UI"

    # Member Grid (4 cards in fixed order)
    members = [
        ("1. Quách Khoa Đức", "1923040025", "Lead, Kiến trúc hệ thống\n& Web Client (Next.js)", "Phần 1: Dễ nhất, mở đầu\n& Web Client Demo", C_BLUE),
        ("2. Đào Trí Khang", "1923040156", "Mobile Software Engineer\n(Android Native Java)", "Phần 2: Ứng dụng Android,\nThreading & Demo App", C_TEAL),
        ("3. Hồ Đoàng Nguyên Khang", "1923040112", "API Engineer & Database\n(ASP.NET Core & Swagger)", "Phần 3: Swagger, 6 chặng,\nJWT 401/403 & DB DTO", C_NAVY),
        ("4. Võ Ngọc Minh Đạt", "1923040088", "Desktop Software Engineer\n(WinForms C#) & BCN CLB", "Phần 4: WinForms, Sự cố CI,\nSo sánh & KẾT THÚC", C_BLUE)
    ]
    x_start = 0.8
    card_w = 2.75
    gap = 0.24
    for idx, (m_name, m_id, m_role, m_part, col) in enumerate(members):
        cur_x = x_start + idx * (card_w + gap)
        card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(cur_x), Inches(3.2), Inches(card_w), Inches(2.3))
        card.fill.solid()
        card.fill.fore_color.rgb = C_WHITE
        card.line.color.rgb = col
        card.line.width = Pt(1.5)

        tx = s1.shapes.add_textbox(Inches(cur_x + 0.1), Inches(3.3), Inches(card_w - 0.2), Inches(2.1))
        tf = tx.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = m_name
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = col
        p.font.name = "Segoe UI"

        p_id = tf.add_paragraph()
        p_id.text = f"MSSV: {m_id}"
        p_id.font.size = Pt(9.5)
        p_id.font.color.rgb = C_MUTED
        p_id.font.name = "Segoe UI"

        p_r = tf.add_paragraph()
        p_r.text = m_role
        p_r.font.size = Pt(9)
        p_r.font.color.rgb = C_DARK
        p_r.font.name = "Segoe UI"

        p_p = tf.add_paragraph()
        p_p.text = "🎯 " + m_part
        p_p.font.size = Pt(8.5)
        p_p.font.bold = True
        p_p.font.color.rgb = col
        p_p.font.name = "Segoe UI"

    # Meta banner at bottom
    meta_box = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(5.65), Inches(11.733), Inches(1.3))
    meta_box.fill.solid()
    meta_box.fill.fore_color.rgb = C_WHITE
    meta_box.line.color.rgb = C_BORDER
    
    tx_meta = s1.shapes.add_textbox(Inches(1.0), Inches(5.7), Inches(11.3), Inches(1.2))
    tf_m = tx_meta.text_frame
    tf_m.word_wrap = True
    
    p = tf_m.paragraphs[0]
    p.text = "🌐 THÔNG TIN TRUY CẬP VÀ XÁC THỰC HỆ THỐNG:"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.font.name = "Segoe UI"

    urls = [
        "• Swagger UI (Kiểm thử API trực tiếp): https://visionary-api-gb51.onrender.com/swagger",
        "• Website Production (Vercel): https://visionary-platform.vercel.app | Mã nguồn: https://github.com/lovemvaf/visionary-api",
        "• Khai báo sử dụng AI: Google Antigravity hỗ trợ kiểm chứng mã nguồn & kiểm thử hồi quy; toàn bộ logic nghiệp vụ do nhóm trực tiếp làm chủ."
    ]
    for u in urls:
        p = tf_m.add_paragraph()
        p.text = u
        p.font.size = Pt(9)
        p.font.color.rgb = C_DARK
        p.font.name = "Segoe UI"

    s1.notes_slide.notes_text_frame.text = (
        "LỜI THUYẾT TRÌNH (QUÁCH KHOA ĐỨC - 35s):\n"
        "Kính chào Thầy và các bạn trong hội đồng! Em tên là Quách Khoa Đức, đại diện nhóm VISIONARY API bảo vệ đồ án tốt nghiệp môn Web API. "
        "Hệ thống của nhóm gồm một Web API trung tâm trên ASP.NET Core 8 và ba ứng dụng khách: Web Next.js, Desktop Windows Forms và Mobile Android. "
        "Bốn thành viên tham gia trình bày theo đúng thứ tự: Em Quách Khoa Đức phụ trách mở đầu, kiến trúc và Web Client; "
        "bạn Đào Trí Khang phụ trách Android; bạn Hồ Đoàng Nguyên Khang phụ trách Web API, Swagger và Database; "
        "và bạn Võ Ngọc Minh Đạt phụ trách Windows Forms cùng phân tích sự cố và kết luận."
    )

    # ==========================================
    # SLIDE 2: BÀI TOÁN & MỤC TIÊU (QUÁCH KHOA ĐỨC)
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "BÀI TOÁN THỰC TẾ & MỤC TIÊU CỦA ĐỀ TÀI VISIONARY", "01. Đặt vấn đề", 2, "Quách Khoa Đức")

    card1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2))
    card1.fill.solid()
    card1.fill.fore_color.rgb = C_WHITE
    card1.line.color.rgb = C_BORDER
    tx1 = s2.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.6))
    tf1 = tx1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "VẤN ĐỀ THỰC TẾ CỦA CLB & SINH VIÊN"
    p.font.size = Pt(13)
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
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_DARK

    card2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.2))
    card2.fill.solid()
    card2.fill.fore_color.rgb = C_WHITE
    card2.line.color.rgb = C_BORDER
    tx2 = s2.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.6))
    tf2 = tx2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "MỤC TIÊU GIẢI PHÁP VISIONARY"
    p.font.size = Pt(13)
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
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_DARK

    s2.notes_slide.notes_text_frame.text = (
        "LỜI THUYẾT TRÌNH (QUÁCH KHOA ĐỨC - 40s):\n"
        "Thưa Thầy, lý do nhóm em chọn đề tài xuất phát từ bài toán thực tế của CLB Tiếng Anh và sinh viên DNTU. "
        "Trước đây, việc quản lý thành viên và điểm danh sự kiện làm bằng file tính thủ công. "
        "Sinh viên cũng thiếu cổng thông tin học thuật tiếng Anh chuyên ngành IT và các cuộc thi quốc tế. "
        "Hệ thống VISIONARY giải quyết trọn vẹn bài toán bằng một Web API trung tâm duy nhất trên ASP.NET Core 8, "
        "kết nối cơ sở dữ liệu PostgreSQL. Cả ba ứng dụng Web, Android và Windows Forms đều dùng chung dữ liệu nên không bao giờ bị lệch số liệu."
    )

    # ==========================================
    # SLIDE 3: SƠ ĐỒ KIẾN TRÚC MỘT API, BA NỀN TẢNG (QUÁCH KHOA ĐỨC)
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "SƠ ĐỒ KIẾN TRÚC HỆ THỐNG: MỘT WEB API, BA NỀN TẢNG", "02. Kiến trúc Hệ sinh thái", 3, "Quách Khoa Đức")

    # 3 Clients on the Left
    b_web = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(3.2), Inches(1.4))
    b_web.fill.solid()
    b_web.fill.fore_color.rgb = C_WHITE
    b_web.line.color.rgb = C_BLUE
    b_web.line.width = Pt(2)
    tx = s3.shapes.add_textbox(Inches(0.9), Inches(1.55), Inches(3.0), Inches(1.3))
    tx.text_frame.word_wrap = True
    tx.text_frame.paragraphs[0].text = "ỨNG DỤNG WEB (Next.js 14)\n• Môi trường: Trình duyệt (Vercel Cloud)\n• Địa chỉ: https://visionary-platform.vercel.app\n• Cổng: HTTPS 443 (Local: 3000)"
    tx.text_frame.paragraphs[0].font.size = Pt(9.5)
    tx.text_frame.paragraphs[0].font.color.rgb = C_DARK

    b_win = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.2), Inches(3.2), Inches(1.4))
    b_win.fill.solid()
    b_win.fill.fore_color.rgb = C_WHITE
    b_win.line.color.rgb = C_TEAL
    b_win.line.width = Pt(2)
    tx = s3.shapes.add_textbox(Inches(0.9), Inches(3.25), Inches(3.0), Inches(1.3))
    tx.text_frame.word_wrap = True
    tx.text_frame.paragraphs[0].text = "ỨNG DỤNG WINDOWS FORMS (C#)\n• Môi trường: Máy tính Windows Desktop\n• Thực thi: Visionary.Desktop.exe (.NET 8)\n• Cổng gọi ra: HTTPS 443"
    tx.text_frame.paragraphs[0].font.size = Pt(9.5)
    tx.text_frame.paragraphs[0].font.color.rgb = C_DARK

    b_and = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.9), Inches(3.2), Inches(1.4))
    b_and.fill.solid()
    b_and.fill.fore_color.rgb = C_WHITE
    b_and.line.color.rgb = C_GREEN
    b_and.line.width = Pt(2)
    tx = s3.shapes.add_textbox(Inches(0.9), Inches(4.95), Inches(3.0), Inches(1.3))
    tx.text_frame.word_wrap = True
    tx.text_frame.paragraphs[0].text = "ỨNG DỤNG ANDROID (Java Native)\n• Môi trường: Máy ảo Android / Điện thoại thật\n• Thực thi: app-debug.apk (Min SDK 28)\n• Gateway máy ảo: 10.0.2.2 / HTTPS Cloud"
    tx.text_frame.paragraphs[0].font.size = Pt(9.5)
    tx.text_frame.paragraphs[0].font.color.rgb = C_DARK

    # Connectors: 3 Arrows from clients to API
    arr1 = s3.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(4.1), Inches(2.0), Inches(1.5), Inches(0.4))
    arr1.fill.solid()
    arr1.fill.fore_color.rgb = C_BLUE
    arr1.line.fill.background()
    s3.shapes.add_textbox(Inches(4.1), Inches(1.65), Inches(1.5), Inches(0.35)).text_frame.paragraphs[0].text = "HTTPS (443)\nJSON"
    s3.shapes.add_textbox(Inches(4.1), Inches(1.65), Inches(1.5), Inches(0.35)).text_frame.paragraphs[0].font.size = Pt(8.5)

    arr2 = s3.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(4.1), Inches(3.7), Inches(1.5), Inches(0.4))
    arr2.fill.solid()
    arr2.fill.fore_color.rgb = C_TEAL
    arr2.line.fill.background()
    s3.shapes.add_textbox(Inches(4.1), Inches(3.35), Inches(1.5), Inches(0.35)).text_frame.paragraphs[0].text = "HTTPS (443)\nJSON"
    s3.shapes.add_textbox(Inches(4.1), Inches(3.35), Inches(1.5), Inches(0.35)).text_frame.paragraphs[0].font.size = Pt(8.5)

    arr3 = s3.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(4.1), Inches(5.4), Inches(1.5), Inches(0.4))
    arr3.fill.solid()
    arr3.fill.fore_color.rgb = C_GREEN
    arr3.line.fill.background()
    s3.shapes.add_textbox(Inches(4.1), Inches(5.05), Inches(1.5), Inches(0.35)).text_frame.paragraphs[0].text = "HTTP (10.0.2.2)\nJSON"
    s3.shapes.add_textbox(Inches(4.1), Inches(5.05), Inches(1.5), Inches(0.35)).text_frame.paragraphs[0].font.size = Pt(8.5)

    # Center: Web API Core
    b_api = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.8), Inches(2.0), Inches(3.8), Inches(4.0))
    b_api.fill.solid()
    b_api.fill.fore_color.rgb = C_NAVY
    b_api.line.color.rgb = C_TEAL
    b_api.line.width = Pt(2)
    tx_api = s3.shapes.add_textbox(Inches(5.9), Inches(2.1), Inches(3.6), Inches(3.8))
    tf_api = tx_api.text_frame
    tf_api.word_wrap = True
    p = tf_api.paragraphs[0]
    p.text = "ASP.NET CORE 8 WEB API"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    api_items = [
        "Kestrel Web Server (.NET 8)",
        "Swagger OpenAPI: /swagger",
        "Pipeline: UseCors -> UseAuthentication -> UseAuthorization -> MapControllers",
        "Clean Architecture: Core, Infra, Api",
        "Bảo mật: JWT Bearer (HMAC-SHA256)",
        "Host Cloud: Render (Port 443)",
        "Host Local: http://localhost:5000"
    ]
    for ai in api_items:
        p = tf_api.add_paragraph()
        p.text = "• " + ai
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_WHITE

    # Arrow from API to DB
    arr_db = s3.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(9.8), Inches(3.8), Inches(1.1), Inches(0.45))
    arr_db.fill.solid()
    arr_db.fill.fore_color.rgb = C_BLUE
    arr_db.line.fill.background()
    s3.shapes.add_textbox(Inches(9.8), Inches(3.35), Inches(1.2), Inches(0.4)).text_frame.paragraphs[0].text = "TCP / SSL\nPort 5432"
    s3.shapes.add_textbox(Inches(9.8), Inches(3.35), Inches(1.2), Inches(0.4)).text_frame.paragraphs[0].font.size = Pt(8.5)

    # Right: Database Supabase
    b_db = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(11.0), Inches(2.6), Inches(1.6), Inches(2.8))
    b_db.fill.solid()
    b_db.fill.fore_color.rgb = C_WHITE
    b_db.line.color.rgb = C_BLUE
    b_db.line.width = Pt(2)
    tx_db = s3.shapes.add_textbox(Inches(11.05), Inches(2.7), Inches(1.5), Inches(2.6))
    tf_db = tx_db.text_frame
    tf_db.word_wrap = True
    p = tf_db.paragraphs[0]
    p.text = "DATABASE"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_BLUE
    db_items = [
        "PostgreSQL 16",
        "Cloud: Supabase",
        "Region: Singapore",
        "EF Core 8 Npgsql",
        "Pooler Port: 5432",
        "1 nguồn dữ liệu duy nhất"
    ]
    for dbi in db_items:
        p = tf_db.add_paragraph()
        p.text = "• " + dbi
        p.font.size = Pt(8.5)
        p.font.color.rgb = C_DARK

    # Bottom Explanation Box
    card_exp = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.45), Inches(11.733), Inches(0.55))
    card_exp.fill.solid()
    card_exp.fill.fore_color.rgb = C_LIGHT_TEAL
    card_exp.line.color.rgb = C_TEAL
    tx_exp = s3.shapes.add_textbox(Inches(0.9), Inches(6.48), Inches(11.5), Inches(0.5))
    p = tx_exp.text_frame.paragraphs[0]
    p.text = "💡 TẠI SAO DÙNG CHUNG MỘT API? Đảm bảo tính nhất quán dữ liệu 100%, tập trung logic kiểm tra quyền trên server, không phân mảnh dữ liệu giữa các client."
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    s3.notes_slide.notes_text_frame.text = (
        "LỜI THUYẾT TRÌNH (QUÁCH KHOA ĐỨC - 45s):\n"
        "Trên màn hình là sơ đồ kiến trúc tổng quan. Ở trung tâm là Web API viết bằng ASP.NET Core 8, "
        "kết nối cơ sở dữ liệu PostgreSQL lưu trên Supabase qua cổng 5432. "
        "Ba ứng dụng gồm: Web Next.js chạy trên Vercel, Windows Forms C# chạy trên máy tính BCN, "
        "và Android Java chạy trên điện thoại sinh viên. "
        "Cả ba ứng dụng đều gửi request qua giao thức HTTPS bằng định dạng JSON chuẩn. "
        "Nhờ dùng chung một API trung tâm, khi BCN điểm danh trên WinForms thì sinh viên trên Android sẽ thấy kết quả ngay."
    )

    # ==========================================
    # SLIDE 4: WEB CLIENT NEXT.JS (QUÁCH KHOA ĐỨC)
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "ỨNG DỤNG WEB CLIENT: GIAO DIỆN & KẾT NỐI API", "03. Ứng dụng Web", 4, "Quách Khoa Đức")

    img_web = os.path.join(EVIDENCE_DIR, "02_web_events.png")
    if os.path.exists(img_web):
        s4.shapes.add_picture(img_web, Inches(0.8), Inches(1.5), width=Inches(4.6))

    # Controls table
    t_web = s4.shapes.add_table(5, 3, Inches(5.6), Inches(1.5), Inches(6.9), Inches(2.0)).table
    t_web.columns[0].width = Inches(2.0)
    t_web.columns[1].width = Inches(1.8)
    t_web.columns[2].width = Inches(3.1)
    headers = ["Tên điều khiển", "Loại điều khiển", "Vai trò nghiệp vụ"]
    for i, h in enumerate(headers):
        cell = t_web.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_BLUE
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = C_WHITE

    ctrl_rows = [
        ("txtSearchEvents", "HTML <input type='text'>", "Nhập từ khóa tìm kiếm sự kiện"),
        ("cboEventCategory", "HTML <select>", "Lọc sự kiện theo danh mục học thuật"),
        ("btnSearch", "HTML <button>", "Kích hoạt gửi request GET /api/events"),
        ("grdEventCards", "HTML <div> (Grid layout)", "Hiển thị danh sách thẻ sự kiện do API trả về")
    ]
    for row_idx, r in enumerate(ctrl_rows, start=1):
        for col_idx, val in enumerate(r):
            cell = t_web.cell(row_idx, col_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_WHITE
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(9)
            p.font.color.rgb = C_DARK

    # Code Box <= 10 lines
    code_box = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.6), Inches(3.7), Inches(6.9), Inches(2.7))
    code_box.fill.solid()
    code_box.fill.fore_color.rgb = C_NAVY
    code_box.line.color.rgb = C_TEAL
    tx_code = s4.shapes.add_textbox(Inches(5.7), Inches(3.75), Inches(6.7), Inches(2.6))
    tf_c = tx_code.text_frame
    tf_c.word_wrap = True
    p = tf_c.paragraphs[0]
    p.text = "// frontend/src/services/eventService.ts – Gọi GET /api/events (Mã nguồn thật):"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    code_lines = [
        "export const getEvents = async (page = 1, pageSize = 10, category?: string) => {",
        "  const params = new URLSearchParams({ page: page.toString(), pageSize: pageSize.toString() });",
        "  if (category) params.append('category', category);",
        "  ",
        "  // Goi API qua ham fetch tap trung, tu dong truyen Bearer token neu co",
        "  const response = await fetchWithAuth(`/api/events?${params.toString()}`, {",
        "    method: 'GET'",
        "  });",
        "  return response; // Tra ve ApiResponse<PagedResponse<EventDto>>",
        "};"
    ]
    for cl in code_lines:
        p = tf_c.add_paragraph()
        p.text = cl
        p.font.size = Pt(9)
        p.font.color.rgb = RGBColor(226, 232, 240)
        p.font.name = "Consolas"

    # Bottom notes
    card_wf = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.45), Inches(11.733), Inches(0.55))
    card_wf.fill.solid()
    card_wf.fill.fore_color.rgb = C_WHITE
    card_wf.line.color.rgb = C_BORDER
    tx_wf = s4.shapes.add_textbox(Inches(0.9), Inches(6.48), Inches(11.5), Inches(0.5))
    p = tx_wf.text_frame.paragraphs[0]
    p.text = "⚡ Khó khăn đặc thù Web & Giải pháp: Trình duyệt ép kiểm tra CORS. Giải pháp: Cấu hình app.UseCors() trên ASP.NET Core và triển khai BFF Proxy route tại /api/[...path]."
    p.font.size = Pt(9)
    p.font.color.rgb = C_DARK

    s4.notes_slide.notes_text_frame.text = (
        "LỜI THUYẾT TRÌNH (QUÁCH KHOA ĐỨC - 45s):\n"
        "Về ứng dụng Web, nhóm xây dựng bằng Next.js 14 với thiết kế hiện đại. "
        "Bên trái là ảnh chụp thật trang Sự kiện. Các điều khiển chính gồm ô tìm kiếm txtSearchEvents, "
        "danh mục cboEventCategory và lưới thẻ sự kiện grdEventCards. "
        "Đoạn mã bên phải lấy trực tiếp từ file eventService.ts, sử dụng hàm getEvents để gọi GET /api/events. "
        "Khó khăn lớn nhất của Web là cơ chế CORS của trình duyệt, nhóm đã giải quyết bằng cách bật CORS trên API "
        "và cấu hình tuyến Proxy BFF. "
        "Sau đây, em xin chuyển lời cho bạn Đào Trí Khang trình bày về ứng dụng Android. Xin mời Khang!"
    )

    # ==========================================
        # ==========================================
    # SLIDE 5: ANDROID NATIVE JAVA (ĐÀO TRÍ KHANG)
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "ỨNG DỤNG DI ĐỘNG: ANDROID NATIVE JAVA", "04. Ứng dụng Android", 5, "Đào Trí Khang")

    img_and = os.path.join(EVIDENCE_DIR, "11_android_events.png")
    if os.path.exists(img_and):
        s5.shapes.add_picture(img_and, Inches(0.8), Inches(1.35), height=Inches(4.95))

    # Controls table
    t5 = s5.shapes.add_table(5, 3, Inches(3.9), Inches(1.35), Inches(8.6), Inches(1.8)).table
    t5.columns[0].width = Inches(2.2)
    t5.columns[1].width = Inches(2.2)
    t5.columns[2].width = Inches(4.2)
    for i, h in enumerate(headers):
        cell = t5.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_GREEN
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(9.5)
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
            p.font.size = Pt(9)
            p.font.color.rgb = C_DARK

    code_box5 = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(3.9), Inches(3.3), Inches(8.6), Inches(3.0))
    code_box5.fill.solid()
    code_box5.fill.fore_color.rgb = C_NAVY
    code_box5.line.color.rgb = C_GREEN
    code_box5.line.width = Pt(1.5)
    tx_c5 = s5.shapes.add_textbox(Inches(4.0), Inches(3.35), Inches(8.4), Inches(2.9))
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
        p.font.size = Pt(8.5)
        p.font.color.rgb = RGBColor(226, 232, 240)
        p.font.name = "Consolas"

    card_w5 = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.45), Inches(11.733), Inches(0.52))
    card_w5.fill.solid()
    card_w5.fill.fore_color.rgb = C_WHITE
    card_w5.line.color.rgb = C_BORDER
    tx_w5 = s5.shapes.add_textbox(Inches(0.9), Inches(6.48), Inches(11.5), Inches(0.48))
    p = tx_w5.text_frame.paragraphs[0]
    p.text = "⚡ Khó khăn đặc thù Android & Giải pháp: Android 9+ chặn kết nối HTTP không mã hóa và máy ảo không dùng localhost. Nhóm cấu hình network_security_config.xml cho phép cleartext traffic trong dev và dùng alias 10.0.2.2."
    p.font.size = Pt(9)
    p.font.color.rgb = C_GREEN

    s5.notes_slide.notes_text_frame.text = (
        "LỜI THUYẾT TRÌNH (ĐÀO TRÍ KHANG - 1p00s):\n"
        "Kính chào Thầy và các bạn! Em tên là Đào Trí Khang, phụ trách ứng dụng di động Android Native bằng Java. "
        "Ứng dụng Android được thiết kế cho sinh viên DNTU để theo dõi hoạt động CLB và đăng ký sự kiện ngay trên điện thoại. "
        "Bên trái là ảnh chụp thật từ ứng dụng Android. "
        "Các điều khiển tuân thủ đúng quy ước đặt tên: danh sách cuộn là lstEvents (RecyclerView), nút đăng ký là btnRegister, vuốt làm mới là swpRefresh. "
        "Đoạn mã bên phải thể hiện hàm loadEvents gọi tới Web API thông qua thư viện Retrofit 2. "
        "Hàm getEvents(1, 20) được đẩy vào phương thức enqueue để thực thi trên luồng nền của OkHttp, "
        "khi có kết quả onResponse sẽ tự động đưa về luồng chính để cập nhật adapter cho RecyclerView."
    )

    # ==========================================
    # SLIDE 6: SƠ ĐỒ ANDROID NETWORKING & THREADING (ĐÀO TRÍ KHANG)
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "SƠ ĐỒ CƠ CHẾ MẠNG & ĐIỀU PHỐI LUỒNG TRÊN ANDROID", "05. Cơ chế Mạng Android", 6, "Đào Trí Khang")

    # Flow Diagram across 5 stages using PowerPoint shapes and connectors
    flow_steps = [
        ("1. Tương tác UI", "Main UI Thread", "Người dùng nhấn btnRegister\nhoặc vuốt làm mới swpRefresh", C_BLUE, Inches(0.8)),
        ("2. Retrofit Enqueue", "OkHttp Dispatcher", "apiService.getEvents().enqueue()\nĐẩy việc vào luồng nền Worker", C_TEAL, Inches(3.25)),
        ("3. Gói tin Mạng", "I/O Network TCP", "Gửi request GET /api/events\ntới Kestrel Server cổng 443", C_NAVY, Inches(5.7)),
        ("4. Giải mã JSON", "Gson Deserializer", "Tự động ánh xạ JSON string\nsang ApiResponse<PagedResponse>", C_TEAL, Inches(8.15)),
        ("5. Cập nhật UI", "Main UI Thread", "Handler.post / onResponse\nCập nhật Adapter cho View", C_GREEN, Inches(10.6))
    ]

    for title, subtitle, desc, col, x_pos in flow_steps:
        box = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x_pos, Inches(1.35), Inches(1.95), Inches(1.4))
        box.fill.solid()
        box.fill.fore_color.rgb = C_WHITE
        box.line.color.rgb = col
        box.line.width = Pt(1.5)

        tx = s6.shapes.add_textbox(x_pos + Inches(0.04), Inches(1.38), Inches(1.87), Inches(1.34))
        tf = tx.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = col
        p.alignment = PP_ALIGN.CENTER

        p_sub = tf.add_paragraph()
        p_sub.text = f"[{subtitle}]"
        p_sub.font.size = Pt(8.5)
        p_sub.font.color.rgb = C_MUTED
        p_sub.alignment = PP_ALIGN.CENTER

        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(8)
        p_desc.font.color.rgb = C_DARK
        p_desc.alignment = PP_ALIGN.CENTER

        if x_pos < Inches(10.0):
            arr = s6.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, x_pos + Inches(1.98), Inches(1.9), Inches(0.44), Inches(0.22))
            arr.fill.solid()
            arr.fill.fore_color.rgb = C_TEAL
            arr.line.fill.background()

    # Middle Section: Actual Android Threading Code Snippet (Answers Teacher's question directly)
    code_box6 = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(2.9), Inches(11.733), Inches(1.8))
    code_box6.fill.solid()
    code_box6.fill.fore_color.rgb = C_NAVY
    code_box6.line.color.rgb = C_GREEN
    code_box6.line.width = Pt(1.5)
    tx_c6 = s6.shapes.add_textbox(Inches(0.9), Inches(2.95), Inches(11.5), Inches(1.7))
    tf_c6 = tx_c6.text_frame
    tf_c6.word_wrap = True
    p = tf_c6.paragraphs[0]
    p.text = "// EventsFragment.java – Hai dòng mã cốt lõi: Tạo luồng nền & Đẩy kết quả về Luồng Chính (Mã nguồn thật):"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_GREEN

    code_lines6 = [
        "// 1. TẠO LUỒNG NỀN: .enqueue() đẩy tác vụ mạng sang OkHttp ThreadPool, tránh chặn Main UI Thread",
        "apiService.getEvents(1, 10).enqueue(new Callback<ApiResponse<PagedResponse<EventItem>>>() {",
        "    @Override public void onResponse(Call<...> call, Response<ApiResponse<PagedResponse<EventItem>>> res) {",
        "        if (res.isSuccessful() && res.body() != null) {",
        "            // 2. ĐẨY VỀ LUỒNG CHÍNH: Looper.getMainLooper() đưa dữ liệu về Main UI Thread để cập nhật Adapter an toàn",
        "            new Handler(Looper.getMainLooper()).post(() -> eventAdapter.setEvents(res.body().getData().getItems()));",
        "        }",
        "    }",
        "});"
    ]
    for cl in code_lines6:
        p = tf_c6.add_paragraph()
        p.text = cl
        p.font.size = Pt(8.5)
        p.font.color.rgb = RGBColor(226, 232, 240)
        p.font.name = "Consolas"

    # Bottom Cards: Warning Exceptions & Network Config
    w_card1 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.85), Inches(5.7), Inches(2.05))
    w_card1.fill.solid()
    w_card1.fill.fore_color.rgb = C_LIGHT_RED
    w_card1.line.color.rgb = C_RED
    w_card1.line.width = Pt(1.5)
    tx_w1 = s6.shapes.add_textbox(Inches(0.9), Inches(4.9), Inches(5.5), Inches(1.95))
    tf_w1 = tx_w1.text_frame
    tf_w1.word_wrap = True
    p = tf_w1.paragraphs[0]
    p.text = "⚠️ HAI NGOẠI LỆ NGUY HIỂM BUỘC PHẢI TRÁNH:"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = C_RED
    w_items = [
        "1. NetworkOnMainThreadException: Xảy ra khi gọi mạng trực tiếp (.execute()) trên Luồng Chính. Hệ thống Android tự động chặn và ném lỗi crash ngay.",
        "2. CalledFromWrongThreadException: Xảy ra khi cố tình sửa đổi View từ luồng nền. Bắt buộc phải đưa về Main Thread qua Handler(Looper.getMainLooper())."
    ]
    for wi in w_items:
        p = tf_w1.add_paragraph()
        p.text = wi
        p.font.size = Pt(8.5)
        p.font.color.rgb = C_DARK

    w_card2 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(4.85), Inches(5.733), Inches(2.05))
    w_card2.fill.solid()
    w_card2.fill.fore_color.rgb = C_WHITE
    w_card2.line.color.rgb = C_TEAL
    w_card2.line.width = Pt(1.5)
    tx_w2 = s6.shapes.add_textbox(Inches(6.9), Inches(4.9), Inches(5.533), Inches(1.95))
    tf_w2 = tx_w2.text_frame
    tf_w2.word_wrap = True
    p = tf_w2.paragraphs[0]
    p.text = "🌐 CẤU HÌNH KẾT NỐI MẠNG ĐẶC THÙ TRÊN ANDROID:"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    cfg_items = [
        "• Địa chỉ 10.0.2.2: Máy ảo Android không dùng 'localhost' vì localhost trỏ về chính nó. 10.0.2.2 là địa chỉ bí danh trỏ về máy tính chủ chạy Web API.",
        "• Khai báo usesCleartextTraffic: Từ Android 9, kết nối HTTP không mã hóa bị chặn. Nhóm cấu hình network_security_config.xml cho môi trường test.",
        "• Tự động gắn JWT qua AuthInterceptor: Token lưu trong SharedPreferences và được tự động chèn vào header Authorization."
    ]
    for ci in cfg_items:
        p = tf_w2.add_paragraph()
        p.text = ci
        p.font.size = Pt(8.5)
        p.font.color.rgb = C_DARK

    s6.notes_slide.notes_text_frame.text = (
        "LỜI THUYẾT TRÌNH (ĐÀO TRÍ KHANG - 1p00s):\n"
        "Thưa Thầy, sơ đồ phía trên mô tả chi tiết đường đi của yêu cầu mạng trên Android qua 5 bước: "
        "Bắt đầu từ nút bấm trên Main UI Thread, hàm enqueue() đẩy việc tải dữ liệu sang luồng nền của OkHttp. "
        "Khi server trả về JSON, thư viện Gson sẽ giải mã thành đối tượng Java và chuyển kết quả an toàn về Luồng Chính để cập nhật danh sách. "
        "Nếu gọi mạng trên Luồng Chính, ứng dụng sẽ bị ném ngoại lệ NetworkOnMainThreadException ngay lập tức. "
        "Còn nếu sửa giao diện từ luồng nền thì gặp lỗi CalledFromWrongThreadException. "
        "Ngoài ra, trên máy ảo Android, địa chỉ IP kết nối phải là 10.0.2.2 chứ không thể là localhost."
    )

# SLIDE 7: DEMO ANDROID TRỰC TIẾP (ĐÀO TRÍ KHANG)
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "DEMO TRỰC TIẾP: ĐĂNG KÝ SỰ KIỆN TRÊN ANDROID APP", "06. Demo Di động", 7, "Đào Trí Khang")

    img_reg = os.path.join(EVIDENCE_DIR, "12_android_registration.png")
    if os.path.exists(img_reg):
        s7.shapes.add_picture(img_reg, Inches(0.8), Inches(1.5), width=Inches(3.8))

    card_d = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.0), Inches(1.5), Inches(7.5), Inches(5.2))
    card_d.fill.solid()
    card_d.fill.fore_color.rgb = C_WHITE
    card_d.line.color.rgb = C_BORDER
    tx_d = s7.shapes.add_textbox(Inches(5.2), Inches(1.7), Inches(7.1), Inches(4.8))
    tf_d = tx_d.text_frame
    tf_d.word_wrap = True
    p = tf_d.paragraphs[0]
    p.text = "KỊCH BẢN THAO TÁC DEMO TRỰC TIẾP TRÊN MÁY ẢO:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_GREEN

    steps = [
        ("Bước 1: Mở ứng dụng Android (app-debug.apk đã nạp sẵn)", "Ứng dụng tự động gửi request GET /api/events nạp danh sách sự kiện lên RecyclerView."),
        ("Bước 2: Chọn sự kiện 'Hội thảo Kỹ năng Hội nhập Quốc tế'", "Màn hình chuyển sang EventDetailActivity hiển thị chi tiết thời gian, địa điểm, diễn giả."),
        ("Bước 3: Nhấn nút 'Đăng ký tham gia' (btnRegister)", "Ứng dụng gửi yêu cầu POST /api/events/{id}/register kèm Bearer Token của tài khoản sinh viên."),
        ("Bước 4: Quan sát phản hồi HTTP 200 từ Web API", "Server tiếp nhận, ghi bản ghi vào PostgreSQL và trả về JSON thành công kèm mã check-in."),
        ("Bước 5: Bàn giao dữ liệu cho WinForms", "Bản ghi vừa đăng ký sẽ được bạn Võ Ngọc Minh Đạt tải và điểm danh ngay trên ứng dụng Windows Forms.")
    ]
    for st, sd in steps:
        p = tf_d.add_paragraph()
        p.text = "👉 " + st
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = C_NAVY
        p2 = tf_d.add_paragraph()
        p2.text = "     " + sd
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = C_DARK

    s7.notes_slide.notes_text_frame.text = (
        "LỜI THUYẾT TRÌNH (ĐÀO TRÍ KHANG - 1'15\"):\n"
        "Sau đây, em xin phép demo trực tiếp ứng dụng Android đang chạy trên máy ảo. "
        "[KHANG THAO TÁC]: Em mở app, danh sách sự kiện được tải về mượt mà qua API GET /api/events. "
        "Em chọn sự kiện 'Hội thảo Kỹ năng Hội nhập Quốc tế' và bấm nút Đăng ký tham gia. "
        "Ứng dụng gửi request POST lên Web API kèm mã Bearer token của sinh viên. "
        "Server xác nhận thành công và hiển thị thông báo đã đăng ký. "
        "Dữ liệu này đã lập tức được lưu vào cơ sở dữ liệu chung và sẽ được anh Đạt kiểm tra ngay trên WinForms ở phần sau. "
        "Sau đây, em xin chuyển lời sang bạn Hồ Đoàng Nguyên Khang để phân tích về Web API và Swagger."
    )

    # ==========================================
    # SLIDE 8: SWAGGER & HỢP ĐỒNG API (HỒ ĐOÀNG NGUYÊN KHANG)
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "SWAGGER UI & BẢNG HỢP ĐỒNG API THỰC TẾ TIÊU THỤ", "07. Hợp đồng API", 8, "Hồ Đoàng Nguyên Khang")

    img_sw = os.path.join(EVIDENCE_DIR, "04_swagger_overview.png")
    if os.path.exists(img_sw):
        s8.shapes.add_picture(img_sw, Inches(0.8), Inches(1.5), width=Inches(4.6))

    # Contract Table
    t8 = s8.shapes.add_table(6, 5, Inches(5.6), Inches(1.5), Inches(6.9), Inches(4.8)).table
    t8.columns[0].width = Inches(1.0)
    t8.columns[1].width = Inches(2.1)
    t8.columns[2].width = Inches(1.2)
    t8.columns[3].width = Inches(1.5)
    t8.columns[4].width = Inches(1.1)

    h8 = ["Method", "Đường dẫn (Endpoint)", "Quyền", "Thân yêu cầu", "Mã trả về"]
    for i, h in enumerate(h8):
        cell = t8.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = C_WHITE

    endpoints = [
        ("POST", "/api/auth/login", "Mở", "username, password", "200 + Token"),
        ("GET", "/api/events", "Mở", "(query phân trang)", "200 + Items"),
        ("GET", "/api/events/{id}", "Mở", "id trên URL", "200 / 404"),
        ("POST", "/api/events", "Admin/BCN", "title, time, location", "201 Created"),
        ("POST", "/api/events/{id}/register", "Student", "Header Bearer Token", "200 OK / 400")
    ]
    for row_idx, (m, ep, role, body, status) in enumerate(endpoints, start=1):
        r_data = [m, ep, role, body, status]
        for col_idx, val in enumerate(r_data):
            cell = t8.cell(row_idx, col_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_WHITE
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(8.5)
            p.font.color.rgb = C_DARK
            if col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = C_BLUE if m == "GET" else C_GREEN

    card_sw_note = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.45), Inches(11.733), Inches(0.55))
    card_sw_note.fill.solid()
    card_sw_note.fill.fore_color.rgb = C_LIGHT_TEAL
    card_sw_note.line.color.rgb = C_TEAL
    tx_sn = s8.shapes.add_textbox(Inches(0.9), Inches(6.48), Inches(11.5), Inches(0.5))
    p = tx_sn.text_frame.paragraphs[0]
    p.text = "📌 Tên trường JSON tuân thủ tuyệt đối chuẩn camelCase (id, title, location, totalCount, items). Khớp 100% giữa ASP.NET Core và cả 3 Client."
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    s8.notes_slide.notes_text_frame.text = (
        "LỜI THUYẾT TRÌNH (HỒ ĐOÀNG NGUYÊN KHANG - 1'00\"):\n"
        "Kính chào Thầy và các bạn! Em tên là Hồ Đoàng Nguyên Khang, phụ trách ASP.NET Core Web API, tài liệu Swagger và Cơ sở dữ liệu. "
        "Bên trái là ảnh chụp Swagger UI thực tế của hệ thống tại địa chỉ visionary-api-gb51.onrender.com/swagger. "
        "Bảng bên phải là hợp đồng API thực tế mà nhóm đã triển khai và tiêu thụ. "
        "Các endpoint được phân định quyền rõ ràng: GET /api/events mở công khai; POST /api/events/{id}/register cần đăng nhập; "
        "và POST /api/events tạo sự kiện bắt buộc quyền Admin hoặc Ban Chủ Nhiệm. "
        "Toàn bộ tên trường JSON đều dùng camelCase, đảm bảo tính nhất quán trên cả ba nền tảng."
    )

    # ==========================================
        # ==========================================
    # SLIDE 9: SƠ ĐỒ XUYÊN SUỐT MỘT YÊU CẦU (6 CHẶNG) (HỒ ĐOÀNG NGUYÊN KHANG)
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "SƠ ĐỒ CHU TRÌNH 6 CHẶNG CỦA MỘT YÊU CẦU: GET /api/events", "08. Chu trình Request", 9, "Hồ Đoàng Nguyên Khang")

    # 2x3 Grid with 6 Connected Stages
    stages_grid = [
        ("CHẶNG 1: THAO TÁC NGƯỜI DÙNG", "Luồng Giao diện [UI Thread]", [
            "• Người dùng kích hoạt hành động trên màn hình",
            "• Web Next.js: Bấm tab 'Sự kiện' / onClick",
            "• WinForms C#: Sự kiện btnTaiDanhSach_Click",
            "• Android Java: onResume() hoặc vuốt swpRefresh"
        ], C_BLUE, Inches(0.8), Inches(1.35), Inches(3.6), Inches(2.4)),

        ("CHẶNG 2: CLIENT XỬ LÝ & GỌI MẠNG", "Bất đồng bộ [Async Worker]", [
            "• Client chuẩn bị tham số & tạo HTTP request",
            "• Web: useEffect() -> api.getEvents(1, 10)",
            "• WinForms: TaiDanhSachAsync() -> _http.GetAsync()",
            "• Android: loadEvents() -> api.getEvents().enqueue()"
        ], C_TEAL, Inches(4.85), Inches(1.35), Inches(3.6), Inches(2.4)),

        ("CHẶNG 3: TRUYỀN GÓI TIN QUA MẠNG", "Đường truyền Mạng [TCP/SSL]", [
            "• Gói tin HTTP chuẩn gửi qua mạng tới cổng 443:",
            "  GET /api/events?pageNumber=1&pageSize=10",
            "• Host: visionary-api-gb51.onrender.com:443",
            "• Headers: Accept: application/json; charset=utf-8"
        ], C_NAVY, Inches(8.9), Inches(1.35), Inches(3.633), Inches(2.4)),

        ("CHẶNG 4: KESTREL SERVER & DATABASE", "ASP.NET Core 8 & PostgreSQL", [
            "• Middleware: UseCors -> UseAuth -> MapControllers",
            "• EventsController.GetEvents() nhận request",
            "• EventService truy vấn PostgreSQL qua EF Core:",
            "  _context.Events.AsNoTracking().ToPagedListAsync()"
        ], C_BLUE, Inches(0.8), Inches(3.95), Inches(3.6), Inches(2.4)),

        ("CHẶNG 5: ĐÓNG GÓI PHẢN HỒI JSON", "Tuần tự hóa [System.Text.Json]", [
            "• Chuyển Entity -> EventDto (ẩn trường nhạy cảm)",
            "• Đóng gói ApiResponse<PagedResponse<EventDto>>",
            "• Trả về HTTP 200 OK với body JSON chuẩn camelCase:",
            "  {\"success\": true, \"data\": {\"items\": [...], ...}}"
        ], C_TEAL, Inches(4.85), Inches(3.95), Inches(3.6), Inches(2.4)),

        ("CHẶNG 6: NHẬN JSON & CẬP NHẬT UI", "Luồng Giao diện [UI Thread]", [
            "• Client giải mã JSON và đưa về Main UI Thread:",
            "• Web: setEvents(data.items) -> Virtual DOM render",
            "• WinForms: grdEvents.DataSource = items (UI)",
            "• Android: runOnUiThread -> adapter.notifyDataSetChanged()"
        ], C_GREEN, Inches(8.9), Inches(3.95), Inches(3.633), Inches(2.4))
    ]

    for title, badge, bullets, col, x, y, w, h in stages_grid:
        box = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
        box.fill.solid()
        box.fill.fore_color.rgb = C_WHITE
        box.line.color.rgb = col
        box.line.width = Pt(1.5)

        tx = s9.shapes.add_textbox(x + Inches(0.08), y + Inches(0.08), w - Inches(0.16), h - Inches(0.16))
        tf = tx.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = col

        p_badge = tf.add_paragraph()
        p_badge.text = f"[{badge}]"
        p_badge.font.size = Pt(8.5)
        p_badge.font.color.rgb = C_MUTED

        for b in bullets:
            p_b = tf.add_paragraph()
            p_b.text = b
            p_b.font.size = Pt(8)
            p_b.font.color.rgb = C_DARK

    # Connector Arrows
    arr1 = s9.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(4.45), Inches(2.35), Inches(0.35), Inches(0.22))
    arr1.fill.solid()
    arr1.fill.fore_color.rgb = C_TEAL
    arr1.line.fill.background()

    arr2 = s9.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(8.5), Inches(2.35), Inches(0.35), Inches(0.22))
    arr2.fill.solid()
    arr2.fill.fore_color.rgb = C_TEAL
    arr2.line.fill.background()

    arr4 = s9.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(4.45), Inches(4.95), Inches(0.35), Inches(0.22))
    arr4.fill.solid()
    arr4.fill.fore_color.rgb = C_TEAL
    arr4.line.fill.background()

    arr5 = s9.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(8.5), Inches(4.95), Inches(0.35), Inches(0.22))
    arr5.fill.solid()
    arr5.fill.fore_color.rgb = C_TEAL
    arr5.line.fill.background()

    # Bottom summary banner
    card_s9_sum = s9.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.48), Inches(11.733), Inches(0.45))
    card_s9_sum.fill.solid()
    card_s9_sum.fill.fore_color.rgb = C_LIGHT_TEAL
    card_s9_sum.line.color.rgb = C_TEAL
    tx_s9 = s9.shapes.add_textbox(Inches(0.9), Inches(6.51), Inches(11.5), Inches(0.4))
    p = tx_s9.text_frame.paragraphs[0]
    p.text = "🎯 ĐIỂM CỐT LÕI: Cả 3 nền tảng đều đi qua đúng 6 chặng này, sử dụng chung hợp đồng API, chung DTO và chung nguồn cơ sở dữ liệu."
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    s9.notes_slide.notes_text_frame.text = (
        "LỜI THUYẾT TRÌNH (HỒ ĐOÀNG NGUYÊN KHANG - 1p00s):\n"
        "Thưa Thầy, để minh họa một chu trình request hoàn chỉnh, nhóm em chọn endpoint GET /api/events "
        "đi qua đủ 6 chặng kỹ thuật: "
        "Chặng 1: Bắt đầu từ thao tác của người dùng trên giao diện. "
        "Chặng 2: Client gọi hàm mạng bất đồng bộ tương ứng ở từng ngôn ngữ. "
        "Chặng 3: Gói tin HTTP mang tham số phân trang gửi tới cổng 443 của máy chủ Kestrel. "
        "Chặng 4: Server tiếp nhận tại EventsController, gọi EventService truy vấn PostgreSQL bằng EF Core. "
        "Chặng 5: Server đóng gói kết quả dạng JSON UTF-8 PagedResponse trả về cho client. "
        "Chặng 6: Client giải mã JSON, đưa về Luồng Chính và đổ dữ liệu lên màn hình. "
        "Cả ba nền tảng đều đi qua đúng 6 chặng này một cách nhất quán."
    )

    # ==========================================
        # ==========================================
    # SLIDE 10: SƠ ĐỒ XÁC THỰC & PHÂN QUYỀN JWT (HỒ ĐOÀNG NGUYÊN KHANG)
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "SƠ ĐỒ VÒNG ĐỜI JWT, XÁC THỰC & PHÂN BIỆT 401 VS 403", "09. Bảo mật & Xác thực", 10, "Hồ Đoàng Nguyên Khang")

    jwt_steps = [
        ("1. Đăng nhập", "POST /api/auth/login\nGửi username & password", C_BLUE, Inches(0.8)),
        ("2. Phát JWT Token", "Ký HMAC-SHA256\nChứa claims UserId & Role", C_TEAL, Inches(3.25)),
        ("3. Lưu trữ Client", "Client Storage\nWeb: LocalStorage\nAndroid: SharedPreferences\nWinForms: AppState", C_DARK, Inches(5.7)),
        ("4. Gọi API cần Auth", "Bearer Header\nGửi header:\nAuthorization: Bearer <token>", C_BLUE, Inches(8.15)),
        ("5. Server Kiểm tra", "Middleware RBAC\nGiải mã token, kiểm tra role:\n• 401: Thiếu / Hết hạn\n• 403: Sai vai trò", C_RED, Inches(10.6))
    ]

    for title, desc, col, x_pos in jwt_steps:
        box = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x_pos, Inches(1.35), Inches(1.95), Inches(1.4))
        box.fill.solid()
        box.fill.fore_color.rgb = C_WHITE
        box.line.color.rgb = col
        box.line.width = Pt(1.5)

        tx = s10.shapes.add_textbox(x_pos + Inches(0.04), Inches(1.38), Inches(1.87), Inches(1.34))
        tf = tx.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = col
        p.alignment = PP_ALIGN.CENTER

        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(8)
        p_desc.font.color.rgb = C_DARK
        p_desc.alignment = PP_ALIGN.CENTER

        if x_pos < Inches(10.0):
            arr = s10.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, x_pos + Inches(1.98), Inches(1.9), Inches(0.44), Inches(0.22))
            arr.fill.solid()
            arr.fill.fore_color.rgb = C_TEAL
            arr.line.fill.background()

    # Evidence: 401 vs 403 cards (Using actual filenames: 13_401_response.png and 14_403_response.png)
    img_401 = os.path.join(EVIDENCE_DIR, "13_401_response.png")
    if os.path.exists(img_401):
        s10.shapes.add_picture(img_401, Inches(0.8), Inches(2.9), width=Inches(5.7))

    img_403 = os.path.join(EVIDENCE_DIR, "14_403_response.png")
    if os.path.exists(img_403):
        s10.shapes.add_picture(img_403, Inches(6.8), Inches(2.9), width=Inches(5.733))

    # Bottom rule
    card_jwt_rule = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.48), Inches(11.733), Inches(0.45))
    card_jwt_rule.fill.solid()
    card_jwt_rule.fill.fore_color.rgb = C_LIGHT_BLUE
    card_jwt_rule.line.color.rgb = C_BLUE
    tx_jr = s10.shapes.add_textbox(Inches(0.9), Inches(6.51), Inches(11.5), Inches(0.4))
    p = tx_jr.text_frame.paragraphs[0]
    p.text = "🔒 NGUYÊN TẮC: 401 Unauthorized (Chưa đăng nhập / Token hết hạn) khác hẳn 403 Forbidden (Đã đăng nhập nhưng không đủ quyền). Server tự đọc UserId từ Claims, tuyệt đối không tin tham số client gửi lên."
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    s10.notes_slide.notes_text_frame.text = (
        "LỜI THUYẾT TRÌNH (HỒ ĐOÀNG NGUYÊN KHANG - 1p05s):\n"
        "Về cơ chế xác thực và phân quyền, hệ thống sử dụng chuẩn JWT HMAC-SHA256. "
        "Lưu ý quan trọng: JWT là token được ký số chứ không phải chuỗi mã hóa; bất kỳ ai cũng có thể giải mã Base64 phần payload "
        "nhưng không thể làm giả chữ ký nếu không có Secret Key trên server. "
        "Hai hình bên dưới là bằng chứng kiểm thử thực tế từ curl và backend log: "
        "Hình bên trái: Khi gọi endpoint quản trị mà không truyền token, Kestrel Middleware chặn ngay lập tức và trả về HTTP 401 Unauthorized. "
        "Hình bên phải: Khi đăng nhập bằng tài khoản Sinh viên (đã có token hợp lệ) nhưng cố gọi API đổi vai trò người dùng, "
        "thuộc tính [Authorize(Roles = \"Admin\")] phát hiện vai trò không thỏa mãn và trả về HTTP 403 Forbidden. "
        "Server tự đọc UserId từ Claims, không bao giờ tin tham số id do client gửi lên."
    )

    # ==========================================
    # SLIDE 11: JSON & DATABASE (HỒ ĐOÀNG NGUYÊN KHANG)
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "JSON, DTO, PHÂN TRANG & THIẾT KẾ CƠ SỞ DỮ LIỆU", "10. Quản lý Dữ liệu", 11, "Hồ Đoàng Nguyên Khang")

    # Left Column: Real JSON Response Box + C# PagedResponse DTO Code Box
    # Top Left: JSON Structure Box
    json_box = s11.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.35), Inches(5.7), Inches(2.5))
    json_box.fill.solid()
    json_box.fill.fore_color.rgb = C_NAVY
    json_box.line.color.rgb = C_TEAL
    json_box.line.width = Pt(1.5)
    tx_jb = s11.shapes.add_textbox(Inches(0.9), Inches(1.4), Inches(5.5), Inches(2.4))
    tf_jb = tx_jb.text_frame
    tf_jb.word_wrap = True
    p = tf_jb.paragraphs[0]
    p.text = "// Phản hồi JSON thực tế (camelCase) từ GET /api/events:"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    json_lines = [
        '{',
        '  "success": true,',
        '  "data": {',
        '    "items": [{ "id": 1, "title": "Workshop: Git & CI/CD", "category": "Tech" }],',
        '    "pageNumber": 1, "pageSize": 10, "totalCount": 24, "totalPages": 3',
        '  }',
        '}'
    ]
    for jl in json_lines:
        p = tf_jb.add_paragraph()
        p.text = jl
        p.font.size = Pt(8.5)
        p.font.color.rgb = RGBColor(226, 232, 240)
        p.font.name = "Consolas"

    # Bottom Left: C# DTO Box (<= 10 lines)
    dto_box = s11.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(3.95), Inches(5.7), Inches(2.4))
    dto_box.fill.solid()
    dto_box.fill.fore_color.rgb = C_NAVY
    dto_box.line.color.rgb = C_BLUE
    dto_box.line.width = Pt(1.5)
    tx_db = s11.shapes.add_textbox(Inches(0.9), Inches(4.0), Inches(5.5), Inches(2.3))
    tf_db = tx_db.text_frame
    tf_db.word_wrap = True
    p = tf_db.paragraphs[0]
    p.text = "// PagedResponse.cs – Vỏ bọc phân trang chuẩn C# (Mã nguồn thật):"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_BLUE

    dto_lines = [
        "public class PagedResponse<T> {",
        "    public List<T> Items { get; set; } = new();",
        "    public int TotalCount { get; set; }",
        "    public int PageNumber { get; set; }",
        "    public int PageSize { get; set; }",
        "    public int TotalPages => (int)Math.Ceiling(TotalCount / (double)PageSize);",
        "    public bool HasNextPage => PageNumber < TotalPages;",
        "}"
    ]
    for dl in dto_lines:
        p = tf_db.add_paragraph()
        p.text = dl
        p.font.size = Pt(8.5)
        p.font.color.rgb = RGBColor(226, 232, 240)
        p.font.name = "Consolas"

    # Right Column: 2 Cards (DTO Role & Database Engineering)
    card_dto_role = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.35), Inches(5.733), Inches(2.5))
    card_dto_role.fill.solid()
    card_dto_role.fill.fore_color.rgb = C_WHITE
    card_dto_role.line.color.rgb = C_BLUE
    card_dto_role.line.width = Pt(1.5)
    tx_dr = s11.shapes.add_textbox(Inches(6.9), Inches(1.4), Inches(5.533), Inches(2.4))
    tf_dr = tx_dr.text_frame
    tf_dr.word_wrap = True
    p = tf_dr.paragraphs[0]
    p.text = "🛡️ VAI TRÒ CỐT LÕI CỦA DTO TRONG HỆ THỐNG:"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = C_BLUE
    dto_roles = [
        "• Không bao giờ trả Entity trực tiếp: Che giấu thông tin nhạy cảm như PasswordHash và trường kiểm toán nội bộ.",
        "• Chống đệ quy vòng lặp JSON (Cyclic Reference) giữa các bảng có quan hệ 1-N trong Entity Framework Core.",
        "• Tối ưu kích thước gói tin mạng (Payload Size), chỉ gửi những trường giao diện thực sự cần."
    ]
    for dr in dto_roles:
        p = tf_dr.add_paragraph()
        p.text = dr
        p.font.size = Pt(8.5)
        p.font.color.rgb = C_DARK

    card_db_eng = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(3.95), Inches(5.733), Inches(2.4))
    card_db_eng.fill.solid()
    card_db_eng.fill.fore_color.rgb = C_WHITE
    card_db_eng.line.color.rgb = C_TEAL
    card_db_eng.line.width = Pt(1.5)
    tx_de = s11.shapes.add_textbox(Inches(6.9), Inches(4.0), Inches(5.533), Inches(2.3))
    tf_de = tx_de.text_frame
    tf_de.word_wrap = True
    p = tf_de.paragraphs[0]
    p.text = "🗄️ THIẾT KẾ DATABASE & TỐI ƯU EF CORE 8:"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    db_items = [
        "• PostgreSQL 16 trên Supabase: Chuẩn ACID, hỗ trợ JSONB, Pooler cổng 5432 giúp phục vụ nhiều kết nối đồng thời.",
        "• Tối ưu AsNoTracking(): Sử dụng cho toàn bộ các API truy vấn đọc dữ liệu, tăng tốc độ phản hồi 30-40%.",
        "• Khóa ngoại (Foreign Keys): Ràng buộc toàn vẹn giữa Users, Roles, Events và Registrations, chống dữ liệu mồ côi."
    ]
    for di in db_items:
        p = tf_de.add_paragraph()
        p.text = di
        p.font.size = Pt(8.5)
        p.font.color.rgb = C_DARK

    # Bottom Banner
    card_s11_sum = s11.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.48), Inches(11.733), Inches(0.45))
    card_s11_sum.fill.solid()
    card_s11_sum.fill.fore_color.rgb = C_LIGHT_TEAL
    card_s11_sum.line.color.rgb = C_TEAL
    tx_s11 = s11.shapes.add_textbox(Inches(0.9), Inches(6.51), Inches(11.5), Inches(0.4))
    p = tx_s11.text_frame.paragraphs[0]
    p.text = "🎯 NGUYÊN TẮC PHÂN TRANG: Luôn phân trang ở tầng Database qua LINQ .Skip().Take(). Giới hạn trần Math.Min(pageSize, 50) ngăn chặn client ép server quá tải."
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    s11.notes_slide.notes_text_frame.text = (
        "LỜI THUYẾT TRÌNH (HỒ ĐOÀNG NGUYÊN KHANG - 1p00s):\n"
        "Về thiết kế dữ liệu, nhóm sử dụng DTO thay vì trả thẳng thực thể Entity ra ngoài. "
        "DTO giúp che giấu mật khẩu đã băm, tránh lỗi vòng lặp đệ quy trong Entity Framework và giảm tải đường truyền. "
        "Mọi danh sách đều được bọc trong PagedResponse có phân trang rõ ràng. "
        "Cơ sở dữ liệu PostgreSQL lưu trên Supabase với các truy vấn đọc đều dùng AsNoTracking để tối ưu hiệu năng. "
        "Tiếp theo, em xin chuyển lời cho anh Võ Ngọc Minh Đạt trình bày về ứng dụng Windows Forms, "
        "phân tích sự cố CI và tổng kết bài báo cáo. Xin mời anh Đạt!"
    )

# SLIDE 12: WINDOWS FORMS C# (VÕ NGỌC MINH ĐẠT)
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "ỨNG DỤNG QUẢN TRỊ DESKTOP: WINDOWS FORMS C#", "11. Ứng dụng Desktop", 12, "Võ Ngọc Minh Đạt")

    img_win = os.path.join(EVIDENCE_DIR, "08_winforms_dashboard.png")
    if os.path.exists(img_win):
        s12.shapes.add_picture(img_win, Inches(0.8), Inches(1.5), width=Inches(4.6))

    # Controls table
    t12 = s12.shapes.add_table(5, 3, Inches(5.6), Inches(1.5), Inches(6.9), Inches(2.0)).table
    t12.columns[0].width = Inches(2.0)
    t12.columns[1].width = Inches(1.8)
    t12.columns[2].width = Inches(3.1)
    for i, h in enumerate(headers):
        cell = t12.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_TEAL
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = C_WHITE

    ctrl_rows12 = [
        ("grdDangKy", "DataGridView", "Hiển thị bảng danh sách sinh viên đăng ký sự kiện"),
        ("btnDiemDanh", "Button", "Xác nhận điểm danh sinh viên tham gia sự kiện"),
        ("cboSuKien", "ComboBox", "Chọn sự kiện cần xem danh sách đăng ký"),
        ("lblTongSo", "Label", "Hiển thị tổng số lượt đăng ký từ server trả về")
    ]
    for row_idx, r in enumerate(ctrl_rows12, start=1):
        for col_idx, val in enumerate(r):
            cell = t12.cell(row_idx, col_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_WHITE
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(9)
            p.font.color.rgb = C_DARK

    # Code Box <= 10 lines
    code_box12 = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.6), Inches(3.7), Inches(6.9), Inches(2.7))
    code_box12.fill.solid()
    code_box12.fill.fore_color.rgb = C_NAVY
    code_box12.line.color.rgb = C_TEAL
    tx_c12 = s12.shapes.add_textbox(Inches(5.7), Inches(3.75), Inches(6.7), Inches(2.6))
    tf_c12 = tx_c12.text_frame
    tf_c12.word_wrap = True
    p = tf_c12.paragraphs[0]
    p.text = "// ApiService.cs – Tái sử dụng HttpClient & async/await (Mã nguồn thật):"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    code_lines12 = [
        "public class ApiService {",
        "    // Dung chung HttpClient duy nhat (Singleton) de tranh can kiet socket",
        "    private static readonly HttpClient _http = new HttpClient();",
        "    ",
        "    public async Task<ApiResponse<T>> GetAsync<T>(string endpoint) {",
        "        using var req = new HttpRequestMessage(HttpMethod.Get, _baseUrl + endpoint);",
        "        if (!string.IsNullOrEmpty(_token)) req.Headers.Authorization = new(\"Bearer\", _token);",
        "        var res = await _http.SendAsync(req); // await tra quyen dieu khien cho UI",
        "        return await res.Content.ReadFromJsonAsync<ApiResponse<T>>();",
        "    }",
        "}"
    ]
    for cl in code_lines12:
        p = tf_c12.add_paragraph()
        p.text = cl
        p.font.size = Pt(8.5)
        p.font.color.rgb = RGBColor(226, 232, 240)
        p.font.name = "Consolas"

    card_w12 = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.45), Inches(11.733), Inches(0.55))
    card_w12.fill.solid()
    card_w12.fill.fore_color.rgb = C_WHITE
    card_w12.line.color.rgb = C_BORDER
    tx_w12 = s12.shapes.add_textbox(Inches(0.9), Inches(6.48), Inches(11.5), Inches(0.5))
    p = tx_w12.text_frame.paragraphs[0]
    p.text = "⚡ Quy tắc sống còn trên WinForms: Tuyệt đối không gọi .Result hoặc .Wait() trên Task vì sẽ gây DEADLOCK khóa cứng giao diện. Luôn dùng async và await."
    p.font.size = Pt(9)
    p.font.color.rgb = C_RED

    s12.notes_slide.notes_text_frame.text = (
        "LỜI THUYẾT TRÌNH (VÕ NGỌC MINH ĐẠT - 55s):\n"
        "Kính chào Thầy và các bạn! Em tên là Võ Ngọc Minh Đạt, phụ trách ứng dụng Windows Forms, phân tích sự cố và kết luận đồ án. "
        "Ứng dụng Windows Forms được xây dựng bằng C# .NET 8 dành cho Ban Chủ Nhiệm quản trị sự kiện và điểm danh. "
        "Bên trái là ảnh chụp thật giao diện quản trị. Các điều khiển gồm bảng grdDangKy, nút btnDiemDanh và cboSuKien. "
        "Đoạn mã bên phải thể hiện lớp ApiService: nhóm dùng chung một đối tượng HttpClient duy nhất theo mẫu Singleton "
        "để tránh cạn kiệt cổng socket (Socket Exhaustion). "
        "Đồng thời, nhóm luôn dùng từ khóa await để giải phóng giao diện trong lúc chờ server, "
        "tuyệt đối không gọi .Result hay .Wait() vì sẽ gây Deadlock khóa cứng cửa sổ phần mềm."
    )

    # ==========================================
    # SLIDE 13: DEMO WINFORMS TRỰC TIẾP (VÕ NGỌC MINH ĐẠT)
    # ==========================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "DEMO TRỰC TIẾP: QUẢN TRỊ VÀ ĐIỂM DANH TRÊN WINFORMS", "12. Demo Quản trị Desktop", 13, "Võ Ngọc Minh Đạt")

    img_ev = os.path.join(EVIDENCE_DIR, "09_winforms_events.png")
    if os.path.exists(img_ev):
        s13.shapes.add_picture(img_ev, Inches(0.8), Inches(1.5), width=Inches(4.6))

    card_dw = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.6), Inches(1.5), Inches(6.9), Inches(5.2))
    card_dw.fill.solid()
    card_dw.fill.fore_color.rgb = C_WHITE
    card_dw.line.color.rgb = C_BORDER
    tx_dw = s13.shapes.add_textbox(Inches(5.8), Inches(1.7), Inches(6.5), Inches(4.8))
    tf_dw = tx_dw.text_frame
    tf_dw.word_wrap = True
    p = tf_dw.paragraphs[0]
    p.text = "KỊCH BẢN THAO TÁC DEMO ĐIỂM DANH TRỰC TIẾP:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_BLUE

    steps_w = [
        ("Bước 1: Mở ứng dụng Visionary.Desktop.exe", "Phần mềm đã được biên dịch sẵn sang .NET 8, mở ra là chạy ngay."),
        ("Bước 2: Đăng nhập tài khoản Ban Chủ Nhiệm (Committee)", "Gọi POST /api/auth/login, nhận JWT token và lưu vào biến tĩnh AppState.Token."),
        ("Bước 3: Chọn sự kiện 'Hội thảo Kỹ năng Hội nhập Quốc tế'", "Gọi GET /api/events/{id}/registrations để nạp danh sách đăng ký lên DataGridView."),
        ("Bước 4: Kiểm chứng sinh viên vừa đăng ký trên Android", "Thấy ngay bản ghi của bạn Trí Khang vừa bấm đăng ký ở phần demo Android trước."),
        ("Bước 5: Nhấn nút 'Xác nhận Điểm danh' (btnDiemDanh)", "Gọi POST /api/events/{id}/attendance, server cập nhật trạng thái 'Đã tham gia' tức thì.")
    ]
    for st, sd in steps_w:
        p = tf_dw.add_paragraph()
        p.text = "👉 " + st
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = C_NAVY
        p2 = tf_dw.add_paragraph()
        p2.text = "     " + sd
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = C_DARK

    s13.notes_slide.notes_text_frame.text = (
        "LỜI THUYẾT TRÌNH (VÕ NGỌC MINH ĐẠT - 1'05\"):\n"
        "Sau đây em xin demo trực tiếp ứng dụng WinForms đã biên dịch sẵn. "
        "[ĐẠT THAO TÁC]: Em mở file Visionary.Desktop.exe và đăng nhập tài khoản Ban Chủ Nhiệm. "
        "Tại màn hình Quản lý Sự kiện, em chọn 'Hội thảo Kỹ năng Hội nhập Quốc tế'. "
        "Trên DataGridView, Thầy có thể thấy ngay dòng đăng ký của bạn Trí Khang vừa thực hiện trên Android ở phần trước. "
        "Em bấm nút 'Điểm danh', phần mềm gửi request POST /attendance lên Web API. "
        "Hệ thống lập tức cập nhật trạng thái 'Đã tham gia' với tick xanh. "
        "Điều này chứng minh ba ứng dụng hoạt động hoàn toàn đồng bộ trên cùng một nguồn dữ liệu duy nhất."
    )

    # ==========================================
    # SLIDE 14: BA ĐIỂM KHÁC BIỆT KỸ THUẬT (VÕ NGỌC MINH ĐẠT)
    # ==========================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "BA ĐIỂM KHÁC BIỆT KỸ THUẬT & ĐIỀU BẮT BUỘC GIỐNG NHAU", "13. So sánh Nền tảng", 14, "Võ Ngọc Minh Đạt")

    # Comparison Table
    t14 = s14.shapes.add_table(5, 4, Inches(0.8), Inches(1.5), Inches(11.733), Inches(3.2)).table
    t14.columns[0].width = Inches(2.5)
    t14.columns[1].width = Inches(3.0)
    t14.columns[2].width = Inches(3.0)
    t14.columns[3].width = Inches(3.2)

    h14 = ["Khác biệt Kỹ thuật", "Web Client (HTML/TS)", "Windows Forms (C#)", "Android Native (Java)"]
    for i, h in enumerate(h14):
        cell = t14.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_WHITE

    diff_rows = [
        ("1. Thư viện mạng &\nBất đồng bộ", "fetch() API\nPromise & async/await\nEvent Loop trình duyệt", "HttpClient\nTask & async/await\nSynchronizationContext", "Retrofit 2 + OkHttp\nCall.enqueue() Callback\nWorker Thread chạy ngầm"),
        ("2. Điều phối Luồng\ngiao diện (UI Thread)", "Tự động hoàn toàn\n(Single-threaded JS Engine\nkhông lo xung đột luồng)", "Tự động quay về UI Thread\nsau lệnh await\n(Tuyệt đối tránh .Result)", "Bắt buộc chuyển thủ công:\nHandler(Looper.getMainLooper())\nđể cập nhật View"),
        ("3. Môi trường chạy &\nQuản lý JWT Token", "Trình duyệt (Browser)\nLưu trong localStorage / Cookie\nMất khi xóa cache", "Desktop Windows OS\nLưu trong biến static AppState\nMất khi tắt tiến trình .exe", "Thiết bị di động Android\nLưu SharedPreferences bền vững\nVẫn còn khi thoát ứng dụng"),
        ("Lý do khác biệt", "Do NỀN TẢNG BẮT BUỘC\n(Engine JS & Browser Sandbox)", "Do NHÓM LỰA CHỌN\n(Tận dụng .NET 8 async/await)", "Do NỀN TẢNG BẮT BUỘC\n(Cơ chế quản lý UI của Android)")
    ]
    for row_idx, (crit, web_v, win_v, and_v) in enumerate(diff_rows, start=1):
        r_data = [crit, web_v, win_v, and_v]
        for col_idx, val in enumerate(r_data):
            cell = t14.cell(row_idx, col_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_WHITE
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(8.5)
            p.font.color.rgb = C_DARK
            if col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = C_BLUE

    # Card for Things that MUST BE IDENTICAL
    card_same = s14.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(5.0), Inches(11.733), Inches(1.85))
    card_same.fill.solid()
    card_same.fill.fore_color.rgb = C_WHITE
    card_same.line.color.rgb = C_TEAL
    card_same.line.width = Pt(1.5)
    tx_same = s14.shapes.add_textbox(Inches(1.0), Inches(5.05), Inches(11.3), Inches(1.75))
    tf_s = tx_same.text_frame
    tf_s.word_wrap = True
    p = tf_s.paragraphs[0]
    p.text = "⭐ NHỮNG ĐIỀU BẮT BUỘC PHẢI GIỐNG HỆT NHAU TRÊN CẢ BA NỀN TẢNG:"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    sames = [
        "1. Hợp đồng API (API Contract): Cùng phương thức HTTP (GET, POST, PUT), cùng đường dẫn (/api/events), cùng tên trường JSON camelCase.",
        "2. Xác thực và Phân quyền: Cùng cấu trúc Header 'Authorization: Bearer <token>', cùng mã lỗi 401 khi hết hạn và 403 khi thiếu quyền.",
        "3. Quy tắc nghiệp vụ (Business Rules): Cùng kiểm tra hạn chót đăng ký trên server, cùng tính số lượng chỗ trống từ cơ sở dữ liệu."
    ]
    for sm in sames:
        p = tf_s.add_paragraph()
        p.text = sm
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_DARK

    s14.notes_slide.notes_text_frame.text = (
        "LỜI THUYẾT TRÌNH (VÕ NGỌC MINH ĐẠT - 55s):\n"
        "Thưa Thầy, dù cùng kết nối vào một Web API, ba nền tảng có 3 điểm khác biệt kỹ thuật:\n"
        "Thứ nhất là thư viện mạng: Web dùng Fetch; WinForms dùng HttpClient với async/await; còn Android dùng Retrofit enqueue.\n"
        "Thứ hai là điều phối luồng: C# tự động quay về UI Thread sau lệnh await; còn Android bắt buộc chuyển qua Handler Looper. "
        "Thứ ba là lưu token: Web lưu LocalStorage, WinForms lưu trong bộ nhớ RAM, còn Android lưu vào SharedPreferences.\n"
        "Ngược lại, những điều bắt buộc phải giống hệt nhau là: URL endpoint, phương thức HTTP, cấu trúc JSON và quy tắc phân quyền trên server."
    )

    # ==========================================
        # ==========================================
    # SLIDE 15: SỰ CỐ THẬT: GITHUB ACTIONS CI RUN #12 -> RUN #40231783994 (VÕ NGỌC MINH ĐẠT)
    # ==========================================
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "SỰ CỐ THỰC TẾ TRÊN GITHUB ACTIONS CI VÀ QUY TRÌNH SỬA LỖI", "14. Quản lý Sự cố & CI/CD", 15, "Võ Ngọc Minh Đạt")

    # 3-Column Layout: Left = Error Log (Run #12), Middle = Root Cause & Architecture Fix, Right = Verified Pass (Run #40231783994)
    img_err = os.path.join(EVIDENCE_DIR, "15_real_error_log.png")
    if os.path.exists(img_err):
        s15.shapes.add_picture(img_err, Inches(0.8), Inches(1.35), width=Inches(3.7))

    # Center box: Root Cause Diagram
    box_diag = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.7), Inches(1.35), Inches(3.9), Inches(5.0))
    box_diag.fill.solid()
    box_diag.fill.fore_color.rgb = C_WHITE
    box_diag.line.color.rgb = C_NAVY
    box_diag.line.width = Pt(1.5)
    
    tx_bd = s15.shapes.add_textbox(Inches(4.8), Inches(1.4), Inches(3.7), Inches(4.9))
    tf_bd = tx_bd.text_frame
    tf_bd.word_wrap = True
    
    p = tf_bd.paragraphs[0]
    p.text = "SƠ ĐỒ CHẨN ĐOÁN & SỬA LỖI"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.alignment = PP_ALIGN.CENTER

    diag_steps = [
        ("1. BẮT ĐẦU: CI RUN #12 THẤT BẠI", "13 Passed / 2 Failed trên Ubuntu Linux.\n• Search test fail dòng 168 (TotalCount = 0)\n• GetPostBySlug fail dòng 183 (404 Not Found)", C_RED),
        ("2. NGUYÊN NHÂN GỐC RỄ (ROOT CAUSE)", "Hai Test Class chạy song song trên xUnit:\nCùng khởi tạo WebApplicationFactory trỏ vào visionary.db -> Đụng độ UNIQUE Roles.Name -> Hủy ngang SeedAsync trước khi nạp Posts!", C_NAVY),
        ("3. GIẢI PHÁP KỸ THUẬT (REMEDIATION)", "• Khóa luồng tĩnh SemaphoreSlim(1,1) trong DbInitializer.SeedAsync().\n• Tạo CustomWebApplicationFactory cấp phát DB test cô lập.\n• Gộp chung [Collection(\"IntegrationTests\")].", C_TEAL),
        ("4. KẾT QUẢ KIỂM CHỨNG (VERIFICATION)", "Chạy lại kiểm thử hồi quy 3 lần liên tiếp:\n15/15 Passed 100% (2.8s) -> Push commit c7af080 lên GitHub -> Run #40231783994 XANH!", C_GREEN)
    ]
    for st, sd, col in diag_steps:
        p = tf_bd.add_paragraph()
        p.text = st
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = col
        p2 = tf_bd.add_paragraph()
        p2.text = sd
        p2.font.size = Pt(8)
        p2.font.color.rgb = C_DARK

    # Right: Fixed Test Log / CI Pass
    img_fix = os.path.join(EVIDENCE_DIR, "16_error_fixed_test.png")
    if os.path.exists(img_fix):
        s15.shapes.add_picture(img_fix, Inches(8.8), Inches(1.35), width=Inches(3.7))

    card_ci_stat = s15.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.48), Inches(11.733), Inches(0.45))
    card_ci_stat.fill.solid()
    card_ci_stat.fill.fore_color.rgb = C_LIGHT_TEAL
    card_ci_stat.line.color.rgb = C_GREEN
    tx_cs = s15.shapes.add_textbox(Inches(0.9), Inches(6.51), Inches(11.5), Inches(0.4))
    p = tx_cs.text_frame.paragraphs[0]
    p.text = "✅ ĐÃ XÁC MINH TRÊN GITHUB ACTIONS: Run #40231783994 (Commit c7af080) hoàn thành xuất sắc – 15/15 Tests Passed 100% trên Linux x64."
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_GREEN

    s15.notes_slide.notes_text_frame.text = (
        "LỜI THUYẾT TRÌNH (VÕ NGỌC MINH ĐẠT - 1p00s):\n"
        "Trong quá trình kiểm thử tự động, nhóm em đã đối mặt với một sự cố kỹ thuật có thật. "
        "Bên trái là log lỗi nguyên văn từ GitHub Actions Run #12: pipeline bị gãy với 13 bài đạt và 2 bài thất bại. "
        "Nguyên nhân gốc rễ do xUnit chạy hai class test song song, cùng tranh chấp file SQLite khiến lệnh Seed bị dừng đột ngột ở ràng buộc Unique Role. "
        "Nhóm đã tự phân tích và khắc phục triệt để bằng khóa SemaphoreSlim và kiến trúc CustomWebApplicationFactory cô lập cơ sở dữ liệu. "
        "Như hình bên phải, toàn bộ 15 bài test đã vượt qua 100% và GitHub Actions Run #40231783994 đã báo xanh hoàn toàn."
    )

# SLIDE 16: GIỚI HẠN, HƯỚNG PHÁT TRIỂN & KẾT THÚC (VÕ NGỌC MINH ĐẠT)
    # ==========================================
    s16 = prs.slides.add_slide(blank_layout)
    add_header(s16, "GIỚI HẠN THỰC TẾ, HƯỚNG PHÁT TRIỂN & KẾT LUẬN", "15. Đánh giá & Hướng phát triển", 16, "Võ Ngọc Minh Đạt")

    card_lim = s16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(4.1))
    card_lim.fill.solid()
    card_lim.fill.fore_color.rgb = C_WHITE
    card_lim.line.color.rgb = C_BORDER
    tx_lim = s16.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(3.7))
    tf_lim = tx_lim.text_frame
    tf_lim.word_wrap = True
    p = tf_lim.paragraphs[0]
    p.text = "BA GIỚI HẠN THỰC TẾ CỦA HỆ THỐNG HIỆN TẠI"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_RED

    lims = [
        "1. Chưa có kiểm thử tự động E2E đa nền tảng đồng thời:",
        "   Nhóm mới kiểm thử tự động xUnit Backend và build APK độc lập; chưa có kịch bản E2E tự động xuyên suốt Web -> Mobile -> Desktop.",
        "2. Chưa có thông báo đẩy thời gian thực (Push Notification):",
        "   Khi BCN điểm danh hoặc có sự kiện mới, sinh viên chưa nhận được thông báo qua Firebase Cloud Messaging (FCM) hoặc SignalR.",
        "3. Một chỗ mã nguồn chưa tối ưu:",
        "   Cơ chế Refresh Token tự động khi JWT 4 giờ hết hạn chưa được triển khai hoàn chỉnh, người dùng vẫn phải đăng nhập lại."
    ]
    for lm in lims:
        p = tf_lim.add_paragraph()
        p.text = lm
        p.font.size = Pt(10)
        p.font.color.rgb = C_DARK

    card_plan = s16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(4.1))
    card_plan.fill.solid()
    card_plan.fill.fore_color.rgb = C_WHITE
    card_plan.line.color.rgb = C_BORDER
    tx_plan = s16.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.3), Inches(3.7))
    tf_plan = tx_plan.text_frame
    tf_plan.word_wrap = True
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
        "3. Bổ sung bộ kiểm thử E2E tự động:",
        "   Viết Playwright kiểm thử Web và Espresso kiểm thử Android để tích hợp vào quy trình CI/CD hoàn chỉnh."
    ]
    for pl in plans:
        p = tf_plan.add_paragraph()
        p.text = pl
        p.font.size = Pt(10)
        p.font.color.rgb = C_DARK

    box_end = s16.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(5.75), Inches(11.733), Inches(1.15))
    box_end.fill.solid()
    box_end.fill.fore_color.rgb = C_NAVY
    tx_end = s16.shapes.add_textbox(Inches(1.0), Inches(5.82), Inches(11.3), Inches(0.95))
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
        "LỜI THUYẾT TRÌNH (VÕ NGỌC MINH ĐẠT - 50s):\n"
        "Kính thưa Thầy, biết mình chưa làm được gì là một dạng hiểu biết chứ không phải lời thú tội. "
        "Dù hệ thống đã chạy tốt các chức năng chính, nhóm em thẳng thắn nhìn nhận ba hạn chế thực tế: "
        "chưa có kiểm thử E2E tự động đa nền tảng, chưa có thông báo đẩy thời gian thực qua SignalR, "
        "và cơ chế refresh token cần được tối ưu tốt hơn. "
        "Nếu có thêm hai tuần, nhóm em sẽ ưu tiên tích hợp SignalR và Room DB để nâng cao độ ổn định của ứng dụng. "
        "Đến đây, nhóm VISIONARY API xin kết thúc bài thuyết trình. "
        "Chúng em xin chân thành cảm ơn Thầy và các bạn đã chú ý lắng nghe. "
        "Nhóm chúng em sẵn sàng bước vào phần trả lời câu hỏi phản biện ạ! [KẾT THÚC TẠI ĐÂY - KHÔNG CHUYỂN LẠI CHO ĐỨC]."
    )

    output_path = "deliverables/VISIONARY_TH71108_FINAL_PRESENTATION.pptx"
    prs.save(output_path)
    print(f"Perfect 16-Slide Presentation generated successfully at: {output_path}")

if __name__ == "__main__":
    generate_perfect_presentation()
