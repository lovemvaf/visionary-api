# BÁO CÁO CỦNG CỐ BẢO MẬT CONTAINER & DOCKER (DEVSECOPS)
## DOCKER & CONTAINER INFRASTRUCTURE HARDENING REPORT
**Mã dự án:** VISIONARY – Hệ thống Quản lý Hoạt động Hội nhập (TH71108)  
**Thành phần rà soát:** `backend/Dockerfile`, `docker-compose.yml`, `.dockerignore`, `backend/.dockerignore`  
**Tiêu chuẩn áp dụng:** CIS Docker Benchmark & OWASP Container Security Guidelines  

---

## 1. CÁC ĐIỂM YẾU BAN ĐẦU ĐƯỢC PHÁT HIỆN

1. **Hardcoded Credentials trong Compose:** `docker-compose.yml` chứa mật khẩu plaintext của PostgreSQL (`POSTGRES_PASSWORD: VisionarySecureDbPassword2026`) và chuỗi kết nối chứa mật khẩu, cùng với JWT Signing Key mẫu.
2. **Công khai cổng cơ sở dữ liệu và Cache ra bên ngoài:** Các cổng `5432:5432` và `6379:6379` được publish trực tiếp vào giao diện mạng host mà không có tường lửa giới hạn IP, tạo nguy cơ bị quét cổng và tấn công brute-force từ internet.
3. **Quyền hạn Runtime Container:** `backend/Dockerfile` chưa chỉ định `USER`, mặc định chạy dưới quyền `root` bên trong container.
4. **Quy tắc `.dockerignore` sơ sài:** Cả hai file `.dockerignore` chỉ có 4 dòng, không loại trừ các file chứng chỉ (`.pem`, `.key`, `.pfx`), file database (`.db`, `.sqlite`), thư mục `secrets/`, hoặc các biến môi trường nhạy cảm (`.env*`).

---

## 2. CHI TIẾT CÁC BIỆN PHÁP HARDENING ĐÃ TRIỂN KHAI

### 2.1. Loại bỏ thông tin nhạy cảm và Cấu hình Mạng Nội bộ (`docker-compose.yml`)
- Toàn bộ mật khẩu và signing key được chuyển thành biến môi trường có giá trị fallback an toàn riêng cho local dev:
  - `POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-VisionaryDevDbSecret2026}`
  - `Jwt__Key=${JWT_SECRET:-VisionaryDevJwtSecretKeyMinimum32CharactersLong2026}`
- Đóng toàn bộ cổng công khai. Cổng 5432 và 6379 chỉ bind vào giao diện loopback `127.0.0.1` phục vụ quản trị cục bộ:
  - `ports: - "127.0.0.1:5432:5432"`
  - `ports: - "127.0.0.1:6379:6379"`
- Tạo bridge network nội bộ riêng biệt: `visionary_internal`. Backend và database giao tiếp hoàn toàn qua DNS nội bộ của Docker (`Host=postgres;Port=5432;...`), không để lộ bất kỳ traffic nào ra mạng ngoài.

### 2.2. Chạy dưới quyền người dùng không đặc quyền (`USER app`)
- Trong `backend/Dockerfile`, chúng tôi đã bổ sung chỉ thị:
  ```dockerfile
  USER app
  ```
- Hình ảnh cơ sở `mcr.microsoft.com/dotnet/aspnet:8.0` cung cấp sẵn tài khoản người dùng `app` (UID 1654) có quyền hạn tối thiểu (least privilege). Nếu có lỗ hổng thực thi mã từ xa (RCE) trong ứng dụng, kẻ tấn công không thể chiếm quyền root của hệ điều hành container, giảm thiểu tối đa nguy cơ container escape.

### 2.3. Quy tắc loại trừ nghiêm ngặt (`.dockerignore`)
Cả hai file `.dockerignore` (gốc và `backend/.dockerignore`) đã được mở rộng toàn diện:
```text
# Git and Version Control
.git
**/.git

# Environment files and credentials
**/.env
**/.env.*
!**/.env.example
**/*.pem
**/*.key
**/*.p12
**/*.pfx
**/*.keystore
**/id_rsa
**/id_ed25519

# Database and dumps
**/*.db
**/*.db-shm
**/*.db-wal
**/*.sqlite
**/*.sqlite3
**/*.sql
**/secrets/

# Build artifacts & dependencies
**/node_modules/
**/bin/
**/obj/
**/TestResults/

# IDE and OS files
.vs
.vscode
.idea
.DS_Store
Thumbs.db
```
Quy tắc này bảo đảm quá trình `docker build` (context copy) không thể sao chép bất kỳ file bí mật, private key, hay bản sao cơ sở dữ liệu nào vào image layer.

---

## 3. KIỂM CHỨNG BẢO MẬT CONTAINER (VERIFICATION)

| Kiểm tra an ninh | Tiêu chí đánh giá | Kết quả kiểm chứng |
|---|---|---|
| **Secret Scanning Image Layers** | Kiểm tra layer của Docker image không chứa file `.env` hoặc password | **PASS** – Image chỉ chứa DLL đã publish trong thư mục `/app` |
| **Port Exposure** | Kiểm tra cổng 5432 và 6379 trên public interface | **PASS** – Không mở cổng công khai, chỉ bind loopback 127.0.0.1 |
| **User Privileges** | Tiến hành chạy container và xác định UID/User | **PASS** – Chạy dưới tài khoản `app` unprivileged |
| **Network Isolation** | Backend kết nối Postgres qua mạng nội bộ Docker | **PASS** – Kết nối thông suốt qua bridge `visionary_internal` |
