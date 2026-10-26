# BÁO CÁO KIỂM THỬ CHẤT LƯỢNG HỆ THỐNG – VISIONARY ECOSYSTEM (QA REPORT)
**Dự án:** VISIONARY – Hệ thống Quản lý Hoạt động Hội nhập (TH71108)  
**Nhóm phát triển:** VISIONARY API  
**Thành viên:** Quách Khoa Đức, Võ Ngọc Minh Đạt, Hồ Đoàn Nguyên Khang, Đào Trí Khang  
**Thời gian cập nhật:** 26/10/2026  
**Nguồn xác minh chuẩn (SSOT):** [`docs/TEST_VERIFICATION_REPORT.md`](./TEST_VERIFICATION_REPORT.md) và [`project-status/verification.json`](../project-status/verification.json)  

---

## 1. TỔNG QUAN KẾT QUẢ KIỂM THỬ HIỆN HÀNH (CURRENT VERIFIED STATUS)

| Hạng mục kiểm thử | Công cụ / Môi trường | Quy mô kiểm thử | Đạt (Pass) | Thất bại (Fail) | Tỷ lệ thành công | Trạng thái & Bằng chứng |
|---|---|---|---|---|---|---|
| **Backend xUnit Suite (Hiện tại)** | xUnit, .NET 8.0 SDK | **19 tests** | **19** | 0 | **100%** | **VERIFIED PASS** (GitHub Actions Run #40339904597) |
| *Backend Auth Boundary (Mốc trước)* | xUnit, .NET 8.0 SDK | *17 tests* | *17* | *0* | *100%* | *HISTORICAL SNAPSHOT* (Giai đoạn trước khi thêm 2 bài test JWT Token Validation Regression) |
| *Backend Posts Invariant (Mốc trước)* | xUnit, .NET 8.0 SDK | *15 tests* | *15* | *0* | *100%* | *HISTORICAL SNAPSHOT* (Giai đoạn trước khi thêm 2 bài test Authorization Boundary) |
| *Backend Core Smoke (Mốc lịch sử)* | xUnit, .NET 8.0 SDK | *9 tests* | *9* | *0* | *100%* | *HISTORICAL SNAPSHOT* (Giai đoạn trước khi thêm 6 bài test Posts Logic) |
| **Windows Forms Desktop Suite** | xUnit, .NET 8.0-windows | **21 tests** | **21** | 0 | **100%** | **VERIFIED PASS** (GitHub Actions Run #40317635884) |
| **Android Native Java Suite** | JUnit 4, Gradle, JDK 17 | **15 tests** | **15** | 0 | **100%** | **VERIFIED PASS** (GitHub Actions Run #40319077411) |
| **Frontend Production Build** | Next.js 14, TypeScript | **19 routes** | **19** | 0 | **100%** | **VERIFIED PASS** (Tất cả 19 tuyến đường biên dịch sạch) |
| **Vercel Cloud Deployment** | Vercel Edge (`visionary19`) | Production | 1 | 0 | **100%** | **ONLINE 24/7** (`https://visionary-platform.vercel.app`) |

---

## 2. CHI TIẾT KIỂM THỬ BACKEND ASP.NET CORE (.NET 8) – HIỆN HÀNH 19 BÀI TEST

Lệnh thực thi: `dotnet test backend/Visionary.Backend.sln`  
Kết quả: `Passed! - Failed: 0, Passed: 19, Skipped: 0, Total: 19, Duration: 5 s`  
Minh chứng CI: GitHub Actions Run ID `40339904597` (Commit `45a56b3` & `2eb86b2` merged via PR #5, #7)

| STT | Tên ca kiểm thử (Test Case) | Suite Kiểm thử | Module | Mục tiêu kiểm tra | Kết quả |
|:---:|---|---|---|---|:---:|
| 1 | `RootEndpoint_ReturnsHealthyStatus` | Integration | API Health | Endpoint `/` trả về JSON trạng thái Healthy | **PASS** |
| 2 | `ClubOverview_ReturnsSuccessData` | Integration | Club Management | Endpoint `/api/club/overview` trả về dữ liệu CLB | **PASS** |
| 3 | `EventsEndpoint_ReturnsSeededEvents` | Integration | Events | Endpoint `/api/events` trả về danh sách sự kiện khởi tạo | **PASS** |
| 4 | `EnglishForItEndpoint_ReturnsResources` | Integration | Learning | Endpoint `/api/english-for-it` trả về thuật ngữ CNTT | **PASS** |
| 5 | `OpportunitiesEndpoint_ReturnsOpportunities` | Integration | Opportunities | Endpoint `/api/opportunities` trả về cuộc thi/học bổng | **PASS** |
| 6 | `JobsEndpoint_ReturnsJobs` | Integration | Careers | Endpoint `/api/careers/jobs` trả về tin tuyển dụng | **PASS** |
| 7 | `Login_WithSeededAdminCredentials_ReturnsJwtToken` | Integration | Security / Auth | Đăng nhập tài khoản Quản trị viên, cấp phát token JWT hợp lệ | **PASS** |
| 8 | `PasswordHasher_ShouldHashAndVerifyCorrectly` | Unit Test | Security / Auth | Mã hóa mật khẩu chuẩn BCrypt với salt ngẫu nhiên | **PASS** |
| 9 | `JwtService_ShouldGenerateAndValidateToken` | Unit Test | Security / JWT | Sinh và xác thực JWT token chuẩn HMAC-SHA256 | **PASS** |
| 10 | `CategoriesEndpoint_ReturnsFourCategoriesWithExactPublishedCounts` | Logic Invariant | Content / Posts | 4 chuyên mục chuẩn với số lượng bài viết xuất bản chính xác | **PASS** |
| 11 | `PublishedPosts_CategoryUnion_StrictlyEquals_AllPublishedPosts` | Logic Invariant | Content / Posts | Bất biến hợp tập: Tổng bài viết theo danh mục bằng tổng bài xuất bản | **PASS** |
| 12 | `Pagination_Metadata_And_ItemCounts_AreAccurate` | Logic Invariant | Core / Pagination | Metadata phân trang (Page, PageSize, TotalCount) tính toán chính xác | **PASS** |
| 13 | `UnpublishedPosts_Draft_And_PendingReview_NeverLeakPublicly` | Security Invariant | Security / RBAC | Chặn hoàn toàn bài viết Draft/Pending rò rỉ ra API công khai | **PASS** |
| 14 | `Search_WithCategory_And_EmptyState_AreAccurate` | Logic Invariant | Content / Search | Tìm kiếm kết hợp lọc danh mục và trạng thái danh sách rỗng | **PASS** |
| 15 | `GetPostBySlug_ValidPublishedPost_Returns200AndIncrementsView` | Logic Invariant | Content / Posts | Lấy chi tiết bài viết qua Slug và tự động tăng lượt xem | **PASS** |
| 16 | `AdminUsers_AnonymousRequest_ReturnsUnauthorized` | Security Regression | Security / RBAC | Yêu cầu ẩn danh tới `/api/admin/users` trả về mã 401 Unauthorized | **PASS** |
| 17 | `Student_CannotAccessAdminOrGrantSelfAdminRole` | Security Regression | Security / RBAC | Sinh viên không được phép truy cập endpoint admin hoặc tự cấp quyền Admin | **PASS** |
| 18 | `AdminUsers_ExpiredBearerToken_ReturnsUnauthorized` | Security Regression | Security / JWT | Yêu cầu với JWT hết hạn tới `/api/admin/users` trả về mã 401 Unauthorized | **PASS** |
| 19 | `AdminUsers_MalformedBearerToken_ReturnsUnauthorized` | Security Regression | Security / JWT | Yêu cầu với Bearer token sai cấu trúc tới `/api/admin/users` trả về mã 401 Unauthorized | **PASS** |

---

## 3. CHI TIẾT KIỂM THỬ FRONTEND NEXT.JS 14 (19 ROUTES)

Lệnh thực thi: `npm run build` (trong thư mục `frontend/`)  
Kết quả: `✓ Compiled successfully. Linting and checking validity of types passed. Generating static pages (19/19)`

| STT | Tuyến đường (Route) | Loại Rendering | First Load JS | Trạng thái |
|:---:|---|---|---|:---:|
| 1 | `/` (Trang chủ) | Static (SSG) | 96.2 kB | **PASS** |
| 2 | `/_not-found` (404 Page) | Static | 88.2 kB | **PASS** |
| 3 | `/about` (Giới thiệu CLB & Nhóm) | Static | 96.2 kB | **PASS** |
| 4 | `/achievements` (Bảng vàng thành tích) | Static | 93.5 kB | **PASS** |
| 5 | `/api/[...path]` (BFF Proxy) | Dynamic (Server) | 0 B | **PASS** |
| 6 | `/auth/login` (Đăng nhập) | Static | 103 kB | **PASS** |
| 7 | `/auth/register` (Đăng ký) | Static | 102 kB | **PASS** |
| 8 | `/careers` (Cơ hội việc làm CNTT) | Static | 95 kB | **PASS** |
| 9 | `/dashboard` (Bảng điều khiển sinh viên) | Static | 93.8 kB | **PASS** |
| 10 | `/dashboard/admin` (Quản trị viên) | Static | 105 kB | **PASS** |
| 11 | `/dashboard/committee` (Ban Chủ Nhiệm) | Static | 104 kB | **PASS** |
| 12 | `/english-for-it` (Thuật ngữ Tiếng Anh) | Static | 103 kB | **PASS** |
| 13 | `/english-for-it/[slug]` (Chi tiết bài học) | Dynamic (Server) | 102 kB | **PASS** |
| 14 | `/events` (Danh sách sự kiện) | Static | 94.5 kB | **PASS** |
| 15 | `/events/[slug]` (Chi tiết sự kiện & Check-in) | Dynamic (Server) | 102 kB | **PASS** |
| 16 | `/opportunities` (Học bổng & Hackathon) | Static | 95 kB | **PASS** |
| 17 | `/posts` (Tin tức & Bài viết) | Static | 104 kB | **PASS** |
| 18 | `/posts/[slug]` (Chi tiết bài viết) | Dynamic (Server) | 102 kB | **PASS** |
| 19 | `/tech-radar` (Xu hướng công nghệ) | Static | 95.4 kB | **PASS** |

---

## 4. ĐÁNH GIÁ CHUỖI CUNG ỨNG VÀ BẢO MẬT (DEVSECOPS)

1. **NuGet Package Audit:** `dotnet list backend/Visionary.Backend.sln package --vulnerable` xác nhận **0 gói có lỗ hổng** trên toàn bộ 4 dự án backend.
2. **Gitleaks Secret Scan:** Toàn bộ mã nguồn hoạt động trên commit mới nhất không chứa secret, API key hay private token hoạt động nào.
3. **Ngoại lệ Upstream Next.js 14:** Đã được kiểm chứng và lập tài liệu ngoại lệ an toàn tại [`docs/security/DEPENDENCY_VULNERABILITY_REPORT.md`](./security/DEPENDENCY_VULNERABILITY_REPORT.md).
