# HƯỚNG DẪN TRIỂN KHAI HẠ TẦNG CLOUD ĐỘC LẬP & PRODUCTION DEVOPS
## HỆ SINH THÁI VISIONARY (VISIONARY API PLATFORM)

Tài liệu này xác định phương án triển khai độc lập 24/7 cho toàn bộ hệ sinh thái VISIONARY, loại bỏ hoàn toàn sự phụ thuộc vào máy tính cá nhân, Cloudflare Quick Tunnel tạm thời hoặc Antigravity runtime.

---

## I. MÔ HÌNH KIẾN TRÚC MỤC TIÊU (PRODUCTION ARCHITECTURE)

```
                            INTERNET (HTTPS)
                                   │
        ┌──────────────────────────┴──────────────────────────┐
        ▼                                                     ▼
┌───────────────────────────────┐              ┌─────────────────────────────┐
│  VISIONARY WEB (Next.js 14)   │              │   NATIVE CLIENTS (C# / Java)│
│  Host: Vercel Production      │              │   • WinForms Desktop C#     │
│  Domain: visionary-platform.  │              │   • Android Native Java     │
│          vercel.app           │              └──────────────┬──────────────┘
│  Alias:  visionary-global.    │                             │
│          vercel.app           │                             │
└───────────────┬───────────────┘                             │
                │                                             │
                │ (Same-Origin BFF Proxy: /api/*)             │
                ▼                                             │
┌─────────────────────────────────────────────────────────────┴──────────────┐
│                  ASP.NET CORE 8 WEB API CLOUD HOST                         │
│                  (Render Free Docker / Oracle Always Free VM)              │
│  • Health Probes: /health/live (Liveness) & /health/ready (Readiness)      │
│  • Granular RBAC (Admin, Committee, Supervisor, Collab, Member, Student)  │
│  • Multi-stage Alpine Container (< 150MB)                                  │
└─────────────────────────────────────┬──────────────────────────────────────┘
                                      │ (Npgsql SSL Encrypted Connection)
                                      ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                    SUPABASE MANAGED POSTGRESQL CLOUD                       │
│  • Tables: Users, Roles, MemberProfiles, Applications, Events, Radar...   │
│  • Connection Pooling (PgBouncer port 6543 / Direct port 5432)             │
│  • Automatic Data Integrity Constraints & Daily Cloud Snapshots            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## II. SO SÁNH CÁC PHƯƠNG ÁN HOSTING BACKEND ĐỘC LẬP

### 1. Phương án A – Oracle Cloud Always Free VM (Ưu tiên hạ tầng chuyên sâu)
- **Tài nguyên được cấp:**
  - Lựa chọn 1 (Khuyên dùng): 4 OCPU ARM Ampere A1, 24 GB RAM, 200 GB Block Storage (chia được tối đa 4 VM).
  - Lựa chọn 2: 2 VM AMD Compute (1 OCPU, 1 GB RAM mỗi máy).
- **Region tối ưu:** Singapore (`ap-singapore-1`) hoặc Tokyo (`ap-tokyo-1`) cho độ trễ thấp nhất từ Việt Nam (~30-45ms).
- **Yêu cầu đăng ký:** Bắt buộc có thẻ thanh toán quốc tế (Visa/Mastercard) để xác minh danh tính (Oracle tạm giữ ~$1 và hoàn lại sau 1-2 ngày).
- **Nguy cơ phát sinh phí:** 0đ nếu giữ cấu hình trong ngưỡng "Always Free Eligible".
- **Chính sách thu hồi VM không hoạt động:** Oracle có chính sách thu hồi (reclaim) các VM Always Free nếu CPU utilization < 20% và Network/RAM nhàn rỗi liên tục trong 7 ngày. Cần thiết lập tải định kỳ hợp lệ hoặc gắn cron task kiểm tra.
- **Quy trình triển khai trên Oracle Linux / Ubuntu VM:**
  1. Cài đặt Docker & Docker Compose:
     ```bash
     sudo apt-get update && sudo apt-get install -y docker.io docker-compose
     ```
  2. Tạo file `docker-compose.prod.yml`:
     ```yaml
     version: '3.8'
     services:
       visionary-api:
         image: lovemvaf/visionary-api:latest
         restart: always
         ports:
           - "5000:8080"
         environment:
           - ASPNETCORE_ENVIRONMENT=Production
           - ConnectionStrings__DefaultConnection=Host=aws-0-ap-southeast-1.pooler.supabase.com;Port=6543;Database=postgres;Username=postgres.xxx;Password=xxx;SSL Mode=Require;Trust Server Certificate=true
           - JWT_SECRET=YourSuperStrongProductionKeyHereAtLeast32Chars!
       caddy:
         image: caddy:alpine
         restart: always
         ports:
           - "80:80"
           - "443:443"
         volumes:
           - ./Caddyfile:/etc/caddy/Caddyfile
           - caddy_data:/data
     volumes:
       caddy_data:
     ```
  3. Cấu hình Caddy tự động cấp chứng chỉ Let's Encrypt SSL:
     ```
     api.visionary-dntu.com {
         reverse_proxy visionary-api:8080
     }
     ```

### 2. Phương án B – Render Free Docker (Khuyên dùng cho giai đoạn phát triển & nghiệm thu tức thì)
- **Đặc điểm:** Hoàn toàn miễn phí, **không yêu cầu thẻ tín dụng**.
- **Cơ chế hoạt động:**
  - Build trực tiếp từ `backend/Dockerfile` qua GitHub repository.
  - Tự động gán HTTPS URL miễn phí: `https://visionary-api.onrender.com`.
  - Hỗ trợ biến môi trường bí mật (Environment Variables).
- **Hiện tượng Cold Start:** Sau 15 phút không có request nào, máy chủ Render Free sẽ chuyển sang chế độ ngủ (spin-down). Khi có request đầu tiên tới, hệ thống mất khoảng 30–50 giây để khởi động lại container (Cold Start).
- **Tuân thủ chính sách:** Không thiết lập bot ping liên tục 24/7 để né tránh chính sách ngủ của Render (tránh vi phạm điều khoản dịch vụ). Người dùng được thông báo rõ ràng về trạng thái Cold Start thông qua thông điệp tiếng Việt lịch sự đã tích hợp sẵn trong `frontend/src/lib/api.ts`.
- **Cách kích hoạt qua Render Blueprint:**
  1. Đăng nhập [https://render.com](https://render.com) bằng tài khoản GitHub `lovemvaf`.
  2. Chọn **New +** → **Blueprint**.
  3. Chọn repository `lovemvaf/visionary-api`. File `render.yaml` sẽ tự động cấu hình service `visionary-api` từ `backend/Dockerfile` với vùng Singapore.

### 3. Phương án C – Google Cloud Run
- **Hạn mức miễn phí hàng tháng:** 2 triệu requests, 360,000 GB-seconds memory.
- **Yêu cầu:** Cần có Google Cloud Project và tài khoản Billing đang kích hoạt.
- Phù hợp khi người dùng đã có dự án GCP cấu hình sẵn.

---

## III. CẤU HÌNH SUPABASE POSTGRESQL PRODUCTION

1. **Thông số kết nối:**
   - Provider: PostgreSQL 15+ trên AWS Region Singapore (`ap-southeast-1`).
   - Sử dụng **Connection Pooling (PgBouncer)** qua cổng `6543` với mode `Transaction` để tối ưu kết nối đồng thời từ Serverless Next.js và Container ASP.NET Core.
   - Định dạng chuỗi kết nối:
     ```
     Host=aws-0-ap-southeast-1.pooler.supabase.com;Port=6543;Database=postgres;Username=postgres.[PROJECT_REF];Password=[YOUR_PASSWORD];SSL Mode=Require;Trust Server Certificate=true
     ```
2. **Chính sách Inactivity của Supabase Free:**
   - Dự án Supabase gói Free sẽ tự động tạm ngắt (Pause) sau 7 ngày nếu không có bất kỳ truy vấn nào.
   - Để khôi phục: Quản trị viên chỉ cần đăng nhập Supabase Dashboard và bấm **Unpause Project** (toàn bộ dữ liệu, schema, index được giữ nguyên vẹn 100%, không bị mất).

---

## IV. BẢO MẬT CREDENTIAL VÀ JWT ROTATION

1. **Khóa ký JWT (Signing Key):**
   - Nghiêm cấm sử dụng signing key mặc định đã từng xuất hiện trong commit cũ.
   - Trong môi trường `Production`, `Program.cs` bắt buộc đọc `JWT_SECRET` từ biến môi trường container / host.
   - Render Blueprint tự động sinh chuỗi cryptographically secure secret ngẫu nhiên trên cloud (`generateValue: true`).
2. **CORS Policy:**
   - Giới hạn origin production cho Web: `https://visionary-platform.vercel.app` và `https://visionary-global.vercel.app`.
   - Mở rộng header và method an toàn cho WinForms C# và Android Java client.
3. **Seed Data:**
   - Phân biệt rõ thành viên nhóm phát triển phần mềm (`VISIONARY API`) với các chức vụ thực tế của Ban Chủ Nhiệm CLB Tiếng Anh DNTU.
   - Khóa mật khẩu mẫu mặc định bằng biến môi trường `ADMIN_SEED_PASSWORD`.

---

## V. KIỂM THỬ SẴN SÀNG VẬN HÀNH (OPERATIONAL READINESS)

- **Health Liveness:** `GET https://[BACKEND_URL]/health/live` → Phản hồi `{"status": "Alive"}` (HTTP 200).
- **Health Readiness:** `GET https://[BACKEND_URL]/health/ready` → Phản hồi `{"status": "Ready", "database": "Connected", "provider": "Npgsql.EntityFrameworkCore.PostgreSQL"}` (HTTP 200).
- **BFF Proxy Check:** `GET https://visionary-platform.vercel.app/api/club/overview` → Phản hồi HTTP 200 với dữ liệu JSON hợp lệ.
