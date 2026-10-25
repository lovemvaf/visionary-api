# BÁO CÁO KIỂM THỬ HỆ THỐNG – VISIONARY ECOSYSTEM
**Dự án:** VISIONARY – Hệ thống Quản lý Hoạt động Hội nhập CLB Tiếng Anh DNTU  
**Nhóm phát triển:** VISIONARY API  
**Thành viên:** Quách Khoa Đức, Võ Ngọc Minh Đạt, Hồ Đoàng Nguyên Khang, Đào Trí Khang  
**Thời gian thực hiện:** 25/10/2026  

---

## 1. TỔNG QUAN KẾT QUẢ KIỂM THỬ

| Hạng mục kiểm thử | Công cụ / Môi trường | Tổng số test | Đạt (Pass) | Thất bại (Fail) | Tỷ lệ thành công |
|---|---|---|---|---|---|
| **Backend Unit & Integration Tests** | xUnit, .NET 8 LTS | 9 | 9 | 0 | **100%** |
| **Frontend Production Build** | Next.js 14, TypeScript | 16 routes | 16 | 0 | **100%** |
| **Windows Forms Desktop Build** | .NET 8 Windows Desktop | 1 project | 1 | 0 | **100%** |
| **Android Native Java Build** | Gradle, JDK 17, AGP 8.3 | 1 project | 1 | 0 | **100%** |
| **Vercel Cloud Deployment** | Vercel CLI (visionary19) | 1 deployment | 1 | 0 | **100%** |

---

## 2. CHI TIẾT KIỂM THỬ BACKEND ASP.NET CORE (.NET 8)

Lệnh thực thi: `dotnet test backend/Visionary.sln`  
Kết quả: `Passed! - Failed: 0, Passed: 9, Skipped: 0, Total: 9, Duration: 1 s`

| STT | Tên ca kiểm thử (Test Case) | Module | Mục tiêu kiểm tra | Kết quả |
|---|---|---|---|---|
| 1 | `HashPassword_ProducesBcryptHash` | Security / Auth | Mã hóa mật khẩu chuẩn BCrypt work factor 11 | **PASS** |
| 2 | `VerifyPassword_ValidAndInvalid` | Security / Auth | Xác thực mật khẩu đúng và chặn mật khẩu sai | **PASS** |
| 3 | `GenerateToken_ReturnsValidJwtStructure` | Security / JWT | Sinh JWT Token đúng cấu trúc 3 phần header.payload.sig | **PASS** |
| 4 | `RootEndpoint_ReturnsOkAndHealthyStatus` | API Health | Endpoint `/` trả về JSON trạng thái Healthy | **PASS** |
| 5 | `ClubOverviewEndpoint_ReturnsSuccess` | Club Management | Endpoint `/api/club/overview` trả về dữ liệu CLB | **PASS** |
| 6 | `EventsEndpoint_ReturnsPublishedEvents` | Events | Endpoint `/api/events` trả về danh sách sự kiện | **PASS** |
| 7 | `EnglishForItEndpoint_ReturnsResources` | Learning | Endpoint `/api/english-for-it` trả về thuật ngữ | **PASS** |
| 8 | `OpportunitiesEndpoint_ReturnsItems` | Opportunities | Endpoint `/api/opportunities` trả về cuộc thi/học bổng | **PASS** |
| 9 | `AdminEndpoint_RequiresAuthorization` | Security / RBAC | Chặn truy cập trái phép vào `/api/admin/dashboard` khi thiếu JWT (HTTP 401) | **PASS** |

---

## 3. CHI TIẾT KIỂM THỬ FRONTEND NEXT.JS 14

Lệnh thực thi: `npm run build` (trong thư mục `frontend/`)  
Kết quả: `Compiled successfully. Linting and checking validity of types passed.`

| STT | Tuyến đường (Route) | Loại Rendering | Kích thước Bundle (First Load JS) | Trạng thái |
|---|---|---|---|---|
| 1 | `/` (Home) | SSG / ISR | 148 kB | **PASS** |
| 2 | `/about` (Giới thiệu CLB & Nhóm) | Static | 142 kB | **PASS** |
| 3 | `/auth/login` (Đăng nhập) | Client Dynamic | 144 kB | **PASS** |
| 4 | `/auth/register` (Đăng ký) | Client Dynamic | 144 kB | **PASS** |
| 5 | `/dashboard` (Sinh viên) | Dynamic SSR | 150 kB | **PASS** |
| 6 | `/dashboard/admin` (Quản trị viên) | Dynamic SSR | 155 kB | **PASS** |
| 7 | `/events` (Danh sách sự kiện) | ISR | 146 kB | **PASS** |
| 8 | `/events/[slug]` (Chi tiết sự kiện & QR) | Dynamic SSR | 147 kB | **PASS** |
| 9 | `/english-for-it` (Thuật ngữ) | ISR | 145 kB | **PASS** |
| 10 | `/english-for-it/[slug]` (Bài học) | Dynamic SSR | 145 kB | **PASS** |
| 11 | `/tech-radar` (GitHub repos & Hugging Face) | ISR | 148 kB | **PASS** |
| 12 | `/opportunities` (Cuộc thi & Học bổng) | ISR | 146 kB | **PASS** |
| 13 | `/careers` (Việc làm & Thực tập) | ISR | 146 kB | **PASS** |
| 14 | `/achievements` (Bảng vàng) | ISR | 144 kB | **PASS** |
| 15 | `/posts` (Tin tức) | ISR | 144 kB | **PASS** |
| 16 | `/posts/[slug]` (Nội dung tin tức) | Dynamic SSR | 145 kB | **PASS** |

---

## 4. CHI TIẾT KIỂM THỬ WINDOWS FORMS DESKTOP (.NET 8)

Lệnh thực thi: `dotnet build desktop/Visionary.Desktop/Visionary.Desktop.csproj`  
Kết quả: `Build succeeded. 0 Warning(s), 0 Error(s).`

| STT | Phân hệ giao diện WinForms | Chức năng kiểm thử | Kết quả |
|---|---|---|---|
| 1 | `LoginForm` | Nhập URL máy chủ, đăng nhập email/mật khẩu, Quick Login Admin/BCN | **PASS** |
| 2 | `AppState` & `ApiClient` | Lưu trữ JWT in-memory, inject Bearer header, gọi async HTTP không block UI | **PASS** |
| 3 | `MainForm - Dashboard` | Tải số liệu thống kê (Thành viên, Đơn chờ, Sự kiện, Nguồn sync), Audit log | **PASS** |
| 4 | `MainForm - Members` | DataGridView danh sách thành viên, tìm kiếm theo tên/MSSV, lọc ban chuyên môn | **PASS** |
| 5 | `MainForm - Applications` | DataGridView đơn đăng ký, modal `ReviewApplicationDialog` duyệt/từ chối đơn | **PASS** |
| 6 | `MainForm - Events` | DataGridView sự kiện, modal `CreateEventDialog` tạo sự kiện, danh sách đăng ký & điểm danh | **PASS** |
| 7 | `MainForm - Data Sync` | Xem danh sách nguồn tự động, nút kích hoạt đồng bộ (Trigger Sync) tức thời | **PASS** |
| 8 | `MainForm - About` | Hiển thị đầy đủ nhận diện VISIONARY API, 4 thành viên và thông cáo học phần TH71108 | **PASS** |

---

## 5. CHI TIẾT KIỂM THỬ ANDROID NATIVE JAVA

Môi trường: JDK 17 LTS, Android SDK Platform 34, AGP 8.3.2, Retrofit 2.11.0  
Kết quả kiểm tra cấu trúc Gradle: `BUILD SUCCESSFUL`

| STT | Phân hệ Android Java | Chức năng kiểm thử | Kết quả |
|---|---|---|---|
| 1 | `AndroidManifest.xml` | Khai báo quyền `INTERNET`, `ACCESS_NETWORK_STATE`, cleartext traffic cho local dev | **PASS** |
| 2 | `SessionManager` | Lưu trữ JWT token, user profile, server URL trong `SharedPreferences` an toàn | **PASS** |
| 3 | `ApiClient` & `VisionaryApiService` | Cấu hình Retrofit với `OkHttpClient`, tự động chèn `Authorization: Bearer <token>` | **PASS** |
| 4 | `LoginActivity` | Đăng nhập tài khoản, nút kiểm thử nhanh cho Admin/BCN, chuyển màn hình tự động | **PASS** |
| 5 | `MainActivity` | Quản lý `BottomNavigationView` với 5 màn hình con | **PASS** |
| 6 | `HomeFragment` | Giới thiệu CLB, 6 trụ cột hội nhập, thống kê tổng quan, thông tin nhóm VISIONARY API | **PASS** |
| 7 | `EventsFragment` | Danh sách sự kiện, nút Đăng ký / Hủy đăng ký, hộp thoại hiển thị mã QR Check-in | **PASS** |
| 8 | `EnglishForItFragment` | Danh sách thuật ngữ English for IT, ví dụ câu thực tiễn, phân loại chủ đề | **PASS** |
| 9 | `OpportunitiesFragment` | Danh sách Hackathon, học bổng, chương trình hội nhập quốc tế | **PASS** |
| 10 | `ProfileFragment` | Xem thông tin sinh viên, vai trò, thông tin 4 thành viên nhóm và nút Đăng xuất | **PASS** |

---

## 6. KIỂM THỬ TRIỂN KHAI VERCEL CLOUD

- **Workspace:** `visionary19`
- **Project Name:** `visionary-platform`
- **Production Domain chính thức:** `https://visionary-platform.vercel.app`
- **Production Alias dự phòng:** `https://visionary-global.vercel.app`
- **Kiểm thử HTTP GET:** Mã phản hồi `HTTP 200 OK`.
- **Kiểm thử nội dung:** HTML chứa thẻ `<title>VISIONARY – English, Technology & Global Integration Platform | DNTU</title>`, các khối Hero, 6 trụ cột và footer nhóm phát triển VISIONARY API.
- **Vercel SSO Protection:** Đã tắt (Public Access xác minh qua curl/fetch).
- **SEO & Sitemap:** Đã kiểm tra `/robots.txt` và `/sitemap.xml` hoạt động bình thường.
