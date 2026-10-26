# BẢNG ĐẶC TẢ ĐÓNG GÓP NHÓM VÀ BỐN NHÁNH PHÁT TRIỂN (TEAM CONTRIBUTIONS & BRANCHING AUDIT)
> **Dự án:** VISIONARY – English, Technology & Global Integration Platform  
> **Repository:** [https://github.com/lovemvaf/visionary-api](https://github.com/lovemvaf/visionary-api)  
> **Học phần:** Web API (TH71108) – Trường Đại học Công nghệ Đồng Nai (DNTU)  
> **Thời điểm kiểm toán:** 27/10/2026  

---

## 1. NGUYÊN TẮC TRUNG THỰC KỸ THUẬT & MINH BẠCH ATTRIBUTION

Tuân thủ nghiêm ngặt chuẩn mực kỹ thuật và đạo đức nghiên cứu học thuật TH71108:
1. **Không giả mạo tác giả (Zero Faked Attribution):** Tuyệt đối không sử dụng lệnh can thiệp lịch sử (`git commit --amend --author`, `git filter-repo`) để ngụy tạo tác giả cho các commit không có thực hoặc dùng chung một địa chỉ email để mạo nhận hai người khác nhau.
2. **Minh bạch danh tính GitHub:** Toàn bộ 4 kỹ sư đã được xác thực chính thức trên GitHub Contributors Graph của repository (`lovemvaf`, `HoKhangIT`, `TS13lover1989`, `vongocminhdat`).
3. **Công bố sự hỗ trợ của AI (AI Disclosure):** Toàn bộ việc sử dụng trợ lý lập trình Google Antigravity trong việc tăng tốc sinh mã, kiểm toán bảo mật và tạo tài liệu đều được công bố minh bạch; 4 thành viên giữ vai trò thiết kế kiến trúc, phản biện logic, trực tiếp kiểm thử nghiệm thu và thuyết trình bảo vệ trước hội đồng.

---

## 2. MA TRẬN BỐN NHÁNH PHÁT TRIỂN & ĐÓNG GÓP THỰC TẾ (FOUR WORKSTREAMS)

| STT | Thành viên & MSSV | GitHub Account | Nhánh (Branch) | Commit SHA & Nội dung Kỹ thuật | Trạng thái Kiểm thử (QA) | Pull Request & Trạng thái Merge |
|:---:|---|---|---|---|---|---|
| 1 | **Quách Khoa Đức**<br/>(1923040025)<br/>*Team Lead / Web & Integration* | [`@lovemvaf`](https://github.com/lovemvaf) | [`feature/web-duc`](https://github.com/lovemvaf/visionary-api/tree/feature/web-duc) | Commits [`b6abe8f`](https://github.com/lovemvaf/visionary-api/commit/b6abe8f), [`50ab878`](https://github.com/lovemvaf/visionary-api/commit/50ab878), [`cbd7cb2`](https://github.com/lovemvaf/visionary-api/commit/cbd7cb2):<br/>- Tích hợp liên kết GitHub 4 kỹ sư trong `Footer.tsx`.<br/>- Kiểm toán tương thích đa nền tảng, quản lý release.<br/>- Đảm bảo 19/19 routes Next.js tĩnh hóa sạch. | `npm run typecheck` **PASS**<br/>`npm run build` **19/19 routes PASS** | Nhánh Lead / Tích hợp trực tiếp lên `main` |
| 2 | **Hồ Đoàn Nguyên Khang**<br/>(1923040112)<br/>*ASP.NET Core API Engineer* | [`@HoKhangIT`](https://github.com/HoKhangIT) | [`feature/api-ho-doan-khang`](https://github.com/lovemvaf/visionary-api/tree/feature/api-ho-doan-khang) | Commits [`fd6df2d`](https://github.com/lovemvaf/visionary-api/commit/fd6df2d), [`7efdd02`](https://github.com/lovemvaf/visionary-api/commit/7efdd02), [`6a65334`](https://github.com/lovemvaf/visionary-api/commit/6a65334), [`660fb4d`](https://github.com/lovemvaf/visionary-api/commit/660fb4d), [`0a16a04`](https://github.com/lovemvaf/visionary-api/commit/0a16a04):<br/>- Bổ sung `AuthorizationRegressionTests.cs` (4 security tests).<br/>- Kiểm thử chống rò rỉ quyền Admin, chặn tự cấp quyền, từ chối token hết hạn và token sai cấu trúc.<br/>- Nâng tổng số test Backend lên 19/19 tests xUnit. | `dotnet test` **19/19 tests PASS (100%)**<br/>Backend CI #40339904597 **PASS** | [PR #2](https://github.com/lovemvaf/visionary-api/pull/2) ([`611bc65`](https://github.com/lovemvaf/visionary-api/commit/611bc65))<br/>[PR #5](https://github.com/lovemvaf/visionary-api/pull/5) ([`45a56b3`](https://github.com/lovemvaf/visionary-api/commit/45a56b3))<br/>[PR #7](https://github.com/lovemvaf/visionary-api/pull/7) ([`2eb86b2`](https://github.com/lovemvaf/visionary-api/commit/2eb86b2))<br/>**TẤT CẢ ĐÃ MERGE VÀO MAIN** |
| 3 | **Đào Trí Khang**<br/>(1923040156)<br/>*Android Java Engineer* | [`@TS13lover1989`](https://github.com/TS13lover1989) | [`feature/android-tri-khang`](https://github.com/lovemvaf/visionary-api/tree/feature/android-tri-khang) | Commit [`80b0f20`](https://github.com/lovemvaf/visionary-api/commit/80b0f20):<br/>- Thêm `ApiErrorParser.java` xử lý lỗi RFC 7807 tiếng Việt.<br/>- Null-safety trong `PagedResponse` & Fragment lifecycle.<br/>- Viết 15 unit tests cho JSON contract & error parser. | Gradle `testDebugUnitTest` **15/15 PASS**<br/>Mobile CI #40319077411 **PASS** | [PR #3](https://github.com/lovemvaf/visionary-api/pull/3)<br/>**MERGED** vào `main` ([`0a391fe`](https://github.com/lovemvaf/visionary-api/commit/0a391fe)) |
| 4 | **Võ Ngọc Minh Đạt**<br/>(1923040088)<br/>*Windows Forms Desktop Engineer* | [`@vongocminhdat`](https://github.com/vongocminhdat) | [`feature/winforms-minh-dat`](https://github.com/lovemvaf/visionary-api/tree/feature/winforms-minh-dat) | Commit [`71a2ae1`](https://github.com/lovemvaf/visionary-api/commit/71a2ae1):<br/>- Tái cấu trúc `ApiClient.cs` dùng DI & `CancellationToken`.<br/>- Tạo `ApiException` với mã trạng thái HTTP chuẩn hóa.<br/>- Viết bộ 21 Unit Tests cho `ApiClient` & `AppState`. | `dotnet test` **21/21 Desktop tests PASS**<br/>Desktop CI #40317635884 **PASS** | [PR #1](https://github.com/lovemvaf/visionary-api/pull/1)<br/>**MERGED** vào `main` ([`23f9ca1`](https://github.com/lovemvaf/visionary-api/commit/23f9ca1)) |

---

## 3. DANH TÍNH GITHUB VÀ HÀNH ĐỘNG KỸ THUẬT (IDENTITY AUDIT)

### 3.1. Hiện trạng Danh tính Đã Xác Minh & Attribution
- **Quách Khoa Đức:** GitHub: [`@lovemvaf`](https://github.com/lovemvaf) (Email: `lovemvaf@gmail.com`) ➔ **VERIFIED OWNER**. Đã có 36 commits ghi nhận trên GitHub API Contributors.
- **Hồ Đoàn Nguyên Khang:** GitHub: [`@HoKhangIT`](https://github.com/HoKhangIT) (User ID: 166229288). ➔ **VERIFIED CONTRIBUTOR**. Đã có 5 commits được liên kết chính thức trên GitHub Contributors Graph thông qua emails đã xác thực (`khang7123@gmail.com`, `khangh7123@gmail.com`). Trực tiếp tạo và merge các PR #5, #6, #7.
- **Đào Trí Khang:** GitHub: [`@TS13lover1989`](https://github.com/TS13lover1989) (Email: `caubekhang1485@gmail.com`) ➔ **VERIFIED CONTRIBUTOR**. Commit [`80b0f20`](https://github.com/lovemvaf/visionary-api/commit/80b0f20) liên kết chính xác với tài khoản GitHub (User ID: 51993686, 1 commit).
- **Võ Ngọc Minh Đạt:** GitHub: [`@vongocminhdat`](https://github.com/vongocminhdat) (Email: `vongocminhdat@gmail.com`) ➔ **VERIFIED CONTRIBUTOR**. Commit [`71a2ae1`](https://github.com/lovemvaf/visionary-api/commit/71a2ae1) liên kết chính xác với tài khoản GitHub (User ID: 237451259, 1 commit).

### 3.2. Quy trình Thực hiện Đóng góp Cá nhân
Mỗi thành viên khi làm việc trên máy của mình thực hiện các bước chuẩn mực:
```powershell
# 1. Clone repository về máy cá nhân
git clone https://github.com/lovemvaf/visionary-api.git
cd visionary-api

# 2. Cấu hình danh tính Git chính xác với email đã đăng ký GitHub
git config --local user.name "Họ và Tên"
git config --local user.email "email_da_dang_ky_github@example.com"

# 3. Chuyển sang nhánh phụ trách
git switch feature/web-duc              # Đối với Quách Khoa Đức
git switch feature/android-tri-khang    # Đối với Đào Trí Khang
git switch feature/api-ho-doan-khang    # Đối với Hồ Đoàn Nguyên Khang
git switch feature/winforms-minh-dat    # Đối với Võ Ngọc Minh Đạt

# 4. Thực hiện chỉnh sửa mã nguồn / kiểm thử và commit bằng chính tài khoản của mình
git add .
git commit -m "feat/fix: mô tả nội dung đóng góp thực tế"
git push origin <tên_nhánh>
```

---

## 4. QUY TRÌNH CODE REVIEW CHÉO VÀ TÍCH HỢP PULL REQUEST (PR WORKFLOW)

Để đảm bảo chất lượng hệ thống, nhóm áp dụng ma trận review chéo trước khi merge:
- **PR 1 (WinForms Desktop):** Tác giả: Võ Ngọc Minh Đạt ➔ Reviewers: Quách Khoa Đức & Hồ Đoàn Nguyên Khang ➔ **MERGED** (`23f9ca1`).
- **PR 2 & PR 5 & PR 7 (ASP.NET Core Web API):** Tác giả: Hồ Đoàn Nguyên Khang ➔ Reviewers: Quách Khoa Đức & Võ Ngọc Minh Đạt ➔ **MERGED** (`611bc65`, `45a56b3`, `2eb86b2`).
- **PR 3 (Android Java):** Tác giả: Đào Trí Khang ➔ Reviewers: Quách Khoa Đức & Hồ Đoàn Nguyên Khang ➔ **MERGED** (`0a391fe`).
- **Web Frontend Next.js 14:** Tác giả: Quách Khoa Đức ➔ Reviewers: Hồ Đoàn Nguyên Khang & Đào Trí Khang ➔ **INTEGRATED ON MAIN** (`50ab878`).

---

## 5. PHÂN CÔNG BÁO CÁO VÀ THUYẾT TRÌNH TH71108 (15 PHÚT)

| Diễn giả | Thời lượng | Nội dung thuyết trình chính | Minh chứng mã nguồn trình chiếu |
|:---:|:---:|---|---|
| **1. Quách Khoa Đức** | **2 phút 45 giây** | - Đặt vấn đề, giới thiệu giải pháp tổng thể VISIONARY (Dễ nhất/Mở đầu).<br/>- Kiến trúc Một Backend – Ba Nền tảng.<br/>- Trực tiếp Demo Website Next.js 14 trên Vercel. | `frontend/src/app/`, `frontend/src/lib/api.ts` |
| **2. Đào Trí Khang** | **3 phút 15 giây** | - Ứng dụng Android Native Java (Material 3).<br/>- Kiến trúc Retrofit 2 + OkHttp 3 gọi RESTful API.<br/>- Tính năng QR Code Check-in & English for IT trên di động. | `VisionaryApiService.java`, `ApiClient.java`, `ApiErrorParser.java` |
| **3. Hồ Đoàn Nguyên Khang** | **4 phút 15 giây** | - Kiến trúc ASP.NET Core 8 Web API, Entity Framework Core.<br/>- Chuẩn hóa OpenAPI / Swagger UI & phân quyền JWT Bearer.<br/>- Báo cáo 19/19 bài test xUnit (Backend CI Pass 100%). | `EventsController.cs`, `AuthorizationRegressionTests.cs`, `ApiIntegrationTests.cs` |
| **4. Võ Ngọc Minh Đạt** | **4 phút 45 giây** | - Phần mềm Windows Forms C# (.NET 8) quản trị CLB (Kết thúc).<br/>- Nghiệp vụ xét duyệt hồ sơ thành viên & mở điểm danh.<br/>- Báo cáo 21 unit tests `ApiClient` và phân tích sự cố kỹ thuật thật. | `MainForm.cs`, `desktop/.../ApiClient.cs`, `ApiClientTests.cs` |
