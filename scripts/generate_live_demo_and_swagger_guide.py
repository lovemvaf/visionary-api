import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from member_guides_helpers import set_cell_background, set_cell_margins, add_callout, add_code_box

def generate_live_demo_guide():
    doc = docx.Document()
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.85)
        s.right_margin = Inches(0.85)

    C_NAVY = RGBColor(15, 23, 42)
    C_BLUE = RGBColor(34, 100, 172)
    C_TEAL = RGBColor(34, 166, 161)
    C_GRAY = RGBColor(100, 116, 139)

    # University header
    p_uni = doc.add_paragraph()
    p_uni.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_uni = p_uni.add_run("TRƯỜNG ĐẠI HỌC CÔNG NGHỆ ĐỒNG NAI (DNTU)\nKHOA CÔNG NGHỆ THÔNG TIN – HỌC PHẦN WEB API (TH71108)")
    r_uni.bold = True
    r_uni.font.size = Pt(10)
    r_uni.font.color.rgb = C_BLUE
    p_uni.paragraph_format.space_after = Pt(4)

    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("HƯỚNG DẪN THAO TÁC DEMO TRỰC TIẾP & KIỂM THỬ SWAGGER TOÀN DIỆN\nHỆ THỐNG QUẢN LÝ HOẠT ĐỘNG HỘI NHẬP – VISIONARY")
    r_title.bold = True
    r_title.font.size = Pt(15)
    r_title.font.color.rgb = C_NAVY
    p_title.paragraph_format.space_after = Pt(4)

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_meta = p_meta.add_run("Tài liệu chuẩn bị cho 15 phút Thuyết trình & 10 phút Phản biện Cuối kỳ TH71108\nNhóm: VISIONARY API | Kịch bản chuỗi nghiệp vụ: Web Next.js -> Android Java -> WinForms C#")
    r_meta.italic = True
    r_meta.font.size = Pt(9.5)
    r_meta.font.color.rgb = C_GRAY
    p_meta.paragraph_format.space_after = Pt(14)

    add_callout(
        doc,
        "Tài liệu này hướng dẫn chi tiết từng cú nhấp chuột, từng tham số gửi lên Swagger, cách kích hoạt lỗi 401 Unauthorized và 403 Forbidden thật, quy trình CRUD chuẩn và quy trình đồng bộ dữ liệu xuyên suốt 3 nền tảng Web, Android, WinForms. Giúp nhóm làm chủ hoàn toàn buổi demo mà không gặp bất kỳ sự cố bất ngờ nào.",
        title="MỤC TIÊU VÀ NGUYÊN TẮC DEMO"
    )

    # Section 1: Chuẩn bị trước buổi demo
    doc.add_heading("13.1. CHECKLIST CHUẨN BỊ TRƯỚC BUỔI DEMO (PRE-FLIGHT CHECKLIST)", level=1)
    
    t_pre = doc.add_table(rows=11, cols=3)
    t_pre.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_pre = ["Bước", "Hạng mục kiểm tra", "Yêu cầu kỹ thuật & Trạng thái mong đợi"]
    for i, h in enumerate(h_pre):
        c = t_pre.cell(0, i)
        c.text = h
        c.paragraphs[0].runs[0].bold = True
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(c, "2264AC")

    pre_items = [
        ("1", "Kiểm tra API Health & Live Server", "Truy cập https://visionary-api-gb51.onrender.com/health trả về HTTP 200 'Healthy'."),
        ("2", "Mở sẵn Swagger UI", "Mở tab trình duyệt tại https://visionary-api-gb51.onrender.com/swagger, sẵn sàng thực thi."),
        ("3", "Kiểm tra Web Client", "Truy cập https://visionary-platform.vercel.app, đảm bảo trang chủ và tab sự kiện tải mượt mà."),
        ("4", "Chuẩn bị tài khoản demo", "Tài khoản BCN/Admin: committee_demo (vai trò Committee) | Tài khoản SV: student_demo (vai trò Student)."),
        ("5", "Khởi động Android Emulator", "Bật Android Studio Virtual Device (Pixel API 34). Cài sẵn app-debug.apk (6.4 MB)."),
        ("6", "Khởi chạy Windows Forms", "Mở sẵn file thực thi Visionary.Desktop.exe từ thư mục bin/Debug/net8.0-windows/."),
        ("7", "Kiểm tra kết nối mạng (Wi-Fi)", "Đảm bảo máy thuyết trình có kết nối internet ổn định hoặc 4G phát từ điện thoại."),
        ("8", "Kiểm tra HTTPS & Chứng chỉ", "Backend chạy HTTPS chuẩn trên Render có chứng chỉ SSL hợp lệ."),
        ("9", "Kiểm tra Cơ sở dữ liệu Supabase", "Kiểm tra kết nối PostgreSQL qua pooler cổng 5432 hoạt động bình thường."),
        ("10", "Chuẩn bị dữ liệu demo an toàn", "Có sẵn 1 sự kiện mẫu 'Hội thảo Kỹ năng Hội nhập Quốc tế' để SV đăng ký và BCN điểm danh.")
    ]
    for r_idx, r_data in enumerate(pre_items):
        for c_idx, val in enumerate(r_data):
            cell = t_pre.cell(r_idx + 1, c_idx)
            cell.text = val
            cell.paragraphs[0].runs[0].font.size = Pt(9)
            if r_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Section 2: Swagger Endpoint Details
    doc.add_heading("13.2. CÁC ENDPOINT SWAGGER CHÍNH TRONG KỊCH BẢN DEMO", level=1)
    
    t_end = doc.add_table(rows=7, cols=5)
    t_end.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_end = ["Phương thức", "Đường dẫn Endpoint", "Quyền yêu cầu", "Thân yêu cầu (Body) / Query", "Mã mong đợi"]
    for i, h in enumerate(h_end):
        c = t_end.cell(0, i)
        c.text = h
        c.paragraphs[0].runs[0].bold = True
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(c, "2264AC")

    endpoints = [
        ("POST", "/api/auth/login", "Mở công khai", '{"username": "...", "password": "..."}', "200 OK + JWT"),
        ("GET", "/api/events", "Mở công khai", "?pageNumber=1&pageSize=10", "200 OK + PagedResponse"),
        ("GET", "/api/events/{id}", "Mở công khai", "id: int trên đường dẫn", "200 OK / 404"),
        ("POST", "/api/events", "Admin, Committee", '{"title": "...", "startDate": "...", "location": "..."}', "201 Created"),
        ("POST", "/api/events/{id}/register", "Đăng nhập (Student)", "Bearer Token qua Header", "200 OK / 400"),
        ("POST", "/api/events/{id}/attendance", "Admin, Committee", '{"studentId": 12, "attended": true}', "200 OK")
    ]
    for r_idx, r_data in enumerate(endpoints):
        for c_idx, val in enumerate(r_data):
            cell = t_end.cell(r_idx + 1, c_idx)
            cell.text = val
            cell.paragraphs[0].runs[0].font.size = Pt(8.5)
            if c_idx == 0:
                cell.paragraphs[0].runs[0].bold = True
            if r_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Section 3: Demo 401 Unauthorized
    doc.add_heading("13.3. QUY TRÌNH DEMO LỖI 401 UNAUTHORIZED TRÊN SWAGGER", level=1)
    doc.add_paragraph(
        "Mục đích: Chứng minh cơ chế bảo mật của Middleware ASP.NET Core khi client chưa xác thực danh tính.\n\n"
        "Thao tác thực hiện trên Swagger:\n"
        "1. Mở nhóm Events trên Swagger UI.\n"
        "2. Tìm endpoint POST /api/events/{id}/register (Đăng ký tham gia sự kiện).\n"
        "3. ĐẢM BẢO CHƯA BẤM NÚT 'Authorize' trên Swagger (chưa gắn token bất kỳ).\n"
        "4. Điền tham số id = 1 và bấm nút 'Execute'.\n"
        "5. Quan sát kết quả phản hồi:\n"
        "   - HTTP Status Code: 401 Unauthorized.\n"
        "   - Response Headers: WWW-Authenticate: Bearer error=\"invalid_token\".\n"
        "   - Ý nghĩa nghiệp vụ: Server từ chối ngay lập tức vì không xác định được ai đang đăng ký."
    )
    add_code_box(
        doc,
        "HTTP/1.1 401 Unauthorized\n"
        "Date: Sun, 26 Oct 2026 02:30:00 GMT\n"
        "WWW-Authenticate: Bearer\n"
        "Content-Length: 0",
        caption="Phản hồi HTTP 401 thực tế từ server khi không gửi Bearer token"
    )

    # Section 4: Demo 403 Forbidden
    doc.add_heading("13.4. QUY TRÌNH DEMO LỖI 403 FORBIDDEN TRÊN SWAGGER", level=1)
    doc.add_paragraph(
        "Mục đích: Chứng minh phân quyền Server-side (Role-based Authorization). Token hoàn toàn hợp lệ nhưng tài khoản không có quyền thực hiện nghiệp vụ quản trị.\n\n"
        "Thao tác thực hiện trên Swagger:\n"
        "1. Gọi POST /api/auth/login với tài khoản Sinh viên (student_demo).\n"
        "2. Sao chép chuỗi token trong JSON phản hồi.\n"
        "3. Bấm nút 'Authorize' (hình ổ khóa) ở góc trên Swagger, dán Bearer <token_sinh_vien> và bấm Authorize.\n"
        "4. Tìm endpoint quản trị: POST /api/events (Tạo sự kiện mới) hoặc PUT /api/admin/users/{id}/roles.\n"
        "5. Điền dữ liệu tạo sự kiện và bấm 'Execute'.\n"
        "6. Quan sát kết quả phản hồi:\n"
        "   - HTTP Status Code: 403 Forbidden.\n"
        "   - Ý nghĩa nghiệp vụ: Server đã giải mã Token, nhận diện đúng sinh viên, nhưng thuộc tính [Authorize(Roles = \"Admin,Committee\")] từ chối quyền truy cập của vai trò Student."
    )
    add_code_box(
        doc,
        "HTTP/1.1 403 Forbidden\n"
        "Date: Sun, 26 Oct 2026 02:31:00 GMT\n"
        "Content-Length: 0",
        caption="Phản hồi HTTP 403 thực tế từ server khi tài khoản không đủ quyền"
    )

    # Section 5: Demo CRUD
    doc.add_heading("13.5. QUY TRÌNH KIỂM THỬ ĐẦY ĐỦ 4 THAO TÁC CRUD", level=1)
    doc.add_paragraph(
        "Nghiệp vụ lựa chọn: QUẢN LÝ SỰ KIỆN (/api/events). Đây là nghiệp vụ chuẩn mực có đầy đủ Create, Read, Update, Delete/Cancel:\n"
        "- Read (GET List): GET /api/events?pageNumber=1&pageSize=10 -> Nhận 200 OK + danh sách phân trang.\n"
        "- Read (GET Detail): GET /api/events/{id} -> Nhận 200 OK chi tiết hoặc 404 Not Found nếu sai id.\n"
        "- Create (POST): BCN đăng nhập -> POST /api/events kèm tiêu đề, ngày diễn ra -> Nhận 201 Created + Header Location: /api/events/{newId}.\n"
        "- Update (PUT): BCN sửa thông tin sự kiện -> PUT /api/events/{id} -> Nhận 204 No Content (hoặc 200 OK).\n"
        "- Delete/Cancel (DELETE/POST): Hủy hoặc đóng sự kiện -> Nhận 204 No Content. Gọi lại GET /api/events/{id} sẽ thấy trạng thái đã chuyển sang 'Cancelled'."
    )

    # Section 6: Phối hợp 3 nền tảng
    doc.add_heading("13.6. KỊCH BẢN DEMO PHỐI HỢP XUYÊN SUỐT 3 NỀN TẢNG (THE MASTER CHAIN)", level=1)
    
    t_chain = doc.add_table(rows=5, cols=4)
    t_chain.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_chain = ["Thứ tự", "Người thao tác & Ứng dụng", "Thao tác trực tiếp", "Kết quả quan sát thấy"]
    for i, h in enumerate(h_chain):
        c = t_chain.cell(0, i)
        c.text = h
        c.paragraphs[0].runs[0].bold = True
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(c, "2264AC")

    chain_steps = [
        ("Chặng 1", "Quách Khoa Đức\n(Website Next.js)", "Mở trang Web, vào tab Sự kiện. Hiển thị sự kiện 'Hội thảo Kỹ năng Hội nhập Quốc tế' với 0 lượt đăng ký ban đầu.", "Gọi GET /api/events thành công. Giao diện Web hiển thị thẻ Card trực quan."),
        ("Chặng 2", "Đào Trí Khang\n(Android Emulator)", "Sinh viên đăng nhập app Android. Mở chi tiết sự kiện 'Hội thảo Kỹ năng Hội nhập Quốc tế'. Bấm nút 'Đăng ký tham gia'.", "Gọi POST /api/events/{id}/register. Nhận thông báo thành công và mã QR sinh ra."),
        ("Chặng 3", "Võ Ngọc Minh Đạt\n(WinForms C#)", "Ban Chủ nhiệm mở WinForms, chọn sự kiện trên DataGridView, bấm 'Xem danh sách đăng ký'. Thấy ngay sinh viên vừa đăng ký trên Android. Bấm 'Điểm danh'.", "Gọi GET /api/events/{id}/registrations và POST .../attendance. Giao diện tick xanh thành công."),
        ("Chặng 4", "Hồ Đoàng Nguyên Khang\n(Swagger UI)", "Mở Swagger, gọi lại GET /api/events/{id} để kiểm chứng dữ liệu thật trong DB PostgreSQL. Số người tham gia tăng lên và trạng thái điểm danh khớp 100%.", "Phản hồi JSON 200 OK xác nhận dữ liệu nhất quán trên cùng một Database.")
    ]
    for r_idx, r_data in enumerate(chain_steps):
        for c_idx, val in enumerate(r_data):
            cell = t_chain.cell(r_idx + 1, c_idx)
            cell.text = val
            cell.paragraphs[0].runs[0].font.size = Pt(9)
            if c_idx == 0:
                cell.paragraphs[0].runs[0].bold = True
            if r_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")
    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    output_path = "deliverables/VISIONARY_LIVE_DEMO_AND_SWAGGER_TEST_GUIDE.docx"
    doc.save(output_path)
    print(f"Generated: {output_path}")

if __name__ == "__main__":
    generate_live_demo_guide()
