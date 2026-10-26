# DANH MỤC THÔNG TIN XÁC THỰC TỪNG BỊ LỘ VÀ TÌNH TRẠNG XỬ LÝ
## INVENTORY OF EXPOSED CREDENTIALS & REMEDIATION STATUS
**Mã dự án:** VISIONARY – Hệ thống Quản lý Hoạt động Hội nhập (TH71108)  
**Tài liệu:** Bảng kiểm kê thông tin nhạy cảm đã phát hiện, mức độ ảnh hưởng và hành động xử lý  
**Phân loại:** Internal Security Audit – Sanitized (Đã khử nhạy cảm toàn bộ giá trị thực)  

---

## 1. NGUYÊN TẮC QUẢN LÝ THÔNG TIN NHẠY CẢM

Mọi thông tin xác thực (Credentials, Passwords, Connection Strings, Private Keys, JWT Signing Keys) từng xuất hiện trong mã nguồn hoặc lịch sử commit đều được định danh cụ thể, phân tích phạm vi ảnh hưởng và đưa vào quy trình xử lý khẩn cấp:
- **Tuyệt đối không lưu trữ giá trị bí mật chưa che chắn trong báo cáo này.**
- **Mọi giá trị được khử nhạy cảm theo chuẩn mặt nạ ký tự (ví dụ: `Ducdatabase***`, `Visionary***`).**

---

## 2. BẢNG KIỂM KÊ CHI TIẾT (EXPOSED SECRETS INVENTORY)

| ID | Loại bí mật | Vị trí phát hiện (File & Commit) | Giá trị đã khử nhạy cảm | Phạm vi tác động | Biện pháp kỹ thuật đã thực hiện | Yêu cầu xoay vòng (Rotation) |
|---|---|---|---|---|---|---|
| **SEC-01** | Database Password (PostgreSQL) | `render.yaml` (Commits: `199ef83`, `2742b34`) | `Password=Ducdatabase272040***` | Cơ sở dữ liệu Supabase Production Pooler | Đã xóa khỏi `render.yaml`, thay bằng `sync: false` để cấu hình bí mật qua Render Dashboard | **Bắt buộc:** Chủ sở hữu đổi mật khẩu database trên Supabase Console |
| **SEC-02** | Local Database Password | `docker-compose.yml` (Commit gốc) | `POSTGRES_PASSWORD=VisionarySecureDb***` | Container PostgreSQL nội bộ | Đã thay thế bằng biến môi trường `${POSTGRES_PASSWORD}` với fallback an toàn cục bộ | **Hoàn tất:** Đã chuyển sang biến môi trường và đóng cổng truy cập công khai |
| **SEC-03** | JWT Signing Secret | `render.yaml`, `docker-compose.yml`, `appsettings.json`, `JwtService.cs` | `VisionaryPlatformSecretKey2026Master***` | Chữ ký phiên làm việc JWT cho toàn bộ Client | Đã thay bằng placeholder trong cấu hình; bắt buộc kiểm tra runtime trong Production cấm sử dụng key này | **Bắt buộc:** Cấp phát khóa JWT mới ngẫu nhiên (>= 32 ký tự) trên Render & Vercel |
| **SEC-04** | Admin/Member Seed Passwords | `README.md`, `OPERATIONS_MANUAL.md` | `Visionary@2026` | Các tài khoản kiểm thử mặc định ban đầu | Đã xóa cột mật khẩu khỏi tài liệu; chuyển sang cơ chế quản lý qua `ADMIN_SEED_PASSWORD` | **Hoàn tất:** Đã xóa khỏi tài liệu, DB seed production tự sinh mật khẩu ngẫu nhiên |
| **SEC-05** | UI Hardcoded Credentials | `frontend/src/app/auth/login/page.tsx` | `Visionary@2026` | Gói bundle JavaScript phía client (Next.js) | Đã xóa hàm gán mật khẩu tự động; chỉ hỗ trợ gợi ý email đăng nhập | **Hoàn tất:** Bundle Next.js đã được biên dịch lại, không còn chứa chuỗi mật khẩu |
| **SEC-06** | Desktop App Hardcoded Password | `desktop/Visionary.Desktop/Forms/LoginForm.cs` | `Visionary@2026` | Ứng dụng Windows Forms | Đã xóa Text khởi tạo của ô mật khẩu và xóa logic tự động gán khi nhấn nút tài khoản mẫu | **Hoàn tất:** Dự án Desktop biên dịch lại sạch sẽ |
| **SEC-07** | Android App Hardcoded Password | `mobile/.../activity_login.xml`, `LoginActivity.java` | `Visionary@2026` | Ứng dụng Android APK | Đã xóa thuộc tính `android:text` trong layout và xóa lệnh `setText` mật khẩu trong Java code | **Hoàn tất:** Mã nguồn Android đã được làm sạch hoàn toàn |

---

## 3. PHÂN TÍCH RỦI RO LỊCH SỬ GIT (HISTORICAL RISK ANALYSIS)

1. **Về file `.env`:** Quét toàn bộ lịch sử Git (`git log --all --name-only -- "**/.env*"`) xác nhận **chưa từng có file `.env` hoặc `.env.local` thực tế nào bị commit vào repository**.
2. **Về `render.yaml`:** Chuỗi kết nối Supabase đã tồn tại trong commit `199ef83` và `2742b34`. Mặc dù file hiện hành đã được làm sạch, bất kỳ ai có quyền đọc lịch sử repository (khi repository đang ở trạng thái Public) đều có thể xem diff của commit này.
3. **Kết luận kỹ thuật:** Việc xóa mật khẩu trong commit mới nhất không làm mất mật khẩu trong lịch sử Git cũ. Do đó, **biện pháp bảo vệ cốt lõi và triệt để nhất là thay đổi (Rotate) mật khẩu database tại nguồn (Supabase)**. Khi mật khẩu cũ đã bị vô hiệu hóa trên nhà cung cấp cloud, dữ liệu trong commit cũ trở nên vô giá trị đối với kẻ tấn công.
