# DANH MỤC THÔNG TIN CẤU HÌNH BỔ SUNG (PENDING CONFIGURATION)

Hệ thống VISIONARY được thiết kế với cơ chế tự phục hồi và tương thích độc lập (Resilient Multi-Provider Architecture). Toàn bộ mã nguồn, cơ sở dữ liệu, API và ứng dụng ba nền tảng đều **hoạt động ngay lập tức** ở chế độ phát triển nội bộ. Khi cần kết nối lên các hạ tầng đám mây thực tế, người dùng có thể bổ sung các khóa sau đây vào biến môi trường:

| Tên dịch vụ | Mục đích | Biến cấu hình | Cách lấy / Nơi cấu hình an toàn | Bắt buộc ngay? | Phần hệ thống bị ảnh hưởng nếu chưa có | Biện pháp thay thế tự động đã hoạt động |
|---|---|---|---|---|---|---|
| **Supabase PostgreSQL** | Lưu trữ CSDL đám mây tập trung | `ConnectionStrings__DefaultConnection` | Lấy URI từ Supabase Project Settings -> Database -> Connection URI. Đặt trong `appsettings.json` hoặc biến môi trường server. | KHÔNG | CSDL lưu trên Supabase Cloud | Hệ thống tự động chuyển sang CSDL SQLite / In-Memory Provider để biên dịch, kiểm thử và chạy thật 100% không gián đoạn. |
| **Google Cloud OAuth** | Đăng nhập tài khoản Google | `Authentication__Google__ClientId` | Lấy từ Google Cloud Console -> APIs & Credentials -> OAuth 2.0 Client ID. | KHÔNG | Xác thực tài khoản Google thật | Hệ thống hỗ trợ đăng ký/đăng nhập đầy đủ bằng Email & Mật khẩu chuẩn mã hóa; đồng thời có luồng kiểm thử Google IdToken an toàn trong Development. |
| **Upstash Redis** | Cache phân tán và Rate Limit tốc độ cao | `Redis__ConnectionString` | Lấy từ Upstash Console -> Databases -> Connect -> REST/TLS URI. | KHÔNG | Cache phân tán qua mạng Internet | Hệ thống tự động chuyển sang `IMemoryCache` (bộ nhớ RAM) và in-memory rate limiter với cùng API contract. |
| **GitHub Personal Token** | Mở rộng quota lấy dữ liệu Trending | `GitHub__Token` | Lấy từ GitHub Settings -> Developer settings -> Personal access tokens. | KHÔNG | Quota gọi API GitHub (60 req/h vs 5000 req/h) | Sử dụng kết nối nặc danh chuẩn với caching 6 tiếng, hoàn toàn không bị gián đoạn. |
