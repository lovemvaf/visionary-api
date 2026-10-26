# BẢNG ĐẶC TẢ ĐÓNG GÓP NHÓM VÀ XÁC MINH DANH TÍNH (TEAM CONTRIBUTIONS AUDIT)
## VISIONARY API – SOFTWARE ENGINEERING ROLES & CONTRIBUTION DISCLOSURE
**Mã dự án:** VISIONARY – Hệ thống Quản lý Hoạt động Hội nhập (TH71108)  
**Trường:** Đại học Công nghệ Đồng Nai (DNTU)  
**Khoa:** Công nghệ Thông tin  
**Thời điểm kiểm toán:** 26/10/2026  

---

## 1. NGUYÊN TẮC TRUNG THỰC HỌC THUẬT & MINH BẠCH (ACADEMIC INTEGRITY)

Tuân thủ nghiêm ngặt chuẩn mực học thuật của DNTU và quy định học phần TH71108:
1. **Không giả mạo lịch sử Git:** Không sử dụng các lệnh can thiệp lịch sử (`git commit --amend --author`, `git filter-repo`) để ngụy tạo tác giả cho các commit cũ đã hoàn thành.
2. **Minh bạch về danh tính:** Báo cáo công khai hiện trạng danh tính Git của 4 thành viên và yêu cầu chuẩn hóa đối với các trường hợp trùng email.
3. **Công bố sự hỗ trợ của AI (AI Disclosure):** Toàn bộ việc sử dụng trợ lý lập trình Google Antigravity trong việc tăng tốc sinh mã, tối ưu hóa CSS và tạo tài liệu đều được công bố minh bạch; 4 sinh viên giữ vai trò thiết kế kiến trúc, phản biện logic, kiểm thử chấp nhận (UAT) và thuyết trình bảo vệ trước hội đồng.

---

## 2. BẢNG PHÂN CÔNG VAI TRÒ & ĐÓNG GÓP THỰC TẾ CỦA BỐN THÀNH VIÊN

| STT | Họ và tên & MSSV | Vai trò kỹ thuật phân công | Email cung cấp | Trạng thái GitHub Identity | Phạm vi thực hiện thực tế & Minh chứng kiểm thử | Vai trò thuyết trình (Thứ tự) |
|:---:|---|---|---|:---:|---|:---:|
| 1 | **Quách Khoa Đức**<br/>(MSSV: 1923040025) | **Team Lead / Principal Architect**<br/>Web Client & Integration | `lovemvaf@gmail.com` | **VERIFIED**<br/>(`lovemvaf`) | - Quản trị repository, thiết lập CI/CD GitHub Actions.<br/>- Xây dựng Next.js 14 App Router (19 static/dynamic routes).<br/>- Tích hợp BFF proxy và cấu hình Vercel deployment.<br/>- Điều phối xoay vòng mật khẩu bảo mật P0. | **Người số 1 (Mở màn)**<br/>Tổng quan đề tài & Kiến trúc (Nội dung súc tích nhất) |
| 2 | **Đào Trí Khang**<br/>(MSSV: 1923040156) | **Mobile Software Engineer**<br/>Android Native Java | `caubekhang1485@gmail.com` | **VERIFIED**<br/>(Chờ link PR độc lập) | - Xây dựng ứng dụng Android Java (SDK 34).<br/>- Triển khai Retrofit 2, OkHttp 3, Gson parser.<br/>- Kiểm thử giao diện Material 3, QR Check-in và English for IT.<br/>- Cấu hình an ninh `network_security_config.xml`. | **Người số 2**<br/>Kiến trúc Android & Networking (3 phút 15 giây) |
| 3 | **Hồ Đoàn Nguyên Khang**<br/>(MSSV: 1923040112) | **Web API Engineer**<br/>ASP.NET Core & Database | `vongocminhdat@gmail.com`<br/>*(Cần cung cấp riêng)* | **IDENTITY_VERIFICATION_REQUIRED**<br/>*(Trùng email với Đạt)* | - Thiết kế RESTful Web API, DTOs và Data Annotations.<br/>- Cấu hình OpenAPI / Swagger UI phục vụ môn học.<br/>- Rà soát xác thực JWT Bearer và băm mật khẩu BCrypt.<br/>- Kiểm toán logic 6 bài test `PostsLogicAuditTests`. | **Người số 3**<br/>API Contract, JWT & Database (4 phút 15 giây) |
| 4 | **Võ Ngọc Minh Đạt**<br/>(MSSV: 1923040088) | **Desktop Software Engineer**<br/>Windows Forms & Operations | `vongocminhdat@gmail.com` | **IDENTITY_VERIFICATION_REQUIRED**<br/>*(Trùng email với Hồ Khang)* | - Xây dựng ứng dụng Windows Forms C# (.NET 8).<br/>- Tích hợp `HttpClient` Singleton gọi Web API.<br/>- Kiểm thử nghiệp vụ quản trị CLB, duyệt đơn và điểm danh.<br/>- Phân tích và khắc phục sự cố CI Run #12 thành công. | **Người số 4 (Kết thúc)**<br/>WinForms, Khắc phục sự cố & Kết luận (4 phút 45 giây) |

---

## 3. GIẢI TRÌNH HIỆN TRẠNG LỊCH SỬ GIT (GIT COMMIT ATTRIBUTION AUDIT)

Lệnh phân tích lịch sử commit toàn bộ repository (`git shortlog -sn --all`) cho thấy:
- **19 commits bởi `lovemvaf`:** Do Quách Khoa Đức đại diện nhóm thực hiện đẩy mã nguồn, cấu hình CI/CD và triển khai cloud tập trung.
- **4 commits bởi `Your Name`:** Do lỗi cấu hình mặc định chưa đặt `user.name` và `user.email` cục bộ trong giai đoạn khởi tạo git ban đầu của dự án.
- **Chính sách nhóm:** Nhóm thống nhất **không viết lại lịch sử commit cũ** để tránh làm sai lệch commit SHA đã trích dẫn trong tài liệu nộp và slide thuyết trình. Kể từ đợt phát triển tiếp theo, mỗi thành viên clone repository riêng và đóng góp thông qua Pull Request với tài khoản GitHub cá nhân đã được xác minh.

---

## 4. HÀNH ĐỘNG CẦN THỰC HIỆN ĐỂ CHUẨN HÓA DANH TÍNH (ACTION ITEMS)

1. **Xác nhận GitHub Username riêng cho Hồ Đoàn Nguyên Khang và Võ Ngọc Minh Đạt:**
   - Hiện tại hai bạn đang được cung cấp cùng một email (`vongocminhdat@gmail.com`).
   - Chủ sở hữu hệ thống cần thu thập username GitHub chính thức của Hồ Đoàn Nguyên Khang và Võ Ngọc Minh Đạt để thêm vào danh sách Collaborators của repository với quyền Read/Write hợp lệ.
2. **Quy trình đóng góp mới:**
   - Tuân thủ hướng dẫn tại [`CONTRIBUTING.md`](../CONTRIBUTING.md) bằng cách tạo nhánh (branch) riêng mang tên tính năng (`feature/api-...`, `feature/winforms-...`, `feature/android-...`) và tạo Pull Request thật để GitHub tự động ghi nhận Contributors chính thức.
