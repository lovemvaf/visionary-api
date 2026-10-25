# CURRENT BLOCKERS & RISKS

*Currently no active blocking errors. Environment SDKs (.NET 8/9, Node.js 24, Java 17, Android SDK, Git, Vercel) are fully available.*

| Blocker ID | Service / Tool | Issue | Mitigation / Fallback | Required Action | Status |
|---|---|---|---|---|---|
| BLK-001 | Supabase Connection | Remote connection string not yet passed via environment | Default to local PostgreSQL / SQLite / In-Memory provider with automated toggle to Npgsql when `ConnectionStrings:DefaultConnection` is configured. | User may supply Supabase PostgreSQL URI when ready. System operates seamlessly in dev mode. | MITIGATED |
| BLK-002 | Google Client ID | External OAuth Credentials | Backend OAuth validator includes mock-verification bypass in Development mode and strict validation in Production mode. | User may supply `Authentication:Google:ClientId` in settings. | MITIGATED |
| BLK-003 | Upstash Redis | External Redis token | Resilient fallback to ASP.NET Core `IMemoryCache` and in-memory rate limiter when Redis is unreachable. | Graceful degradation active. | MITIGATED |
