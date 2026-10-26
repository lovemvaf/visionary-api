# KẾT QUẢ KIỂM THỬ BẢO MẬT VÀ KIỂM THỬ HỒI QUY (SECURITY TEST RESULTS)
## SYSTEM-WIDE SECURITY & REGRESSION VERIFICATION REPORT
**Mã dự án:** VISIONARY – Hệ thống Quản lý Hoạt động Hội nhập (TH71108)  
**Hình thức kiểm thử:** Automated Integration Tests (xUnit), Build Verification, Static Analysis  
**Thời điểm thực thi:** Tháng 10/2026  

---

## 1. KẾT QUẢ KIỂM THỬ TỰ ĐỘNG BACKEND XUNIT (15/15 TESTS PASS)

Toàn bộ 15 kịch bản kiểm thử tích hợp và kiểm thử an ninh của Backend đã được thực thi thông qua lệnh:
```powershell
dotnet test backend/Visionary.Backend.sln
```

### Chi tiết các ca kiểm thử:
```text
Passed!  - Failed: 0, Passed: 15, Skipped: 0, Total: 15, Duration: 2 s - Visionary.Tests.dll (net8.0)
```

| Tên bài kiểm thử | Đối tượng kiểm thử | Mục đích kiểm thử an ninh & nghiệp vụ | Kết quả |
|---|---|---|---|
| `HashPassword_ProducesDifferentHashForSamePassword` | `PasswordHasher` | Kiểm tra tính duy nhất của Salt ngẫu nhiên cho mỗi lần băm mật khẩu | **PASS** |
| `VerifyPassword_WithCorrectPassword_ReturnsTrue` | `PasswordHasher` | Kiểm tra khả năng xác thực mật khẩu chính xác với hash BCrypt | **PASS** |
| `VerifyPassword_WithWrongPassword_ReturnsFalse` | `PasswordHasher` | Kiểm tra từ chối mật khẩu sai, chống bypass xác thực | **PASS** |
| `GenerateToken_ReturnsValidJwtString` | `JwtService` | Kiểm tra cấu trúc token JWT hợp lệ với chữ ký an toàn | **PASS** |
| `ValidateToken_WithValidToken_ReturnsTrue` | `JwtService` | Kiểm tra khả năng giải mã và xác thực token JWT hợp lệ | **PASS** |
| `ValidateToken_WithInvalidToken_ReturnsFalse` | `JwtService` | Kiểm tra từ chối token giả mạo hoặc token bị sửa đổi chữ ký | **PASS** |
| `RootEndpoint_ReturnsOkAndHealthyStatus` | `Program.cs (/)` | Kiểm tra endpoint gốc trả về thông tin trạng thái chuẩn, không leak thông tin cá nhân | **PASS** |
| `HealthLive_ReturnsAliveStatus` | `Program.cs (/health/live)` | Kiểm tra liveness probe cho container orchestrator | **PASS** |
| `HealthReady_WhenDbAvailable_ReturnsReadyAndConnected` | `Program.cs (/health/ready)` | Kiểm tra readiness probe, xác nhận CSDL sẵn sàng mà không để lộ chi tiết lỗi | **PASS** |
| `Events_GetList_ReturnsPagedEvents` | `EventsController` | Kiểm tra phân trang và lọc sự kiện công khai | **PASS** |
| `EnglishTerms_GetList_ReturnsPagedTerms` | `EnglishTermsController` | Kiểm tra truy xuất thuật ngữ Tiếng Anh CNTT | **PASS** |
| `Opportunities_GetList_ReturnsPagedOpportunities` | `OpportunitiesController` | Kiểm tra truy xuất học bổng & việc làm | **PASS** |
| `TechRadar_GetList_ReturnsPagedTechnologies` | `TechRadarController` | Kiểm tra truy xuất xu hướng công nghệ | **PASS** |
| `Posts_GetList_ReturnsPagedPosts` | `PostsController` | Kiểm tra danh sách bài viết & tin tức | **PASS** |
| `Login_WithSeededAdminCredentials_ReturnsJwtToken` | `AuthController (/api/auth/login)` | Kiểm tra luồng đăng nhập an toàn của Quản trị viên, cấp phát JWT hợp lệ | **PASS** |

---

## 2. KẾT QUẢ KIỂM TRA BIÊN DỊCH VÀ XÂY DỰNG ỨNG DỤNG (BUILD INTEGRITY)

### 2.1. Ứng dụng Desktop Windows Forms C# (.NET 8)
- **Lệnh thực hiện:** `dotnet build desktop/Visionary.Desktop/Visionary.Desktop.csproj`
- **Kết quả:**
  ```text
  Build succeeded.
      0 Warning(s)
      0 Error(s)
  Time Elapsed: 00:00:02.42
  ```
- **Xác nhận an ninh:** Giao diện `LoginForm` không chứa mật khẩu mặc định trong thuộc tính `Text`. Ô nhập liệu ẩn mật khẩu bằng ký tự chấm đen.

### 2.2. Ứng dụng Web Next.js 14 (TypeScript / App Router)
- **Lệnh thực hiện:** `npm run build` (thư mục `frontend/`)
- **Kết quả:**
  ```text
  ✓ Compiled successfully
  ✓ Linting and checking validity of types ...
  ✓ Generating static pages (19/19)
  ✓ Finalizing page optimization ...
  ```
- **Xác nhận an ninh:** 19/19 tuyến đường (routes) biên dịch thành công. Không có lỗi kiểu dữ liệu. Mã nguồn JavaScript đã bundle không chứa mật khẩu tĩnh hay server secret.

### 2.3. Ứng dụng Di động Android Java (SDK 34)
- **Rà soát file cấu hình:**
  - `AndroidManifest.xml`: Đã kích hoạt `android:allowBackup="false"` và gán `android:networkSecurityConfig="@xml/network_security_config"`.
  - `activity_login.xml`: Không còn thuộc tính `android:text="Visionary@2026"`.
  - `LoginActivity.java`: Không còn lệnh gán mật khẩu tự động.

---

## 3. KẾT LUẬN KIỂM THỬ

Toàn bộ các biện pháp củng cố an ninh đã được tích hợp thành công vào mã nguồn dự án mà **không làm phát sinh bất kỳ lỗi biên dịch nào và không làm hỏng bất kỳ chức năng nghiệp vụ nào** của hệ thống đa nền tảng VISIONARY.
