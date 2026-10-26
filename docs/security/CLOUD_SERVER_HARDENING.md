# BÁO CÁO CỦNG CỐ BẢO MẬT MÁY CHỦ VÀ HẠ TẦNG ĐÁM MÂY
## CLOUD SERVER & HOSTING INFRASTRUCTURE HARDENING
**Mã dự án:** VISIONARY – Hệ thống Quản lý Hoạt động Hội nhập (TH71108)  
**Nền tảng hạ tầng:** Render Web Service (Backend), Supabase Cloud (PostgreSQL), Vercel Edge Network (Next.js Frontend)  

---

## 1. NGUYÊN TẮC BẢO VỆ HẠ TẦNG CLOUD

Hệ thống VISIONARY được xây dựng theo mô hình Modern Cloud-Native Microservices kết hợp PaaS/SaaS chuyên dụng:
- **Nguyên tắc Phòng thủ Chiều sâu (Defense-in-Depth):** Không phụ thuộc vào một lớp bảo vệ duy nhất; từng tầng mạng, container, gateway và database đều có chốt kiểm soát độc lập.
- **Nguyên tắc Quyền hạn Tối thiểu (Principle of Least Privilege):** Các thành phần chỉ có quyền truy cập tối thiểu cần thiết để hoàn thành nghiệp vụ.
- **Không công khai cổng trực tiếp:** Chỉ có Reverse Proxy / Edge Ingress tiếp nhận traffic người dùng (HTTPS Port 443). Mọi kết nối tới Database và Cache bắt buộc qua TLS có xác thực.

---

## 2. RÀ SOÁT VÀ BẢO VỆ CÁC THÀNH PHẦN HẠ TẦNG

### 2.1. Render Web Service (ASP.NET Core Web API)
- **Tình trạng trước kiểm toán:** File cấu hình tự động `render.yaml` chứa thông tin nhạy cảm dạng plaintext.
- **Biện pháp đã triển khai:**
  1. Loại bỏ các giá trị secret khỏi `render.yaml`, chuyển sang `sync: false`.
  2. Bắt buộc người quản trị đưa connection string và JWT key vào **Render Environment Variables** (chế độ bảo vệ Secret, không hiển thị trong build logs).
  3. Cấu hình Health Check Endpoint `/health/live` để tự động khởi động lại container khi có sự cố, không để lộ thông tin cấu hình nội bộ.
  4. Cấu hình giới hạn bộ nhớ và CPU nhằm ngăn chặn tấn công từ chối dịch vụ (DoS) cạn kiệt tài nguyên.

### 2.2. Supabase Cloud Database (PostgreSQL)
- **Cơ chế kết nối an toàn:**
  1. Bắt buộc sử dụng giao thức TLS/SSL (`SSL Mode=Require;Trust Server Certificate=true`).
  2. Sử dụng Transaction Pooler (Port 5432/6543) để bảo vệ database khỏi tình trạng cạn kiệt connection do bùng nổ lưu lượng (Connection Starvation).
  3. Mật khẩu kết nối được tách biệt hoàn toàn khỏi mã nguồn, chỉ được nạp tại runtime qua biến môi trường máy chủ.
  4. Thực thi quy trình đổi mật khẩu (Reset Password) tại Supabase Console sau khi phát hiện rò rỉ trong lịch sử commit.

### 2.3. Vercel Edge Network (Next.js Frontend)
- **Bảo vệ biên mạng (Edge Protection):**
  1. Vercel cung cấp sẵn khả năng chống DDoS tự động ở tầng L3/L4/L7 qua Cloudflare Anycast CDN.
  2. Toàn bộ các yêu cầu HTTP đều tự động chuyển hướng sang HTTPS với chứng chỉ SSL/TLS tự động gia hạn (Let's Encrypt).
  3. Biến môi trường trên Vercel được phân định rõ ràng giữa Server-side (ví dụ `API_BASE_URL`) và Client-side (`NEXT_PUBLIC_*`). Tuyệt đối không đưa bất kỳ API secret, database credential hoặc service role key nào vào tiền tố `NEXT_PUBLIC_`.

---

## 3. CHECKLIST KIỂM SOÁT HẠ TẦNG (INFRASTRUCTURE SECURITY CHECKLIST)

| Hạng mục kiểm soát | Trạng thái | Đánh giá an ninh |
|---|---|---|
| **HTTPS/TLS 1.2+ Enforcement** | **ĐẠT** | 100% traffic Web, API và Database đều mã hóa trên đường truyền |
| **Direct DB Internet Access** | **ĐÃ CÔ LẬP** | Cổng database trong Docker đóng hoàn toàn; Supabase yêu cầu SSL & credentials mạnh |
| **No Secrets in Startup Logs** | **ĐẠT** | `Program.cs` không in connection string hoặc JWT key ra console khi khởi động |
| **Rollback & Uptime Safeguard** | **ĐẠT** | Git commit sạch; có thể rollback bất kỳ lúc nào qua Render/Vercel Dashboard |
| **Zero Server Secrets in Frontend** | **ĐẠT** | Rà soát `frontend/` xác nhận không có server secret trong `NEXT_PUBLIC_*` |
