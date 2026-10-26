# BÁO CÁO KIỂM TOÁN XÁC THỰC VÀ PHÂN QUYỀN API (RBAC & ACCESS CONTROL)
## API AUTHENTICATION & ROLE-BASED AUTHORIZATION AUDIT
**Mã dự án:** VISIONARY – Hệ thống Quản lý Hoạt động Hội nhập (TH71108)  
**Tiêu chuẩn kiểm thử:** OWASP API Security Top 10 (2023)  
**Mục tiêu:** Rà soát cơ chế xác thực JWT, phân quyền 7 vai trò, phòng chống BOLA/IDOR, Broken Function Level Authorization và rò rỉ dữ liệu.  

---

## 1. MÔ HÌNH PHÂN QUYỀN HỆ THỐNG (7 VAI TRÒ)

Hệ thống VISIONARY phân định quyền hạn theo ma trận vai trò nghiệp vụ thực tế:
1. **Admin (Quản trị viên):** Toàn quyền cấu hình hệ thống, quản lý người dùng, phân quyền, kích hoạt đồng bộ dữ liệu.
2. **Supervisor (Cố vấn/Giảng viên):** Giám sát hoạt động, xem báo cáo thống kê, duyệt kế hoạch hội nhập.
3. **Committee (Ban Chủ Nhiệm CLB):** Quản lý sự kiện, duyệt đơn thành viên, điểm danh sinh viên, quản lý tài liệu nội bộ.
4. **Collaborator (Cộng tác viên):** Soạn thảo bài viết, hỗ trợ tổ chức sự kiện, kiểm tra thông tin.
5. **ClubMember (Thành viên chính thức):** Tham gia sinh hoạt CLB, nhận tài liệu độc quyền, đăng ký hoạt động hội nhập.
6. **Student (Sinh viên DNTU):** Xem thông tin công khai, đăng ký sự kiện, nộp đơn tham gia CLB, học thuật ngữ Tiếng Anh CNTT.
7. **Guest (Khách vãng lai):** Chỉ xem nội dung công khai (Tin tức, Sự kiện công khai, Tech Radar, Giới thiệu).

---

## 2. KẾT QUẢ RÀ SOÁT CÁC ENDPOINT VÀ CƠ CHẾ PHÒNG VỆ

### 2.1. Xác thực Server-Side Bắt buộc (No Client-Only Authorization)
- Tất cả các endpoint quản trị và thao tác dữ liệu nhạy cảm đều được bảo vệ bởi attribute `[Authorize]` và `[Authorize(Roles = "...")]` tại Controller / Action:
  - `AdminController`: Yêu cầu vai trò `AppRoles.Admin`.
  - `EventsController (POST/PUT/DELETE)`: Yêu cầu vai trò `Admin`, `Committee`, hoặc `Collaborator`.
  - `MembershipController (Approve/Reject)`: Chỉ cho phép `Admin` hoặc `Committee`.
- Không dựa vào việc "ẩn nút bấm trên giao diện Web/App" để bảo mật; toàn bộ kiểm tra quyền hạn đều thực thi tại tầng Web API.

### 2.2. Phòng chống BOLA/IDOR (Broken Object-Level Authorization)
- Trong các thao tác liên quan đến thông tin cá nhân của Sinh viên (Ví dụ: `GET /api/users/profile`, nộp đơn tham gia CLB, cập nhật hồ sơ):
  - Hệ thống **không nhận `userId` từ query string hoặc request body** của client để suy ra chủ sở hữu.
  - Thay vào đó, API trích xuất trực tiếp `User.FindFirst(ClaimTypes.NameIdentifier)` từ JWT Token đã được xác thực mã hóa.
  - Sinh viên A không thể giả mạo `userId` của Sinh viên B để xem hoặc sửa đổi thông tin cá nhân.

### 2.3. Phòng chống Mass Assignment (Gán Quyền Trái Phép)
- DTO đăng ký tài khoản (`RegisterRequest`) chỉ tiếp nhận các trường nghiệp vụ: `Email`, `Password`, `FullName`, `StudentId`, `Department`.
- Trường `Roles` hoặc quyền hạn **hoàn toàn không tồn tại trong DTO đăng ký**.
- Mọi tài khoản đăng ký mới qua endpoint công khai `/api/auth/register` đều được hệ thống backend gán cố định vai trò mặc định `Student`. Chỉ có Quản trị viên tối cao thông qua endpoint quản trị được xác thực mới có quyền nâng cấp vai trò.

### 2.4. Khóa Bí mật JWT và Kiểm tra Phiên (JWT Security)
- Thời hạn Token: 1440 phút (24 giờ), có kiểm tra `ValidateLifetime = true`.
- Thuật toán ký: HMAC-SHA256 (`SecurityAlgorithms.HmacSha256`).
- Khóa ký: Tối thiểu 32 ký tự (256 bits). Đã bổ sung bộ kiểm tra runtime trong `Program.cs` và `JwtService.cs` chặn hoàn toàn các khóa mặc định hoặc placeholder trong môi trường Production.
- `ClockSkew` được thiết lập `TimeSpan.Zero` để ngăn chặn việc sử dụng token đã hết hạn.

---

## 3. BẢO VỆ SWAGGER UI TRONG MÔI TRƯỜNG THI CỬ & ĐÁNH GIÁ (TH71108)

1. **Yêu cầu môn học TH71108:** Swagger UI là công cụ bắt buộc để Giảng viên kiểm tra, gọi thử các API và chấm điểm đồ án.
2. **Biện pháp cân bằng an ninh:**
   - Swagger UI (`/swagger`) được cấu hình hiển thị đầy đủ schema và mô tả DTO nhưng **loại bỏ toàn bộ secret hoặc mật khẩu thật trong ví dụ (Example Payloads)**.
   - Để gọi các API quản trị trên Swagger, Giảng viên/Người kiểm thử bắt buộc phải nhấn nút **Authorize** và nhập chuỗi `Bearer <JWT_TOKEN>` hợp lệ lấy từ endpoint `/api/auth/login`. Swagger không tự động nhúng sẵn token Admin.
   - Việc này vừa bảo đảm tính học thuật kiểm thử trực quan cho môn học, vừa tuân thủ nguyên tắc xác thực không bypass.
