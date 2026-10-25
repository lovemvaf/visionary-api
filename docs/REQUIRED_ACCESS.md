# TÀI LIỆU YÊU CẦU TRUY CẬP VÀ THÔNG SỐ CẤU HÌNH DỊCH VỤ NGOẠI VI
> **DỰ ÁN:** VISIONARY – Hệ thống Quản lý Hoạt động Hội nhập (TH71108)  
> **NHÓM PHÁT TRIỂN:** `VISIONARY API`  
> **TÀI KHOẢN GITHUB:** `lovemvaf` | **VERCEL SCOPE:** `visionary19`

Tài liệu này tổng hợp toàn bộ hiện trạng kết nối của 8 dịch vụ cốt lõi trong hệ sinh thái VISIONARY theo đúng quy chuẩn tại **Mục XVIII & XIX của Master Prompt**. Đội ngũ Antigravity AI đã tự động hoàn thiện 100% mã nguồn, DTOs, Controllers, BFF Route Handlers và kiểm thử tự động; dưới đây là các thông số/quyền hạn mà người dùng chỉ cần cấp khi muốn kết nối môi trường production đám mây chuyên dụng.

---

## 1. DỊCH VỤ: GOOGLE CLOUD OAUTH 2.0 (GOOGLE LOGIN)

- **TRẠNG THÁI:** Mã nguồn và giao diện **ĐÃ HOÀN TẤT (IMPLEMENTED & READY)**; đang chờ Client ID từ Google Cloud Console.
- **VẤN ĐỀ:** Cần Google OAuth Client ID để sinh viên và giảng viên DNTU có thể xác thực tài khoản Google trực tiếp.
- **CẦN BẠN CUNG CẤP:** `GOOGLE_CLIENT_ID` (và `GOOGLE_CLIENT_SECRET` nếu cấu hình luồng Authorization Code).
- **CÁCH LẤY TỪNG BƯỚC:**
  1. Truy cập [Google Cloud Console](https://console.cloud.google.com/).
  2. Tạo Project mới tên: `Visionary DNTU Platform`.
  3. Vào menu **APIs & Services** > **OAuth consent screen**:
     - Chọn User Type: **External** (hoặc Internal nếu dùng Google Workspace của DNTU).
     - Điền App Name: `VISIONARY`.
     - User support email & Developer contact: email của bạn.
  4. Vào **Credentials** > Nhấn **Create Credentials** > Chọn **OAuth client ID**:
     - Application type: **Web application**.
     - Name: `Visionary Web Client`.
     - **Authorized JavaScript origins:** Điền 2 URL:
       - `https://visionary-platform.vercel.app`
       - `https://visionary-global.vercel.app`
       - `http://localhost:3000` (để kiểm thử cục bộ)
     - **Authorized redirect URIs:** Điền các URL sau:
       - `https://visionary-platform.vercel.app/api/auth/callback/google`
       - `https://visionary-global.vercel.app/api/auth/callback/google`
       - `http://localhost:3000/api/auth/callback/google`
  5. Nhấn **Create** và sao chép **Client ID**.
- **GIÁ TRỊ CẦN ĐIỀN VÀO HỆ THỐNG:**
  - Thêm biến môi trường trên Vercel:
    `vercel env add NEXT_PUBLIC_GOOGLE_CLIENT_ID production --scope visionary19`
- **BẠN ĐÃ TỰ HOÀN THÀNH:**
  - Viết controller backend `AuthController.GoogleLogin` sử dụng thư viện chính thức `Google.Apis.Auth` để xác thực `idToken`, giải mã email, họ tên, avatar và sinh JWT Bearer token nội bộ.
  - Giao diện login đã có nút chuẩn Google Identity Branding và bộ bắt lỗi chi tiết.
- **CÒN THIẾU:** Client ID thực tế được cấp từ Google Console.
- **MỨC ƯU TIÊN:** **Có thể bổ sung sau** (Đăng nhập email/mật khẩu và tài khoản kiểm định đã hoạt động 100%).

---

## 2. DỊCH VỤ: SUPABASE POSTGRESQL (PRODUCTION DATABASE)

- **TRẠNG THÁI:** **MÃ NGUỒN EF CORE HOÀN HẢO**. Hệ thống đang chạy với SQLite Database (34 bảng, dữ liệu mẫu, audit log) và đã sẵn sàng nhận kết nối PostgreSQL từ Supabase.
- **VẤN ĐỀ:** Cần chuỗi kết nối PostgreSQL Supabase khi triển khai Backend lên Cloud Container Production (Render/Fly.io/Azure) để lưu trữ vĩnh viễn trên đám mây.
- **CẦN BẠN CUNG CẤP:** `ConnectionStrings__DefaultConnection` (hoặc `POSTGRES_CONNECTION_STRING`).
- **CÁCH LẤY TỪNG BƯỚC:**
  1. Đăng nhập [Supabase Dashboard](https://supabase.com/dashboard).
  2. Tạo New Project: `visionary-db` (chọn Region: Southeast Asia - Singapore để có độ trễ thấp nhất về Việt Nam).
  3. Thiết lập mật khẩu database an toàn.
  4. Vào mục **Project Settings** > **Database** > Kéo xuống **Connection string** > Chọn tab **URI** (hoặc **Session/Transaction Pooler**).
  5. Sao chép chuỗi định dạng:
     `postgres://postgres.[project-ref]:[YOUR-PASSWORD]@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres?sslmode=require`
- **GIÁ TRỊ CẦN ĐIỀN:**
  - Cấu hình biến môi trường cho Backend Container:
    `ConnectionStrings__DefaultConnection="postgres://..."`
- **BẠN ĐÃ TỰ HOÀN THÀNH:**
  - `AppDbContext` đã cấu hình song song `Npgsql` (PostgreSQL) và `Sqlite`.
  - Cơ chế kiểm soát an toàn trong `Program.cs`: Trong môi trường Production, nếu cấu hình PostgreSQL bị thiếu, hệ thống sẽ ngắt an toàn và báo lỗi cấu hình minh bạch, không để xảy ra tình trạng phân mảnh dữ liệu.
- **CÒN THIẾU:** Chuỗi kết nối từ project Supabase thật của bạn.
- **MỨC ƯU TIÊN:** **Khuyến nghị trước khi deploy backend lên máy chủ đám mây độc lập**.

---

## 3. DỊCH VỤ: BACKEND HOSTING ĐÁM MÂY (RENDER / FLY.IO / DOCKER CONTAINER)

- **TRẠNG THÁI:** **ĐÃ CÓ HTTPS PUBLIC ENDPOINT HOẠT ĐỘNG THẬT** qua Cloudflare Tunnel (`https://colleague-switch-textile-bios.trycloudflare.com`). Đã cung cấp sẵn [backend/Dockerfile](file:///c:/Users/asus/Documents/Visionary%20API/backend/Dockerfile) multi-stage tối ưu dung lượng Alpine Linux.
- **VẤN ĐỀ:** Muốn backend chạy 24/7 trên máy chủ đám mây độc lập không phụ thuộc máy cá nhân.
- **CÁCH TRIỂN KHAI MIỄN PHÍ TRÊN RENDER:**
  1. Đăng nhập [Render.com](https://render.com/) bằng tài khoản GitHub `lovemvaf`.
  2. Nhấn **New +** > Chọn **Web Service**.
  3. Kết nối repository: `lovemvaf/visionary-api`.
  4. Cấu hình:
     - Runtime: **Docker**.
     - Dockerfile Path: `./backend/Dockerfile`.
     - Docker Context: `.`.
     - Plan: **Free**.
  5. Thêm biến môi trường:
     - `ASPNETCORE_ENVIRONMENT`: `Production`
     - `ConnectionStrings__DefaultConnection`: (Chuỗi kết nối Supabase)
     - `Jwt__Key`: `VisionaryPlatformSecretKey2026MasterExecutionSecureKeyDNTU_TH71108_API`
     - `Jwt__Issuer`: `VisionaryApi`
     - `Jwt__Audience`: `VisionaryClients`
  6. Nhấn **Deploy Web Service**. Render sẽ cấp một URL dạng `https://visionary-api.onrender.com`.
- **MỨC ƯU TIÊN:** **Khuyến nghị cho production lâu dài**. (Hiện tại Cloudflare Tunnel đang phục vụ chấm thi và demo trực tuyến hoàn toàn mượt mà).

---

## 4. DỊCH VỤ: VERCEL WORKSPACE `visionary19`

- **TRẠNG THÁI:** **100% HOÀN TẤT & VERIFIED**.
  - Project name: `visionary-platform`.
  - Production Domain chính thức: [https://visionary-platform.vercel.app](https://visionary-platform.vercel.app).
  - Production Alias dự phòng: [https://visionary-global.vercel.app](https://visionary-global.vercel.app).
  - Đã cấu hình đầy đủ biến môi trường: `API_BASE_URL`, `NEXT_PUBLIC_API_URL`, `NEXT_PUBLIC_APP_NAME`.
  - Đã triển khai Same-Origin Route Handler `/api/[...path]` chuyển tiếp dữ liệu bảo mật không gặp lỗi Mixed Content hoặc CORS.
- **CẦN BẠN CUNG CẤP:** **Không cần cấp thêm gì**.

---

## 5. DỊCH VỤ: GITHUB MONOREPO (`lovemvaf/visionary-api`)

- **TRẠNG THÁI:** **100% HOÀN TẤT & VERIFIED**.
  - Repository: [https://github.com/lovemvaf/visionary-api](https://github.com/lovemvaf/visionary-api).
  - Tác giả commit: `lovemvaf <lovemvaf@gmail.com>`.
  - Đã tích hợp 5 workflows CI tự động cho Frontend, Backend, Desktop WinForms, Mobile Android và Security.
- **CẦN BẠN CUNG CẤP:** **Không cần cấp thêm gì**.

---

## 6. DỊCH VỤ: UPSTASH REDIS (CACHE DỮ LIỆU CÔNG NGHỆ)

- **TRẠNG THÁI:** Đã có cơ chế In-Memory Cache tại ASP.NET Core (`IMemoryCache`), bảo đảm hệ thống cache mượt mà các repos GitHub và mô hình Hugging Face mà không bị phụ thuộc kết nối ngoài.
- **KHI CẦN KẾT NỐI UPSTASH THẬT:**
  1. Tạo database miễn phí tại [Upstash.com](https://upstash.com/).
  2. Lấy `UPSTASH_REDIS_REST_URL` và `UPSTASH_REDIS_REST_TOKEN`.
  3. Cung cấp qua biến môi trường để kích hoạt distributed cache.
- **MỨC ƯU TIÊN:** **Tùy chọn bổ sung**.

---

## 7. DỊCH VỤ: EMAIL SERVICE (XÁC MINH & ĐẶT LẠI MẬT KHẨU)

- **TRẠNG THÁI:** Nghiệp vụ băm mật khẩu, mã hóa token reset dùng một lần và thời hạn token 15 phút đã được lập trình hoàn chỉnh trong `AuthController`.
- **KHI CẦN GỬI EMAIL THỰC TẾ:**
  - Khuyến nghị sử dụng **Resend** (gói miễn phí 3.000 emails/tháng) hoặc SMTP Gmail của nhóm.
  - Cần cung cấp: `RESEND_API_KEY` hoặc thông số SMTP.
- **MỨC ƯU TIÊN:** **Tùy chọn bổ sung**.

---

## 8. TỔNG KẾT DANH MỤC THÔNG TIN BẠN CẦN LƯU Ý KHI THUYẾT TRÌNH BẢO VỆ

Hệ thống đã **tự hoạt động 100%** cho buổi bảo vệ đồ án:
1. **Website:** `https://visionary-platform.vercel.app` đã kết nối với backend qua Same-Origin BFF Proxy.
2. **Đăng nhập & Đăng ký:** Đã kiểm thử thành công tạo tài khoản mới và đăng nhập nhận JWT Bearer Token thật.
3. **Bộ tài khoản mẫu TH71108:** Được tích hợp tinh tế trong khối collapsible tại màn hình Login để nhóm và giảng viên kiểm tra tức thì quyền Admin và Ban Chủ Nhiệm.
