# HƯỚNG DẪN VẬN HÀNH HỆ THỐNG – VISIONARY OPERATIONS MANUAL
**Dự án:** VISIONARY – Hệ thống Quản lý Hoạt động Hội nhập CLB Tiếng Anh DNTU  
**Nhóm phát triển:** VISIONARY API  
**Thành viên:** Quách Khoa Đức, Võ Ngọc Minh Đạt, Hồ Đoàng Nguyên Khang, Đào Trí Khang  
**Học phần:** Web API (TH71108) – Trường Đại học Công nghệ Đồng Nai (DNTU)  

---

## 1. TỔNG QUAN HỆ THỐNG VÀ KIẾN TRÚC MỘT BACKEND – BA NỀN TẢNG

Hệ sinh thái VISIONARY được xây dựng theo kiến trúc tập trung:
- **Backend Nghiệp vụ duy nhất:** ASP.NET Core 8 Web API (`backend/Visionary.sln`) chạy Kestrel server trên cổng 5000 (hoặc 8080 trong Docker).
- **Cơ sở dữ liệu tập trung:** PostgreSQL Supabase (với SQLite/InMemory auto-fallback an toàn).
- **Ba nền tảng Client kết nối chung một API:**
  1. **Web:** Next.js 14 App Router (`frontend/`)
  2. **Desktop:** Windows Forms C# .NET 8 (`desktop/Visionary.Desktop`)
  3. **Mobile:** Android Native Java (`mobile/VisionaryAndroid`)

---

## 2. HƯỚNG DẪN KHỞI CHẠY BACKEND ASP.NET CORE

### Cách 1: Chạy trực tiếp qua .NET CLI
Mở terminal tại thư mục gốc dự án:
```powershell
dotnet run --project backend/src/Visionary.Api/Visionary.Api.csproj
```
- Máy chủ sẽ lắng nghe tại: `http://localhost:5000`
- Giao diện tài liệu Swagger UI: `http://localhost:5000/swagger`
- Trạng thái kiểm tra sức khỏe hệ thống: `http://localhost:5000/` (Trả về JSON Health status)

### Cách 2: Chạy qua Docker Compose
```powershell
docker compose up -d --build
```
Dịch vụ sẽ tự động đóng gói ứng dụng ASP.NET Core và khởi chạy trên cổng `http://localhost:5000`.

---

## 3. HƯỚNG DẪN KHỞI CHẠY WEBSITE NEXT.JS

### Chạy môi trường phát triển (Development)
```powershell
cd frontend
npm install
npm run dev
```
Truy cập: `http://localhost:3000`

### Biên dịch bản phát hành (Production Build)
```powershell
cd frontend
npm run build
npm run start
```

### Địa chỉ Website Trực tuyến đã Triển khai (Vercel)
- **Production URL chính thức:** `https://visionary-platform.vercel.app`
- **Production Alias dự phòng:** `https://visionary-global.vercel.app`
- **Vercel Scope / Project:** `visionary19` / `visionary-platform`
- **GitHub Monorepo:** `https://github.com/lovemvaf/visionary-api`

---

## 4. HƯỚNG DẪN VẬN HÀNH PHẦN MỀM DESKTOP (WINDOWS FORMS C#)

### Biên dịch ứng dụng
```powershell
dotnet build desktop/Visionary.Desktop/Visionary.Desktop.csproj
```

### Chạy ứng dụng Desktop
```powershell
dotnet run --project desktop/Visionary.Desktop/Visionary.Desktop.csproj
```
Hoặc chạy trực tiếp tệp nhị phân đã build tại:
`desktop/Visionary.Desktop/bin/Debug/net8.0-windows/Visionary.Desktop.exe`

### Các bước thao tác trên Desktop:
1. **Đăng nhập:** Tại màn hình `LoginForm`, nhấn nút "Quản trị viên (Đức)" hoặc "Ban Chủ Nhiệm (Đạt)" để tự động điền tài khoản mẫu. Nhấn "ĐĂNG NHẬP HỆ THỐNG".
2. **Xem Bảng điều khiển (Dashboard):** Xem các thẻ thống kê thời gian thực (Thành viên chính thức, Đơn chờ xét duyệt, Sự kiện hoạt động, Nguồn tự động) và nhật ký hoạt động gần đây.
3. **Quản lý Thành viên (Members):** Xem bảng danh sách thành viên CLB, tìm kiếm theo tên hoặc MSSV, lọc theo ban chuyên môn.
4. **Xét duyệt Đơn Gia Nhập (Applications):** Chọn một đơn có trạng thái "Pending" trong bảng, nhấn "Xem & Xét Duyệt Đơn", chọn quyết định "Chấp thuận" hoặc "Từ chối", gán vị trí/vai trò và ghi chú phản hồi, nhấn "Xác nhận duyệt".
5. **Quản lý Sự kiện & Điểm danh (Events):**
   - Nhấn "Tạo Sự kiện Mới" để mở hộp thoại nhập tiêu đề, địa điểm, sức chứa và thời gian.
   - Nhấp vào một sự kiện trong danh sách để xem danh sách sinh viên đã đăng ký bên dưới.
   - Chọn một sinh viên và nhấn "Xác nhận Điểm danh (Check-in)" để hoàn tất xác thực tham dự.
6. **Điều khiển Đồng bộ Dữ liệu (Data Sync):** Chọn một nguồn trong bảng (GitHub / Hugging Face / RSS) và nhấn "Kích hoạt Nạp Dữ liệu Ngay (Trigger Sync)".
7. **Xem thông tin Về VISIONARY (About):** Xem nhận diện thương hiệu VISIONARY API, danh sách đầy đủ 4 thành viên và thông cáo học phần TH71108.

---

## 5. HƯỚNG DẪN VẬN HÀNH ỨNG DỤNG DI ĐỘNG (ANDROID NATIVE JAVA)

### Mở trong Android Studio
1. Mở Android Studio -> Chọn `Open...` -> Trỏ đến thư mục `mobile/VisionaryAndroid`.
2. Chờ Gradle đồng bộ tự động theo `settings.gradle` và `build.gradle`.

### Biên dịch qua dòng lệnh (Gradle)
```powershell
cd mobile/VisionaryAndroid
.\gradlew.bat assembleDebug
```
Tệp APK debug sẽ được xuất ra tại:  
`mobile/VisionaryAndroid/app/build/outputs/apk/debug/app-debug.apk`

### Cấu hình địa chỉ máy chủ:
- Khi chạy trên **Android Emulator (Trình giả lập)**: Sử dụng địa chỉ mặc định `http://10.0.2.2:5000` (đây là địa chỉ loopback đặc biệt để emulator kết nối đến localhost của máy tính host).
- Khi chạy trên **Điện thoại thật kết nối cùng Wi-Fi**: Nhập địa chỉ IP mạng nội bộ của máy tính chạy backend (ví dụ: `http://192.168.1.15:5000`).
- Khi kết nối với **Production API**: Nhập URL production của backend.

### Các phân hệ chính trên ứng dụng Android:
1. **Màn hình Đăng nhập (`LoginActivity`):** Hỗ trợ đăng nhập sinh viên hoặc nhấn nhanh nút đăng nhập mẫu.
2. **Thanh điều hướng dưới (`BottomNavigationView`):**
   - **Tab Trang chủ:** Giới thiệu CLB, 6 trụ cột hội nhập, thống kê.
   - **Tab Sự kiện:** Danh sách sự kiện, nút "Đăng ký tham gia" / "Hủy đăng ký", nút "Mã QR" để mở hộp thoại xem mã check-in cá nhân.
   - **Tab English IT:** Kho thuật ngữ tiếng Anh CNTT chuyên ngành, ví dụ mẫu câu.
   - **Tab Cơ hội:** Cuộc thi Hackathon, học bổng quốc tế, chương trình trao đổi ASEAN.
   - **Tab Cá nhân:** Thông tin tài khoản sinh viên, quyền hạn, thông tin 4 thành viên nhóm phát triển và nút "Đăng xuất".

---

## 6. DANH SÁCH TÀI KHOẢN MẪU KIỂM THỬ HỆ THỐNG

Tất cả tài khoản kiểm thử đã được cấu hình trong hệ thống kiểm tra và cơ sở dữ liệu (`DbInitializer`):

> 🔒 **Chính sách bảo mật:** Mật khẩu kiểm thử nội bộ không được lưu trữ công khai. Đối với môi trường phát triển cục bộ, mật khẩu khởi tạo được cung cấp thông qua biến môi trường `ADMIN_SEED_PASSWORD`. Đối với môi trường máy chủ và Production, mật khẩu được phân định độc lập theo từng tài khoản thực tế và không sử dụng giá trị mặc định.

| Vai trò | Họ và tên | Email đăng nhập | Cơ chế mật khẩu | Quyền hạn chính |
|---|---|---|---|---|
| **Quản trị viên (Admin)** | Quách Khoa Đức | `quachkhoaduc@visionary.dntu.edu.vn` | Quản lý qua `ADMIN_SEED_PASSWORD` / Nội bộ | Toàn quyền quản trị hệ thống, quản lý tài khoản, cấu hình nguồn |
| **Ban Chủ Nhiệm (BCN)** | Võ Ngọc Minh Đạt | `vongocminhdat@visionary.dntu.edu.vn` | Quản lý qua `ADMIN_SEED_PASSWORD` / Nội bộ | Duyệt đơn gia nhập, tạo sự kiện, điểm danh sinh viên, xem báo cáo |
| **Thành viên Ban Dữ liệu** | Hồ Đoàng Nguyên Khang | `hodoangnguyenkhang@visionary.dntu.edu.vn` | Quản lý qua `ADMIN_SEED_PASSWORD` / Nội bộ | Quản lý cơ hội, học bổng, việc làm và kiểm tra nguồn dữ liệu |
| **Thành viên Ban Kỹ thuật** | Đào Trí Khang | `daotrikhang@visionary.dntu.edu.vn` | Quản lý qua `ADMIN_SEED_PASSWORD` / Nội bộ | Quản lý nội dung công nghệ, kiểm thử di động, hỗ trợ thành viên |
| **Sinh viên mẫu** | Nguyễn Văn An | `student.test@visionary.dntu.edu.vn` | Quản lý qua `ADMIN_SEED_PASSWORD` / Nội bộ | Đăng ký sự kiện, nộp đơn gia nhập CLB, xem thuật ngữ và cơ hội |

---

## 7. QUY TRÌNH AN TOÀN VÀ PHỤC HỒI DỮ LIỆU

1. **Bảo toàn dữ liệu:** Không thực hiện reset, drop database hay xóa bảng trên production.
2. **Khôi phục khi máy chủ offline:** Khi mất kết nối máy chủ, ứng dụng WinForms và Android tự động hiển thị thông báo thân thiện và chuyển sang chế độ an toàn, không gây crash ứng dụng.
3. **Mã hóa và Bảo mật:** Mọi mật khẩu lưu trữ trong bảng `Users` đều được băm bằng thuật toán BCrypt với salt ngẫu nhiên. Mọi token JWT đều có chữ ký bí mật từ máy chủ và thời hạn xác thực cụ thể.
