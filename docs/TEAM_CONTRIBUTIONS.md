# BẢNG ĐẶC TẢ ĐÓNG GÓP NHÓM VÀ BỐN NHÁNH PHÁT TRIỂN (TEAM CONTRIBUTIONS & BRANCHING AUDIT)
> **Dự án:** VISIONARY – English, Technology & Global Integration Platform  
> **Repository:** [https://github.com/lovemvaf/visionary-api](https://github.com/lovemvaf/visionary-api)  
> **Học phần:** Web API (TH71108) – Trường Đại học Công nghệ Đồng Nai (DNTU)  
> **Thời điểm kiểm toán:** 26/10/2026  

---

## 1. NGUYÊN TẮC TRUNG THỰC KỸ THUẬT & MINH BẠCH ATTRIBUTION

Tuân thủ nghiêm ngặt chuẩn mực kỹ thuật và đạo đức nghiên cứu học thuật TH71108:
1. **Không giả mạo tác giả (Zero Faked Attribution):** Tuyệt đối không sử dụng lệnh can thiệp lịch sử (`git commit --amend --author`, `git filter-repo`) để ngụy tạo tác giả cho các commit không có thực hoặc dùng chung một địa chỉ email để mạo nhận hai người khác nhau.
2. **Minh bạch danh tính GitHub:** Báo cáo công khai hiện trạng tài khoản GitHub của 4 kỹ sư; các thành viên chưa xác nhận username độc lập được gắn nhãn `IDENTITY_VERIFICATION_REQUIRED` rõ ràng.
3. **Công bố sự hỗ trợ của AI (AI Disclosure):** Toàn bộ việc sử dụng trợ lý lập trình Google Antigravity trong việc tăng tốc sinh mã, kiểm toán bảo mật và tạo tài liệu đều được công bố minh bạch; 4 thành viên giữ vai trò thiết kế kiến trúc, phản biện logic, trực tiếp kiểm thử nghiệm thu và thuyết trình bảo vệ trước hội đồng.

---

## 2. MA TRẬN BỐN NHÁNH PHÁT TRIỂN & ĐÓNG GÓP THỰC TẾ (FOUR WORKSTREAMS)

| STT | Thành viên & MSSV | Nhánh Phát triển (Branch) | Commit SHA & Nội dung Kỹ thuật | Trạng thái Kiểm thử (QA) | Pull Request URL |
|:---:|---|---|---|---|---|
| 1 | **Quách Khoa Đức**<br/>(1923040025)<br/>*Team Lead / Web Client* | [`feature/web-duc`](https://github.com/lovemvaf/visionary-api/tree/feature/web-duc) | Commit [`6a0f4ba`](https://github.com/lovemvaf/visionary-api/commit/6a0f4ba):<br/>- Bổ sung lệnh `typecheck` (`tsc --noEmit`) vào `frontend/package.json`.<br/>- Kiểm tra Next.js 14 App Router tĩnh hóa thành công 19/19 routes. | `npm run typecheck` **PASS**<br/>`npm run build` **19/19 routes PASS** | [Tạo / Xem PR Web](https://github.com/lovemvaf/visionary-api/pull/new/feature/web-duc) |
| 2 | **Đào Trí Khang**<br/>(1923040156)<br/>*Android Java Engineer* | [`feature/android-tri-khang`](https://github.com/lovemvaf/visionary-api/tree/feature/android-tri-khang) | Commit [`f21c968`](https://github.com/lovemvaf/visionary-api/commit/f21c968):<br/>- Nâng connect/read/write timeout trong `ApiClient.java` lên 30s chịu tải cold start.<br/>- Đổi log level sang `HEADERS` để bảo vệ mã token trong Logcat. | Cấu hình Retrofit OkHttp **PASS**<br/>Xác thực cấu hình mạng an toàn | [Tạo / Xem PR Android](https://github.com/lovemvaf/visionary-api/pull/new/feature/android-tri-khang) |
| 3 | **Hồ Đoàn Nguyên Khang**<br/>(1923040112)<br/>*ASP.NET Core API Engineer* | [`feature/api-ho-doan-khang`](https://github.com/lovemvaf/visionary-api/tree/feature/api-ho-doan-khang) | Commit [`c69f702`](https://github.com/lovemvaf/visionary-api/commit/c69f702):<br/>- Ràng buộc tham số phân trang (`pageIndex >= 1`, `1 <= pageSize <= 100`) trong `EventsController.cs`.<br/>- Kiểm tra tương thích dữ liệu JSON DTOs chéo nền tảng. | `dotnet test` **15/15 tests PASS (100%)**<br/>Kiểm tra Swagger OpenAPI khớp DTO | [Tạo / Xem PR Backend](https://github.com/lovemvaf/visionary-api/pull/new/feature/api-ho-doan-khang) |
| 4 | **Võ Ngọc Minh Đạt**<br/>(1923040088)<br/>*Windows Forms Desktop Engineer* | [`feature/winforms-minh-dat`](https://github.com/lovemvaf/visionary-api/tree/feature/winforms-minh-dat) | Commit [`b6005ca`](https://github.com/lovemvaf/visionary-api/commit/b6005ca):<br/>- Tăng timeout `HttpClient` lên 30s trong `ApiClient.cs`.<br/>- Thêm cơ chế bắt lỗi `TaskCanceledException` và hiển thị thông báo lỗi tiếng Việt thân thiện khi backend khởi động chậm. | `dotnet build` WinForms **0 Error, 0 Warning**<br/>Kiểm thử Form login và Check-in | [Tạo / Xem PR Desktop](https://github.com/lovemvaf/visionary-api/pull/new/feature/winforms-minh-dat) |

---

## 3. DANH TÍNH GITHUB VÀ HÀNH ĐỘNG KỸ THUẬT (IDENTITY AUDIT)

### 3.1. Hiện trạng Danh tính Đã Xác Minh
- **Quách Khoa Đức:** GitHub: [`@lovemvaf`](https://github.com/lovemvaf) (Email: `lovemvaf@gmail.com`) ➔ **VERIFIED OWNER**. Tác giả chính điều phối hệ thống.
- **Hồ Đoàn Nguyên Khang:** GitHub: [`@HoKhangIT`](https://github.com/HoKhangIT) ➔ **VERIFIED COLLABORATOR**. Nhánh phụ trách: `feature/api-ho-doan-khang` (Hướng dẫn thao tác: [`HO_KHANG_GITHUB_ACTION.md`](../HO_KHANG_GITHUB_ACTION.md)).
- **Đào Trí Khang:** GitHub: [`@TS13lover1989`](https://github.com/TS13lover1989) ➔ **VERIFIED COLLABORATOR**. Nhánh phụ trách: `feature/android-tri-khang` (Hướng dẫn thao tác: [`TRI_KHANG_GITHUB_ACTION.md`](../TRI_KHANG_GITHUB_ACTION.md)).
- **Võ Ngọc Minh Đạt:** GitHub: [`@vongocminhdat`](https://github.com/vongocminhdat) ➔ **VERIFIED COLLABORATOR**. Nhánh phụ trách: `feature/winforms-minh-dat` (Hướng dẫn thao tác: [`MINH_DAT_GITHUB_ACTION.md`](../MINH_DAT_GITHUB_ACTION.md)).

### 3.2. Hướng dẫn Dành cho Từng Thành viên Thực hiện Đóng góp Cá nhân
Mỗi thành viên khi làm việc trên máy của mình cần thực hiện các bước chuẩn mực:
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
- **PR 1 (Web Next.js):** Tác giả: Quách Khoa Đức ➔ Reviewers: Hồ Đoàn Nguyên Khang & Đào Trí Khang.
- **PR 2 (Android Java):** Tác giả: Đào Trí Khang ➔ Reviewers: Quách Khoa Đức & Hồ Đoàn Nguyên Khang.
- **PR 3 (Web API Backend):** Tác giả: Hồ Đoàn Nguyên Khang ➔ Reviewers: Quách Khoa Đức & Võ Ngọc Minh Đạt.
- **PR 4 (WinForms Desktop):** Tác giả: Võ Ngọc Minh Đạt ➔ Reviewers: Hồ Đoàn Nguyên Khang & Quách Khoa Đức.

---

## 5. PHÂN CÔNG BÁO CÁO VÀ THUYẾT TRÌNH TH71108 (15 PHÚT)

| Diễn giả | Thời lượng | Nội dung thuyết trình chính | Minh chứng mã nguồn trình chiếu |
|:---:|:---:|---|---|
| **1. Quách Khoa Đức** | ~3.0 phút | - Đặt vấn đề, giới thiệu giải pháp tổng thể VISIONARY.<br/>- Kiến trúc Một Backend – Ba Nền tảng.<br/>- Trực tiếp Demo Website Next.js 14 trên Vercel. | `frontend/src/app/`, `frontend/src/lib/api.ts` |
| **2. Đào Trí Khang** | ~3.5 phút | - Ứng dụng Android Native Java (Material 3).<br/>- Kiến trúc Retrofit 2 + OkHttp 3 gọi RESTful API.<br/>- Tính năng QR Code Check-in & English for IT trên di động. | `VisionaryApiService.java`, `ApiClient.java` |
| **3. Hồ Đoàn Nguyên Khang** | ~4.0 phút | - Kiến trúc ASP.NET Core 8 Web API, Entity Framework Core.<br/>- Chuẩn hóa OpenAPI / Swagger UI & phân quyền JWT Bearer.<br/>- Báo cáo 15/15 bài test xUnit (Backend CI #14 Pass 100%). | `EventsController.cs`, `ApiIntegrationTests.cs` |
| **4. Võ Ngọc Minh Đạt** | ~4.5 phút | - Phần mềm Windows Forms C# (.NET 8) quản trị CLB.<br/>- Nghiệp vụ xét duyệt hồ sơ thành viên & mở điểm danh.<br/>- Phân tích sự cố kỹ thuật thật và bài học kinh nghiệm. | `MainForm.cs`, `desktop/.../ApiClient.cs` |
