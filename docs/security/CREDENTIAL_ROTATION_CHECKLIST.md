# QUY TRÌNH XOAY VÒNG VÀ CẬP NHẬT THÔNG TIN XÁC THỰC BẢO MẬT
## CREDENTIAL ROTATION & CONTAINMENT SOP
**Mã dự án:** VISIONARY – Hệ thống Quản lý Hoạt động Hội nhập (TH71108)  
**Mục tiêu:** Hướng dẫn từng bước cho Chủ sở hữu hệ thống thực hiện thu hồi mật khẩu/token cũ và cấu hình an toàn trên các nền tảng Cloud  
**Nguyên tắc an ninh:** Không gửi mật khẩu mới qua kênh chat AI. Chủ sở hữu trực tiếp cấu hình trên trang quản trị nhà cung cấp dịch vụ.  

---

## BƯỚC 1: ĐỔI MẬT KHẨU CƠ SỞ DỮ LIỆU SUPABASE (ƯU TIÊN P0)

Do chuỗi kết nối Supabase cũ đã từng xuất hiện trong lịch sử commit, việc thay đổi mật khẩu là bắt buộc:

1. Đăng nhập vào trang quản trị Supabase: [https://supabase.com/dashboard](https://supabase.com/dashboard)
2. Chọn dự án: `rylazywrudutcjnvutte` (hoặc project tương ứng của VISIONARY).
3. Điều hướng tới: **Project Settings** (biểu tượng bánh răng) ➔ **Database**.
4. Cuộn xuống phần **Database password** ➔ Nhấn **Reset database password**.
5. Nhập mật khẩu mới an toàn (tối thiểu 16 ký tự bao gồm chữ hoa, chữ thường, chữ số và ký tự đặc biệt). *Lưu ý: Lưu mật khẩu an toàn vào trình quản lý mật khẩu cá nhân (ví dụ: Bitwarden / 1Password).*
6. Lưu lại chuỗi kết nối mới dạng Transaction Pooler (Port 6543 hoặc 5432 IPv4):
   ```text
   Host=aws-0-ap-southeast-1.pooler.supabase.com;Port=5432;Database=postgres;Username=postgres.rylazywrudutcjnvutte;Password=<MAT_KHAU_MOI_CUA_BAN>;SSL Mode=Require;Trust Server Certificate=true;Timeout=30;Keepalive=30
   ```

---

## BƯỚC 2: CẬP NHẬT BIẾN MÔI TRƯỜNG TRÊN RENDER CLOUD HOSTING (BACKEND)

1. Đăng nhập trang quản trị Render: [https://dashboard.render.com](https://dashboard.render.com)
2. Chọn dịch vụ Web Service: **visionary-api**.
3. Điều hướng tới mục **Environment** trong menu bên trái.
4. Cập nhật các biến sau (chọn chế độ Secret/Hidden):
   - **`ConnectionStrings__DefaultConnection`**: Dán chuỗi kết nối Supabase mới đã tạo ở Bước 1.
   - **`JWT_SECRET`**: Tạo một chuỗi ngẫu nhiên dài ít nhất 32 ký tự (ví dụ dùng PowerShell: `[System.Convert]::ToBase64String((1..32 | % { [byte](Get-Random -Max 256) }))`).
   - **`Jwt__Key`**: Đặt cùng giá trị với `JWT_SECRET`.
   - **`ADMIN_SEED_PASSWORD`**: (Tùy chọn) Nhập mật khẩu quản trị viên cấp phát cho nhóm để khởi tạo tài khoản ban đầu nếu cần.
5. Nhấn **Save Changes**. Render sẽ tự động trigger một đợt triển khai mới (Redeploy) với các biến bí mật đã được bảo vệ.

---

## BƯỚC 3: CẬP NHẬT BIẾN MÔI TRƯỜNG TRÊN VERCEL (FRONTEND WEB)

1. Đăng nhập trang quản trị Vercel: [https://vercel.com/visionary19](https://vercel.com/visionary19)
2. Chọn project: **visionary-platform**.
3. Điều hướng tới: **Settings** ➔ **Environment Variables**.
4. Rà soát và cấu hình:
   - **`API_BASE_URL`**: Đường dẫn máy chủ Backend thật (ví dụ URL Render: `https://visionary-api.onrender.com` hoặc domain nội bộ bảo mật). Loại bỏ hoàn toàn các URL đường hầm Cloudflare Tunnel thử nghiệm tạm thời.
   - **`NEXT_PUBLIC_API_URL`**: Cấu hình tương tự hoặc trỏ qua proxy Next.js `/api/...`.
5. Đảm bảo các biến được tích chọn cho cả **Production**, **Preview**, và **Development**.
6. Nhấn **Save** và kích hoạt **Redeploy** trên Vercel để áp dụng cấu hình mới.

---

## BƯỚC 4: THU HỒI HIỆU LỰC JWT TOKEN VÀ PHIÊN LÀM VIỆC CŨ

Khi `JWT_SECRET` trên máy chủ Backend được đổi sang giá trị mới:
1. Tất cả các JWT token cũ do khóa bí mật cũ ký sẽ **ngay lập tức bị từ chối** (`HTTP 401 Unauthorized`) bởi middleware xác thực ASP.NET Core (`TokenValidationParameters` phát hiện sai chữ ký điện tử).
2. Toàn bộ các phiên đăng nhập trước đây của mọi người dùng (bao gồm các phiên thử nghiệm) bị vô hiệu hóa an toàn, ngăn chặn hoàn toàn nguy cơ kẻ gian lợi dụng token cũ.
3. Người dùng và ban quản trị chỉ cần đăng nhập lại với mật khẩu mới để nhận JWT token mới được ký bằng khóa bí mật mới.

---

## BƯỚC 5: XÁC MINH VẬN HÀNH SAU XOAY VÒNG (POST-ROTATION VERIFICATION)

| Hạng mục kiểm tra | Thao tác thực hiện | Kết quả mong đợi | Xác nhận |
|---|---|---|---|
| **Health Check Backend** | Truy cập `GET /health/ready` | Trả về `{"status":"Ready","database":"Connected"}` (HTTP 200) | [ ] |
| **Đăng nhập Web API** | Gọi `POST /api/auth/login` với tài khoản quản trị | Nhận được JWT Token mới hợp lệ | [ ] |
| **Đăng nhập Website** | Đăng nhập trên `https://visionary-platform.vercel.app` | Điều hướng thành công vào Dashboard | [ ] |
| **Đăng nhập WinForms** | Mở ứng dụng Desktop, nhập email và mật khẩu mới | Đăng nhập và tải danh sách sự kiện bình thường | [ ] |
| **Đăng nhập Android** | Mở ứng dụng Android trên máy ảo/điện thoại, đăng nhập | Kết nối thành công tới Backend API | [ ] |
