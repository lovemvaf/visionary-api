# BẢO MẬT VÀ TUÂN THỦ OWASP (SECURITY SPECIFICATION)

## 1. Bảo vệ trước OWASP API Security Top 10

1. **Broken Object Level Authorization (BOLA):**
   - Mọi thao tác sửa/xóa tài nguyên cá nhân (đơn đăng ký, hồ sơ, bài viết) đều kiểm tra quyền sở hữu (`UserId == CurrentUser.Id` hoặc người dùng có vai trò `Admin`).
   - Sử dụng Guid/UUID ngẫu nhiên cho khóa chính, chống kỹ thuật duyệt ID tuần tự (Insecure Direct Object Reference).

2. **Broken Authentication:**
   - Mật khẩu được băm (hash) bằng giải thuật tiêu chuẩn công nghiệp (PBKDF2 / BCrypt) với salt ngẫu nhiên.
   - JWT được ký bằng thuật toán HMAC-SHA256 với secret key tối thiểu 256 bits.
   - Google OAuth xác minh IdToken bằng thư viện chính thức `Google.Apis.Auth` trên server ASP.NET Core, kiểm tra đúng Client ID, Issuer (`accounts.google.com`), và hạn dùng.

3. **Broken Object Property Level Authorization (Mass Assignment):**
   - Sử dụng DTO riêng biệt (Data Transfer Objects) cho từng thao tác Create, Update.
   - Tuyệt đối không cho phép client gửi trường `Role`, `IsActive`, `IsVerified` trong payload cập nhật thông thường.

4. **Unrestricted Resource Consumption & Rate Limiting:**
   - Áp dụng Rate Limiting trên các endpoint nhạy cảm (Đăng nhập: tối đa 5 lần/phút; Tìm kiếm: tối đa 60 lần/phút).
   - Mọi truy vấn danh sách đều bắt buộc phân trang (mặc định 10-20 items, tối đa 50 items/trang).

5. **Broken Function Level Authorization (BFLA):**
   - Áp dụng `[Authorize(Roles = "Admin,Committee")]` trên toàn bộ controller hoặc action quản trị.

6. **Server-Side Request Forgery (SSRF):**
   - Bộ thu thập dữ liệu tự động chỉ cho phép gọi các tên miền trong whitelist đã đăng ký trong bảng `ContentSources`.
   - Chặn tuyệt đối các địa chỉ IP nội bộ (`127.0.0.1`, `localhost`, `10.0.0.0/8`, `192.168.0.0/16`, `169.254.169.254`).

7. **Security Misconfiguration & F12 Client-side Protection:**
   - Không đặt bất kỳ API keys bí mật, connection string hay credentials nào vào bundle browser.
   - Không sử dụng biến tiền tố `NEXT_PUBLIC_` cho bất kỳ secret nào.
   - Thiết lập các HTTP Security Headers: Content-Security-Policy (CSP), Strict-Transport-Security (HSTS), X-Content-Type-Options, X-Frame-Options.
   - Tắt chi tiết stack trace trên môi trường Production.
