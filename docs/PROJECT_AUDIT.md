# BÁO CÁO KHẢO SÁT DỰ ÁN (PROJECT AUDIT REPORT)
**Hệ thống:** VISIONARY – Hệ thống Quản lý Hoạt động Hội nhập  
**Đơn vị thực hiện:** VISIONARY API (Quách Khoa Đức, Võ Ngọc Minh Đạt, Hồ Đoàn Nguyên Khang, Đào Trí Khang)  
**Thời gian khảo sát:** 25/10/2026  

---

## 1. Hiện trạng Workspace ban đầu
- Workspace ban đầu: `c:\Users\asus\Documents\Visionary API` là một thư mục mới tinh chưa có mã nguồn, cho phép triển khai kiến trúc Clean Architecture chuẩn mực ngay từ đầu mà không gặp rủi ro mã rác hay xung đột legacy code.
- Môi trường phát triển cục bộ của máy tính chủ (`asus`):
  - **Git:** v2.54.0.windows.1 – Sẵn sàng quản lý mã nguồn, branch, commit và GitHub remote.
  - **.NET SDK:** Phiên bản 8.0.205, 8.0.413 (LTS) và 9.0.305. Runtimes bao gồm đầy đủ `Microsoft.AspNetCore.App` (8.0 và 9.0) và `Microsoft.WindowsDesktop.App` (8.0 và 9.0). Điều này đảm bảo cả ASP.NET Core 8 Web API và Windows Forms Desktop C# đều biên dịch và thực thi 100% tự nhiên trên máy tính này.
  - **Node.js & npm:** Node.js v24.13.0, npm v11.6.2 – Sẵn sàng cho Next.js 14/15 App Router, TypeScript và Tailwind CSS.
  - **Java SDK:** Java 17 LTS (build 17.0.13+10-LTS-268) HotSpot 64-Bit Server VM – Đúng chuẩn yêu cầu của Android Native và Gradle hiện đại.
  - **Android SDK:** Được cấu hình tại `C:\Users\asus\AppData\Local\Android\Sdk` với đầy đủ `build-tools`, `platforms`, `cmdline-tools`, `platform-tools`.
  - **Vercel CLI:** Phiên bản 65.2.0, đã đăng nhập tài khoản `lovemvaf`, kết nối trực tiếp đến Workspace `visionary19` (Plan: hobby).
  - **Docker:** Phiên bản 29.1.3 (build f52814d) sẵn sàng cho containerization và local database testing.

---

## 2. Phân tích Yêu cầu Kỹ thuật môn học TH71108 Web API
- Khóa học yêu cầu xây dựng backend **ASP.NET Core Web API** hoàn chỉnh, độc lập, có RESTful endpoints, Swagger/OpenAPI, Entity Framework Core, quan hệ bảng chặt chẽ, xác thực JWT, phân quyền theo vai trò (Role-based Authorization), xử lý ngoại lệ tập trung (Global Exception Handling Middleware), và khả năng phục vụ đồng thời nhiều client.
- **Nguyên tắc "Một Backend – Ba Nền tảng":**
  1. **Web:** Next.js App Router (TypeScript, Tailwind CSS, SSR/Server Actions)
  2. **Desktop:** Windows Forms C# (.NET 8 Windows Desktop, HttpClient, DTO mapping)
  3. **Mobile:** Android Native Java (JDK 17, Retrofit 2, Material 3)
- Tuyệt đối không để mỗi nền tảng có database riêng hay logic nghiệp vụ mâu thuẫn.

---

## 3. Đánh giá Rủi ro và Biện pháp Giảm thiểu
1. **Rủi ro phụ thuộc bên ngoài (External Credentials):**
   - *Supabase Connection String / Upstash Redis Token / Google OAuth Client Secret* chưa được nhúng cố định trong code để đảm bảo an toàn bảo mật tuyệt đối.
   - *Biện pháp:* Thiết kế giải pháp kiến trúc **Resilient Multi-Provider**:
     - Database: Hỗ trợ chuyển đổi mượt mà giữa PostgreSQL (Npgsql) khi có chuỗi kết nối Supabase, và SQLite / In-Memory EF Core Provider khi chạy local offline/unit testing mà không phải sửa một dòng logic nghiệp vụ nào.
     - Cache: Sử dụng `IDistributedCache` abstraction – tự động kích hoạt Upstash Redis khi có token và fallback tức thì sang `IMemoryCache` trong bộ nhớ RAM nếu Redis chưa cấu hình hoặc mất mạng.
     - OAuth: Controller xác thực token của Google bằng thư viện `Google.Apis.Auth`, có fallback mock-token dành riêng cho kiểm thử cục bộ (`ASPNETCORE_ENVIRONMENT=Development`).
2. **Bảo mật và F12:**
   - Không đặt bất kỳ API Secret, Service Role Key hay DB Connection String nào vào phía Next.js Client Bundle (`NEXT_PUBLIC_`).
   - Mọi thao tác ghi dữ liệu, duyệt thành viên, duyệt bài viết đều phải đi qua ASP.NET Core Web API có xác minh JWT token và quyền hạn (Claims/Roles) tại server.
