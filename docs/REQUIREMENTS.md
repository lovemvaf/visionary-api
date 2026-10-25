# YÊU CẦU HỆ THỐNG VISIONARY (SYSTEM REQUIREMENTS SPECIFICATION)

## 1. Yêu cầu Chức năng (Functional Requirements)

### Module 1: Xác thực & Quản lý Tài khoản (Identity & Access Management)
- FR-IAM-01: Đăng ký tài khoản sinh viên bằng Email và Mật khẩu (mã hóa chuẩn BCrypt/Identity PasswordHasher).
- FR-IAM-02: Đăng nhập cấp mã truy cập JWT (JSON Web Token) có thời hạn, chứa Claims (UserId, Email, FullName, Roles).
- FR-IAM-03: Đăng nhập một chạm bằng Google OAuth 2.0 / OpenID Connect, xác minh IdToken từ Google backend trước khi cấp JWT ứng dụng.
- FR-IAM-04: Đổi mật khẩu, quên mật khẩu và quản lý hồ sơ cá nhân (họ tên, MSSV, khoa/chuyên ngành, khóa học, avatar, bio).
- FR-IAM-05: Hệ thống phân quyền chặt chẽ trên 7 cấp độ: Guest, Registered Student, Club Member, Collaborator, Club Committee (BCN), Club Supervisor, System Administrator.

### Module 2: Quản lý Hoạt động CLB Tiếng Anh DNTU (Club Operations)
- FR-CLB-01: Trang giới thiệu CLB: Sứ mệnh, cơ cấu tổ chức, các ban chuyên môn, nhiệm kỳ, thông tin liên hệ chính thức.
- FR-CLB-02: Nộp đơn đăng ký gia nhập CLB trực tuyến, quy trình xét duyệt đơn của BCN (Duyệt / Từ chối kèm lý do).
- FR-CLB-03: Quản trị danh sách thành viên: lọc theo chuyên ban, trạng thái hoạt động, khóa sinh viên, vai trò trong CLB.
- FR-CLB-04: Quản lý sự kiện: Tạo sự kiện mới, thời gian, địa điểm, hạn đăng ký, số lượng tối đa, banner, mô tả.
- FR-CLB-05: Đăng ký và Hủy đăng ký sự kiện cho thành viên/sinh viên; kiểm soát quá số lượng (capacity check).
- FR-CLB-06: Điểm danh sự kiện: Hỗ trợ cả điểm danh thủ công (danh sách BCN tích chọn) và mã QR điểm danh động có thời hạn.
- FR-CLB-07: Bảng vàng thành tích (Hall of Achievement): Tôn vinh các thành tích Academic, Technology, English, Global Engagement, Community Contribution với quy trình đề xuất - minh chứng - duyệt bài.

### Module 3: Cổng Nội dung & CMS (Content Management System)
- FR-CMS-01: Quản lý bài viết tin tức hội nhập quốc tế, bài học tiếng Anh, công nghệ mới.
- FR-CMS-02: Trình soạn thảo định dạng phong phú (Rich Text), tải ảnh minh họa, gắn thẻ (Tags) và chuyên mục (Categories).
- FR-CMS-03: Quy trình biên tập: Bản nháp (Draft) -> Chờ duyệt (Pending Review) -> Đã xuất bản (Published) -> Gỡ bài (Archived).

### Module 4: English for IT – Trung tâm Học tập
- FR-ENG-01: Phân loại theo 4 cấp độ: Beginner, Intermediate, Advanced, Professional/Developer.
- FR-ENG-02: Chuyên đề chuyên sâu: Programming English, Web Dev, REST API, AI/ML, Cloud & DevOps, CV & Interview.
- FR-ENG-03: Mỗi bài học có thuật ngữ song ngữ Anh - Việt, ngữ cảnh sử dụng thực tế, ví dụ code và tài liệu tham khảo chính thống.

### Module 5: Technology Radar & Kho Open-Source
- FR-RAD-01: Theo dõi xu hướng công nghệ nóng (AI/LLM, Computer Vision, Cloud, Cybersecurity, Frontend/Backend).
- FR-RAD-02: Tích hợp metadata kho GitHub (Tên, tác giả, ngôn ngữ, stars, forks, license, mô tả, liên kết chính thức).
- FR-RAD-03: Tích hợp metadata mô hình Hugging Face (Tasks, model card, license, tags, downloads).

### Module 6: Tổng hợp Cuộc thi, Học bổng & Hội nhập (Opportunities)
- FR-OPP-01: Danh mục phân loại: Hackathon, AI Challenge, Lập trình thuật toán (ICPC), Cybersecurity CTF, Học bổng quốc tế, Trao đổi sinh viên ASEAN.
- FR-OPP-02: Thông tin chi tiết: Đơn vị tổ chức, thể lệ, đối tượng, hình thức (Online/Offline), hạn chót nộp hồ sơ, trạng thái đăng ký, đường dẫn đăng ký chính thức.
- FR-OPP-03: Tính năng lọc thông minh theo ngành, quốc gia, chi phí (miễn phí/có phí), hình thức tham gia.

### Module 7: Career Gateway (Việc làm & Thực tập Quốc tế)
- FR-CAR-01: Cơ hội thực tập (Internship), Fresher, Junior trong lĩnh vực CNTT và các vị trí đòi hỏi tiếng Anh chuyên môn.
- FR-CAR-02: Phân loại hình thức làm việc: Remote, Hybrid, On-site tại Việt Nam hoặc Quốc tế.
- FR-CAR-03: Nút điều hướng nộp đơn trực tiếp tại website chính thức của nhà tuyển dụng (Apply on Official Website).

### Module 8: Pipeline Thu thập & Kiểm chứng Dữ liệu Tự động (Data Automation)
- FR-AUT-01: Source Registry: Đăng ký và quản lý các nguồn tin chính thống (GitHub, Hugging Face, RSS công nghệ, arXiv, Dev.to).
- FR-AUT-02: Trình thu thập dữ liệu (Collector) có cơ chế retry, rate limit, kiểm tra trùng lặp (Deduplication) theo URL và mã định danh.
- FR-AUT-03: Hàng đợi kiểm duyệt (Human Review Queue): Phân định rõ ràng giữa nội dung đã xác minh (Verified) và nội dung chờ kiểm tra (Needs Verification).

---

## 2. Yêu cầu Phi Chức năng (Non-Functional Requirements)

1. **Hiệu năng & Tải (Performance):**
   - Thời gian phản hồi của REST API dưới 200ms cho các truy vấn có bộ nhớ đệm (Cache).
   - Website Next.js đạt chỉ số Core Web Vitals tối ưu, điểm Lighthouse > 90 trên cả Desktop và Mobile.
2. **Bảo mật (Security - OWASP Top 10):**
   - Mọi mật khẩu được mã hóa một chiều an toàn; JWT ký bằng thuật ngữ HMAC-SHA256 với secret an toàn.
   - Chặn tuyệt đối SQL Injection thông qua EF Core parameterized queries.
   - Chặn XSS bằng việc khử khuẩn mã HTML và thiết lập Content Security Policy (CSP).
   - Thiết lập CORS đúng nguồn cho phép; bảo vệ chống truy cập trái phép bằng Authorize attributes ở cấp độ Controller và Action.
3. **Trải nghiệm Người dùng (UI/UX):**
   - Phong cách thiết kế: **Premium Academic Technology Platform** (Màu chủ đạo: Deep Navy `#142D4E`, Visionary Blue `#2264AC`, Teal Accent `#22A6A1`, Nền sáng `#F5F7FB`).
   - Hỗ trợ giao diện sáng/tối (Dark Mode) hoàn chỉnh, tương phản đạt chuẩn WCAG 2.2 AA.
   - Hỗ trợ đa ngôn ngữ (Tiếng Việt và Tiếng Anh) trên toàn bộ hệ thống.
4. **Khả năng Bảo trì & Mở rộng (Maintainability & Extensibility):**
   - Áp dụng nguyên tắc Clean Architecture và SOLID cho ASP.NET Core Web API.
   - Client Web, Desktop và Mobile dùng chung Data Transfer Objects (DTO) và API Contract chuẩn.
