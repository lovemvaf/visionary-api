import os

def update_slides_10_and_11():
    with open('scripts/build_perfect_presentation.py', 'r', encoding='utf-8') as f:
        content = f.read()

    new_s10 = '''    # ==========================================
    # SLIDE 10: SƠ ĐỒ XÁC THỰC & PHÂN QUYỀN JWT (HỒ ĐOÀN NGUYÊN KHANG)
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "SƠ ĐỒ VÒNG ĐỜI JWT, XÁC THỰC & PHÂN BIỆT 401 VS 403", "09. Bảo mật & Xác thực", 10, "Hồ Đoàn Nguyên Khang")

    jwt_steps = [
        ("1. Đăng nhập", "POST /api/auth/login\\nGửi username & password", C_BLUE, Inches(0.8)),
        ("2. Phát JWT Token", "Ký HMAC-SHA256\\nChứa claims UserId & Role", C_TEAL, Inches(3.25)),
        ("3. Lưu trữ Client", "Client Storage\\nWeb: LocalStorage\\nAndroid: SharedPreferences\\nWinForms: AppState", C_DARK, Inches(5.7)),
        ("4. Gọi API cần Auth", "Bearer Header\\nGửi header:\\nAuthorization: Bearer <token>", C_BLUE, Inches(8.15)),
        ("5. Server Kiểm tra", "Middleware RBAC\\nGiải mã token, kiểm tra role:\\n• 401: Thiếu / Hết hạn\\n• 403: Sai vai trò", C_RED, Inches(10.6))
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
        "LỜI THUYẾT TRÌNH (HỒ ĐOÀN NGUYÊN KHANG - 1p05s):\\n"
        "Về cơ chế xác thực và phân quyền, hệ thống sử dụng chuẩn JWT HMAC-SHA256. "
        "Lưu ý quan trọng: JWT là token được ký số chứ không phải chuỗi mã hóa; bất kỳ ai cũng có thể giải mã Base64 phần payload "
        "nhưng không thể làm giả chữ ký nếu không có Secret Key trên server. "
        "Hai hình bên dưới là bằng chứng kiểm thử thực tế từ curl và backend log: "
        "Hình bên trái: Khi gọi endpoint quản trị mà không truyền token, Kestrel Middleware chặn ngay lập tức và trả về HTTP 401 Unauthorized. "
        "Hình bên phải: Khi đăng nhập bằng tài khoản Sinh viên (đã có token hợp lệ) nhưng cố gọi API đổi vai trò người dùng, "
        "thuộc tính [Authorize(Roles = \\"Admin\\")] phát hiện vai trò không thỏa mãn và trả về HTTP 403 Forbidden. "
        "Server tự đọc UserId từ Claims, không bao giờ tin tham số id do client gửi lên."
    )
'''

    new_s11 = '''    # ==========================================
    # SLIDE 11: JSON & DATABASE (HỒ ĐOÀN NGUYÊN KHANG)
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "JSON, DTO, PHÂN TRANG & THIẾT KẾ CƠ SỞ DỮ LIỆU", "10. Quản lý Dữ liệu", 11, "Hồ Đoàn Nguyên Khang")

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
        "LỜI THUYẾT TRÌNH (HỒ ĐOÀN NGUYÊN KHANG - 1p00s):\\n"
        "Về thiết kế dữ liệu, nhóm sử dụng DTO thay vì trả thẳng thực thể Entity ra ngoài. "
        "DTO giúp che giấu mật khẩu đã băm, tránh lỗi vòng lặp đệ quy trong Entity Framework và giảm tải đường truyền. "
        "Mọi danh sách đều được bọc trong PagedResponse có phân trang rõ ràng. "
        "Cơ sở dữ liệu PostgreSQL lưu trên Supabase với các truy vấn đọc đều dùng AsNoTracking để tối ưu hiệu năng. "
        "Tiếp theo, em xin chuyển lời cho anh Võ Ngọc Minh Đạt trình bày về ứng dụng Windows Forms, "
        "phân tích sự cố CI và tổng kết bài báo cáo. Xin mời anh Đạt!"
    )
'''

    # Replace slide 10
    s10_start = content.find('# SLIDE 10: SƠ ĐỒ XÁC THỰC')
    s11_start = content.find('# SLIDE 11: JSON')
    s12_start = content.find('# SLIDE 12: WINDOWS FORMS')

    content = content[:s10_start] + new_s10 + '\n' + new_s11 + '\n' + content[s12_start:]

    with open('scripts/build_perfect_presentation.py', 'w', encoding='utf-8') as f:
        f.write(content)

    print('Updated Slide 10 and Slide 11 successfully.')

if __name__ == '__main__':
    update_slides_10_and_11()
