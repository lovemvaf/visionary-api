# NHẬT KÝ THAY ĐỔI – VISIONARY CHANGELOG

Tất cả các thay đổi quan trọng của hệ sinh thái **VISIONARY** được ghi nhận chi tiết tại đây.

---

## [v1.0.0] – 25/10/2026 – Triển khai Hệ sinh thái Toàn diện (One Backend – Three Platforms)

### 🚀 Tính năng & Nền tảng Đã Hoàn thiện
- **Kiến trúc Tổng thể:**
  - Thiết kế kiến trúc chuẩn Clean Architecture: Một Backend ASP.NET Core 8 Web API dùng chung cho 3 nền tảng (Web Next.js, Desktop Windows Forms, Mobile Android Native Java).
  - Không tạo database riêng cho từng nền tảng, không phân mảnh logic nghiệp vụ.
  - Phân quyền RBAC nghiêm ngặt: Guest, Registered Student, Club Member, Collaborator, Club Committee/BCN, System Administrator.
  - Tích hợp chuẩn nhận diện nhóm **VISIONARY API** với 4 thành viên: Quách Khoa Đức, Võ Ngọc Minh Đạt, Hồ Đoàng Nguyên Khang, Đào Trí Khang.
  - Thông cáo học phần TH71108 rõ ràng, minh bạch trên toàn bộ giao diện và tài liệu.

- **Backend ASP.NET Core 8 Web API (`backend/`):**
  - Khởi tạo Master Solution `backend/Visionary.sln` với 4 projects: `Visionary.Core`, `Visionary.Infrastructure`, `Visionary.Api`, `Visionary.Tests`.
  - Triển khai Domain Entities cho toàn bộ 34 bảng nghiệp vụ (Identity, Club, Events, CMS, Achievements, Tech Resources, Opportunities, Jobs, Ingestion, Audit Logs).
  - Tích hợp Npgsql PostgreSQL với cơ chế tự động chuyển đổi SQLite/InMemory cho môi trường kiểm thử và fallback ngoại tuyến.
  - Tích hợp mã hóa mật khẩu bảo mật chuẩn BCrypt work factor 11.
  - Tích hợp xác thực JWT Bearer Token với thuật toán HMAC-SHA256, thời hạn 24h.
  - Tích hợp tài liệu OpenAPI/Swagger UI tại `/swagger`.
  - Tích hợp `DataAutomationService` tự động thu thập từ GitHub REST API, Hugging Face Hub API và RSS feeds.
  - Bộ kiểm thử xUnit đạt 9/9 tests (100% Pass).

- **Website Frontend Next.js 14 App Router (`frontend/`):**
  - Next.js 14 App Router, TypeScript strict mode, Tailwind CSS, Lucide icons.
  - Hệ thống nhận diện màu sắc cao cấp: Deep Navy (`#142D4E`), Visionary Blue (`#2264AC`), Teal Accent (`#22A6A1`), Surface (`#F5F7FB`).
  - Xây dựng hoàn chỉnh 16 routes: Trang chủ, Giới thiệu CLB & nhóm, Đăng nhập, Đăng ký, Bảng điều khiển sinh viên, Bảng điều khiển quản trị viên, Sự kiện, Chi tiết sự kiện & điểm danh QR, English for IT, Chi tiết thuật ngữ, Tech Radar, Cơ hội & Học bổng, Cổng việc làm, Bảng vàng thành tích, Tin tức CMS, Chi tiết bài viết.
  - Triển khai thành công lên Vercel Cloud Workspace `visionary19` tại `https://frontend-d84n3thit-visionary19.vercel.app` (Alias: `https://frontend-ten-murex-yaos2b181w.vercel.app`).

- **Phần mềm Quản trị Desktop Windows Forms C# (`desktop/`):**
  - Xây dựng ứng dụng desktop chuyên nghiệp `Visionary.Desktop` trên nền tảng .NET 8 Windows Desktop (`net8.0-windows`).
  - Tham chiếu trực tiếp thư viện chia sẻ `Visionary.Core` để tái sử dụng 100% DTOs và Enums.
  - Triển khai `ApiClient` bất đồng bộ (`HttpClient`) kết nối máy chủ Web API, quản lý token JWT in-memory.
  - Màn hình đăng nhập `LoginForm` với nút đăng nhập mẫu nhanh cho Quản trị viên và Ban Chủ Nhiệm.
  - Màn hình chính `MainForm` với thanh điều hướng màu Deep Navy, quản lý 6 phân hệ: Dashboard thống kê, Danh sách thành viên, Xét duyệt đơn gia nhập (`ReviewApplicationDialog`), Quản lý sự kiện & điểm danh (`CreateEventDialog`), Điều khiển đồng bộ dữ liệu tự động, Màn hình giới thiệu About Visionary.
  - Biên dịch thành công 0 lỗi, 0 cảnh báo và tích hợp vào `Visionary.sln`.

- **Ứng dụng Di động Android Native Java (`mobile/`):**
  - Xây dựng ứng dụng Android native `VisionaryAndroid` bằng ngôn ngữ Java 17 LTS, Android SDK Platform 34, Material Design 3.
  - Sử dụng Retrofit 2.11.0 và OkHttp 3 với HTTP Logging Interceptor và Interceptor tự động tiêm `Authorization: Bearer <token>`.
  - Quản lý phiên đăng nhập an toàn qua `SessionManager` lưu trữ trong `SharedPreferences`.
  - Giao diện `MainActivity` với `BottomNavigationView` chuyển đổi 5 phân hệ: Trang chủ, Sự kiện (Đăng ký/Hủy/Mã QR check-in), English for IT (Thuật ngữ chuyên ngành), Cơ hội (Hackathon/Học bổng), Hồ sơ cá nhân & Thông tin nhóm phát triển.
  - Cấu hình linh hoạt URL máy chủ cho Android Emulator (`http://10.0.2.2:5000`) và máy chủ thực tế.
  - Thiết lập Gradle Wrapper 8.4 độc lập, sẵn sàng mở và chạy trong Android Studio.

- **Tài liệu Kỹ thuật Toàn diện (`docs/`):**
  - `PROJECT_AUDIT.md`: Báo cáo khảo sát toàn bộ môi trường và hiện trạng.
  - `ARCHITECTURE.md`: Sơ đồ kiến trúc một Backend ba nền tảng, luồng dữ liệu và cơ chế bảo mật.
  - `REQUIREMENTS.md`: Đặc tả 8 phân hệ cốt lõi và ma trận yêu cầu chức năng/phi chức năng.
  - `DATABASE_SCHEMA.md`: Thiết kế ERD 34 bảng, ràng buộc khóa ngoại, chỉ mục và chính sách bảo vệ dữ liệu.
  - `API_CONTRACT.md`: Hợp đồng REST API chi tiết, định dạng request/response và mã lỗi.
  - `DATA_SOURCES.md`: Danh mục nguồn dữ liệu công khai, chu kỳ làm mới và cơ chế deduplication.
  - `SECURITY.md`: Chính sách an toàn OWASP Top 10, quản lý secret, chống lộ dữ liệu trên F12 DevTools.
  - `DEPLOYMENT.md`: Hướng dẫn triển khai Vercel, Docker Kestrel và biến môi trường.
  - `QA_TEST_REPORT.md`: Báo cáo kiểm thử chi tiết 5 phân hệ với tỷ lệ đạt 100%.
  - `OPEN_SOURCE_AUDIT.md`: Đánh giá giấy phép và độ tin cậy của tất cả thư viện mã nguồn mở.
  - `PENDING_CONFIGURATION.md`: Danh sách cấu hình bổ sung khi vận hành production.
