# BÁO CÁO TOÀN DIỆN KIỂM TOÁN BẢO MẬT HỆ THỐNG VISIONARY
## VISIONARY SYSTEM-WIDE CYBERSECURITY AUDIT REPORT
**Mã dự án:** VISIONARY – Hệ thống Quản lý Hoạt động Hội nhập (TH71108)  
**Tổ chức:** Trường Đại học Công nghệ Đồng Nai (DNTU)  
**Đơn vị thực hiện:** Nhóm Kỹ sư An toàn Thông tin & Kiến trúc Phần mềm VISIONARY  
**Thời gian kiểm toán:** Tháng 10/2026  
**Trạng thái kiểm toán:** HOÀN TẤT & ĐÃ TRIỂN KHAI CÁC BIỆN PHÁP KHẮC PHỤC (REMEDIATED)  

---

## 1. TỔNG QUAN VÀ PHẠM VI KIỂM TOÁN (AUDIT SCOPE)

Kiểm toán bảo mật chuyên sâu được tiến hành trên toàn bộ các thành phần thuộc kiến trúc đa nền tảng VISIONARY nhằm phát hiện, cô lập và triệt tiêu các lỗ hổng an ninh thông tin, rò rỉ thông tin xác thực, cấu hình mạng thiếu an toàn và các rủi ro chuỗi cung ứng:

1. **Mã nguồn và Lịch sử Git:** Repository `lovemvaf/visionary-api`, toàn bộ commit tree, file cấu hình, tài liệu hướng dẫn và biến môi trường mẫu.
2. **Backend Web API:** Ứng dụng ASP.NET Core 8 Web API, Entity Framework Core, middleware xử lý lỗi, endpoint sức khỏe, Swagger UI, và cơ chế xác thực JWT Bearer.
3. **Cơ sở dữ liệu & Cache:** Supabase PostgreSQL Pooler, SQLite cục bộ, Redis Cache trong container.
4. **Hạ tầng Container & Máy chủ:** `backend/Dockerfile`, `docker-compose.yml`, `.dockerignore`, `render.yaml`.
5. **Ứng dụng Web:** Next.js 14 App Router triển khai trên nền tảng Vercel Edge (`visionary-platform.vercel.app`).
6. **Ứng dụng Desktop:** Windows Forms C# (.NET 8).
7. **Ứng dụng Di động:** Android Java (SDK 34).
8. **Quy trình CI/CD:** GitHub Actions Workflows (`security.yml`, `backend.yml`, `frontend.yml`, `desktop.yml`, `android.yml`).

---

## 2. BẢNG PHÂN LOẠI LỖ HỔNG THEO MỨC ĐỘ NGUY HIỂM (SEVERITY MATRIX)

| Mã lỗ hổng | Thành phần ảnh hưởng | Mô tả chi tiết lỗ hổng | Mức độ | Trạng thái khắc phục |
|---|---|---|---|---|
| **SEC-P0-01** | `render.yaml` | Connection string PostgreSQL chứa mật khẩu Supabase thật được commit trực tiếp lên Git | **P0 - Critical** | **ĐÃ KHẮC PHỤC** (Chuyển sang `sync: false`, loại bỏ chuỗi mật khẩu khỏi mã nguồn) |
| **SEC-P0-02** | `docker-compose.yml` | Hardcode mật khẩu cơ sở dữ liệu và signing key JWT mẫu trong file Compose | **P0 - Critical** | **ĐÃ KHẮC PHỤC** (Thay thế bằng biến môi trường `${POSTGRES_PASSWORD}` và `${JWT_SECRET}`) |
| **SEC-P0-03** | `docker-compose.yml` | Công khai cổng PostgreSQL `5432:5432` và Redis `6379:6379` ra ngoài host | **P0 - Critical** | **ĐÃ KHẮC PHỤC** (Cô lập mạng nội bộ `visionary_internal`, bind `127.0.0.1` cho truy cập quản trị) |
| **SEC-P0-04** | `README.md`, `OPERATIONS_MANUAL.md` | Bảng tài khoản kiểm thử công khai kèm mật khẩu khởi tạo cố định | **P0 - Critical** | **ĐÃ KHẮC PHỤC** (Xóa hoàn toàn mật khẩu khỏi tài liệu, áp dụng chính sách `ADMIN_SEED_PASSWORD`) |
| **SEC-P0-05** | `frontend`, `desktop`, `mobile` | Mật khẩu mẫu bị nhúng trực tiếp trong bundle JavaScript, WinForms form và layout XML | **P0 - Critical** | **ĐÃ KHẮC PHỤC** (Xóa mọi cơ chế tự động điền mật khẩu cố định, chỉ hỗ trợ gợi ý email kiểm thử) |
| **SEC-P1-01** | `appsettings.json`, `Program.cs` | Signing key JWT mẫu trong file cấu hình có nguy cơ được sử dụng trên production | **P1 - High** | **ĐÃ KHẮC PHỤC** (Cấu hình placeholder, chặn khởi động Production nếu key không đủ 32 ký tự hoặc dùng key mẫu) |
| **SEC-P1-02** | `ExceptionHandlingMiddleware` | Trả về `exception.Message` trực tiếp cho client khi phát sinh lỗi hệ thống | **P1 - High** | **ĐÃ KHẮC PHỤC** (Chỉ trả Correlation ID / TraceIdentifier trên production, che giấu chi tiết ngoại lệ) |
| **SEC-P1-03** | `security.yml` | Dùng lệnh `npm audit || true` bỏ qua lỗi phụ thuộc | **P1 - High** | **ĐÃ KHẮC PHỤC** (Loại bỏ `|| true`, bổ sung kiểm toán NuGet, xuất báo cáo artifact có kiểm soát) |
| **SEC-P1-04** | `backend/Dockerfile` | Container chạy dưới quyền người dùng `root` | **P1 - High** | **ĐÃ KHẮC PHỤC** (Bổ sung chỉ thị `USER app` để thực thi dưới quyền unprivileged user) |
| **SEC-P2-01** | `Program.cs` | Endpoint `/health/ready` làm lộ tên DB Provider và chi tiết ngoại lệ kết nối | **P2 - Medium** | **ĐÃ KHẮC PHỤC** (Chuẩn hóa trả về trạng thái tối giản, không rò rỉ topology) |
| **SEC-P2-02** | `Program.cs` | CORS cấu hình chính sách wildcard không kiểm soát | **P2 - Medium** | **ĐÃ KHẮC PHỤC** (Chỉ cho phép các origin hợp lệ từ Vercel và localhost development) |
| **SEC-P2-03** | `mobile/AndroidManifest.xml` | Bật `android:allowBackup="true"` và không có `network_security_config.xml` | **P2 - Medium** | **ĐÃ KHẮC PHỤC** (Tắt backup, áp dụng cấu hình bắt buộc TLS cho production) |

---

## 3. CHI TIẾT CÁC BIỆN PHÁP KHẮC PHỤC (REMEDIATION ACTIONS)

### 3.1. Triệt tiêu Rò rỉ Thông tin xác thực (Credentials Sanitization)
- **`render.yaml`:** Toàn bộ thông tin nhạy cảm bao gồm connection string Supabase và secret JWT đã được xóa bỏ khỏi YAML. Cấu hình được chuyển sang `sync: false`, hướng dẫn người quản trị thiết lập trực tiếp qua giao diện bảo mật Render Dashboard.
- **`docker-compose.yml`:** Các giá trị plaintext bị xóa bỏ và thay bằng biến môi trường. Các cổng nội bộ 5432 và 6379 được đưa vào mạng riêng `visionary_internal` và bind vào loopback `127.0.0.1`.
- **`appsettings.json`:** Khóa JWT được thay bằng chuỗi placeholder. Tại `Program.cs` và `JwtService.cs`, cơ chế kiểm tra runtime bắt buộc từ chối khởi động nếu môi trường `Production` sử dụng khóa mặc định hoặc khóa dưới 32 ký tự (256 bits).
- **`README.md` & `OPERATIONS_MANUAL.md`:** Cột mật khẩu được loại bỏ hoàn toàn. Bổ sung cảnh báo an ninh về quản lý mật khẩu khởi tạo thông qua biến môi trường `ADMIN_SEED_PASSWORD`.

### 3.2. Bảo vệ Ứng dụng Client (Web, Desktop, Android)
- **Frontend Next.js:** Loại bỏ hàm điền mật khẩu tự động trong mã nguồn React, bảo đảm bundle biên dịch không chứa mật khẩu tĩnh.
- **Desktop WinForms:** Xóa bỏ mật khẩu mặc định khỏi `TextBox` và sự kiện click demo.
- **Android App:** Xóa bỏ `android:text` trong XML layout, xóa mã gán mật khẩu tự động trong Java code, tắt `allowBackup` và thêm `network_security_config.xml` để cấm cleartext ra internet.

### 3.3. Tăng cường Bảo vệ Tầng Ứng dụng Backend & API
- **Middleware Xử lý Lỗi:** `ExceptionHandlingMiddleware` được tái cấu trúc để ghi log chi tiết lỗi kèm Correlation ID vào máy chủ, đồng thời chỉ trả về mã định danh `TraceIdentifier` cho client ở môi trường ngoài Development.
- **Health Check Endpoints:** `/health/ready` và `/` được làm sạch, không công bố thông tin cá nhân của thành viên nhóm lập trình, không tiết lộ tên DB Provider hoặc thông tin kết nối máy chủ.
- **Chính sách CORS:** Giới hạn chặt chẽ origin đến các domain chính thức (`visionary-platform.vercel.app`, `visionary-global.vercel.app`) và môi trường local development.

---

## 4. KẾT LUẬN & ĐÁNH GIÁ RỦI RO CÒN LẠI (RESIDUAL RISK)

Sau khi hoàn tất toàn bộ các bước khắc phục:
1. **Mã nguồn hiện hành:** Hoàn toàn sạch, không chứa bất kỳ secret, token hay mật khẩu hoạt động nào.
2. **Khả năng hoạt động:** 15/15 Integration Tests của Backend xUnit đạt PASS 100%. Các ứng dụng Web, Windows Forms và Android biên dịch thành công và duy trì toàn vẹn nghiệp vụ.
3. **Rủi ro còn lại (Residual Risk):** Các thông tin xác thực đã từng xuất hiện trong lịch sử commit cũ cần được chủ sở hữu hệ thống thực hiện quy trình thu hồi và xoay vòng (Rotate) trên Supabase Dashboard và Render Dashboard theo tài liệu hướng dẫn `CREDENTIAL_ROTATION_CHECKLIST.md`.
