# BÁO CÁO KIỂM TOÁN VÀ NGHIỆM THU TỔNG THỂ REPOSITORY (FINAL AUDIT)
## VISIONARY API – MASTER REPOSITORY CLEANUP, SECURITY HARDENING & CONSISTENCY AUDIT
**Mã dự án:** VISIONARY – Hệ thống Quản lý Hoạt động Hội nhập (TH71108)  
**Đơn vị đào tạo:** Trường Đại học Công nghệ Đồng Nai (DNTU) – Khoa Công nghệ Thông tin  
**Người quản lý & Chủ sở hữu hệ thống:** Quách Khoa Đức  
**Thời điểm nghiệm thu toàn diện:** 26/10/2026  
**Commit xác minh hiện hành:** `9f7b152de978b52494d290b1109ef46ed4cf0b9a` (và các commit hoàn tất cleanup)  
**Minh chứng CI/CD:** GitHub Actions Run ID `#40254874364` (Backend CI #14)  

---

## MỤC LỤC
1. [A. So sánh Hiện trạng Repository Trước và Sau Dọn dẹp (Repository Before/After)](#a-so-sánh-hiện-trạng-repository-trước-và-sau-dọn-dẹp)
2. [B. An toàn Thông tin & Củng cố Hạ tầng (Security Hardening)](#b-an-toàn-thông-tin--củng-cố-hạ-tầng)
3. [C. Kết quả Kiểm thử & Nguồn Sự Thật Chuẩn (Test Results & SSOT)](#c-kết-quả-kiểm-thử--nguồn-sự-thật-chuẩn)
4. [D. Đồng bộ Hóa Tài liệu Kỹ thuật (Documentation Consistency)](#d-đồng-bộ-hóa-tài-liệu-kỹ-thuật)
5. [E. Danh tính & Đóng góp của Bốn Thành viên (Team Contributions)](#e-danh-tính--đóng-góp-của-bốn-thành-viên)
6. [F. Mức độ Sẵn sàng Nghiệm thu Học phần TH71108 (Academic Readiness)](#f-mức-độ-sẵn-sàng-nghiệm-thu-học-phần-th71108)
7. [G. Hiện trạng Vận hành Production & Giới hạn Thực tế (Production & Limitations)](#g-hiện-trạng-vận-hành-production--giới-hạn-thực-tế)

---

## A. SO SÁNH HIỆN TRẠNG REPOSITORY TRƯỚC VÀ SAU DỌN DẸP

| Tiêu chí so sánh | Trạng thái Ban đầu (Before) | Trạng thái Sau Chuẩn hóa (After) | Lý do & Ý nghĩa kỹ thuật |
|---|---|---|---|
| **Cấu hình nhạy cảm trong Git** | `render.yaml` chứa password Supabase thật; `docker-compose.yml` hardcode credentials; `README.md` lộ mật khẩu kiểm thử. | **ĐÃ LÀM SẠCH 100%**. Chuyển sang `sync: false`, biến môi trường `${POSTGRES_PASSWORD}` và xóa bỏ mật khẩu khỏi tài liệu. | Triệt tiêu nguy cơ rò rỉ credential lên internet. |
| **Python Cache (.pyc)** | 2 file `.pyc` trong `scripts/__pycache__/` bị Git theo dõi. | **ĐÃ UNTRACK** bằng `git rm --cached` và bổ sung vào `.gitignore`. | Ngăn chặn ô nhiễm repository bởi mã máy biên dịch tạm thời. |
| **Tên thành viên Hồ Đoàn** | Bị viết sai chính tả phụ âm cuối tại 244 vị trí trên 64 file. | **100% SỬA THÀNH "Hồ Đoàn"** trên toàn bộ markdown, code C#, TypeScript, XML, Java, script, DOCX, PPTX và PDF. | Bảo đảm tính trang nghiêm, chính xác học thuật trước hội đồng. |
| **Số liệu Test Backend** | Mâu thuẫn giữa 9/9 tests (docs cũ), PENDING (.agent), và 15/15 tests (source & CI). | **THỐNG NHẤT 15/15 TESTS** trên toàn bộ hệ thống; ghi rõ 9/9 là mốc lịch sử ban đầu. | Thiết lập Single Source of Truth (SSOT) qua `verification.json`. |
| **Tên file Member Guide số 3** | Mang tên cũ `03_HO_DOANG_NGUYEN_KHANG_API_GUIDE.docx/.pdf`. | Đã đổi tên chuẩn thành `03_HO_DOAN_NGUYEN_KHANG_API_GUIDE.docx/.pdf`. | Đồng bộ tuyệt đối tên file và nội dung. |
| **Local Backend Launcher** | `start-backend.bat` tự động bật Cloudflare Quick Tunnel ra ngoài. | Sửa thành launcher nội bộ thuần túy bind `127.0.0.1:5000`, không mở tunnel tùy tiện. | Cô lập môi trường phát triển cục bộ, độc lập với Cloud 24/7. |
| **Security CI Workflow** | Dùng `|| true` và `continue-on-error: true`, có nguy cơ pass giả. | **LOẠI BỎ PASS GIẢ**, cấu hình `.gitleaks.toml`, quét NuGet packages và kiểm tra chính sách bảo mật thực chất. | DevSecOps thực chất, không ngụy tạo kết quả kiểm tra. |

---

## B. AN TOÀN THÔNG TIN & CỦNG CỐ HẠ TẦNG

1. **Phân loại Rò rỉ & Xử lý:**
   - Đã biên soạn đầy đủ 13 báo cáo an ninh chuyên sâu lưu trữ tại [`docs/security/`](./security/).
   - Quét lịch sử Git xác nhận chưa từng có file `.env` thật nào bị commit.
   - Chuỗi kết nối Supabase cũ trong commit `199ef83` được ghi nhận trong [`EXPOSED_SECRETS_INVENTORY.md`](./security/EXPOSED_SECRETS_INVENTORY.md) kèm quy trình đổi mật khẩu tại nguồn trong [`CREDENTIAL_ROTATION_CHECKLIST.md`](./security/CREDENTIAL_ROTATION_CHECKLIST.md).
2. **Hardening Docker & Server:**
   - `backend/Dockerfile` bổ sung chỉ thị `USER app` chạy dưới quyền người dùng không đặc quyền.
   - `docker-compose.yml` cô lập database và cache trong mạng bridge `visionary_internal`, chỉ mở cổng loopback `127.0.0.1`.
3. **Phân quyền & Chống rò rỉ dữ liệu API:**
   - `ExceptionHandlingMiddleware` tích hợp Correlation ID, che giấu hoàn toàn stack trace và thông báo lỗi hệ thống trên môi trường ngoài Development.
   - Endpoints `/` và `/health/ready` được thu gọn, không leak tên DB Provider hay danh sách sinh viên.
   - Chính sách CORS chỉ cho phép các web origin hợp lệ từ Vercel và localhost development.

---

## C. KẾT QUẢ KIỂM THỬ & NGUỒN SỰ THẬT CHUẨN (SSOT)

Nguồn dữ liệu chuẩn: [`project-status/verification.json`](../project-status/verification.json) và [`docs/TEST_VERIFICATION_REPORT.md`](./TEST_VERIFICATION_REPORT.md).

```text
Backend xUnit Suite: Total: 15 | Passed: 15 | Failed: 0 | Skipped: 0 | Duration: 2.1s
- ApiIntegrationTests (7 tests): RootEndpoint, ClubOverview, Events, EnglishForIt, Opportunities, Jobs, LoginAdmin.
- AuthTests (2 tests): PasswordHasher, JwtService.
- PostsLogicAuditTests (6 tests): Categories, CategoryUnion, Pagination, DraftSecurity, Search, PostBySlug.
```
- **Build Frontend Next.js 14:** 19 tuyến đường tĩnh và động biên dịch thành công 100%.
- **Build Windows Forms .NET 8:** 0 Warning, 0 Error.
- **Build Android Java SDK 34:** Cấu hình bảo mật `network_security_config.xml` và `allowBackup="false"` đạt chuẩn.

---

## D. ĐỒNG BỘ HÓA TÀI LIỆU KỸ THUẬT

1. **Giải quyết triệt để mâu thuẫn 9/9 và 15/15:**
   - Số liệu 9/9 tests được định danh chính xác là **Mốc lịch sử ban đầu (Historical Milestone)** trước khi bổ sung suite kiểm toán logic tin bài.
   - Số liệu 15/15 tests được định danh là **Mốc hiện hành (Current Verified Active Suite)**, khớp 100% với mã nguồn và GitHub Actions Run #40254874364.
2. **Đồng bộ hóa Deliverables (PPTX, DOCX, PDF):**
   - Đã tái tạo lại toàn bộ file PowerPoint [`VISIONARY_TH71108_FINAL_PRESENTATION.pptx`](../deliverables/VISIONARY_TH71108_FINAL_PRESENTATION.pptx), tài liệu kịch bản thuyết trình, hướng dẫn demo, ngân hàng câu hỏi Q&A và 4 Member Guides bằng Microsoft Office Automation, bảo đảm tên "Hồ Đoàn Nguyên Khang" và số liệu 15 bài test xuất hiện đồng nhất trên mọi định dạng.

---

## E. DANH TÍNH & ĐÓNG GÓP CỦA BỐN THÀNH VIÊN

> [!NOTE]
> Chi tiết minh bạch: [`docs/TEAM_CONTRIBUTIONS.md`](./TEAM_CONTRIBUTIONS.md) và [`CONTRIBUTING.md`](../CONTRIBUTING.md)

1. **Roster 4 Thành viên & Thứ tự Thuyết trình:**
   - **Quách Khoa Đức (Team Lead):** Người số 1 – Mở màn, Tổng quan sản phẩm & Kiến trúc Web (Phần dễ nhất).
   - **Đào Trí Khang:** Người số 2 – Ứng dụng Di động Android Native Java & Networking Retrofit.
   - **Hồ Đoàn Nguyên Khang:** Người số 3 – Web API, OpenAPI/Swagger, JWT & Cơ sở dữ liệu.
   - **Võ Ngọc Minh Đạt:** Người số 4 – Windows Forms Desktop, Phân tích Sự cố CI #12 & Kết luận.
2. **Cảnh báo Danh tính Cần Xác minh (Blocker):**
   - Hiện tại tài khoản của Hồ Đoàn Nguyên Khang và Võ Ngọc Minh Đạt đang được cấp chung một email (`vongocminhdat@gmail.com`).
   - Nhóm ghi nhận trạng thái `IDENTITY_VERIFICATION_REQUIRED` và yêu cầu Chủ sở hữu cung cấp username GitHub riêng biệt cho từng bạn để thêm vào Collaborators thay vì tạo commit giả mạo.

---

## F. MỨC ĐỘ SẴN SÀNG NGHIỆM THU HỌC PHẦN TH71108

1. **Tiêu chí 1 Backend dùng chung 3 nền tảng:** Đạt 100% (Một RESTful Web API ASP.NET Core phục vụ đồng thời Next.js Web, WinForms Desktop và Android Mobile).
2. **Swagger UI:** Hoạt động trực tiếp tại `/swagger`, sẵn sàng cho giảng viên gọi thử nghiệm thu.
3. **Phân tích Sự cố Kỹ thuật Thật (Technical Incident):** Trình bày minh bạch sự cố đụng độ race condition SQLite giữa 2 test suite trong Run #12 và giải pháp 2 tầng (`SemaphoreSlim` + `CustomWebApplicationFactory`) dẫn tới chiến thắng tại Run #14 (15/15 tests PASS).

---

## G. HIỆN TRẠNG VẬN HÀNH PRODUCTION & GIỚI HẠN THỰC TẾ

- **Website Production:** [https://visionary-platform.vercel.app/](https://visionary-platform.vercel.app/) (Online 24/7 trên Vercel Edge).
- **Backend API Production:** [https://visionary-api-gb51.onrender.com](https://visionary-api-gb51.onrender.com) (Render Docker container).
- **Database Cloud:** Supabase Managed PostgreSQL Singapore (`aws-0-ap-southeast-1.pooler.supabase.com:5432`, SSL Required).
- **Giới hạn kỹ thuật cần ghi nhận:** Gói Free của Render có cơ chế ngủ sau 15 phút không có request; khi truy cập lại cần thời gian Cold Start khoảng 30-50 giây. Hệ thống đã tích hợp thông báo người dùng thân thiện tại Web, Desktop và Android để xử lý trường hợp này.
- **Tuyên bố an ninh thực chất:** Dự án đã triển khai đầy đủ các biện pháp phòng thủ chiều sâu và kiểm soát rủi ro thực tế; không đưa ra các tuyên bố phi thực tế như "không thể bị hack" hay "an toàn 100% tuyệt đối".
