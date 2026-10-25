# HỢP ĐỒNG REST API CHUẨN HÓA (API CONTRACT SPECIFICATION)
**Tiêu chuẩn:** RESTful API, JSON serialization, JWT Bearer Authentication, RFC 7807 Problem Details.  
**Cơ chế dùng chung:** Cả ba nền tảng (Next.js Web, Windows Forms C#, Android Java) giao tiếp trực tiếp qua tập hợp API endpoints này.

---

## 1. Chuẩn Hóa Response Body
Tất cả các endpoint trả về cấu trúc chuẩn:
```json
{
  "success": true,
  "message": "Thao tác thành công",
  "data": { ... },
  "errors": [],
  "timestamp": "2026-10-25T15:00:00Z"
}
```

Đối với danh sách phân trang:
```json
{
  "success": true,
  "data": {
    "items": [ ... ],
    "pageIndex": 1,
    "pageSize": 10,
    "totalCount": 42,
    "totalPages": 5,
    "hasNextPage": true,
    "hasPreviousPage": false
  },
  "timestamp": "2026-10-25T15:00:00Z"
}
```

---

## 2. Danh mục Endpoints Chi tiết

### Auth & User (`/api/auth`)
- `POST /api/auth/register` – Đăng ký tài khoản sinh viên mới (Email, Password, FullName, StudentId).
- `POST /api/auth/login` – Đăng nhập bằng Email/Password, trả về JWT Token và User Profile.
- `POST /api/auth/google` – Đăng nhập bằng Google IdToken (OpenID Connect).
- `GET /api/auth/me` – Lấy thông tin tài khoản đang đăng nhập (Yêu cầu JWT Bearer).
- `PUT /api/auth/profile` – Cập nhật thông tin hồ sơ cá nhân.
- `POST /api/auth/change-password` – Đổi mật khẩu.

### Câu lạc bộ & Thành viên (`/api/club`)
- `GET /api/club/overview` – Thông tin giới thiệu CLB Tiếng Anh, sứ mệnh, ban chuyên môn, giảng viên.
- `GET /api/club/departments` – Danh sách ban chuyên môn (Học thuật, Truyền thông, Sự kiện, Đối ngoại).
- `GET /api/club/members` – Danh sách thành viên (lọc theo ban, khóa, vai trò; phân trang).
- `GET /api/club/committee` – Danh sách Ban Chủ Nhiệm theo nhiệm kỳ hiện tại.
- `POST /api/club/applications` – Nộp đơn đăng ký gia nhập CLB (Sinh viên).
- `GET /api/club/applications` – Danh sách đơn xin gia nhập (Quyền BCN / Admin).
- `PUT /api/club/applications/{id}/review` – Phê duyệt hoặc từ chối đơn gia nhập (Quyền BCN / Admin).

### Sự kiện & Điểm danh (`/api/events`)
- `GET /api/events` – Lấy danh sách sự kiện (Lọc theo Status: Upcoming, Ongoing, Past; phân trang).
- `GET /api/events/{slug}` – Chi tiết sự kiện theo Slug.
- `POST /api/events` – Tạo sự kiện mới (Quyền BCN / Admin).
- `PUT /api/events/{id}` – Cập nhật sự kiện (Quyền BCN / Admin).
- `DELETE /api/events/{id}` – Hủy hoặc xóa sự kiện (Quyền BCN / Admin).
- `POST /api/events/{id}/register` – Đăng ký tham gia sự kiện.
- `POST /api/events/{id}/cancel` – Hủy đăng ký tham gia sự kiện.
- `GET /api/events/{id}/registrations` – Danh sách sinh viên đăng ký tham gia (Quyền BCN / Admin).
- `POST /api/events/{id}/attendance` – Điểm danh thủ công hoặc bằng mã QR (Quyền BCN / Admin).
- `GET /api/events/my-events` – Danh sách sự kiện người dùng hiện tại đã đăng ký.

### Cổng Nội dung & CMS (`/api/posts`)
- `GET /api/posts` – Danh sách bài viết công khai đã duyệt (Lọc theo Category, Tag, Search; phân trang).
- `GET /api/posts/{slug}` – Chi tiết bài viết theo Slug.
- `POST /api/posts` – Tạo bài viết mới (Quyền CTV, BCN, Admin).
- `PUT /api/posts/{id}` – Chỉnh sửa bài viết.
- `PUT /api/posts/{id}/status` – Duyệt bài / xuất bản bài viết (Quyền BCN, Admin).
- `DELETE /api/posts/{id}` – Gỡ bài viết.
- `GET /api/posts/categories` – Danh mục bài viết.

### Bảng vàng Thành tích (`/api/achievements`)
- `GET /api/achievements` – Danh sách vinh danh thành tích (Lọc theo Category, năm).
- `POST /api/achievements/nominate` – Đề xuất thành tích mới kèm minh chứng.
- `PUT /api/achievements/{id}/verify` – Phê duyệt vinh danh thành tích (Quyền Giảng viên, BCN, Admin).

### English for IT (`/api/english-for-it`)
- `GET /api/english-for-it` – Danh sách bài học/thuật ngữ (Lọc theo Level, Topic; tìm kiếm).
- `GET /api/english-for-it/{slug}` – Chi tiết bài học, danh mục từ vựng, bài tập mẫu.
- `POST /api/english-for-it` – Thêm bài học mới (Quyền CTV, Admin).

### Technology Radar (`/api/tech-radar`)
- `GET /api/tech-radar` – Danh sách công nghệ mới, repo GitHub nổi bật, mô hình Hugging Face.
- `GET /api/tech-radar/{id}` – Chi tiết công nghệ, metadata, đánh giá mức độ phù hợp sinh viên.
- `POST /api/tech-radar/sync` – Kích hoạt đồng bộ dữ liệu mới nhất từ GitHub/Hugging Face (Admin).

### Cơ hội & Cuộc thi (`/api/opportunities`)
- `GET /api/opportunities` – Danh sách Hackathon, Cuộc thi AI, Học bổng, Chương trình ASEAN.
- `GET /api/opportunities/{id}` – Chi tiết cơ hội, thể lệ, link nộp đơn chính thức.
- `POST /api/opportunities` – Thêm cơ hội mới (Quyền BCN, Admin).

### Career Gateway (`/api/jobs`)
- `GET /api/jobs` – Danh sách việc làm, thực tập CNTT & Tiếng Anh (Lọc theo Type, Location).
- `GET /api/jobs/{id}` – Chi tiết yêu cầu công việc và link nộp đơn.

### Tự động hóa & Quản trị (`/api/admin`)
- `GET /api/admin/dashboard` – Thống kê tổng quan (Thành viên, Sự kiện, Bài viết, Đơn chờ duyệt).
- `GET /api/admin/sources` – Danh sách các nguồn dữ liệu tự động.
- `POST /api/admin/sources/trigger/{id}` – Chạy thủ công một nguồn thu thập dữ liệu.
- `GET /api/admin/audit-logs` – Xem lịch sử kiểm toán hệ thống.

---

## 5. Địa chỉ kiểm thử Swagger UI (OpenAPI Interactive Testing)

Swagger UI được tích hợp sẵn để phục vụ kiểm thử trực tiếp các endpoint, schema request/response, và xác thực JWT Bearer Token:

### 🌐 1. Môi trường Production (Cloud Render)
- **URL Swagger UI:** [https://visionary-api-gb51.onrender.com/swagger](https://visionary-api-gb51.onrender.com/swagger)
- **URL OpenAPI Specification JSON:** [https://visionary-api-gb51.onrender.com/swagger/v1/swagger.json](https://visionary-api-gb51.onrender.com/swagger/v1/swagger.json)

### 💻 2. Môi trường Local Development (Máy cá nhân)
- Khi chạy lệnh `dotnet run --project backend/src/Visionary.Api`:
  - **HTTP:** [http://localhost:5000/swagger](http://localhost:5000/swagger)
  - **HTTPS:** [https://localhost:5001/swagger](https://localhost:5001/swagger)

### 🔑 3. Hướng dẫn Test API cần quyền (Authorize JWT trong Swagger)
1. Mở endpoint `POST /api/auth/login` trên giao diện Swagger.
2. Bấm **"Try it out"**, nhập tài khoản (ví dụ tài khoản quản trị Admin: `ducqk@dntu.edu.vn` / `VisionaryAdmin@2026`).
3. Bấm **"Execute"**, sao chép chuỗi mã `token` trong JSON kết quả trả về.
4. Cuộn lên đầu trang Swagger, bấm vào nút **"Authorize"** (có biểu tượng ổ khóa màu xanh lá).
5. Nhập vào ô Value theo cú pháp: `Bearer <token_cua_ban>` (hoặc chỉ cần dán token tùy phiên bản swagger-ui).
6. Bấm **Authorize** -> **Close**. Sau đó có thể thực thi tất cả các API phân quyền (`/api/admin/*`, `/api/posts` thêm/sửa/xóa, `/api/events`...) trực tiếp trên Swagger.
