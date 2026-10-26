# HƯỚNG DẪN THIẾT LẬP MÔI TRƯỜNG PHÁT TRIỂN NỘI BỘ (TEAM SETUP GUIDE)
## VISIONARY ECOSYSTEM – LOCAL DEVELOPMENT & ONBOARDING SOP
**Dành cho:** Thành viên nhóm lập trình VISIONARY API & Sinh viên kiểm thử  
**Học phần:** Web API (TH71108) – Đại học Công nghệ Đồng Nai (DNTU)  

---

## 1. YÊU CẦU CÔNG CỤ VÀ SDK CẦN THIẾT (PREREQUISITES)

Trước khi bắt đầu, máy tính của bạn cần cài đặt:
1. **Git for Windows:** [https://git-scm.com/](https://git-scm.com/)
2. **.NET 8.0 SDK:** [https://dotnet.microsoft.com/download/dotnet/8.0](https://dotnet.microsoft.com/download/dotnet/8.0)
3. **Node.js 20 LTS:** [https://nodejs.org/](https://nodejs.org/)
4. **Visual Studio 2022** (với workload *.NET Desktop Development* cho WinForms) hoặc **VS Code**.
5. **Android Studio** (Hedgehog hoặc mới hơn với Android SDK 34 và JDK 17).

---

## 2. QUY TRÌNH CLONE VÀ CẤU HÌNH BIẾN MÔI TRƯỜNG

### Bước 1: Clone Repository
```powershell
git clone https://github.com/lovemvaf/visionary-api.git
cd "visionary-api"
```

### Bước 2: Tạo file `.env` cục bộ từ template an toàn
```powershell
cp .env.example .env
```
File `.env` trên máy cá nhân của bạn mặc định sử dụng SQLite cục bộ và không yêu cầu bất kỳ mật khẩu đám mây nào:
- `ConnectionStrings__DefaultConnection=Data Source=visionary.db`
- `Jwt__Key=VisionaryDevJwtSecretKeyMinimum32CharactersLong2026`
- `API_BASE_URL=http://localhost:5000`

---

## 3. KHỞI CHẠY CÁC THÀNH PHẦN HỆ THỐNG

### 3.1. Khởi chạy Backend ASP.NET Core 8 Web API
```powershell
# Chạy trực tiếp qua .NET CLI
dotnet run --project backend/src/Visionary.Api/Visionary.Api.csproj

# Hoặc khởi chạy qua script an toàn
.\start-backend.bat
```
- **Tài liệu Swagger UI:** [http://localhost:5000/swagger](http://localhost:5000/swagger)
- **Kiểm tra trạng thái Health:** [http://localhost:5000/health/live](http://localhost:5000/health/live)
- *Cơ sở dữ liệu SQLite `visionary.db` sẽ tự động được khởi tạo và nạp dữ liệu mẫu ban đầu mà không cần cấu hình thêm.*

### 3.2. Khởi chạy Website Next.js 14
Mở cửa sổ terminal mới:
```powershell
cd frontend
npm install
npm run dev
```
Truy cập website trên trình duyệt: [http://localhost:3000](http://localhost:3000)

### 3.3. Khởi chạy Ứng dụng Desktop Windows Forms (.NET 8)
Mở solution `backend/Visionary.sln` hoặc chạy lệnh:
```powershell
dotnet run --project desktop/Visionary.Desktop/Visionary.Desktop.csproj
```
Ứng dụng sẽ mở giao diện đăng nhập `LoginForm` và tự động kết nối tới API tại `http://localhost:5000`.

### 3.4. Khởi chạy Ứng dụng Di động Android
1. Mở thư mục `mobile/VisionaryAndroid` trong Android Studio.
2. Đợi Gradle đồng bộ hóa xong (Gradle Sync).
3. Chọn máy ảo Android Emulator (Pixel 6/7, Android 13/14) và nhấn nút **Run 'app'** (Shift + F10).
4. *Lưu ý:* Máy ảo Android kết nối vào backend máy chủ cục bộ thông qua địa chỉ IP `10.0.2.2:5000` (đã được cấu hình trong `network_security_config.xml`).

---

## 4. CHẠY KIỂM THỬ TỰ ĐỘNG XÁC NHẬN CHẤT LƯỢNG

Trước khi commit bất kỳ thay đổi nào:
```powershell
# Chạy toàn bộ 15 bài kiểm thử xUnit của Backend
dotnet test backend/Visionary.Backend.sln

# Kiểm tra biên dịch bản phát hành của Website
cd frontend
npm run build
```

---

## 5. XỬ LÝ SỰ CỐ PHỔ BIẾN (TROUBLESHOOTING)

| Hiện tượng lỗi | Nguyên nhân | Cách khắc phục |
|---|---|---|
| Cổng 5000 bị chiếm dụng | Có một instance backend cũ đang chạy ngầm | Chạy PowerShell: `Get-Process -Name Visionary.Api -ErrorAction SilentlyContinue \| Stop-Process` |
| Lỗi SQLite database lock | Chạy nhiều test song song cùng lúc | Chạy `dotnet test backend/Visionary.Backend.sln` (đã có `SemaphoreSlim` và `CustomWebApplicationFactory` giải quyết) |
| Android không kết nối được API | Địa chỉ máy chủ trên Android bị sai | Đảm bảo nhập `http://10.0.2.2:5000` trên máy ảo Emulator, không dùng `localhost` |
| Website báo lỗi mạng khi gọi API | Backend cục bộ chưa được bật | Khởi chạy `start-backend.bat` trước khi chạy `npm run dev` |
