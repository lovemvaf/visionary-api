import os
import sys

def apply_updates():
    with open('scripts/build_perfect_presentation.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Define new slide 5
    new_s5 = '''    # ==========================================
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
        "LỜI THUYẾT TRÌNH (ĐÀO TRÍ KHANG - 1'00\"):\\n"
        "Kính chào Thầy và các bạn! Em tên là Đào Trí Khang, phụ trách ứng dụng di động Android Native bằng Java. "
        "Ứng dụng Android được thiết kế cho sinh viên DNTU để theo dõi hoạt động CLB và đăng ký sự kiện ngay trên điện thoại. "
        "Bên trái là ảnh chụp thật từ ứng dụng Android. "
        "Các điều khiển tuân thủ đúng quy ước đặt tên: danh sách cuộn là lstEvents (RecyclerView), nút đăng ký là btnRegister, vuốt làm mới là swpRefresh. "
        "Đoạn mã bên phải thể hiện hàm loadEvents gọi tới Web API thông qua thư viện Retrofit 2. "
        "Hàm getEvents(1, 20) được đẩy vào phương thức enqueue để thực thi trên luồng nền của OkHttp, "
        "khi có kết quả onResponse sẽ tự động đưa về luồng chính để cập nhật adapter cho RecyclerView."
    )
'''

    # Define new slide 6
    new_s6 = '''    # ==========================================
    # SLIDE 6: SƠ ĐỒ ANDROID NETWORKING & THREADING (ĐÀO TRÍ KHANG)
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "SƠ ĐỒ CƠ CHẾ MẠNG & ĐIỀU PHỐI LUỒNG TRÊN ANDROID", "05. Cơ chế Mạng Android", 6, "Đào Trí Khang")

    # Flow Diagram across 5 stages using PowerPoint shapes and connectors
    flow_steps = [
        ("1. Tương tác UI", "Main UI Thread", "Người dùng nhấn btnRegister\\nhoặc vuốt làm mới swpRefresh", C_BLUE, Inches(0.8)),
        ("2. Retrofit Enqueue", "OkHttp Dispatcher", "apiService.getEvents().enqueue()\\nĐẩy việc vào luồng nền Worker", C_TEAL, Inches(3.25)),
        ("3. Gói tin Mạng", "I/O Network TCP", "Gửi request GET /api/events\\ntới Kestrel Server cổng 443", C_NAVY, Inches(5.7)),
        ("4. Giải mã JSON", "Gson Deserializer", "Tự động ánh xạ JSON string\\nsang ApiResponse<PagedResponse>", C_TEAL, Inches(8.15)),
        ("5. Cập nhật UI", "Main UI Thread", "Handler.post / onResponse\\nCập nhật Adapter cho View", C_GREEN, Inches(10.6))
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
        "LỜI THUYẾT TRÌNH (ĐÀO TRÍ KHANG - 1'00\"):\\n"
        "Thưa Thầy, sơ đồ phía trên mô tả chi tiết đường đi của yêu cầu mạng trên Android qua 5 bước: "
        "Bắt đầu từ nút bấm trên Main UI Thread, hàm enqueue() đẩy việc tải dữ liệu sang luồng nền của OkHttp. "
        "Khi server trả về JSON, thư viện Gson sẽ giải mã thành đối tượng Java và chuyển kết quả an toàn về Luồng Chính để cập nhật danh sách. "
        "Nếu gọi mạng trên Luồng Chính, ứng dụng sẽ bị ném ngoại lệ NetworkOnMainThreadException ngay lập tức. "
        "Còn nếu sửa giao diện từ luồng nền thì gặp lỗi CalledFromWrongThreadException. "
        "Ngoài ra, trên máy ảo Android, địa chỉ IP kết nối phải là 10.0.2.2 chứ không thể là localhost."
    )
'''

    # Define new slide 9
    new_s9 = '''    # ==========================================
    # SLIDE 9: SƠ ĐỒ XUYÊN SUỐT MỘT YÊU CẦU (6 CHẶNG) (HỒ ĐOÀN NGUYÊN KHANG)
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "SƠ ĐỒ CHU TRÌNH 6 CHẶNG CỦA MỘT YÊU CẦU: GET /api/events", "08. Chu trình Request", 9, "Hồ Đoàn Nguyên Khang")

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
            "  {\\"success\\": true, \\"data\\": {\\"items\\": [...], ...}}"
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
        "LỜI THUYẾT TRÌNH (HỒ ĐOÀN NGUYÊN KHANG - 1'00\"):\\n"
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
'''

    # Define new slide 10
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

    # Evidence: 401 vs 403 cards
    img_401 = os.path.join(EVIDENCE_DIR, "13_jwt_401_evidence.png")
    if os.path.exists(img_401):
        s10.shapes.add_picture(img_401, Inches(0.8), Inches(2.9), width=Inches(5.7))

    img_403 = os.path.join(EVIDENCE_DIR, "14_jwt_403_evidence.png")
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
        "LỜI THUYẾT TRÌNH (HỒ ĐOÀN NGUYÊN KHANG - 1'05\"):\\n"
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

    # Define new slide 15
    new_s15 = '''    # ==========================================
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
        ("1. BẮT ĐẦU: CI RUN #12 THẤT BẠI", "13 Passed / 2 Failed trên Ubuntu Linux.\\n• Search test fail dòng 168 (TotalCount = 0)\\n• GetPostBySlug fail dòng 183 (404 Not Found)", C_RED),
        ("2. NGUYÊN NHÂN GỐC RỄ (ROOT CAUSE)", "Hai Test Class chạy song song trên xUnit:\\nCùng khởi tạo WebApplicationFactory trỏ vào visionary.db -> Đụng độ UNIQUE Roles.Name -> Hủy ngang SeedAsync trước khi nạp Posts!", C_NAVY),
        ("3. GIẢI PHÁP KỸ THUẬT (REMEDIATION)", "• Khóa luồng tĩnh SemaphoreSlim(1,1) trong DbInitializer.SeedAsync().\\n• Tạo CustomWebApplicationFactory cấp phát DB test cô lập.\\n• Gộp chung [Collection(\\"IntegrationTests\\")].", C_TEAL),
        ("4. KẾT QUẢ KIỂM CHỨNG (VERIFICATION)", "Chạy lại kiểm thử hồi quy 3 lần liên tiếp:\\n15/15 Passed 100% (2.8s) -> Push commit c7af080 lên GitHub -> Run #40231783994 XANH!", C_GREEN)
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
        "LỜI THUYẾT TRÌNH (VÕ NGỌC MINH ĐẠT - 1'00\"):\\n"
        "Trong quá trình kiểm thử tự động, nhóm em đã đối mặt với một sự cố kỹ thuật có thật. "
        "Bên trái là log lỗi nguyên văn từ GitHub Actions Run #12: pipeline bị gãy với 13 bài đạt và 2 bài thất bại. "
        "Nguyên nhân gốc rễ do xUnit chạy hai class test song song, cùng tranh chấp file SQLite khiến lệnh Seed bị dừng đột ngột ở ràng buộc Unique Role. "
        "Nhóm đã tự phân tích và khắc phục triệt để bằng khóa SemaphoreSlim và kiến trúc CustomWebApplicationFactory cô lập cơ sở dữ liệu. "
        "Như hình bên phải, toàn bộ 15 bài test đã vượt qua 100% và GitHub Actions Run #40231783994 đã báo xanh hoàn toàn."
    )
'''

    # Perform slice replacements
    # Slide 5
    s5_start = content.find('# SLIDE 5: ANDROID NATIVE JAVA')
    s6_start = content.find('# SLIDE 6: SƠ ĐỒ ANDROID NETWORKING')
    content = content[:s5_start] + new_s5 + '\n' + content[s6_start:]

    # Slide 6
    s6_start = content.find('# SLIDE 6: SƠ ĐỒ ANDROID NETWORKING')
    s7_start = content.find('# SLIDE 7: DEMO ANDROID')
    content = content[:s6_start] + new_s6 + '\n' + content[s7_start:]

    # Slide 9
    s9_start = content.find('# SLIDE 9: SƠ ĐỒ XUYÊN SUỐT')
    s10_start = content.find('# SLIDE 10: SƠ ĐỒ XÁC THỰC')
    content = content[:s9_start] + new_s9 + '\n' + content[s10_start:]

    # Slide 10
    s10_start = content.find('# SLIDE 10: SƠ ĐỒ XÁC THỰC')
    s11_start = content.find('# SLIDE 11: JSON')
    content = content[:s10_start] + new_s10 + '\n' + content[s11_start:]

    # Slide 15
    s15_start = content.find('# SLIDE 15: SỰ CỐ THẬT')
    s16_start = content.find('# SLIDE 16: GIỚI HẠN')
    content = content[:s15_start] + new_s15 + '\n' + content[s16_start:]

    with open('scripts/build_perfect_presentation.py', 'w', encoding='utf-8') as f:
        f.write(content)

    print('Updated scripts/build_perfect_presentation.py successfully.')

if __name__ == '__main__':
    apply_updates()
