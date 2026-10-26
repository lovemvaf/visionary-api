# BÁO CÁO BẢO MẬT CƠ SỞ DỮ LIỆU VÀ QUẢN LÝ DỮ LIỆU SUPABASE
## DATABASE & SUPABASE SECURITY AUDIT REPORT
**Mã dự án:** VISIONARY – Hệ thống Quản lý Hoạt động Hội nhập (TH71108)  
**Hệ quản trị CSDL:** Supabase PostgreSQL 16 (Production) & SQLite (Local Development/Test)  
**Tầng truy cập dữ liệu:** Entity Framework Core 8  

---

## 1. NGUYÊN TẮC TRUY CẬP CƠ SỞ DỮ LIỆU

Hệ thống VISIONARY áp dụng kiến trúc **Single Point of Database Access via Backend Web API**:
1. **Không có bất kỳ ứng dụng client nào (Next.js Web, Windows Forms Desktop, Android Mobile) được cấp quyền kết nối trực tiếp vào cơ sở dữ liệu.**
2. Tất cả mọi truy vấn và thao tác ghi đều bắt buộc phải thông qua lớp Web API trung gian được bảo vệ bởi xác thực JWT và kiểm tra quyền hạn RBAC.
3. Không cung cấp tài khoản `postgres` superuser hoặc direct connection string cho bất kỳ thành phần nào ngoài dịch vụ Backend trên Render.

---

## 2. RÀ SOÁT LỖ HỔNG CƠ SỞ DỮ LIỆU (DATABASE VULNERABILITY AUDIT)

### 2.1. Phòng chống SQL Injection (SQLi)
- Toàn bộ các thao tác truy vấn dữ liệu trong `Visionary.Infrastructure` và `Visionary.Api` đều sử dụng **Entity Framework Core với LINQ và Parameterized Queries**:
  - Không có bất kỳ câu lệnh `FromSqlRaw` hoặc `ExecuteSqlRaw` nào sử dụng kỹ thuật cộng chuỗi (string concatenation) với dữ liệu do người dùng nhập vào.
  - Các tham số tìm kiếm (ví dụ: keyword, slug, email) đều được biên dịch thành biến tham số `@p0, @p1` bởi Npgsql/Microsoft.Data.Sqlite driver.
  - **Kết luận:** Nguy cơ SQL Injection đạt mức **0% (Không thể khai thác)**.

### 2.2. Mã hóa Dữ liệu Nhạy cảm (Data Encryption)
- **Mã hóa trên đường truyền (In-Transit):**
  - Mọi kết nối từ Backend tới Supabase bắt buộc sử dụng cờ `SSL Mode=Require;Trust Server Certificate=true`. Dữ liệu trao đổi giữa máy chủ ứng dụng và CSDL đều được mã hóa bằng TLS.
- **Mã hóa mật khẩu người dùng (At-Rest):**
  - Mật khẩu người dùng được băm (hashing) bằng thuật toán **BCrypt** (`IPasswordHasher` với Work Factor tiêu chuẩn và Salt ngẫu nhiên theo từng người dùng).
  - Hệ thống không bao giờ lưu trữ mật khẩu ở dạng văn bản rõ (plaintext).
  - Không có chức năng khôi phục mật khẩu lộ ngược mật khẩu cũ; chỉ hỗ trợ cấp lại hoặc đổi mật khẩu sau khi xác thực danh tính.

### 2.3. Quản lý Quyền Hạn Supabase (Supabase Least Privilege)
- Không lưu trữ `SUPABASE_SERVICE_ROLE_KEY` trong mã nguồn frontend hoặc ứng dụng mobile/desktop.
- Khóa `anon` của Supabase nếu được tích hợp trong tương lai chỉ được áp dụng kèm theo chính sách **Row-Level Security (RLS)** nghiêm ngặt.
- Toàn bộ kết nối hiện tại đi qua Transaction Pooler IPv4 trên cổng 5432/6543 của Supabase, bảo đảm độ trễ thấp và kiểm soát số lượng kết nối đồng thời.

---

## 3. CHÍNH SÁCH BẢO LƯU VÀ KHÔI PHỤC DỮ LIỆU (BACKUP & RESTORE)

1. **Bảo toàn dữ liệu môn học:** Nghiêm cấm chạy lệnh `DROP DATABASE`, `DROP TABLE`, hoặc xóa hàng loạt trên môi trường máy chủ. Quá trình khởi tạo cơ sở dữ liệu `DbInitializer` chỉ tạo bảng nếu chưa có (`CreateTablesAsync` / `EnsureCreatedAsync`) và không bao giờ xóa dữ liệu đã tồn tại.
2. **Khôi phục từ xa:** Supabase Cloud tự động thực hiện snapshot sao lưu định kỳ hàng ngày (Daily automated backups). Trong trường hợp xảy ra sự cố thao tác sai, quản trị viên có thể sử dụng chức năng Point-in-Time Recovery của Supabase để khôi phục trạng thái dữ liệu nguyên vẹn.
