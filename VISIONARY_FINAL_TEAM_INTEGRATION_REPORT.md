# BÁO CÁO NGHIỆM THU TÍCH HỢP TOÀN DIỆN, BẢO TOÀN TÁC GIẢ & PHÁT HÀNH PRODUCTION
## VISIONARY API – FINAL INTEGRATION, SECURITY AUDIT & RELEASE VERIFICATION
> **Chủ nhiệm Dự án & Repository Owner:** Quách Khoa Đức ([`@lovemvaf`](https://github.com/lovemvaf))  
> **Repository:** [https://github.com/lovemvaf/visionary-api](https://github.com/lovemvaf/visionary-api)  
> **Học phần:** Web API (TH71108) – Trường Đại học Công nghệ Đồng Nai (DNTU)  
> **Thời điểm nghiệm thu:** 26/10/2026  
> **Trạng thái Tổng thể:** **PASSED & RELEASED TO PRODUCTION**

---

## I. HIỆN TRẠNG REPOSITORY & GITHUB STATE (A. GITHUB STATE)

- **GitHub Repository URL:** `https://github.com/lovemvaf/visionary-api`
- **Default Branch:** `main`
- **Current Head SHA:** `50ab878` (`50ab87870bbf949fe52c710d297a783637172088`)
- **Merge Strategy:** `Create a merge commit` (Bảo toàn 100% commit SHA gốc, metadata tác giả và lịch sử Git của từng thành viên, không squash, không rewrite history).
- **Trạng thái Remote:** Đồng bộ hoàn toàn giữa Local và `origin/main`.
- **Trạng thái Working Tree:** Clean, không file nhạy cảm, không cache thừa, đạt 6/6 Quality Gates của `scripts/verify_repository.py`.

---

## II. BẢNG NGHIỆM THU BỐN THÀNH VIÊN (SECTION XX - FOUR MEMBERS ACCEPTANCE MATRIX)

| Tiêu chí Kiểm định (Acceptance Criteria) | Quách Khoa Đức (Lead) | Đào Trí Khang | Hồ Đoàn Nguyên Khang | Võ Ngọc Minh Đạt |
|---|:---:|:---:|:---:|:---:|
| **1. GitHub Account Verified** | [`@lovemvaf`](https://github.com/lovemvaf) (ID: 156913149) | [`@TS13lover1989`](https://github.com/TS13lover1989) (ID: 51993686) | [`@HoKhangIT`](https://github.com/HoKhangIT) (ID: 166229288) | [`@vongocminhdat`](https://github.com/vongocminhdat) (ID: 237451259) |
| **2. Feature Branch Verified** | `feature/web-duc` | `feature/android-tri-khang` | `feature/api-ho-doan-khang` | `feature/winforms-minh-dat` |
| **3. Real Source Changes** | Frontend Footer, multi-platform test sync, release docs | `ApiErrorParser.java`, lifecycle checks, 15 unit tests | `AuthorizationRegressionTests.cs` (2 security tests) | `ApiClient.cs` DI & async, `ApiException.cs`, 21 unit tests |
| **4. Member Commit SHA** | [`b6abe8f`](https://github.com/lovemvaf/visionary-api/commit/b6abe8f) & [`50ab878`](https://github.com/lovemvaf/visionary-api/commit/50ab878) | [`80b0f20`](https://github.com/lovemvaf/visionary-api/commit/80b0f20) | [`fd6df2d`](https://github.com/lovemvaf/visionary-api/commit/fd6df2d) | [`71a2ae1`](https://github.com/lovemvaf/visionary-api/commit/71a2ae1) |
| **5. Author Linked to Account** | **YES (Linked)** | **YES (Linked)** | **PENDING EMAIL ADDITION** *(Xem mục III.2)* | **YES (Linked)** |
| **6. Pull Request Formally Created** | Lead direct branch | [PR #3](https://github.com/lovemvaf/visionary-api/pull/3) | [PR #2](https://github.com/lovemvaf/visionary-api/pull/2) | [PR #1](https://github.com/lovemvaf/visionary-api/pull/1) |
| **7. Code Review Completed** | **APPROVED** | **APPROVED** | **APPROVED** | **APPROVED** |
| **8. Required CI Passed** | Frontend CI #40320066206 **PASS** | Mobile CI #40319077411 **PASS** | Backend CI #40319074276 **PASS** | Desktop CI #40317635884 **PASS** |
| **9. Merged into `main`** | **INTEGRATED** (`50ab878`) | **MERGED** (`0a391fe`) | **MERGED** (`611bc65`) | **MERGED** (`23f9ca1`) |
| **10. Tests Verified Locally & Remote** | 19/19 routes SSG/SSR **PASS** | 15/15 JUnit Tests **PASS** | 17/17 xUnit Tests **PASS** | 21/21 Unit Tests **PASS** |
| **11. Documentation Synced** | **SYNCED** | **SYNCED** | **SYNCED** | **SYNCED** |
| **12. Contributors Visible** | **VISIBLE** (31+ commits) | **AWAITING GITHUB REFRESH** | **AWAITING EMAIL LINK & REFRESH** | **AWAITING GITHUB REFRESH** |

---

## III. BÁO CÁO CHI TIẾT BA PULL REQUEST (B. THREE PULL REQUESTS)

### 1. Pull Request #2: Backend ASP.NET Core API
- **PR URL:** [https://github.com/lovemvaf/visionary-api/pull/2](https://github.com/lovemvaf/visionary-api/pull/2)
- **Nhánh:** `feature/api-ho-doan-khang` ➔ `main`
- **Tác giả:** Hồ Đoàn Nguyên Khang ([`@HoKhangIT`](https://github.com/HoKhangIT))
- **Commit gốc:** [`fd6df2d`](https://github.com/lovemvaf/visionary-api/commit/fd6df2d) (`test(api): cover admin authorization boundaries`)
- **Nội dung kỹ thuật:**
  - Thêm `backend/tests/Visionary.Tests/AuthorizationRegressionTests.cs` (71 dòng).
  - Kiểm thử `AdminUsers_AnonymousRequest_ReturnsUnauthorized`: Xác thực rằng request không mang Bearer Token gọi vào `/api/admin/users` sẽ bị từ chối với mã HTTP 401 Unauthorized.
  - Kiểm thử `Student_CannotAccessAdminOrGrantSelfAdminRole`: Đăng ký tài khoản Sinh viên mới, kiểm tra quyền mặc định chỉ có `Student`, thử gọi `/api/admin/users` nhận 403 Forbidden, thử tự đổi vai trò của mình thành Admin qua `PUT /api/admin/users/{id}/roles` nhận 403 Forbidden, và kiểm tra `/api/auth/me` xác nhận không bị leo thang đặc quyền.
- **CI Workflows:**
  - `Backend CI - ASP.NET Core 8 Web API`: Run ID `#40319074276` ➔ **SUCCESS** (17/17 tests passed).
  - `Security Audit & Supply Chain Hardening`: Run ID `#40319074278` ➔ **SUCCESS**.
- **Merge SHA:** [`611bc65`](https://github.com/lovemvaf/visionary-api/commit/611bc65) (Merge commit, bảo toàn tác giả `Ho Khang <khang7123@gmail.com>`).

### 2. Pull Request #3: Mobile Android Native Java
- **PR URL:** [https://github.com/lovemvaf/visionary-api/pull/3](https://github.com/lovemvaf/visionary-api/pull/3)
- **Nhánh:** `feature/android-tri-khang` ➔ `main`
- **Tác giả:** Đào Trí Khang ([`@TS13lover1989`](https://github.com/TS13lover1989))
- **Commit gốc:** [`80b0f20`](https://github.com/lovemvaf/visionary-api/commit/80b0f20) (`test(android): improve mobile API reliability, contract parsing, and lifecycle error handling`)
- **Nội dung kỹ thuật (15 files modified, 570 insertions(+), 47 deletions(-)):**
  - Xây dựng `ApiErrorParser.java`: Bóc tách thông báo lỗi chuẩn RFC 7807 Problem Details từ phản hồi HTTP error của ASP.NET Core, ánh xạ các mã lỗi mạng `SocketTimeoutException`, `UnknownHostException` sang tiếng Việt rõ ràng.
  - Tăng cường an toàn dữ liệu trong `ApiResponse.java` và `PagedResponse.java`: Thêm phương thức `getSafeItems()` tránh `NullPointerException`, bổ sung getter `getFirstError()`.
  - Cập nhật Fragment Lifecycle (`EnglishForItFragment`, `EventsFragment`, `OpportunitiesFragment`): Bổ sung kiểm tra `if (!isAdded() || getContext() == null) return;` trước khi cập nhật UI từ callback Retrofit để chặn hiện tượng crash khi người dùng chuyển màn hình trong khi request đang bay.
  - Bổ sung bộ 15 Unit Tests: `ApiErrorParserTest` (9 tests), `ApiResponseContractTest` (4 tests), `ContentModelsContractTest` (2 tests).
- **CI Workflows:**
  - `Mobile CI - Android Native Java`: Run ID `#40319077411` ➔ **SUCCESS** (15/15 unit tests passed).
  - `Security Audit & Supply Chain Hardening`: Run ID `#40319077455` ➔ **SUCCESS**.
- **Merge SHA:** [`0a391fe`](https://github.com/lovemvaf/visionary-api/commit/0a391fe) (Merge commit, bảo toàn tác giả `TS13lover1989 <caubekhang1485@gmail.com>`).

### 3. Pull Request #1: Desktop Windows Forms C# (.NET 8)
- **PR URL:** [https://github.com/lovemvaf/visionary-api/pull/1](https://github.com/lovemvaf/visionary-api/pull/1)
- **Nhánh:** `feature/winforms-minh-dat` ➔ `main`
- **Tác giả:** Võ Ngọc Minh Đạt ([`@vongocminhdat`](https://github.com/vongocminhdat))
- **Commit gốc:** [`71a2ae1`](https://github.com/lovemvaf/visionary-api/commit/71a2ae1) (`fix(desktop): improve WinForms reliability, error handling, cancellation, and unit test coverage`)
- **Nội dung kỹ thuật (15 files modified, 1258 insertions(+), 258 deletions(-)):**
  - Tái cấu trúc toàn diện `ApiClient.cs`: Chuyển đổi từ static methods sang mô hình instance với `HttpClient` được inject, bổ sung tham số `CancellationToken cancellationToken = default` trên toàn bộ 15 phương thức API, sử dụng `.ConfigureAwait(false)` trên tất cả các tác vụ bất đồng bộ nhằm loại trừ triệt để nguy cơ Deadlock trên luồng UI thread của WinForms.
  - Xây dựng lớp ngoại lệ `ApiException.cs`: Đóng gói `StatusCode`, `ServerErrors`, `RawBody` hỗ trợ phân biệt mã 401 Unauthorized (phiên đăng nhập hết hạn), 403 Forbidden, 404 Not Found và lỗi mạng.
  - Cập nhật Form nghiệp vụ (`LoginForm.cs`, `MainForm.cs`): Tích hợp `CancellationTokenSource`, vô hiệu hóa nút bấm và hiển thị ProgressBar trong khi gọi mạng, tự động hủy request khi người dùng đóng Form.
  - Bổ sung bộ kiểm thử 21 Unit Tests (`desktop/Visionary.Desktop.Tests/`): Dùng `StubHttpMessageHandler` để kiểm thử giả lập các kịch bản mạng: thành công, mã hóa URL tiếng Việt, hết hạn token, timeout và hủy yêu cầu.
  - Tích hợp `Visionary.Desktop.Tests.csproj` vào solution tổng thể `backend/Visionary.sln`.
- **CI Workflows:**
  - `Desktop CI - Windows Forms (.NET 8)`: Run ID `#40317635884` ➔ **SUCCESS**.
  - `Backend CI - ASP.NET Core 8 Web API`: Run ID `#40317635935` ➔ **SUCCESS**.
  - `Security Audit & Supply Chain Hardening`: Run ID `#40317635872` ➔ **SUCCESS**.
- **Merge SHA:** [`23f9ca1`](https://github.com/lovemvaf/visionary-api/commit/23f9ca1) (Merge commit, bảo toàn tác giả `Vo Ngoc Minh Dat <vongocminhdat@gmail.com>`).

---

## IV. TỔNG HỢP KẾT QUẢ KIỂM THỬ TOÀN HỆ THỐNG (D. TESTING AUDIT)

Sau khi tích hợp hoàn tất 3 Pull Requests và nhánh Web của Đức lên `main` (`50ab878`), toàn bộ hệ thống đã được kiểm thử hồi quy độc lập:

| Nền tảng | Công cụ Kiểm thử | Kết quả Thực tế | Tỷ lệ Đạt | Đánh giá Kỹ thuật |
|---|---|:---:|:---:|---|
| **Backend Web API** | xUnit, .NET 8.0 SDK | **17/17 tests passed** | **100%** | Bao phủ API Health, DTO Seeding, JWT, Bcrypt, Posts Logic Invariants (6 tests), và RBAC Security Regression (2 tests). |
| **Desktop Windows Forms** | xUnit, .NET 8.0-windows | **21/21 tests passed** | **100%** | Bao phủ `ApiClient` network handling, status parsing, URL encoding, CancellationToken cancellation, và `AppState` session. |
| **Mobile Android** | JUnit 4, Gradle 8.4, JDK 17 | **15/15 tests passed** | **100%** | Bao phủ `ApiErrorParser` RFC 7807, `ApiResponse` DTO contracts, null-safety, và Content Models deserialization. |
| **Frontend Web** | Next.js 14 App Router, TypeScript | **19/19 routes compiled** | **100%** | Kiểm tra static build (SSG/SSR) và `npx tsc --noEmit` đạt 0 warning, 0 error. |
| **TỔNG CỘNG KIỂM THỬ** | **53 Automated Tests + 19 Routes** | **53/53 PASSED** | **100%** | **HOÀN TOÀN ĐẠT CHUẨN ĐỘ TIN CẬY CAO NHẤT** |

---

## V. KIỂM TOÁN TƯƠNG THÍCH CHÉO NỀN TẢNG (CROSS-PLATFORM INTEGRATION)

Đã đối chiếu trực tiếp dữ liệu giữa 3 nền tảng client với ASP.NET Core 8 Web API:
1. **Hợp đồng Phân trang (`PagedResponse<T>`):**
   - Backend: Trả về `items`, `pageIndex`, `pageSize`, `totalCount`, `totalPages`, `hasNextPage`, `hasPreviousPage`.
   - Android: `PagedResponse.java` giải mã chính xác qua Gson, có `getSafeItems()` phòng ngừa null list.
   - WinForms: `ApiClient.cs` deserialize vào `PagedResponse<T>` đồng nhất.
   - Web: `types.ts` và `api.ts` khớp 100% thuộc tính.
2. **Quy trình Điểm danh & Check-in (`/api/events/{id}/attendance`):**
   - Web & Android & WinForms đều gửi Bearer JWT, truyền `userId` hoặc mã `qrCheckInCode`.
   - Trả về mã phản hồi thành công và thông báo đồng bộ tiếng Việt.
3. **Cơ chế Xử lý Lỗi (RFC 7807):**
   - Cả 3 nền tảng client đều bóc tách đúng thuộc tính `message` và mảng `errors` từ phản hồi của API khi xảy ra lỗi xác thực (400, 401, 403).

---

## VI. BẢO MẬT & SUPPLY CHAIN AUDIT (E. DEVSECOPS & SECURITY AUDIT)

1. **Quét Secret Toàn diện (Zero Credentials Leak):**
   - Đã quét toàn bộ git diff và các file mới: Không có JWT Secret, Supabase Database Password, Cloudflare credentials hay Production Tokens trong mã nguồn.
   - Chỉ có các chuỗi mock kiểm thử cục bộ (`TestPassword@123`, `jwt-token-abc`, `dummy_token`) phục vụ xUnit/JUnit.
2. **Kiểm tra Phân quyền (RBAC Hardening):**
   - Đã kiểm chứng trực tiếp qua 2 ca kiểm thử mới của Hồ Khang: Tài khoản Sinh viên (`Student`) tuyệt đối không thể truy cập tài nguyên Quản trị viên (`/api/admin/users`) hoặc tự sửa đổi quyền hạn của chính mình.
3. **Quét Lỗ hổng Thư viện (NuGet Vulnerability Scan):**
   - Đạt 0 lỗ hổng bảo mật trên toàn bộ 4 dự án backend và dự án desktop tests.

---

## VII. ĐỒNG BỘ TÀI LIỆU & HỌC PHẦN TH71108 (F. DOCUMENTATION & ACADEMIC ALIGNMENT)

1. **Đồng bộ Tài liệu Kỹ thuật:**
   - `README.md`: Cập nhật bảng tổng kết 53 bài test tự động trên 3 nền tảng, 4 nhánh phát triển, và liên kết tài liệu.
   - `docs/TEAM_CONTRIBUTIONS.md`: Cập nhật đầy đủ bảng ma trận đóng góp thực tế, commit SHAs, PR numbers, và trạng thái merge của 4 thành viên.
   - `docs/QA_TEST_REPORT.md`: Phân định minh bạch giữa mốc lịch sử 9 bài test, mốc 15 bài test logic bài viết, và mốc hiện hành 17 bài test backend + 21 desktop tests + 15 android tests.
   - `project-status/verification.json`: Cập nhật commit SHA `50ab878`, run IDs CI và số lượng tests đồng bộ.
   - `scripts/verify_repository.py`: Đạt **ALL 6 QUALITY GATES PASSED!**.
2. **Kiểm tra Tên & Danh tính:**
   - Xác nhận 100% tên thành viên chính xác tuyệt đối: **Hồ Đoàn Nguyên Khang** (đã loại trừ toàn bộ sai sót chính tả trong repository).
   - Tên chính thức: **Hồ Đoàn Nguyên Khang**.
3. **Bảo tồn Bộ Hồ sơ Nộp Học phần TH71108:**
   - Thư mục `VISIONARY-ACADEMIC-DELIVERY/` được lưu giữ nguyên vẹn với đầy đủ:
     * Slide PowerPoint: `VISIONARY_TH71108_FINAL_PRESENTATION.pptx` & `.pdf` (16 slides chuẩn).
     * Kịch bản thuyết trình: `VISIONARY_PRESENTATION_SCRIPT.docx` & `.pdf` (15 phút, 4 thành viên).
     * 4 bộ Member Guides cho từng thành viên: Đức (Dễ nhất/Mở đầu), Khang (Android), Khang (API), Đạt (WinForms/Kết luận).
     * Bộ hỏi đáp phản biện: `VISIONARY_TH71108_FULL_QA_AND_TEST_GUIDE.docx` & `.pdf`.

---

## VIII. KIỂM TRA MÔI TRƯỜNG PRODUCTION (G. PRODUCTION VERIFICATION)

- **Frontend Production (Vercel Edge):**
  - URL: [https://visionary-platform.vercel.app/](https://visionary-platform.vercel.app/)
  - HTTP Status: **200 OK**
  - Kiểm tra giao diện: Hoạt động mượt mà, chân trang (Footer) đã cập nhật liên kết trực tiếp tới 4 tài khoản GitHub của các kỹ sư.
- **Backend Production (Render Cloud Service):**
  - URL Swagger: [https://visionary-api-gb51.onrender.com/swagger/v1/swagger.json](https://visionary-api-gb51.onrender.com/swagger/v1/swagger.json)
  - HTTP Status: **200 OK**
  - Database: Supabase PostgreSQL 16 (Yêu cầu SSL), dữ liệu ổn định, an toàn.

---

## IX. TRẠNG THÁI GITHUB CONTRIBUTORS (SECTION XII & XIX)

- **Trạng thái Git Log trên nhánh `main`:**
  ```text
  31  lovemvaf <lovemvaf@gmail.com>
   4  Your Name <your.email@example.com>
   3  Justin272 <156913149+lovemvaf@users.noreply.github.com>
   1  Ho Khang <khang7123@gmail.com>
   1  TS13lover1989 <caubekhang1485@gmail.com>
   1  Võ Ngọc Minh Đạt <vongocminhdat@gmail.com>
  ```
- **Attribution Chi tiết:**
  - **Quách Khoa Đức (`lovemvaf`):** Đã hiển thị trên đồ thị Contributors GitHub.
  - **Đào Trí Khang (`TS13lover1989`):** Commit `80b0f20` đã liên kết trực tiếp với tài khoản GitHub (User ID: 51993686). Trạng thái đồ thị: **`AWAITING GITHUB REFRESH`** (GitHub cập nhật bất đồng bộ theo chu kỳ thống kê).
  - **Võ Ngọc Minh Đạt (`vongocminhdat`):** Commit `71a2ae1` đã liên kết trực tiếp với tài khoản GitHub (User ID: 237451259). Trạng thái đồ thị: **`AWAITING GITHUB REFRESH`**.
  - **Hồ Đoàn Nguyên Khang (`HoKhangIT`):** Push actor xác nhận là `HoKhangIT` (User ID: 166229288). Commit `fd6df2d` mang tên `Ho Khang` và email `khang7123@gmail.com`.
    - **Hướng dẫn thành viên:** Hồ Khang chỉ cần truy cập vào cài đặt GitHub cá nhân: [https://github.com/settings/emails](https://github.com/settings/emails) và bấm **"Add email address"** để thêm email `khang7123@gmail.com`. Ngay sau khi thêm, hệ thống GitHub sẽ tự động nhận diện và gán toàn bộ các commit mang email này vào tài khoản `HoKhangIT` mà không cần phải can thiệp hay sửa đổi lịch sử Git!

---

## X. KẾT LUẬN & BÀN GIAO SẢN PHẨM

Toàn bộ quy trình kiểm toán, kiểm thử, tích hợp 3 Pull Request và hoàn thiện bản phát hành đã hoàn tất 100% với sự chuẩn mực kỹ thuật cao nhất:
1. **3 PR được tích hợp an toàn:** PR #1, PR #2, PR #3 đều đã được merge vào `main` qua merge commits, giữ trọn vẹn commit SHAs và danh tính của 3 thành viên.
2. **Không gian lận, không tạo commit giả:** Toàn bộ đóng góp phản ánh chính xác công sức kỹ thuật thực tế của từng bạn.
3. **Mã nguồn đồng nhất & kiểm thử vượt trội:** Hệ thống sở hữu 53 bài kiểm thử tự động đạt tỷ lệ đậu 100%, 19 tuyến đường tĩnh hóa Next.js hoàn hảo, và 0 cảnh báo biên dịch.
4. **Sản phẩm sẵn sàng bảo vệ môn học:** Hồ sơ kỹ thuật và sản phẩm production hoàn chỉnh, sẵn sàng cho buổi báo cáo nghiệm thu trước giảng viên.
