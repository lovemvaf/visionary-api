# BÁO CÁO XÁC MINH KIỂM THỬ HỆ THỐNG TOÀN DIỆN (TEST VERIFICATION REPORT)
## SINGLE SOURCE OF TRUTH (SSOT) – KIỂM THỬ ĐA NỀN TẢNG VISIONARY
**Mã dự án:** VISIONARY – Hệ thống Quản lý Hoạt động Hội nhập (TH71108)  
**Trường:** Đại học Công nghệ Đồng Nai (DNTU)  
**Commit xác minh mới nhất:** `9f7b152de978b52494d290b1109ef46ed4cf0b9a`  
**GitHub Actions Run ID:** `#40254874364` (Backend CI #14)  
**Thời điểm phát hành báo cáo:** 26/10/2026  

---

## 1. GIẢI TRÌNH LỊCH SỬ: ĐỐI CHIẾU MỐC 9/9 VÀ HIỆN TRẠNG 15/15 TESTS

Trong quá trình phát triển dự án VISIONARY, số lượng kiểm thử tự động xUnit của Backend đã trải qua hai giai đoạn mốc quan trọng:

1. **Mốc lịch sử ban đầu (Historical Milestone – 9/9 Tests):**
   - *Giai đoạn:* Từ khi hoàn thành kiến trúc nền tảng 3 tầng đến trước đợt kiểm toán bất biến phân loại tin bài (Posts Logic Audit).
   - *Quy mô:* Gồm 7 bài test tích hợp API (`ApiIntegrationTests.cs`) và 2 bài test xác thực băm mật khẩu/JWT (`AuthTests.cs`).
   - *Ghi nhận:* Các tài liệu QA giai đoạn đầu (`docs/QA_TEST_REPORT.md` bản cũ) ghi nhận 9/9 tests PASS là hoàn toàn chính xác theo mã nguồn ở các commit trước đó.
2. **Mốc mở rộng hiện hành (Current Active Suite – 15/15 Tests):**
   - *Giai đoạn:* Bổ sung suite kiểm toán logic chuyên sâu `PostsLogicAuditTests.cs` (gồm 6 bài test kiểm tra bất biến hợp tập danh mục, bảo mật bài viết bản nháp không lộ ra ngoài, tính chính xác của phân trang, và tìm kiếm rỗng).
   - *Quy mô hiện tại:* Tổng cộng **15 bài test** (7 API Integration + 2 Auth + 6 Posts Logic Audit = 15 tests).
   - *Minh chứng thực tế:* GitHub Actions Backend CI #14 (Run ID `40254874364`) trên commit `9f7b152` chạy thành công:
     ```text
     Test Run Successful.
     Total tests: 15
          Passed: 15
          Failed: 0
         Skipped: 0
      Duration: 2.1s
     ```

---

## 2. BẢNG DANH MỤC 15 BÀI TEST BACKEND XUNIT CHI TIẾT

| STT | Namespace & Tên Test Case | Suite Kiểm thử | Phạm vi kiểm tra | Trạng thái |
|:---:|---|---|---|:---:|
| 1 | `Visionary.Tests.ApiIntegrationTests.RootEndpoint_ReturnsHealthyStatus` | Integration | Kiểm tra endpoint gốc `/` trả về HTTP 200 và chuỗi metadata an toàn | **VERIFIED PASS** |
| 2 | `Visionary.Tests.ApiIntegrationTests.ClubOverview_ReturnsSuccessData` | Integration | Kiểm tra lấy tổng quan hoạt động CLB Tiếng Anh | **VERIFIED PASS** |
| 3 | `Visionary.Tests.ApiIntegrationTests.EventsEndpoint_ReturnsSeededEvents` | Integration | Kiểm tra truy xuất danh sách sự kiện hội nhập khởi tạo | **VERIFIED PASS** |
| 4 | `Visionary.Tests.ApiIntegrationTests.EnglishForItEndpoint_ReturnsResources` | Integration | Kiểm tra tài nguyên thuật ngữ English for IT | **VERIFIED PASS** |
| 5 | `Visionary.Tests.ApiIntegrationTests.OpportunitiesEndpoint_ReturnsOpportunities` | Integration | Kiểm tra dữ liệu cơ hội, học bổng và việc làm quốc tế | **VERIFIED PASS** |
| 6 | `Visionary.Tests.ApiIntegrationTests.JobsEndpoint_ReturnsJobs` | Integration | Kiểm tra API tuyển dụng chuyên ngành CNTT | **VERIFIED PASS** |
| 7 | `Visionary.Tests.ApiIntegrationTests.Login_WithSeededAdminCredentials_ReturnsJwtToken` | Integration | Kiểm tra luồng đăng nhập quản trị viên, cấp phát token JWT chuẩn | **VERIFIED PASS** |
| 8 | `Visionary.Tests.AuthTests.PasswordHasher_ShouldHashAndVerifyCorrectly` | Unit Test | Kiểm tra thuật toán băm BCrypt với salt ngẫu nhiên | **VERIFIED PASS** |
| 9 | `Visionary.Tests.AuthTests.JwtService_ShouldGenerateAndValidateToken` | Unit Test | Kiểm tra tạo và giải mã chữ ký JWT HMAC-SHA256 | **VERIFIED PASS** |
| 10 | `Visionary.Tests.PostsLogicAuditTests.CategoriesEndpoint_ReturnsFourCategoriesWithExactPublishedCounts` | Logic Invariant | Kiểm tra 4 chuyên mục chuẩn với số lượng bài viết xuất bản chính xác | **VERIFIED PASS** |
| 11 | `Visionary.Tests.PostsLogicAuditTests.PublishedPosts_CategoryUnion_StrictlyEquals_AllPublishedPosts` | Logic Invariant | Kiểm tra bất biến hợp tập: Tổng bài viết theo từng danh mục đúng bằng danh sách tổng | **VERIFIED PASS** |
| 12 | `Visionary.Tests.PostsLogicAuditTests.Pagination_Metadata_And_ItemCounts_AreAccurate` | Logic Invariant | Kiểm tra tính toán metadata phân trang (Page, PageSize, TotalCount) | **VERIFIED PASS** |
| 13 | `Visionary.Tests.PostsLogicAuditTests.UnpublishedPosts_Draft_And_PendingReview_NeverLeakPublicly` | Security Invariant | Kiểm tra bài viết Draft/Pending không bao giờ bị rò rỉ ra API công khai | **VERIFIED PASS** |
| 14 | `Visionary.Tests.PostsLogicAuditTests.Search_WithCategory_And_EmptyState_AreAccurate` | Logic Invariant | Kiểm tra thuật toán tìm kiếm kết hợp lọc danh mục và trạng thái kết quả rỗng | **VERIFIED PASS** |
| 15 | `Visionary.Tests.PostsLogicAuditTests.GetPostBySlug_ValidPublishedPost_Returns200AndIncrementsView` | Logic Invariant | Kiểm tra truy xuất chi tiết bài viết qua Slug và tự động tăng lượt xem | **VERIFIED PASS** |

---

## 3. MA TRẬN TRẠNG THÁI KIỂM THỬ ĐA NỀN TẢNG (CROSS-PLATFORM TEST MATRIX)

Để bảo đảm tính trung thực học thuật, hệ thống phân định rõ ràng giữa kết quả **Build Verification (Kiểm tra biên dịch)** và **Runtime / E2E Testing (Kiểm thử thực thi)**:

| Tầng công nghệ | Nền tảng | Kiểm tra Biên dịch (Build) | Kiểm thử Thực thi / E2E | Ghi chú & Bằng chứng xác minh |
|---|---|:---:|:---:|---|
| **Backend API** | ASP.NET Core 8 Web API | **VERIFIED PASS** | **VERIFIED PASS (15/15)** | `dotnet test` đạt 15/15 tests. GitHub Actions Run #40254874364 |
| **Frontend Web** | Next.js 14 App Router | **VERIFIED PASS** | **MANUAL_VERIFIED** | `npm run build` xuất bản thành công 19/19 static routes; xác minh qua trình duyệt |
| **Desktop App** | Windows Forms .NET 8 | **VERIFIED PASS** | **MANUAL_VERIFIED** | `dotnet build` đạt 0 Warning, 0 Error; kiểm thử giao diện `LoginForm` và `MainForm` |
| **Mobile App** | Android Java SDK 34 | **CONFIG_VERIFIED** | **EMULATOR_VERIFIED** | Cấu hình bảo mật `network_security_config.xml` chặn cleartext; kiểm thử qua Android Emulator |
| **Chuỗi Cung ứng** | NuGet & Gitleaks | **VERIFIED PASS** | **VERIFIED PASS** | Backend có 0 lỗ hổng NuGet. Gitleaks xác nhận 0 secret trong mã nguồn hoạt động |

---

## 4. KẾT LUẬN & ĐỒNG BỘ DỮ LIỆU

Báo cáo này là **Nguồn sự thật chuẩn (Single Source of Truth)** thay thế mọi số liệu mâu thuẫn trước đây. Tất cả các tài liệu khác trong repository (`README.md`, `.agent/STATE.md`, `.agent/TEST_RESULTS.md`, `QA_TEST_REPORT.md`, và Slide thuyết trình) đều được quy chiếu và đồng bộ thống nhất theo số liệu 15/15 bài test Backend của báo cáo này.
