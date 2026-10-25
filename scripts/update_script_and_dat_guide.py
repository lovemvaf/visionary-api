import os

def update_presentation_script():
    with open('scripts/generate_presentation_script_doc.py', 'r', encoding='utf-8') as f:
        content = f.read()

    old_s15_script = '''            ("Slide 15 – Một sự cố thật và Quy trình Khắc phục (1 phút)", [
                "Lời thoại:",
                "\"Trong quá trình xây dựng hệ thống, nhóm em đã gặp một sự cố thật rất điển hình trong pipeline CI/CD.",
                "Bên trái là log lỗi nguyên văn từ GitHub Actions: NETSDK1100.",
                "Lỗi xảy ra vì file solution chung ban đầu chứa cả dự án Windows Forms (.NET 8 Windows Desktop). Khi đưa lên runner Ubuntu Linux của GitHub Actions để build backend, hệ điều hành Linux từ chối biên dịch các thư viện giao diện Windows.",
                "Nhóm em đã chẩn đoán nguyên nhân và khắc phục bằng cách tách thành solution Visionary.Backend.sln độc lập chỉ chứa Core, Infrastructure, Api và Tests.",
                "Dự án Windows Forms được biên dịch trong workflow riêng desktop.yml trên máy ảo Windows.",
                "Sau khi sửa, toàn bộ 15 bài kiểm thử hồi quy xUnit và 5 workflow CI đều vượt qua 100% như hình bên phải.\""
            ]),'''

    new_s15_script = '''            ("Slide 15 – Một sự cố thật và Quy trình Khắc phục (1 phút)", [
                "Lời thoại:",
                "\"Trong quá trình kiểm thử tự động, nhóm em đã đối mặt với một sự cố kỹ thuật có thật trên GitHub Actions Backend CI Run #12.",
                "Bên trái là log lỗi nguyên văn: pipeline báo Build FAILED dù không có lỗi biên dịch C#, với 13 bài đạt và 2 bài kiểm thử thất bại (bài Search dòng 168 và bài GetPostBySlug dòng 183).",
                "Đi sâu vào log, nhóm phát hiện thông báo lỗi SQLite Error 19: UNIQUE constraint failed: Roles.Name.",
                "Nguyên nhân gốc rễ do xUnit kích hoạt hai class kiểm thử chạy song song, cùng khởi tạo WebApplicationFactory trỏ vào chung một file visionary.db, gây xung đột ghi đồng thời khiến chu trình nạp dữ liệu SeedAsync bị dừng đột ngột trước khi kịp nạp bài viết.",
                "Nhóm em đã tự phân tích và xử lý triệt để bằng giải pháp hai tầng: Thứ nhất, đặt khóa luồng tĩnh SemaphoreSlim(1, 1) trong DbInitializer; Thứ hai, xây dựng CustomWebApplicationFactory cấp phát cơ sở dữ liệu test cô lập và gộp chung Collection kiểm thử.",
                "Như hình bên phải, toàn bộ 15/15 bài test đã vượt qua 100% và GitHub Actions Run #40231783994 trên Linux đã báo xanh hoàn toàn.\""
            ]),'''

    if old_s15_script in content:
        content = content.replace(old_s15_script, new_s15_script)
        with open('scripts/generate_presentation_script_doc.py', 'w', encoding='utf-8') as f:
            f.write(content)
        print('Updated scripts/generate_presentation_script_doc.py successfully.')
    else:
        print('Warning: old_s15_script not found in generate_presentation_script_doc.py!')

def update_dat_guide():
    with open('scripts/build_dat_winforms_guide.py', 'r', encoding='utf-8') as f:
        content = f.read()

    old_spot3 = '''        ("Điểm 3: Khắc phục lỗi NETSDK1100 trong file .github/workflows/backend.yml",
         "Giảng viên hỏi: Nhóm đã sửa lỗi NETSDK1100 như thế nào? Tại sao không để Ubuntu build WinForms?\\n"
         "-> Đạt trả lời: 'Dạ thưa Thầy, WinForms gắn chặt với Windows API nên không thể compile bằng .NET SDK chuẩn trên Linux Ubuntu trừ khi dùng giả lập WINE rất phức tạp. Nhóm giải quyết theo đúng kiến trúc micro-solution: Tạo file backend/Visionary.Backend.sln độc lập chỉ chứa các project Web API đa nền tảng và cho GitHub Actions build file này trên Ubuntu. Còn WinForms được build độc lập trên môi trường Windows.'")'''

    new_spot3 = '''        ("Điểm 3: Khắc phục sự cố GitHub Actions Backend CI Run #12 (13/15 Passed -> 15/15 Passed Run #40231783994)",
         "Giảng viên hỏi: Nhóm đã phân tích và sửa hai bài test thất bại trên GitHub Actions Run #12 như thế nào?\\n"
         "-> Đạt trả lời: 'Dạ thưa Thầy, trong Run #12, test Search (dòng 168) và test GetBySlug (dòng 183) bị fail do chu trình SeedAsync bị hủy ngang khi gặp lỗi SQLite Error 19 UNIQUE constraint failed: Roles.Name. Nguyên nhân do hai test class chạy song song cùng tranh chấp file visionary.db. Nhóm em đã giải quyết triệt để bằng cách thêm SemaphoreSlim(1, 1) trong DbInitializer.SeedAsync, tạo CustomWebApplicationFactory cấp phát database SQLite biệt lập cho mỗi lần test và gộp chung [Collection(\"IntegrationTests\")]. Sau khi commit c7af080, GitHub Actions Run #40231783994 đã vượt qua 100% cả 15/15 bài test trên runner Linux x64.'")'''

    if old_spot3 in content:
        content = content.replace(old_spot3, new_spot3)
        with open('scripts/build_dat_winforms_guide.py', 'w', encoding='utf-8') as f:
            f.write(content)
        print('Updated scripts/build_dat_winforms_guide.py successfully.')
    else:
        print('Warning: old_spot3 not found in build_dat_winforms_guide.py!')

if __name__ == '__main__':
    update_presentation_script()
    update_dat_guide()
