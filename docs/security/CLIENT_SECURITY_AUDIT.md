# BÁO CÁO BẢO MẬT CÁC ỨNG DỤNG CLIENT (WEB, WINDOWS FORMS & ANDROID)
## CLIENT-SIDE SECURITY AUDIT REPORT (NEXT.JS, WINFORMS, ANDROID)
**Mã dự án:** VISIONARY – Hệ thống Quản lý Hoạt động Hội nhập (TH71108)  
**Nền tảng kiểm toán:** Next.js 14 Web, Windows Forms .NET 8, Android SDK 34  

---

## 1. BẢO MẬT ỨNG DỤNG WEB (NEXT.JS 14 / TYPESCRIPT)

### 1.1. Rà soát Biến môi trường Client-side
- **Tiêu chuẩn:** Không để lộ server secret qua các biến có tiền tố `NEXT_PUBLIC_`.
- **Thực tế kiểm tra:**
  - `NEXT_PUBLIC_API_URL`: Trỏ tới URL API công khai của hệ thống (hợp lệ).
  - `NEXT_PUBLIC_APP_NAME`: Tên ứng dụng `VISIONARY` (không nhạy cảm).
  - `NEXT_PUBLIC_GOOGLE_CLIENT_ID`: Public OAuth Client ID dùng cho luồng xác thực Google Login tại trình duyệt (chuẩn thiết kế OAuth 2.0).
  - **Kết luận:** Không phát hiện bất kỳ API Secret, Database Connection String hay Private Key nào bị rò rỉ trong frontend bundle.

### 1.2. Loại bỏ Thông tin xác thực trong Giao diện Đăng nhập
- Trước đây, trang `/auth/login` có khối nút hỗ trợ kiểm định với hàm `fillQuickAccount` nhúng cứng mật khẩu `Visionary@2026`.
- **Khắc phục:** Đã loại bỏ hoàn toàn tham số mật khẩu khỏi hàm `fillQuickAccount`. Khối kiểm định hiện tại chỉ hỗ trợ tự động điền Email đại diện cho từng vai trò (`quachkhoaduc@visionary.dntu.edu.vn` và `vongocminhdat@visionary.dntu.edu.vn`), người kiểm thử phải tự nhập mật khẩu được cấp phát qua tài liệu bảo mật nội bộ.
- Chuỗi mật khẩu không còn tồn tại trong mã nguồn TypeScript cũng như trong bundle JavaScript đã biên dịch (`.next/static/chunks`).

---

## 2. BẢO MẬT ỨNG DỤNG DESKTOP (WINDOWS FORMS C# .NET 8)

### 2.1. Kiến trúc Kết nối
- Ứng dụng Desktop **hoàn toàn không chứa chuỗi kết nối cơ sở dữ liệu** (`ConnectionString`).
- Toàn bộ giao tiếp với dữ liệu đều thông qua lớp dịch vụ HTTP `ApiService`, sử dụng thư viện `HttpClient` để gọi RESTful API tới Backend.

### 2.2. Xóa bỏ Mật khẩu Hardcode
- Trong `LoginForm.cs`:
  - Thuộc tính `Text` của `_txtPassword` đã được xóa sạch (trước đây đặt mặc định `Visionary@2026`).
  - Các sự kiện click nút nhanh của Ban Chủ Nhiệm và Quản trị viên chỉ điền địa chỉ email và xóa trắng ô mật khẩu, đặt con trỏ nhập liệu vào ô mật khẩu kèm thông báo hướng dẫn.
  - Ô nhập mật khẩu bật thuộc tính `PasswordChar = '•'`, ngăn chặn nhìn trộm màn hình (Shoulder Surfing).

---

## 3. BẢO MẬT ỨNG DỤNG DI ĐỘNG (ANDROID JAVA SDK 34)

### 3.1. Rà soát Mã nguồn và Layout
- Trong `activity_login.xml`: Thuộc tính `android:text="Visionary@2026"` trong trường `etPassword` đã bị xóa bỏ hoàn toàn.
- Trong `LoginActivity.java`: Lệnh `etPassword.setText("Visionary@2026")` trong bộ lắng nghe sự kiện của các nút nhanh đã được xóa bỏ, thay bằng thao tác xóa trắng ô mật khẩu `etPassword.setText("")`.

### 3.2. Cấu hình An toàn Ứng dụng (`AndroidManifest.xml`)
1. **Vô hiệu hóa Trích xuất Sao lưu (`android:allowBackup="false"`):** Ngăn chặn việc trích xuất SharedPreferences (nơi lưu JWT token và phiên đăng nhập) thông qua lệnh `adb backup` từ máy tính khi cắm cáp USB.
2. **Kiểm soát Lưu lượng Mạng qua `network_security_config.xml`:**
   - Đã tạo file cấu hình an ninh mạng `res/xml/network_security_config.xml`.
   - Mặc định cấm hoàn toàn lưu lượng truyền thông không mã hóa (Cleartext HTTP) ra ngoài internet (`cleartextTrafficPermitted="false"`).
   - Chỉ cho phép cleartext traffic đối với địa chỉ loopback và emulator cục bộ (`10.0.2.2`, `localhost`, `127.0.0.1`) phục vụ quá trình debug và kiểm thử đồ án môn học.
   - Khi triển khai trên môi trường thật, toàn bộ kết nối tới domain máy chủ (Render, Supabase) đều bắt buộc phải chạy qua giao thức HTTPS có chứng chỉ số hợp lệ.
