# BẢNG TỔNG HỢP YÊU CẦU TRUY CẬP VÀ CẤU HÌNH DỊCH VỤ NGOẠI VI
> **DỰ ÁN:** VISIONARY – Hệ sinh thái Quản lý Hoạt động Hội nhập (DNTU)  
> **NHÓM PHÁT TRIỂN:** `VISIONARY API` (Quách Khoa Đức, Võ Ngọc Minh Đạt, Hồ Đoàn Nguyên Khang, Đào Trí Khang)  
> **KHO MÃ NGUỒN GITHUB:** [https://github.com/lovemvaf/visionary-api](https://github.com/lovemvaf/visionary-api)  
> **VERCEL PRODUCTION:** [https://visionary-platform.vercel.app](https://visionary-platform.vercel.app) (Alias: `https://visionary-global.vercel.app`)

Tài liệu này xác định danh sách các dịch vụ ngoại vi cần thiết để hệ thống vận hành độc lập 24/7 trên môi trường cloud.  
**LƯU Ý BẢO MẬT:** Tuyệt đối KHÔNG dán trực tiếp mật khẩu, private key hoặc connection string thô vào cửa sổ chat với AI. Tất cả các giá trị bí mật phải được nhập trực tiếp tại giao diện quản lý biến môi trường bảo mật (Vercel Project Settings, Render Dashboard, hoặc Oracle Secret Manager).

---

## 1. DỊCH VỤ: CLOUD HOSTING BACKEND ĐỘC LẬP (RENDER FREE DOCKER HOẶC ORACLE ALWAYS FREE VM)

- **Service:** Backend Cloud Container Hosting (ASP.NET Core Web API).
- **Current status:** Đã có `backend/Dockerfile` multi-stage Alpine, `render.yaml` Blueprint tự động hóa. Đang kiểm thử với Kestrel & Cloudflare Tunnel.
- **Required action:** Tạo Web Service trên Render hoặc cấp VM trên Oracle Cloud để chạy container độc lập 24/7 không phụ thuộc máy cá nhân.
- **Where to click:**
  - *Render:* Truy cập [https://dashboard.render.com](https://dashboard.render.com) → Nhấn **New +** → Chọn **Blueprint** (hoặc **Web Service**).
  - *Oracle:* Truy cập [https://cloud.oracle.com](https://cloud.oracle.com) → Chọn **Compute** → **Instances** → **Create Instance** (chọn Shape *VM.Standard.A1.Flex* Always Free).
- **Required non-secret identifiers:**
  - Repository URL: `https://github.com/lovemvaf/visionary-api`
  - Branch: `main`
  - Region: `Singapore` (độ trễ tối ưu cho người dùng Việt Nam)
- **Secret name:**
  - `JWT_SECRET` (Chuỗi bí mật tối thiểu 32 ký tự dùng để ký JWT Bearer token)
  - `ConnectionStrings__DefaultConnection` (Chuỗi kết nối PostgreSQL Supabase)
- **Secure entry location:** Render Dashboard → Environment Variables Tab (hoặc `/etc/environment` trên Oracle VM).
- **What I need to do:**
  1. Đăng nhập Render bằng tài khoản GitHub `lovemvaf`.
  2. Kết nối repo `lovemvaf/visionary-api` qua file `render.yaml`.
  3. Điền chuỗi kết nối Supabase vào biến `ConnectionStrings__DefaultConnection`.
  4. Lấy URL công khai dạng `https://visionary-api.onrender.com` và cập nhật biến `API_BASE_URL` trên Vercel.
- **What Antigravity will do:**
  - Đã đóng gói sẵn Dockerfile chuẩn hóa, port 8080/5000, cấu hình CORS, health probes `/health/live` và `/health/ready`.
  - Cập nhật Next.js BFF proxy `/api/[...path]` tự động chuyển tiếp request không gặp CORS/Mixed Content.
- **Priority:** **P0 – Bắt buộc để hệ thống độc lập 24/7 khi tắt máy tính cá nhân**.
- **Blocking modules:** Đăng nhập, đăng ký, đồng bộ WinForms/Android khi máy tính cá nhân tắt.

---

## 2. DỊCH VỤ: SUPABASE MANAGED POSTGRESQL (PRODUCTION DATABASE)

- **Service:** Cloud PostgreSQL Database & Connection Pooling.
- **Current status:** Mã nguồn EF Core hỗ trợ song song Npgsql (PostgreSQL) và SQLite. Đang chạy kiểm thử với SQLite local.
- **Required action:** Cấp database PostgreSQL trên Supabase Cloud để lưu trữ dữ liệu bền vững.
- **Where to click:** [https://supabase.com/dashboard](https://supabase.com/dashboard) → **New Project** → Đặt tên `visionary-prod-db` → Chọn Region: **Southeast Asia (Singapore)**.
- **Required non-secret identifiers:**
  - Project Reference ID (dạng `xyzabcdefgh...`)
  - Host URI: `aws-0-ap-southeast-1.pooler.supabase.com`
  - Port: `6543` (Transaction Pooler) hoặc `5432` (Direct)
- **Secret name:**
  - Database Password (mật khẩu người dùng PostgreSQL `postgres`)
- **Secure entry location:** Nhập trực tiếp vào biến `ConnectionStrings__DefaultConnection` trong Render hoặc Oracle VM.
- **What I need to do:**
  1. Tạo project Supabase miễn phí tại vùng Singapore.
  2. Vào mục **Settings** → **Database** → Sao chép URI kết nối dạng Pooler (`Port 6543`).
  3. Gắn URI này vào biến môi trường của Backend Cloud.
- **What Antigravity will do:**
  - Tự động thực thi `db.Database.EnsureCreatedAsync()` và migration schema (34 bảng, quan hệ khóa ngoại, index tìm kiếm) ngay khi API khởi động trên Cloud.
- **Priority:** **P0 – Bắt buộc để ba nền tảng (Web, WinForms, Android) chia sẻ cùng một nguồn dữ liệu thật**.
- **Blocking modules:** Khả năng đồng bộ chéo nền tảng khi tắt máy local.

---

## 3. DỊCH VỤ: GOOGLE CLOUD OAUTH 2.0 (GOOGLE IDENTITY LOGIN)

- **Service:** Google OAuth 2.0 Client Authentication.
- **Current status:** Backend `AuthController.GoogleLogin` đã tích hợp `Google.Apis.Auth` xác thực ID Token. Frontend đã có nút đăng nhập Google chuẩn Identity UX.
- **Required action:** Đăng ký OAuth Client ID trên Google Cloud Console để kích hoạt nút đăng nhập Google thực tế.
- **Where to click:** [https://console.cloud.google.com/apis/credentials](https://console.cloud.google.com/apis/credentials) → **Create Credentials** → **OAuth client ID** → Loại: **Web application**.
- **Required non-secret identifiers:**
  - Authorized JavaScript origins:
    - `https://visionary-platform.vercel.app`
    - `https://visionary-global.vercel.app`
    - `http://localhost:3000`
  - Authorized redirect URIs:
    - `https://visionary-platform.vercel.app/api/auth/callback/google`
    - `https://visionary-global.vercel.app/api/auth/callback/google`
    - `http://localhost:3000/api/auth/callback/google`
  - Client ID (dạng `xxxx.apps.googleusercontent.com`)
- **Secret name:** `Authentication__Google__ClientId` (Frontend & Backend).
- **Secure entry location:** Vercel Environment Variables (`NEXT_PUBLIC_GOOGLE_CLIENT_ID`).
- **What I need to do:**
  1. Tạo OAuth Client ID trên Google Cloud Console theo các URL trên.
  2. Nhập Client ID vào Vercel Settings → Environment Variables.
- **What Antigravity will do:**
  - Tự động nhận diện token từ Google, tạo mới hồ sơ sinh viên DNTU nếu lần đầu đăng nhập, và cấp JWT phiên chuẩn mực.
- **Priority:** **P1 – Nâng cấp trải nghiệm người dùng sinh viên DNTU** (Đăng ký/đăng nhập email & mật khẩu đã hoạt động 100%).
- **Blocking modules:** Tính năng "Đăng nhập nhanh bằng Google" trên Web và Android.

---

## 4. DỊCH VỤ: VERCEL WORKSPACE `visionary19`

- **Service:** Frontend Next.js 14 Production Edge Hosting.
- **Current status:** **100% HOÀN TẤT & HOẠT ĐỘNG THỰC TẾ**.
  - Project: `visionary-platform`
  - Workspace: `visionary19`
  - Domain chính thức: [https://visionary-platform.vercel.app](https://visionary-platform.vercel.app)
  - Domain phụ: [https://visionary-global.vercel.app](https://visionary-global.vercel.app)
  - SSO Protection: Đã tắt (Public Access 100%).
  - Same-Origin BFF Proxy: `/api/[...path]` hoạt động hoàn hảo.
- **Required action:** Duy trì đồng bộ khi push code mới.
- **Required non-secret identifiers:** Scope `visionary19`, project `visionary-platform`.
- **What I need to do:** Không cần thao tác thủ công, Antigravity tự động build và deploy qua Vercel CLI.
- **Priority:** Hoàn tất.
- **Blocking modules:** Không.
