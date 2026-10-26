# VISIONARY – English, Technology & Global Integration Platform
> **A Unified Digital Ecosystem for Academic & Student Club Governance**  
> *One Clean Backend Web API powering Modern Web, Native Android, and Desktop Windows Forms clients.*

[![GitHub Repository](https://img.shields.io/badge/GitHub-lovemvaf%2Fvisionary--api-181717?logo=github)](https://github.com/lovemvaf/visionary-api)
[![Vercel Deployment](https://img.shields.io/badge/Vercel-visionary--platform-black?logo=vercel)](https://visionary-platform.vercel.app)
[![.NET 8 LTS](https://img.shields.io/badge/.NET-8.0%20LTS-purple?logo=dotnet)](https://dotnet.microsoft.com/)
[![Next.js 14](https://img.shields.io/badge/Next.js-14%20App%20Router-black?logo=next.js)](https://nextjs.org/)
[![WinForms .NET 8](https://img.shields.io/badge/WinForms-C%23%20.NET%208-blue?logo=windows)](https://learn.microsoft.com/en-us/dotnet/desktop/winforms/)
[![Android Java](https://img.shields.io/badge/Android-Java%2017%20Native-green?logo=android)](https://developer.android.com/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL%20Supabase-336791?logo=postgresql)](https://supabase.com/)
[![xUnit Tests](https://img.shields.io/badge/Tests-15%2F15%20Passed-success?logo=xunit)](docs/TEST_VERIFICATION_REPORT.md)

---

## 📖 Tổng quan Sản phẩm (Product Overview)

**VISIONARY** là nền tảng quản trị và kết nối toàn diện dành cho các Câu lạc bộ Tiếng Anh, sinh viên khối ngành công nghệ và các tổ chức học thuật. Dự án giải quyết các bài toán vận hành cốt lõi:
1. **Quản trị hoạt động CLB:** Số hóa quy trình xét duyệt hồ sơ gia nhập, quản lý thành viên, tổ chức sự kiện và điểm danh sự kiện theo thời gian thực.
2. **Không gian học tập chuyên ngành:** Chuyên mục *English for IT* cung cấp từ vựng, thuật ngữ và bài viết kỹ thuật song ngữ được kiểm duyệt.
3. **Cập nhật Công nghệ (Technology Radar):** Tự động tổng hợp và phân loại xu hướng mã nguồn mở (GitHub Trending), mô hình AI (Hugging Face) và tin tức khoa học.
4. **Cổng Thông tin Cơ hội (Opportunity & Career Gateway):** Cung cấp dữ liệu học bổng, các cuộc thi Hackathon và cơ hội việc làm công nghệ.

Toàn bộ hệ sinh thái tuân theo nguyên tắc **Một Backend Duy nhất (Single Source of Truth)**: tất cả các ứng dụng Web, Desktop và Mobile đều giao tiếp với cùng một RESTful API trung tâm và cơ sở dữ liệu quan hệ đồng nhất.

---

## 🏛️ Kiến trúc Hệ thống: Một Backend – Ba Nền tảng

```
                                ┌─────────────────────────────────┐
                                │       PostgreSQL Database       │
                                │   (EF Core + Migrations + RLS)  │
                                └────────────────┬────────────────┘
                                                 │
                                                 ▼
                                ┌─────────────────────────────────┐
                                │     ASP.NET Core 8 Web API      │
                                │  - RESTful Endpoints + Swagger  │
                                │  - BCrypt + JWT Bearer Auth     │
                                │  - Automated Data Ingestion     │
                                │  - Role-Based Access Control    │
                                └──────┬─────────┼─────────┬──────┘
                                       │         │         │
                    ┌──────────────────┘         │         └──────────────────┐
                    │ HTTPS / JSON               │ HTTPS / JSON               │ HTTPS / JSON
                    ▼                            ▼                            ▼
   ┌─────────────────────────────────┐ ┌───────────────────┐ ┌─────────────────────────────────┐
   │     Web Client: Next.js 14      │ │ Desktop: WinForms │ │ Mobile Client: Android Native   │
   │  - App Router, TypeScript       │ │ - C# .NET 8       │ │ - Java 17, Material Design 3    │
   │  - Responsive Tailwind CSS      │ │ - Club Management │ │ - Retrofit 2 + OkHttp 3         │
   │  - Deployed on Vercel           │ │ - Check-in & BCN  │ │ - Event Registration & Learning │
   └─────────────────────────────────┘ └───────────────────┘ └─────────────────────────────────┘
```

---

## 🛠️ Công nghệ Sử dụng (Technology Stack)

| Thành phần | Công nghệ chính | Thư viện & Công cụ bổ trợ |
| :--- | :--- | :--- |
| **Backend API** | ASP.NET Core 8 Web API | Entity Framework Core, Npgsql, BCrypt.Net, JWT Bearer, Swashbuckle OpenAPI |
| **Database** | PostgreSQL (Supabase Compatible) | Relational constraints, Foreign Keys, B-Tree Indexes, Migrations |
| **Frontend Web** | Next.js 14+ (App Router), React 18+ | TypeScript, Tailwind CSS, Lucide Icons, Fetch API, SSR/ISR |
| **Desktop Client** | Windows Forms (.NET 8 Windows Desktop) | RestSharp / HttpClient, System.Text.Json |
| **Mobile Client** | Android Native Java (JDK 17, SDK 34) | Retrofit 2, OkHttp 3, Gson, Android Jetpack, Material Design 3 |
| **DevOps & QA** | GitHub Actions CI/CD | Docker, Gitleaks Security Scan, xUnit Test Runner, Dependabot |

---

## 🚀 Hướng dẫn Cài đặt & Khởi chạy Nhanh (Quick Start)

### Yêu cầu Hệ thống Tiên quyết
- **.NET SDK 8.0+**: [Tải về .NET SDK](https://dotnet.microsoft.com/download)
- **Node.js 18.x+ / 20.x+**: [Tải về Node.js](https://nodejs.org/)
- **Android Studio** (Dành cho Mobile): Android SDK 34, JDK 17
- **Git**: [Tải về Git](https://git-scm.com/)

### 1. Khởi chạy Backend Web API
```powershell
# Chạy trực tiếp từ mã nguồn
dotnet run --project backend/src/Visionary.Api/Visionary.Api.csproj

# Chạy toàn bộ bộ kiểm thử tự động (15/15 tests PASS)
dotnet test backend/Visionary.Backend.sln
```
- Swagger UI (Tài liệu API tương tác): `http://localhost:5000/swagger`
- Health check endpoint: `http://localhost:5000/health/live`

### 2. Khởi chạy Website Next.js 14
```powershell
cd frontend
npm install
npm run dev
```
- Mở trình duyệt tại: `http://localhost:3000`

### 3. Khởi chạy Ứng dụng Desktop Windows Forms (.NET 8)
```powershell
dotnet run --project desktop/Visionary.Desktop/Visionary.Desktop.csproj
```

### 4. Khởi chạy Ứng dụng Android Native
- Mở thư mục `mobile/VisionaryAndroid` bằng Android Studio và kết nối máy ảo (Emulator) hoặc thiết bị thật.
- Hoặc biên dịch tệp APK Debug bằng lệnh:
```powershell
cd mobile/VisionaryAndroid
.\gradlew.bat assembleDebug
```
- Tệp APK được sinh tại: `mobile/VisionaryAndroid/app/build/outputs/apk/debug/app-debug.apk`

---

## ⚙️ Cấu hình Môi trường (Environment Setup)

Tất cả các biến môi trường cần thiết được cung cấp dưới dạng bản mẫu an toàn tại [.env.example](.env.example):
- `ConnectionStrings__DefaultConnection`: Chuỗi kết nối PostgreSQL.
- `Jwt__Key`, `Jwt__Issuer`, `Jwt__Audience`: Cấu hình chữ ký số JWT.
- `NEXT_PUBLIC_API_URL`: URL Backend mà ứng dụng Web/Desktop/Mobile kết nối đến.

> 🔒 **Chính sách Bảo mật:** Repository tuyệt đối không lưu trữ chuỗi kết nối production hoặc secrets thực tế. Xem thêm chi tiết tại [docs/SECURITY.md](docs/SECURITY.md).

---

## 🧪 Kiểm thử và Đảm bảo Chất lượng (Quality Assurance)

Dự án áp dụng quy trình kiểm thử nghiêm ngặt trên GitHub Actions CI/CD:
- **Bộ 15 xUnit Tests Backend:** Bao gồm 7 bài kiểm thử tích hợp RESTful API (`ApiIntegrationTests`), 2 bài kiểm thử xác thực bảo mật (`AuthTests`), và 6 bài kiểm thử toàn vẹn logic bài viết (`PostsLogicAuditTests`).
- **Báo cáo Kiểm định Trực tiếp:** Xem chi tiết tại [docs/TEST_VERIFICATION_REPORT.md](docs/TEST_VERIFICATION_REPORT.md).
- **Lệnh kiểm tra Quality Gate tự động:**
  ```powershell
  python scripts/verify_repository.py
  ```

---

## 👥 Đội ngũ Kỹ sư Phát triển (Engineering Team)

Dự án được xây dựng và duy trì bởi nhóm **VISIONARY API**:

| Thành viên | GitHub Account | Vai trò Kỹ thuật | Trách nhiệm Chính |
| :--- | :--- | :--- | :--- |
| **Quách Khoa Đức** | [`@lovemvaf`](https://github.com/lovemvaf) | Principal Software Architect | Thiết kế kiến trúc tổng thể, ASP.NET Core Web API, Next.js Web Frontend, CI/CD DevSecOps |
| **Đào Trí Khang** | [`@TS13lover1989`](https://github.com/TS13lover1989) | Mobile Software Engineer | Phát triển ứng dụng Android Native Java (Retrofit 2, Material 3), Mobile Testing |
| **Hồ Đoàn Nguyên Khang** | [`@HoKhangIT`](https://github.com/HoKhangIT) | Backend & Database Engineer | ASP.NET Core 8 Web API, Entity Framework Core, Swagger OpenAPI, API Integration Tests |
| **Võ Ngọc Minh Đạt** | [`@vongocminhdat`](https://github.com/vongocminhdat) | Desktop Software Engineer | Phát triển ứng dụng Windows Forms C# (.NET 8), Nghiệp vụ Quản trị CLB, Desktop Client Testing |

### 🌿 Bốn Nhánh Phát triển Chuyên biệt (Feature Branches)
- **Web Frontend & Architecture (Quách Khoa Đức):** [`feature/web-duc`](https://github.com/lovemvaf/visionary-api/tree/feature/web-duc)
- **Android Native Mobile (Đào Trí Khang):** [`feature/android-tri-khang`](https://github.com/lovemvaf/visionary-api/tree/feature/android-tri-khang)
- **ASP.NET Core Web API (Hồ Đoàn Nguyên Khang):** [`feature/api-ho-doan-khang`](https://github.com/lovemvaf/visionary-api/tree/feature/api-ho-doan-khang)
- **Windows Forms Desktop (Võ Ngọc Minh Đạt):** [`feature/winforms-minh-dat`](https://github.com/lovemvaf/visionary-api/tree/feature/winforms-minh-dat)

*Chi tiết về ma trận đóng góp và quy trình cộng tác xem tại [docs/TEAM_CONTRIBUTIONS.md](docs/TEAM_CONTRIBUTIONS.md) và [CONTRIBUTING.md](CONTRIBUTING.md).*

---

## 📄 Bản quyền và Tài liệu Kỹ thuật

- **Tài liệu Kiến trúc & Quyết định Kỹ thuật (ADR):** [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Đặc tả RESTful API Contract:** [docs/API_CONTRACT.md](docs/API_CONTRACT.md)
- **Lược đồ Cơ sở Dữ liệu (Database Schema):** [docs/DATABASE_SCHEMA.md](docs/DATABASE_SCHEMA.md)
- **Hướng dẫn Vận hành & Triển khai:** [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) & [docs/OPERATIONS_MANUAL.md](docs/OPERATIONS_MANUAL.md)
- **Chính sách An toàn Thông tin (Security Policy):** [docs/SECURITY.md](docs/SECURITY.md)
