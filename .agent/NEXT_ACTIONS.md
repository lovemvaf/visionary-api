# NEXT ACTIONS – VISIONARY ECOSYSTEM

## 1. Hệ thống đã hoàn tất và kiểm chứng (Completed & Verified)
- [x] Phase 1: Khảo sát, thiết kế kiến trúc và khởi tạo hệ thống state (.agent/, docs/)
- [x] Phase 2: Xây dựng Backend ASP.NET Core 8 Web API (`backend/Visionary.sln`, 9/9 xUnit tests PASS)
- [x] Phase 3: Hoàn thiện Website Next.js 14 App Router (`frontend/`, 16/16 routes compiled thành công)
- [x] Phase 4: Xây dựng Data Automation Service kết nối GitHub REST API, Hugging Face API, RSS Feeds
- [x] Phase 5: Triển khai Website lên Vercel Cloud Workspace `visionary19`
- [x] Phase 6: Xây dựng và kiểm thử phần mềm Quản trị Desktop Windows Forms C# (`desktop/Visionary.Desktop`, 0 lỗi, 0 cảnh báo)
- [x] Phase 7: Xây dựng và biên dịch ứng dụng Di động Android Native Java (`mobile/VisionaryAndroid`, Gradle 8.4, Retrofit, Material 3)
- [x] Phase 8: Đồng bộ hợp đồng API ba nền tảng, hoàn thiện bộ 12 tài liệu kỹ thuật và báo cáo nghiệm thu toàn diện
- [x] Phase 9: Cấu hình tên miền chuyên nghiệp Vercel: `https://visionary-platform.vercel.app` (Alias: `https://visionary-global.vercel.app`)
- [x] Phase 10: Khởi tạo và liên kết GitHub Monorepo: `https://github.com/lovemvaf/visionary-api` (Owner: `lovemvaf`)
- [x] Phase 11: Thiết lập 5 GitHub Actions Workflows (Frontend, Backend, Desktop, Android, Security)
- [x] Phase 12: Tăng cường an toàn database production (chặn silent fallback), tích hợp Google Login & SEO Sitemap
- [x] Phase 13: Xử lý triệt để lỗi "Failed to fetch" qua Same-Origin BFF Proxy Route Handler `/api/[...path]` trên Vercel
- [x] Phase 14: Kích hoạt Cloudflare Public HTTPS Tunnel cho ASP.NET Core Web API và cấu hình biến môi trường Vercel
- [x] Phase 15: Kiểm thử E2E Browser & REST API luồng Đăng ký, Đăng nhập và điều hướng Admin Dashboard thành công
- [x] Phase 16: Soạn thảo tài liệu chuẩn hóa thông số dịch vụ ngoại vi (Google, Supabase, Render, Redis) tại `docs/REQUIRED_ACCESS.md`

## 2. Các kịch bản trình diễn khi báo cáo đồ án Web API (TH71108):
1. **Trình diễn Đăng nhập & Bảng Quản trị (Admin Portal):**
   - Truy cập: `https://visionary-platform.vercel.app/auth/login`
   - Đăng nhập với tài khoản Quách Khoa Đức hoặc nhấn nhanh tài khoản kiểm định.
   - Trình chiếu hệ thống điều hướng trực tiếp vào Bảng Quản trị `/dashboard/admin`, hiển thị 6 chỉ số thời gian thực từ cơ sở dữ liệu.
2. **Trình diễn Đăng ký Tài khoản Sinh viên Mới:**
   - Mở `https://visionary-platform.vercel.app/auth/register`, điền thông tin sinh viên và đăng ký.
   - Chứng minh tài khoản được tạo ngay trong database và tự động chuyển về trang cá nhân.
3. **Trình diễn Đồng bộ Ba Nền tảng (One Backend – Three Platforms):**
   - Mở song song Web Next.js, Desktop Windows Forms và Android (tất cả đều kết nối cùng một Backend API).
4. **Trình chiếu Báo cáo Cấu hình Dịch vụ:**
   - Mở file `docs/REQUIRED_ACCESS.md` để giải trình về kiến trúc sẵn sàng kết nối Google Cloud OAuth, Supabase PostgreSQL và Render Docker.
