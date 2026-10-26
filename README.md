# VISIONARY – Hệ thống Quản lý Hoạt động Hội nhập CLB Tiếng Anh DNTU
> **English, Technology & Global Integration Platform**  
> **Phát triển bởi nhóm:** `VISIONARY API`  
> **Học phần:** Web API (TH71108) – Trường Đại học Công nghệ Đồng Nai (DNTU)

[![GitHub Repository](https://img.shields.io/badge/GitHub-lovemvaf%2Fvisionary--api-181717?logo=github)](https://github.com/lovemvaf/visionary-api)
[![Vercel Deployment](https://img.shields.io/badge/Vercel-visionary--platform-black?logo=vercel)](https://visionary-platform.vercel.app)
[![.NET 8 LTS](https://img.shields.io/badge/.NET-8.0%20LTS-purple?logo=dotnet)](https://dotnet.microsoft.com/)
[![Next.js 14](https://img.shields.io/badge/Next.js-14%20App%20Router-black?logo=next.js)](https://nextjs.org/)
[![WinForms .NET 8](https://img.shields.io/badge/WinForms-C%23%20.NET%208-blue?logo=windows)](https://learn.microsoft.com/en-us/dotnet/desktop/winforms/)
[![Android Java](https://img.shields.io/badge/Android-Java%2017%20Native-green?logo=android)](https://developer.android.com/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL%20Supabase-336791?logo=postgresql)](https://supabase.com/)

---

## 👥 THÀNH VIÊN NHÓM PHÁT TRIỂN (VISIONARY API)

| STT | Họ và Tên | Vai trò chính trong dự án | Phụ trách kỹ thuật |
|---|---|---|---|
| 1 | **Quách Khoa Đức** | Principal Software Architect | Thiết kế kiến trúc tổng thể, ASP.NET Core Web API, Next.js Frontend, JWT & Database |
| 2 | **Võ Ngọc Minh Đạt** | Club Operations & Desktop Engineer | Phân tích nghiệp vụ CLB, Windows Forms C# Desktop Administration, Xét duyệt & Điểm danh |
| 3 | **Hồ Đoàng Nguyên Khang** | Data Pipeline & Automation Engineer | Data Automation (GitHub/Hugging Face/RSS), Hệ thống Cuộc thi (Hackathon), Học bổng & Việc làm |
| 4 | **Đào Trí Khang** | Mobile Software Engineer & QA Lead | Android Native Java Client (Retrofit, Material 3), Kiểm thử tích hợp đa nền tảng |

---

## 📌 THÔNG BÁO HỌC PHẦN & TÍNH PHÁP LÝ

Dự án được xây dựng phục vụ nghiên cứu và đánh giá trong học phần **Web API (TH71108)** tại **Trường Đại học Công nghệ Đồng Nai (DNTU)**.  
Hệ thống là sản phẩm nghiên cứu ứng dụng độc lập của nhóm sinh viên **VISIONARY API** nhằm số hóa bài toán quản trị CLB Tiếng Anh và mở rộng kết nối công nghệ hội nhập; dự án **không tự nhận là cổng thông tin chính thức được trường phê duyệt**.  
Mọi dữ liệu công khai (GitHub repository, Hugging Face model, tin tức công nghệ) đều tuân thủ chính sách bản quyền và giới hạn sử dụng của nhà cung cấp API.

---

## 🏛️ KIẾN TRÚC HỆ THỐNG: MỘT BACKEND – BA NỀN TẢNG

```
                             ┌─────────────────────────────────┐
                             │       PostgreSQL Supabase       │
                             │  (EF Core + Auto SQLite Cache)  │
                             └────────────────┬────────────────┘
                                              │
                                              ▼
                             ┌─────────────────────────────────┐
                             │    ASP.NET Core 8 Web API       │
                             │  - Clean Architecture (Core)    │
                             │  - BCrypt + JWT Bearer Auth     │
                             │  - Data Automation (GitHub/HF)  │
                             │  - OpenAPI / Swagger UI         │
                             └──────┬─────────┼─────────┬──────┘
                                    │         │         │
                 ┌──────────────────┘         │         └──────────────────┐
                 │ HTTP / JSON                │ HTTP / JSON                │ HTTP / JSON
                 ▼                            ▼                            ▼
┌─────────────────────────────────┐ ┌───────────────────┐ ┌─────────────────────────────────┐
│     Web: Next.js 14 App Router  │ │ Desktop: WinForms │ │ Mobile: Android Native Java     │
│  - TypeScript, Tailwind CSS     │ │ - .NET 8 Desktop  │ │ - JDK 17, Material Design 3     │
│  - 16 Tuyến đường SSR/ISR       │ │ - Quản trị CLB    │ │ - Retrofit 2 + OkHttp 3         │
│  - Deployed trên Vercel Cloud   │ │ - Duyệt & Checkin │ │ - Điểm danh QR & English IT     │
└─────────────────────────────────┘ └───────────────────┘ └─────────────────────────────────┘
```

---

## 🌐 ĐỊA CHỈ TRỰC TUYẾN & MÃ NGUỒN CHÍNH THỨC

- **Website Production (Chính thức):** [https://visionary-platform.vercel.app](https://visionary-platform.vercel.app)
- **Production Alias (Dự phòng):** [https://visionary-global.vercel.app](https://visionary-global.vercel.app)
- **GitHub Monorepo:** [https://github.com/lovemvaf/visionary-api](https://github.com/lovemvaf/visionary-api)
- **Vercel Workspace Scope:** `visionary19` (Project: `visionary-platform`)

---

## 🔑 TÀI KHOẢN MẪU KIỂM THỬ HỆ THỐNG

> 🔒 **Chính sách bảo mật:** Mật khẩu kiểm thử không lưu trữ công khai trên tài liệu mã nguồn. Đối với môi trường phát triển cục bộ, mật khẩu khởi tạo được quản lý qua biến môi trường `ADMIN_SEED_PASSWORD`. Đối với môi trường Production, toàn bộ tài khoản quản trị được bảo vệ bằng mật khẩu độc lập và chứng thực phiên an toàn. Giảng viên và hội đồng nghiệm thu học phần TH71108 nhận thông tin kiểm thử qua tài liệu bàn giao nội bộ bảo mật.

| Tài khoản | Email định danh | Quyền hạn chính |
|---|---|---|
| **Quản trị viên (Admin)** | `quachkhoaduc@visionary.dntu.edu.vn` | Toàn quyền cấu hình, tài khoản, dữ liệu tự động |
| **Ban Chủ Nhiệm (BCN)** | `vongocminhdat@visionary.dntu.edu.vn` | Duyệt đơn gia nhập, tạo sự kiện, điểm danh |
| **Ban Dữ liệu** | `hodoangnguyenkhang@visionary.dntu.edu.vn` | Quản lý học bổng, hackathon, việc làm |
| **Ban Kỹ thuật** | `daotrikhang@visionary.dntu.edu.vn` | Quản lý tài nguyên công nghệ, kiểm thử di động |
| **Sinh viên mẫu** | `student.test@visionary.dntu.edu.vn` | Đăng ký sự kiện, xem thuật ngữ, nộp đơn |

---

## 🚀 HƯỚNG DẪN CHẠY DỰ ÁN CỤC BỘ

### 1. Khởi chạy Backend ASP.NET Core 8 Web API
```powershell
# Chạy trực tiếp qua .NET CLI
dotnet run --project backend/src/Visionary.Api/Visionary.Api.csproj

# Hoặc chạy kiểm thử tự động toàn bộ giải pháp (9/9 tests PASS)
dotnet test backend/Visionary.sln
```
- Swagger UI tài liệu API: `http://localhost:5000/swagger`
- Health check API: `http://localhost:5000/`

### 2. Khởi chạy Website Next.js 14
```powershell
cd frontend
npm install
npm run dev
```
Truy cập: `http://localhost:3000`

### 3. Khởi chạy Desktop Windows Forms (.NET 8)
```powershell
dotnet run --project desktop/Visionary.Desktop/Visionary.Desktop.csproj
```
Hoặc mở tệp `.exe` đã biên dịch tại:
`desktop/Visionary.Desktop/bin/Debug/net8.0-windows/Visionary.Desktop.exe`

### 4. Mở và Biên dịch Ứng dụng Di động Android
Mở thư mục `mobile/VisionaryAndroid` trong Android Studio hoặc chạy lệnh:
```powershell
cd mobile/VisionaryAndroid
.\gradlew.bat assembleDebug
```
Tệp APK debug tạo tại: `mobile/VisionaryAndroid/app/build/outputs/apk/debug/app-debug.apk`

---

## 📁 CẤU TRÚC THƯ MỤC MONOREPO

```
Visionary API/
├── .agent/                  # Hệ thống quản lý tiến độ và tự phục hồi (Autonomous Engine)
├── .github/workflows/       # CI/CD Workflows (Frontend, Backend, Desktop, Android, Security)
├── backend/                 # Solution ASP.NET Core 8 Web API
│   ├── src/Visionary.Core/           # Domain Entities, DTOs, Enums, Interfaces
│   ├── src/Visionary.Infrastructure/ # AppDbContext, Seed Data, JWT, Data Automation
│   ├── src/Visionary.Api/            # REST Controllers, Middlewares, Program.cs
│   └── tests/Visionary.Tests/        # Bộ xUnit Integration & Security Tests
├── desktop/                 # Phần mềm Quản trị Windows Forms C# (.NET 8)
│   └── Visionary.Desktop/   # Forms, ApiClient, AppState, Dialogs
├── frontend/                # Website Next.js 14 App Router (Vercel)
│   ├── src/app/             # 16 Tuyến đường giao diện người dùng
│   ├── src/components/      # Navbar, Footer, ThemeToggle
│   └── src/lib/             # API client, TypeScript types
├── mobile/                  # Ứng dụng Android Native Java (Gradle 8.4)
│   └── VisionaryAndroid/    # Activities, Fragments, Retrofit Services, Material 3
├── docs/                    # Bộ 12 tài liệu kỹ thuật chuẩn mực
└── docker-compose.yml       # Cấu hình container Kestrel
```

---

## 📜 BẢN QUYỀN VÀ GIẤY PHÉP

Hệ thống được phát triển độc quyền bởi nhóm **VISIONARY API** phục vụ học tập và nghiên cứu ứng dụng môn học TH71108.  
Mọi quyền sở hữu trí tuệ thuộc về nhóm phát triển.
