# HƯỚNG DẪN TRIỂN KHAI VÀ DEVOPS (DEPLOYMENT SPECIFICATION)

## 1. Triển khai Frontend Web lên Vercel Workspace `visionary19`
- **Tài khoản xác thực:** `lovemvaf`
- **Workspace đích:** `visionary19` (https://vercel.com/visionary19)
- **Framework:** Next.js (App Router)
- **Thư mục gốc (Root Directory):** `frontend`
- **Lệnh Build:** `npm run build`
- **Lệnh Install:** `npm install`
- **Biến môi trường cần thiết trên Vercel:**
  - `NEXT_PUBLIC_API_URL`: URL công khai của backend ASP.NET Core Web API (hoặc URL proxy/tunnel).
  - `NEXT_PUBLIC_APP_NAME`: `VISIONARY`

---

## 2. Triển khai Backend ASP.NET Core Web API
- **Containerization (Docker):**
  - Xây dựng file `backend/Dockerfile` multi-stage build tối ưu dựa trên image chính thức của Microsoft:
    - Build: `mcr.microsoft.com/dotnet/sdk:8.0-alpine`
    - Runtime: `mcr.microsoft.com/dotnet/aspnet:8.0-alpine`
  - Đảm bảo image gọn nhẹ (< 150MB), khởi động cực nhanh và bảo mật tối đa.
- **Nền tảng Hosting:**
  - Hỗ trợ triển khai Docker Container lên Render Free / Fly.io / Railway / Azure App Service.
  - Cung cấp cấu hình `docker-compose.yml` để chạy trọn gói cục bộ (Web API + PostgreSQL + Redis).

---

## 3. Triển khai Windows Forms C#
- **Build Release:**
  - `dotnet publish desktop/Visionary.Desktop/Visionary.Desktop.csproj -c Release -r win-x64 --self-contained false`
  - Đầu ra: Thư mục thực thi `.exe` độc lập cho hệ điều hành Windows 10/11.

---

## 4. Triển khai Android Native Java
- **Build APK:**
  - Sử dụng Gradle Wrapper trong thư mục `mobile/VisionaryAndroid`:
  - `.\gradlew assembleDebug`
  - Đầu ra: File `app-debug.apk` cài đặt trực tiếp trên điện thoại Android hoặc máy ảo Emulator.
