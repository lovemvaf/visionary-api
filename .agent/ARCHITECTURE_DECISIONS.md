# ARCHITECTURAL DECISION RECORDS (ADR)

## ADR-001: Unified Backend Architecture (One API, Three Platforms)
- **Status:** ACCEPTED
- **Context:** The system serves three target client applications: Visionary Web (Next.js), Windows Forms (C#), and Android (Native Java).
- **Decision:** Build a single ASP.NET Core 8 Web API backend exposing RESTful endpoints with standard JSON DTOs and JWT Bearer authentication. Next.js, WinForms, and Android will all consume this identical API. No platform will have its own private database.
- **Consequences:** Eliminates business logic duplication, ensures data consistency across web, desktop, and mobile, simplifies grading for TH71108 Web API.

## ADR-002: Technology Stack Selection
- **Status:** ACCEPTED
- **Context:** Platform requirements demand high performance, academic compliance, and cross-platform clients.
- **Decisions:**
  - Backend: ASP.NET Core 8 Web API, Entity Framework Core, Npgsql PostgreSQL provider, OpenAPI/Swagger.
  - Database: PostgreSQL (Supabase compatible) with migrations, indexes, and foreign key integrity.
  - Frontend: Next.js 14+ App Router, React 18+, TypeScript, Tailwind CSS, Lucide icons.
  - Desktop: Windows Forms (.NET 8 Windows Desktop), System.Net.Http.HttpClient, System.Text.Json.
  - Mobile: Android Native Java, Android SDK 34, Retrofit 2, Material 3 components.
  - Cache & Rate Limiting: Memory Cache fallback + Upstash Redis integration when credentials provided.

## ADR-003: Authentication & Security Model
- **Status:** ACCEPTED
- **Context:** Identity must support email/password and Google OAuth, with strict role-based access control.
- **Decision:** ASP.NET Core issues signed JWT tokens containing user claims, role claims, and user ID. Google OAuth tokens are verified server-side (validating signature, issuer, audience, expiry) before issuing app JWTs. No role elevation from client-side payloads.
- **Consequences:** Client apps never store database credentials. All security enforcement resides in backend middleware and action filters.
