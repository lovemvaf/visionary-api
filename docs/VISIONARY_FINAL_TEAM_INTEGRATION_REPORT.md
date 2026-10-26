# BÁO CÁO NGHIỆM THU TÍCH HỢP TOÀN DIỆN, BẢO TOÀN TÁC GIẢ & PHÁT HÀNH PRODUCTION
## VISIONARY API – FINAL INTEGRATION, SECURITY AUDIT & RELEASE VERIFICATION
> **Chủ nhiệm Dự án & Repository Owner:** Quách Khoa Đức ([`@lovemvaf`](https://github.com/lovemvaf))  
> **Repository:** [https://github.com/lovemvaf/visionary-api](https://github.com/lovemvaf/visionary-api)  
> **Học phần:** Web API (TH71108) – Trường Đại học Công nghệ Đồng Nai (DNTU)  
> **Thời điểm nghiệm thu:** 27/10/2026  
> **Trạng thái Tổng thể:** **PASSED & RELEASED TO PRODUCTION (100% QUALITY GATES MET)**

---

## I. HIỆN TRẠNG REPOSITORY & GITHUB STATE (A. GITHUB STATE)

- **GitHub Repository URL:** [https://github.com/lovemvaf/visionary-api](https://github.com/lovemvaf/visionary-api)
- **Default Branch:** `main`
- **Current Head SHA:** `2eb86b2` (`2eb86b21354292cbb10368ed9b6e32d1f4b08557`)
- **Merge Strategy:** `Create a merge commit` (Bảo toàn 100% commit SHA gốc, metadata tác giả và lịch sử Git thực tế của từng thành viên, tuyệt đối không squash, không rewrite commit history, không fake attribution).
- **Trạng thái Remote:** Đồng bộ hoàn toàn giữa Local và `origin/main`.
- **Trạng thái Working Tree:** Sạch, không file nhạy cảm, không cache thừa, vượt qua 6/6 Quality Gates của `scripts/verify_repository.py`.

---

## II. BẢNG NGHIỆM THU BỐN THÀNH VIÊN (SECTION XX - FOUR MEMBERS ACCEPTANCE MATRIX)

| Tiêu chí Kiểm định (Acceptance Criteria) | Quách Khoa Đức (Lead) | Đào Trí Khang | Hồ Đoàn Nguyên Khang | Võ Ngọc Minh Đạt |
|---|:---:|:---:|:---:|:---:|
| **1. GitHub Account Verified** | [`@lovemvaf`](https://github.com/lovemvaf)<br/>*(ID: 156913149)* | [`@TS13lover1989`](https://github.com/TS13lover1989)<br/>*(ID: 51993686)* | [`@HoKhangIT`](https://github.com/HoKhangIT)<br/>*(ID: 166229288)* | [`@vongocminhdat`](https://github.com/vongocminhdat)<br/>*(ID: 237451259)* |
| **2. Feature Branch Verified** | `feature/web-duc` | `feature/android-tri-khang` | `feature/api-ho-doan-khang` | `feature/winforms-minh-dat` |
| **3. Real Source Changes** | Frontend Footer, multi-platform test sync, release docs | `ApiErrorParser.java`, lifecycle checks, 15 unit tests | `AuthorizationRegressionTests.cs` (4 security tests) | `ApiClient.cs` DI & async, `ApiException.cs`, 21 unit tests |
| **4. Member Commit SHAs** | [`b6abe8f`](https://github.com/lovemvaf/visionary-api/commit/b6abe8f), [`50ab878`](https://github.com/lovemvaf/visionary-api/commit/50ab878), [`cbd7cb2`](https://github.com/lovemvaf/visionary-api/commit/cbd7cb2) | [`80b0f20`](https://github.com/lovemvaf/visionary-api/commit/80b0f20) | [`fd6df2d`](https://github.com/lovemvaf/visionary-api/commit/fd6df2d), [`7efdd02`](https://github.com/lovemvaf/visionary-api/commit/7efdd02), [`6a65334`](https://github.com/lovemvaf/visionary-api/commit/6a65334), [`660fb4d`](https://github.com/lovemvaf/visionary-api/commit/660fb4d), [`0a16a04`](https://github.com/lovemvaf/visionary-api/commit/0a16a04) | [`71a2ae1`](https://github.com/lovemvaf/visionary-api/commit/71a2ae1) |
| **5. Author Linked to Account** | **YES (Verified)** | **YES (Verified)** | **YES (Verified via GitHub API)** | **YES (Verified)** |
| **6. Pull Request Formally Created** | Lead direct branch | [PR #3](https://github.com/lovemvaf/visionary-api/pull/3) | [PR #2](https://github.com/lovemvaf/visionary-api/pull/2), [PR #5](https://github.com/lovemvaf/visionary-api/pull/5), [PR #7](https://github.com/lovemvaf/visionary-api/pull/7) | [PR #1](https://github.com/lovemvaf/visionary-api/pull/1) |
| **7. Code Review Completed** | **APPROVED** | **APPROVED** | **APPROVED** | **APPROVED** |
| **8. Required CI Passed** | Frontend CI #40320066206 **PASS** | Mobile CI #40319077411 **PASS** | Backend CI #40339904597 **PASS** | Desktop CI #40317635884 **PASS** |
| **9. Merged into `main`** | **INTEGRATED** | **MERGED** ([`0a391fe`](https://github.com/lovemvaf/visionary-api/commit/0a391fe)) | **MERGED** ([`611bc65`](https://github.com/lovemvaf/visionary-api/commit/611bc65), [`45a56b3`](https://github.com/lovemvaf/visionary-api/commit/45a56b3), [`2eb86b2`](https://github.com/lovemvaf/visionary-api/commit/2eb86b2)) | **MERGED** ([`23f9ca1`](https://github.com/lovemvaf/visionary-api/commit/23f9ca1)) |
| **10. Tests Verified Locally & Remote** | 19/19 routes SSG/SSR **PASS** | 15/15 JUnit Tests **PASS** | 19/19 xUnit Tests **PASS** | 21/21 Unit Tests **PASS** |
| **11. Documentation Synced** | **SYNCED** | **SYNCED** | **SYNCED** | **SYNCED** |
| **12. Contributors Visible** | **VISIBLE (36 commits)** | **VISIBLE (1 commit)** | **VISIBLE (5 commits)** | **VISIBLE (1 commit)** |

---

## III. BÁO CÁO CHI TIẾT BA WORKSTREAM & CÁC PULL REQUEST (B. THREE PULL REQUESTS)

### 1. Pull Request #1: Desktop Windows Forms C# (.NET 8)
- **PR URL:** [https://github.com/lovemvaf/visionary-api/pull/1](https://github.com/lovemvaf/visionary-api/pull/1)
- **Nhánh:** `feature/winforms-minh-dat` ➔ `main`
- **Tác giả:** Võ Ngọc Minh Đạt ([`@vongocminhdat`](https://github.com/vongocminhdat))
- **Commit gốc:** [`71a2ae1`](https://github.com/lovemvaf/visionary-api/commit/71a2ae1) (`fix(desktop): improve WinForms reliability, error handling, cancellation, and unit test coverage`)
- **Nội dung kỹ thuật (15 files modified, 1258 insertions(+), 258 deletions(-)):**
  - Tái cấu trúc toàn diện `ApiClient.cs`: Chuyển đổi từ static methods sang mô hình instance với `HttpClient` được inject qua DI container, bổ sung tham số `CancellationToken cancellationToken = default` trên toàn bộ 15 phương thức API, sử dụng `.ConfigureAwait(false)` trên tất cả các tác vụ bất đồng bộ nhằm loại trừ triệt để nguy cơ Deadlock trên luồng UI thread của WinForms.
  - Xây dựng lớp ngoại lệ `ApiException.cs`: Đóng gói `StatusCode`, `ServerErrors`, `RawBody` hỗ trợ phân biệt mã 401 Unauthorized (phiên đăng nhập hết hạn), 403 Forbidden, 404 Not Found và lỗi mạng.
  - Cập nhật Form nghiệp vụ (`LoginForm.cs`, `MainForm.cs`): Tích hợp `CancellationTokenSource`, vô hiệu hóa nút bấm và hiển thị ProgressBar trong khi gọi mạng, tự động hủy request khi người dùng đóng Form.
  - Bổ sung bộ kiểm thử 21 Unit Tests (`desktop/Visionary.Desktop.Tests/`): Dùng `StubHttpMessageHandler` để kiểm thử giả lập các kịch bản mạng: thành công, mã hóa URL tiếng Việt, hết hạn token, timeout và hủy yêu cầu.
  - Tích hợp `Visionary.Desktop.Tests.csproj` vào solution tổng thể `backend/Visionary.Backend.sln`.
- **CI Workflows:**
  - `Desktop CI - Windows Forms (.NET 8)`: Run ID `#40317635884` ➔ **SUCCESS**.
  - `Security Audit & Supply Chain Hardening`: Run ID `#40317635872` ➔ **SUCCESS**.
- **Merge SHA:** [`23f9ca1`](https://github.com/lovemvaf/visionary-api/commit/23f9ca1) (Merge commit, bảo toàn tác giả `Vo Ngoc Minh Dat <vongocminhdat@gmail.com>`).

### 2. Pull Request #2, #5, #7: Backend ASP.NET Core Web API (.NET 8)
- **PR URLs:**
  - [PR #2](https://github.com/lovemvaf/visionary-api/pull/2) ➔ Merge Commit [`611bc65`](https://github.com/lovemvaf/visionary-api/commit/611bc65)
  - [PR #5](https://github.com/lovemvaf/visionary-api/pull/5) ➔ Merge Commit [`45a56b3`](https://github.com/lovemvaf/visionary-api/commit/45a56b3)
  - [PR #7](https://github.com/lovemvaf/visionary-api/pull/7) ➔ Merge Commit [`2eb86b2`](https://github.com/lovemvaf/visionary-api/commit/2eb86b2)
- **Nhánh:** `feature/api-ho-doan-khang` ➔ `main`
- **Tác giả:** Hồ Đoàn Nguyên Khang ([`@HoKhangIT`](https://github.com/HoKhangIT))
- **Commit gốc:** [`fd6df2d`](https://github.com/lovemvaf/visionary-api/commit/fd6df2d), [`7efdd02`](https://github.com/lovemvaf/visionary-api/commit/7efdd02), [`6a65334`](https://github.com/lovemvaf/visionary-api/commit/6a65334), [`660fb4d`](https://github.com/lovemvaf/visionary-api/commit/660fb4d), [`0a16a04`](https://github.com/lovemvaf/visionary-api/commit/0a16a04)
- **Nội dung kỹ thuật:**
  - Bổ sung file `backend/tests/Visionary.Tests/AuthorizationRegressionTests.cs` với 4 ca kiểm thử bảo mật nâng cao:
    1. `AdminUsers_AnonymousRequest_ReturnsUnauthorized`: Kiểm tra request ẩn danh gọi vào `/api/admin/users` bị chặn với mã HTTP 401 Unauthorized.
    2. `Student_CannotAccessAdminOrGrantSelfAdminRole`: Đăng ký tài khoản Sinh viên mới, kiểm tra quyền mặc định `Student`, gọi `/api/admin/users` nhận 403 Forbidden, thử tự đổi role thành Admin nhận 403 Forbidden, bảo đảm chống leo quyền triệt để.
    3. `AdminUsers_ExpiredBearerToken_ReturnsUnauthorized`: Kiểm tra token JWT có chữ ký hợp lệ nhưng đã quá hạn (`DateTime.UtcNow.AddMinutes(-5)`) gọi vào `/api/admin/users` bị từ chối 401 Unauthorized.
    4. `AdminUsers_MalformedBearerToken_ReturnsUnauthorized`: Kiểm tra Authorization header chứa chuỗi rác (`not-a-valid-jwt`) bị từ chối 401 Unauthorized, không gây crash API.
  - Nâng tổng quy mô kiểm thử tự động của Backend từ 15 lên **19 bài test xUnit** (100% Passed).
- **CI Workflows:**
  - `Backend CI - ASP.NET Core 8 Web API`: Run ID `#40339904597` ➔ **SUCCESS** (19/19 tests passed).
  - `Security Audit & Supply Chain Hardening`: Run ID `#40345219844` ➔ **SUCCESS**.
- **Merge SHAs:** [`611bc65`](https://github.com/lovemvaf/visionary-api/commit/611bc65), [`45a56b3`](https://github.com/lovemvaf/visionary-api/commit/45a56b3), [`2eb86b2`](https://github.com/lovemvaf/visionary-api/commit/2eb86b2) (Bảo toàn tác giả Hồ Đoàn Nguyên Khang).

### 3. Pull Request #3: Mobile Android Native Java
- **PR URL:** [https://github.com/lovemvaf/visionary-api/pull/3](https://github.com/lovemvaf/visionary-api/pull/3)
- **Nhánh:** `feature/android-tri-khang` ➔ `main`
- **Tác giả:** Đào Trí Khang ([`@TS13lover1989`](https://github.com/TS13lover1989))
- **Commit gốc:** [`80b0f20`](https://github.com/lovemvaf/visionary-api/commit/80b0f20) (`test(android): improve mobile API reliability, contract parsing, and lifecycle error handling`)
- **Nội dung kỹ thuật (15 files modified, 570 insertions(+), 47 deletions(-)):**
  - Xây dựng `ApiErrorParser.java`: Bóc tách thông báo lỗi chuẩn RFC 7807 Problem Details từ phản hồi HTTP error của ASP.NET Core, ánh xạ các mã lỗi mạng `SocketTimeoutException`, `UnknownHostException` sang tiếng Việt rõ ràng, thân thiện với người dùng.
  - Tăng cường an toàn dữ liệu trong `ApiResponse.java` và `PagedResponse.java`: Thêm phương thức `getSafeItems()` phòng chống `NullPointerException`, bổ sung getter `getFirstError()`.
  - Cập nhật Fragment Lifecycle (`EnglishForItFragment`, `EventsFragment`, `OpportunitiesFragment`): Bổ sung kiểm tra `if (!isAdded() || getContext() == null) return;` trước khi cập nhật UI từ callback Retrofit để chặn hiện tượng crash khi người dùng chuyển màn hình trong khi request đang bay.
  - Bổ sung bộ 15 Unit Tests: `ApiErrorParserTest` (9 tests), `ApiResponseContractTest` (4 tests), `ContentModelsContractTest` (2 tests).
- **CI Workflows:**
  - `Mobile CI - Android Native Java`: Run ID `#40319077411` ➔ **SUCCESS** (15/15 unit tests passed).
  - `Security Audit & Supply Chain Hardening`: Run ID `#40319077455` ➔ **SUCCESS**.
- **Merge SHA:** [`0a391fe`](https://github.com/lovemvaf/visionary-api/commit/0a391fe) (Merge commit, bảo toàn tác giả `TS13lover1989 <caubekhang1485@gmail.com>`).

---

## IV. TỔNG HỢP KẾT QUẢ KIỂM THỬ TOÀN HỆ THỐNG (D. TESTING AUDIT)

Sau khi tích hợp hoàn tất các Pull Requests lên `main` (`2eb86b2`), toàn bộ hệ thống đã được kiểm thử hồi quy độc lập:

| Nền tảng | Công cụ Kiểm thử | Kết quả Thực tế | Tỷ lệ Đạt | Đánh giá Kỹ thuật |
|---|---|:---:|:---:|---|
| **Backend Web API** | xUnit, .NET 8.0 SDK | **19/19 tests passed** | **100%** | Bao phủ API Health, DTO Seeding, JWT, BCrypt, Posts Logic Invariants (6 tests), và RBAC/Token Security Regression (4 tests). |
| **Desktop Windows Forms** | xUnit, .NET 8.0-windows | **21/21 tests passed** | **100%** | Bao phủ `ApiClient` network handling, status parsing, URL encoding, CancellationToken cancellation, và `AppState` session. |
| **Mobile Android** | JUnit 4, Gradle 8.4, JDK 17 | **15/15 tests passed** | **100%** | Bao phủ `ApiErrorParser` RFC 7807, `ApiResponse` DTO contracts, null-safety, và Content Models deserialization. |
| **Frontend Web** | Next.js 14 App Router, TypeScript | **19/19 routes compiled** | **100%** | Kiểm tra static build (SSG/SSR) và `npx tsc --noEmit` đạt 0 warning, 0 error. |
| **TỔNG CỘNG KIỂM THỬ** | **55 Automated Tests + 19 Routes** | **55/55 PASSED** | **100%** | **HOÀN TOÀN ĐẠT CHUẨN ĐỘ TIN CẬY CAO NHẤT** |

---

## V. KIỂM TOÁN TƯƠNG THÍCH CHÉO NỀN TẢNG (CROSS-PLATFORM INTEGRATION)

Đã đối chiếu trực tiếp dữ liệu giữa 3 nền tảng client với ASP.NET Core 8 Web API:
1. **Hợp đồng Phân trang (`PagedResponse<T>`):**
   - Backend: Trả về `items`, `pageIndex`, `pageSize`, `totalCount`, `totalPages`, `hasNextPage`, `hasPreviousPage`.
   - Android: `PagedResponse.java` giải mã chính xác qua Gson, có `getSafeItems()` phòng ngừa null list.
   - WinForms: `ApiClient.cs` deserialize vào `PagedResponse<T>` đồng nhất.
   - Web: `types.ts` và `api.ts` khớp 100% thuộc tính.
2. **Quy trình Điểm danh & Check-in (`/api/events/{id}/attendance`):**
   - Web, Android và WinForms đều gửi Bearer JWT, truyền `userId` hoặc mã `qrCheckInCode`.
   - Trả về mã phản hồi thành công và thông báo đồng bộ tiếng Việt.
3. **Cơ chế Xử lý Lỗi (RFC 7807):**
   - Cả 3 nền tảng client đều bóc tách đúng thuộc tính `message` và mảng `errors` từ phản hồi của API khi xảy ra lỗi xác thực (400, 401, 403).

---

## VI. BẢO MẬT & SUPPLY CHAIN AUDIT (E. DEVSECOPS & SECURITY AUDIT)

1. **Quét Secret Toàn diện (Zero Credentials Leak):**
   - Đã quét toàn bộ git diff và các file mới: Không có JWT Secret, Supabase Database Password, Cloudflare credentials hay Production Tokens trong mã nguồn.
   - Chỉ có các chuỗi mock kiểm thử cục bộ (`TestPassword@123`, `jwt-token-abc`, `dummy_token`) phục vụ xUnit/JUnit.
2. **Kiểm tra Phân quyền (RBAC Hardening):**
   - Đã kiểm chứng trực tiếp qua 4 ca kiểm thử bảo mật của Hồ Khang: Tài khoản Sinh viên (`Student`) tuyệt đối không thể truy cập tài nguyên Quản trị viên (`/api/admin/users`) hoặc tự sửa đổi quyền hạn của chính mình; token hết hạn và token sai cú pháp đều bị từ chối 401.
3. **Quét Lỗ hổng Thư viện (NuGet Vulnerability Scan):**
   - Đạt 0 lỗ hổng bảo mật trên toàn bộ 4 dự án backend và dự án desktop tests.

---

## VII. ĐỒNG BỘ TÀI LIỆU & HỌC PHẦN TH71108 (F. DOCUMENTATION & ACADEMIC ALIGNMENT)

1. **Đồng bộ Tài liệu Kỹ thuật:**
   - `README.md`: Cập nhật bảng tổng kết 55 bài test tự động trên 3 nền tảng, 4 nhánh phát triển, và liên kết tài liệu.
   - `docs/TEAM_CONTRIBUTIONS.md`: Cập nhật đầy đủ bảng ma trận đóng góp thực tế, commit SHAs, PR numbers, và trạng thái merge của 4 thành viên.
   - `docs/QA_TEST_REPORT.md`: Phân định minh bạch giữa mốc lịch sử 9 bài test, mốc 15 bài test logic bài viết, mốc 17 bài test authorization, và mốc hiện hành 19 bài test backend + 21 desktop tests + 15 android tests (Tổng 55 tests).
   - `project-status/verification.json`: Cập nhật commit SHA `2eb86b2`, run IDs CI và số lượng tests đồng bộ.
   - `scripts/verify_repository.py`: Đạt **ALL 6 QUALITY GATES PASSED!**.
2. **Kiểm tra Tên & Danh tính:**
   - Xác nhận 100% tên thành viên chính xác tuyệt đối: **Hồ Đoàn Nguyên Khang** (đã loại trừ toàn bộ sai sót chính tả trong repository).
3. **Bảo tồn Bộ Hồ sơ Nộp Học phần TH71108:**
   - Thư mục `VISIONARY-ACADEMIC-DELIVERY/` được lưu giữ nguyên vẹn với đầy đủ:
     * Slide PowerPoint: `VISIONARY_TH71108_FINAL_PRESENTATION.pptx` & `.pdf` (16 slides chuẩn).
     * Kịch bản thuyết trình: `VISIONARY_PRESENTATION_SCRIPT.docx` & `.pdf` (15 phút chuẩn: Đức 2m45s, Trí Khang 3m15s, Hồ Khang 4m15s, Đạt 4m45s).
     * 4 bộ Member Guides cho từng thành viên: Đức (Dễ nhất/Mở đầu), Trí Khang (Android), Hồ Khang (API), Đạt (WinForms/Kết thúc).
     * Bộ hỏi đáp phản biện: `VISIONARY_TH71108_FULL_QA_AND_TEST_GUIDE.docx` & `.pdf`.

---

## VIII. KIỂM TRA MÔI TRƯỜNG PRODUCTION (G. PRODUCTION VERIFICATION)

- **Frontend Production (Vercel Edge):**
  - URL: [https://visionary-platform.vercel.app/](https://visionary-platform.vercel.app/)
  - HTTP Status: **200 OK**
  - Giao diện: Hoạt động mượt mà, chân trang (Footer) hiển thị đầy đủ liên kết tới 4 tài khoản GitHub của các kỹ sư.
- **Backend Production (Render Cloud Service):**
  - URL Swagger: [https://visionary-api-gb51.onrender.com/swagger/v1/swagger.json](https://visionary-api-gb51.onrender.com/swagger/v1/swagger.json)
  - HTTP Status: **200 OK**
  - Database: Supabase PostgreSQL 16 (Yêu cầu SSL), dữ liệu ổn định, an toàn.

---

## IX. TRẠNG THÁI GITHUB CONTRIBUTORS (SECTION XII & XVI)

Kết quả truy vấn trực tiếp từ GitHub REST API (`https://api.github.com/repos/lovemvaf/visionary-api/contributors`):
```text
- lovemvaf (User ID: 156913149): 36 commits
- HoKhangIT (User ID: 166229288): 5 commits
- TS13lover1989 (User ID: 51993686): 1 commit
- vongocminhdat (User ID: 237451259): 1 commit
```
**Xác nhận chính thức:** Cả 4 thành viên trong nhóm phát triển đều đã được GitHub nhận diện thành công và hiển thị trực tiếp trên đồ thị Contributors Graph! Không còn trường hợp nào bị thiếu sót hoặc chờ đợi refresh.

---

## X. TỔNG KẾT VẤN ĐỀ VÀ TRẠNG THÁI CUỐI CÙNG (G. STATUS SUMMARY)

| Hạng mục kiểm tra | Trạng thái | Bằng chứng kỹ thuật |
|---|:---:|---|
| **Backend API Build & 19 Tests** | **PASS** | `dotnet test` đạt 19/19 Passed (GitHub Actions Run #40339904597). |
| **Desktop WinForms Build & 21 Tests** | **PASS** | `dotnet test` đạt 21/21 Passed (GitHub Actions Run #40317635884). |
| **Android Native Build & 15 Tests** | **PASS** | Gradle `testDebugUnitTest` đạt 15/15 Passed (GitHub Actions Run #40319077411). |
| **Frontend Next.js Build (19 Routes)** | **PASS** | `npm run build` và `npx tsc --noEmit` đạt 0 warning, 0 error. |
| **Bảo mật & Secrets** | **PASS** | Quét Gitleaks 0 secrets rò rỉ, NuGet 0 lỗ hổng. |
| **Repository Quality Gates (6/6)** | **PASS** | `python scripts/verify_repository.py` thông qua toàn bộ 6/6 cổng chất lượng. |
| **Chính tả Họ tên Hồ Đoàn Nguyên Khang** | **PASS** | 0 trường hợp sai chính tả trong toàn bộ kho mã nguồn. |
| **GitHub Contributors Graph (4 Thành viên)** | **PASS** | Đầy đủ 4 tài khoản được xác nhận trên API GitHub. |
| **Production Frontend & Backend** | **PASS** | Vercel và Render hoạt động 24/7, HTTP 200 OK. |
| **Bộ Hồ sơ TH71108 (Slide, Kịch bản, Guides)** | **PASS** | Nguyên vẹn trong thư mục `VISIONARY-ACADEMIC-DELIVERY/`. |
| **FAIL / BLOCKED / UNRESOLVED** | **ZERO (0)** | Không có bất kỳ vấn đề nào bị chặn hoặc chưa giải quyết. |
