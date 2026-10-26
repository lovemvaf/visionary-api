# BÁO CÁO NGHIỆM THU TỔNG THỂ & MỨC ĐỘ SẴN SÀNG BẢO VỆ ĐỒ ÁN
## HỌC PHẦN WEB API (TH71108) – TRƯỜNG ĐẠI HỌC CÔNG NGHỆ ĐỒNG NAI (DNTU)

**Đề tài:** VISIONARY – Hệ thống Quản lý Hoạt động Hội nhập  
**Nhóm sinh viên thực hiện:** VISIONARY API  
1. **Quách Khoa Đức** (MSSV: 1923040025) – Trưởng nhóm / Kiến trúc hệ thống & Web Client Next.js 14  
2. **Đào Trí Khang** (MSSV: 1923040156) – Thành viên / Mobile Software Engineer (Android Native Java)  
3. **Hồ Đoàn Nguyên Khang** (MSSV: 1923040112) – Thành viên / Web API Engineer, Swagger, JWT & Database  
4. **Võ Ngọc Minh Đạt** (MSSV: 1923040088) – Thành viên / Windows Forms Desktop, Quản lý Sự cố CI & Tổng kết  

**Ngày nghiệm thu:** 26/10/2026  
**Repository GitHub:** [https://github.com/lovemvaf/visionary-api](https://github.com/lovemvaf/visionary-api)  
**Website Production:** [https://visionary-platform.vercel.app/](https://visionary-platform.vercel.app/)  
**Backend API Live:** [https://visionary-api-gb51.onrender.com](https://visionary-api-gb51.onrender.com) | [Swagger UI](https://visionary-api-gb51.onrender.com/swagger)  

---

## 1. PHÂN LOẠI TRẠNG THÁI NGHIỆM THU HỆ THỐNG

Tuân thủ nghiêm ngặt nguyên tắc trung thực học thuật và phân loại kỹ thuật khách quan:

| Hạng mục | Trạng thái kỹ thuật | Bằng chứng thực tế / Cơ chế kiểm chứng |
| :--- | :---: | :--- |
| **Sự cố Backend CI #12 (2 tests fail)** | **FIXED AND VERIFIED** | Commit `c7af080`, GitHub Actions Run `#40231783994` SUCCESS (15/15 tests Passed trên Ubuntu Linux x64). |
| **Lỗi SQLite Concurrency & Table Exists** | **FIXED AND VERIFIED** | Thêm khóa `SemaphoreSlim(1,1)` trong `DbInitializer.SeedAsync()`, kiểm tra `HasTablesAsync()`, tạo `CustomWebApplicationFactory`. |
| **Bài test Search (PostsLogicAuditTests)** | **FIXED AND VERIFIED** | Seed hoàn tất, truy vấn `search=Clean Architecture` tìm thấy bài viết chính xác (`TotalCount >= 1`). |
| **Bài test GetPostBySlug (PostsLogicAuditTests)**| **FIXED AND VERIFIED** | Seed bài viết `chao-mung-he-sinh-thai-visionary-2026` đầy đủ, trả về `HTTP 200 OK` và tăng `ViewCount`. |
| **Slide Thuyết trình PowerPoint (.pptx & .pdf)** | **FIXED AND VERIFIED** | 16 slide chuẩn 16:9, bảng màu Academic Navy/Blue/Teal, đầy đủ 2 logo DNTU & CNTT, không lỗi tràn khung. |
| **5 Sơ đồ kỹ thuật bắt buộc** | **FIXED AND VERIFIED** | Vẽ bằng PowerPoint shapes & connectors: Kiến trúc (Slide 3), Android Threading (Slide 6), Chu trình 6 chặng (Slide 9), JWT (Slide 10), Sự cố CI (Slide 15). |
| **Kịch bản Thuyết trình 15 phút (.docx & .pdf)** | **FIXED AND VERIFIED** | Căn chuẩn thời gian: Đức (2m45s) -> Trí Khang (3m15s) -> Hồ Khang (4m15s) -> Minh Đạt (4m45s). Đạt kết thúc, không chuyển ngược về Đức. |
| **Ngân hàng câu hỏi Q&A (.docx & .pdf)** | **FIXED AND VERIFIED** | 66 câu hỏi chi tiết bao gồm 18 câu gốc trong PDF thầy + 30 câu source code + 18 câu chuyên sâu về sự cố CI #12. |
| **Hướng dẫn Demo & Swagger (.docx & .pdf)** | **FIXED AND VERIFIED** | Hướng dẫn từng bước thao tác Web, Android, WinForms, tài khoản test an toàn, phương án dự phòng mất mạng. |
| **4 Hướng dẫn thành viên (Member Guides)** | **FIXED AND VERIFIED** | 4 file docx và 4 file pdf riêng biệt được cá nhân hóa cho từng sinh viên, Đức nhận phần dễ nhất. |
| **Ứng dụng Web (Next.js 14 / TypeScript)** | **FIXED AND VERIFIED** | Triển khai trên Vercel, kết nối qua BFF proxy, giao diện responsive, lọc sự kiện và phân trang. |
| **Ứng dụng Windows Forms (C# / .NET 8)** | **FIXED AND VERIFIED** | Đã biên dịch bản Release tại `desktop/Visionary.Desktop/bin/Release/net8.0-windows/`, Singleton HttpClient, async/await. |
| **Ứng dụng Di động Android (Java Native)** | **FIXED AND VERIFIED** | Đã xuất bản `app-debug.apk` (6.4 MB) tại `mobile/VisionaryAndroid/app/build/outputs/apk/debug/`, Retrofit 2 + OkHttp + Gson. |
| **Database PostgreSQL trên Cloud** | **FIXED AND VERIFIED** | PostgreSQL 16 trên Supabase (Singapore), kết nối qua Connection Pooler IPv4 cổng 5432, AsNoTracking(). |

---

## 2. MINH CHỨNG KHẮC PHỤC SỰ CỐ CI RUN #12 -> RUN #40231783994

### 2.1. Hiện tượng ban đầu:
- **Run ID:** `40226894806` (Run #12)
- **Kết quả:** `Total tests: 15. Passed: 13. Failed: 2. Build FAILED. Process completed with exit code 1.`
- **Hai bài kiểm thử thất bại:**
  1. `Search_WithCategory_And_EmptyState_AreAccurate` (dòng 168): `Assert.True() Failure` (TotalCount = 0).
  2. `GetPostBySlug_ValidPublishedPost_Returns200AndIncrementsView` (dòng 183): `HttpRequestException: 404 (Not Found)`.
- **Lỗi hệ thống:** `SQLite Error 19: UNIQUE constraint failed: Roles.Name` và `SQLite Error 1: table "AchievementCategories" already exists`.

### 2.2. Nguyên nhân cốt lõi (Root Cause):
xUnit kích hoạt 2 test class (`PostsLogicAuditTests` và `ApiIntegrationTests`) chạy song song trên runner đa luồng. Cả 2 cùng khởi tạo `WebApplicationFactory<Program>` trỏ vào cùng file `visionary.db`. Xung đột xảy ra khi cả 2 luồng cùng gọi `DbInitializer.SeedAsync()` tại cùng một thời điểm: luồng 2 ném lỗi `UNIQUE constraint failed: Roles.Name` ở dòng 52, làm **hủy ngang chu trình seed** trước khi kịp nạp `PostCategories` và `Posts`. Dẫn đến cơ sở dữ liệu test bị rỗng, search trả về 0 kết quả và slug trả về 404.

### 2.3. Giải pháp hai tầng (Two-Tier Architectural Fix):
1. **Tầng 1 (Codebase Level):**
   - Bổ sung `private static readonly SemaphoreSlim _seedLock = new(1, 1);` trong `DbInitializer.cs`.
   - Bọc toàn bộ thân hàm `SeedAsync()` trong `await _seedLock.WaitAsync()` và `finally { _seedLock.Release(); }`.
   - Kiểm tra `!await databaseCreator.HasTablesAsync()` trước khi phát lệnh tạo bảng.
2. **Tầng 2 (Test Fixture Level):**
   - Xây dựng `CustomWebApplicationFactory.cs` tự động cấp phát file SQLite cô lập `visionary_test_{Guid:N}.db`.
   - Gộp chung toàn bộ integration tests vào `[Collection("IntegrationTests")]` để đồng bộ hóa tài nguyên.

### 2.4. Kết quả kiểm chứng xác thực:
- **Cục bộ (Local):** `dotnet test` 3 lần liên tiếp: **15/15 Passed (100%)** với thời gian 2.8s, 1.0s, 1.0s.
- **Từ xa (Remote CI):**
  - **Commit SHA:** `c7af080`
  - **Run ID:** `40231783994`
  - **Kết luận:** **SUCCESS (All 15 tests passed on Linux runner)**
  - **URL:** [https://github.com/lovemvaf/visionary-api/actions/runs/40231783994](https://github.com/lovemvaf/visionary-api/actions/runs/40231783994)
  - **Security Workflow:** Run ID `40231784031` -> **SUCCESS**.

---

## 3. DANH MỤC CÁC TỆP ĐẦU RA ĐÃ ĐỒNG BỘ HOÀN HẢO

Tất cả các tệp đều được kiểm tra tính khả chuyển, không lỗi layout, không lỗi font và sẵn sàng trình chiếu / nộp bài:

```text
deliverables/
├── VISIONARY_TH71108_FINAL_PRESENTATION.pptx      (Slide PowerPoint 16 slide chính)
├── VISIONARY_TH71108_FINAL_PRESENTATION.pdf       (Bản xuất PDF chất lượng cao)
├── VISIONARY_PRESENTATION_SCRIPT.docx             (Kịch bản 4 thành viên chuẩn 15 phút)
├── VISIONARY_PRESENTATION_SCRIPT.pdf              (Bản PDF kịch bản thuyết trình)
├── VISIONARY_TH71108_FULL_QA_AND_TEST_GUIDE.docx (Bộ 66 câu hỏi & đáp án chuyên sâu)
├── VISIONARY_TH71108_FULL_QA_AND_TEST_GUIDE.pdf  (Bản PDF ngân hàng câu hỏi)
├── VISIONARY_LIVE_DEMO_AND_SWAGGER_TEST_GUIDE.docx (Hướng dẫn demo & test Swagger)
├── VISIONARY_LIVE_DEMO_AND_SWAGGER_TEST_GUIDE.pdf  (Bản PDF hướng dẫn demo)
├── member-guides/
│   ├── 01_QUACH_KHOA_DUC_EASY_PRESENTATION_GUIDE.docx (Hướng dẫn dễ nhất cho Đức)
│   ├── 01_QUACH_KHOA_DUC_EASY_PRESENTATION_GUIDE.pdf
│   ├── 02_DAO_TRI_KHANG_ANDROID_GUIDE.docx            (Hướng dẫn Android cho Trí Khang)
│   ├── 02_DAO_TRI_KHANG_ANDROID_GUIDE.pdf
│   ├── 03_HO_DOAN_NGUYEN_KHANG_API_GUIDE.docx        (Hướng dẫn API cho Hồ Khang)
│   ├── 03_HO_DOAN_NGUYEN_KHANG_API_GUIDE.pdf
│   ├── 04_VO_NGOC_MINH_DAT_WINFORMS_GUIDE.docx        (Hướng dẫn WinForms & CI cho Đạt)
│   └── 04_VO_NGOC_MINH_DAT_WINFORMS_GUIDE.pdf
├── evidence/                                          (17 ảnh chụp bằng chứng thực tế)
└── slide-previews/                                    (16 ảnh PNG render từ PDF)

docs/
├── TH71108_REQUIREMENTS_TRACEABILITY_MATRIX.md   (Ma trận đối chiếu 28 yêu cầu)
├── TH71108_REAL_CI_INCIDENT_REPORT.md            (Hồ sơ chi tiết sự cố CI #12)
└── TH71108_FINAL_READINESS_REPORT.md             (Báo cáo nghiệm thu tổng thể này)
```

---

## 4. CHIẾN THUẬT VÀ PHÂN BỔ THỜI GIAN 15 PHÚT BẢO VỆ

| Thứ tự | Thành viên | Slide phụ trách | Nội dung chính | Thời lượng | Vai trò tâm lý |
| :---: | :--- | :---: | :--- | :---: | :--- |
| **1** | **Quách Khoa Đức** | 1 – 4 | Mở đầu, giới thiệu nhóm, bài toán, mục tiêu, kiến trúc tổng thể một API ba nền tảng, Web Next.js. | **2 phút 45 giây** | **Phần dễ nhất:** Thuộc lòng kịch bản, nói to rõ, tự tin, tạo ấn tượng mở màn tốt cho nhóm. |
| **2** | **Đào Trí Khang** | 5 – 7 | Ứng dụng Android Java Native, điều phối luồng giao diện, mã Retrofit enqueue, demo trực tiếp trên điện thoại. | **3 phút 15 giây** | **Kỹ thuật di động:** Trực quan, thao tác demo mượt mà, nhấn mạnh cơ chế tránh lỗi NetworkOnMainThread. |
| **3** | **Hồ Đoàn Nguyên Khang** | 8 – 11 | Hợp đồng Swagger, chu trình 6 chặng của `GET /api/events`, vòng đời JWT, phân biệt 401 vs 403, thiết kế DTO/EF Core/DB. | **4 phút 15 giây** | **Trọng tâm môn học:** Thể hiện kiến thức vững chắc về RESTful, HTTP headers, Claims-based identity và database. |
| **4** | **Võ Ngọc Minh Đạt** | 12 – 16 | WinForms C#, Singleton HttpClient, demo điểm danh, 3 điểm khác biệt, phân tích sự cố CI Run #12, hạn chế và kết luận. | **4 phút 45 giây** | **Kết thúc quyết định:** Bản lĩnh kỹ thuật, giải thích thuyết phục sự cố thật và tự tin mở lời mời phản biện. |
| **-** | **TỔNG CỘNG** | **16 Slide** | **Toàn bộ bài thuyết trình bao gồm cả 2 phần live demo** | **15 phút 00 giây** | **Không để Đức kết luận; Đạt là người chốt bài.** |

---

## 5. KẾT LUẬN & KIẾN NGHỊ ĐỐI VỚI BUỔI BẢO VỆ

1. **Sản phẩm hoàn toàn có thật:** Mã nguồn chạy trên 3 nền tảng thực tế, gọi về Web API thật trên đám mây, dữ liệu lưu trữ trên PostgreSQL Supabase và có hệ thống kiểm thử tự động xanh trên GitHub Actions.
2. **Khắc phục sự cố trung thực:** Nhóm không che giấu lỗi mà biến sự cố CI Run #12 thành minh chứng sắc bén nhất cho tiêu chí tự sửa lỗi của sinh viên kỹ thuật.
3. **Mọi tiêu chuẩn của giảng viên đều được đối chiếu và đáp ứng trọn vẹn:** Đầy đủ sơ đồ theo shapes, cổng mạng, giao thức, ảnh thật, code dưới 10 dòng, phân vai mạch lạc và tài liệu luyện phản biện toàn diện.
