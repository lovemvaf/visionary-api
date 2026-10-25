# BẢNG BẰNG CHỨNG MÃ NGUỒN HỆ THỐNG VISIONARY (TH71108)
## PHỤC VỤ GIẢI THÍCH MÃ NGUỒN VÀ TRẢ LỜI PHẢN BIỆN (30 ĐIỂM + 15 ĐIỂM)
**Học phần:** Web API – TH71108 | **Trường Đại học Công nghệ Đồng Nai (DNTU)**
**Nhóm phát triển:** VISIONARY API (*Quách Khoa Đức, Đào Trí Khang, Hồ Đoàng Nguyên Khang, Võ Ngọc Minh Đạt*)
**Commit SHA kiểm chứng:** `af38413` / `77a20d4`

---

## TỔNG HỢP MÃ NGUỒN MINH CHỨNG THEO 16 SLIDE

### 1. Slide 4 – Web Client (Next.js 14 App Router)
- **Nền tảng:** Web Next.js (TypeScript)
- **Tập tin nguồn:** [frontend/src/app/events/page.tsx](file:///c:/Users/asus/Documents/Visionary%20API/frontend/src/app/events/page.tsx#L40-L49)
- **Hàm xử lý:** `loadEvents(searchQuery)`
- **HTTP Method & Endpoint:** `GET /api/events?pageIndex=1&pageSize=12`
- **Đoạn mã (8 dòng thực tế):**
```typescript
const query = new URLSearchParams();
query.set("pageIndex", "1");
query.set("pageSize", "12");
if (searchQuery.trim()) query.set("search", searchQuery.trim());
const res = await fetch(`/api/events?${query.toString()}`, {
  signal: abortController.signal,
  headers: { "Content-Type": "application/json" }
});
const data: ApiResponse<PagedResponse<EventItem>> = await res.json();
if (res.ok && data.success) setEvents(data.data.items);
```
- **Giải thích kỹ thuật:**
  - `URLSearchParams`: Mã hóa an toàn từ khóa tìm kiếm (tránh lỗi injection ký tự đặc biệt trên URL).
  - `/api/events`: Gọi qua BFF (Backend-for-Frontend) cùng nguồn gốc, loại bỏ hoàn toàn lỗi CORS trên trình duyệt.
  - `signal`: Sử dụng `AbortController` để hủy request cũ nếu người dùng gõ từ khóa mới, chống Race Condition.
  - `setEvents(data.data.items)`: Đổ dữ liệu sự kiện thật từ backend vào State React để render ra giao diện.
- **Người trình bày:** Quách Khoa Đức
- **Bằng chứng ảnh:** `deliverables/evidence/02_web_events.png`

---

### 2. Slide 5 & 6 – Android Native (Java 17, Retrofit 2, OkHttp 3)
- **Nền tảng:** Android Native Java
- **Tập tin nguồn:** [mobile/VisionaryAndroid/app/src/main/java/com/visionary/studentconnect/ui/fragments/EventsFragment.java](file:///c:/Users/asus/Documents/Visionary%20API/mobile/VisionaryAndroid/app/src/main/java/com/visionary/studentconnect/ui/fragments/EventsFragment.java#L52-L61)
- **Hàm xử lý:** `loadEvents()`
- **HTTP Method & Endpoint:** `GET /api/events` (qua Retrofit interface)
- **Đoạn mã (10 dòng thực tế):**
```java
ApiClient.getService(getContext()).getEvents(1, 20)
    .enqueue(new Callback<ApiResponse<PagedResponse<EventItem>>>() {
        @Override
        public void onResponse(@NonNull Call<ApiResponse<PagedResponse<EventItem>>> call,
                               @NonNull Response<ApiResponse<PagedResponse<EventItem>>> res) {
            swipeRefresh.setRefreshing(false);
            if (res.isSuccessful() && res.body() != null && res.body().isSuccess()) {
                adapter.setEvents(res.body().getData().getItems());
            }
        }
        @Override
        public void onFailure(@NonNull Call<ApiResponse<PagedResponse<EventItem>>> call, @NonNull Throwable t) {
            swipeRefresh.setRefreshing(false);
        }
    });
```
- **Giải thích kỹ thuật:**
  - `enqueue(...)`: Bắt buộc thực thi yêu cầu mạng trên **Luồng Nền (Worker Thread)** do OkHttp quản lý. Nếu gọi trên Main Thread, Android sẽ ném ngoại lệ `NetworkOnMainThreadException` và văng app ngay lập tức.
  - `onResponse`: Tự động được Retrofit điều phối đưa kết quả quay về **Luồng Giao diện chính (Main/UI Thread)** thông qua `Handler(Looper.getMainLooper())`.
  - `adapter.setEvents(...)`: Cập nhật danh sách phần tử vào RecyclerView Adapter để hiển thị trên điện thoại.
- **Người trình bày:** Đào Trí Khang
- **Bằng chứng ảnh:** `deliverables/evidence/11_android_events.png`

---

### 3. Slide 8 & 9 – ASP.NET Core 8 Web API & Xuyên Suốt Một Request
- **Nền tảng:** ASP.NET Core 8 Web API (.NET 8 LTS)
- **Tập tin nguồn:** [backend/src/Visionary.Api/Controllers/EventsController.cs](file:///c:/Users/asus/Documents/Visionary%20API/backend/src/Visionary.Api/Controllers/EventsController.cs#L35-L45)
- **Hàm xử lý:** `GetEvents(EventStatus? status, string? search, int pageIndex, int pageSize)`
- **HTTP Method & Endpoint:** `GET /api/events`
- **Đoạn mã (9 dòng thực tế):**
```csharp
[HttpGet]
public async Task<ActionResult<ApiResponse<PagedResponse<EventDto>>>> GetEvents(
    [FromQuery] EventStatus? status = null, [FromQuery] string? search = null,
    [FromQuery] int pageIndex = 1, [FromQuery] int pageSize = 10)
{
    var query = _context.Events.AsNoTracking().Where(e => e.Status != EventStatus.Draft);
    if (!string.IsNullOrWhiteSpace(search)) query = query.Where(e => e.Title.Contains(search.Trim()));
    var total = await query.CountAsync();
    var items = await query.OrderByDescending(e => e.StartTime).Skip((pageIndex - 1) * pageSize).Take(pageSize).ToListAsync();
    return Ok(ApiResponse<PagedResponse<EventDto>>.Ok(new PagedResponse<EventDto>(items, total, pageIndex, pageSize)));
}
```
- **Giải thích kỹ thuật:**
  - `AsNoTracking()`: Tối ưu hiệu năng truy vấn chỉ đọc, không tốn bộ nhớ lưu trạng thái theo dõi trong DbContext.
  - `e.Status != EventStatus.Draft`: Bảo mật tuyệt đối, ngăn chặn rò rỉ sự kiện nháp ra công chúng.
  - `Skip((pageIndex - 1) * pageSize).Take(pageSize)`: Phân trang trực tiếp tại câu lệnh SQL (`OFFSET / LIMIT` trên PostgreSQL), không tải toàn bộ dữ liệu vào RAM server.
  - `ApiResponse<PagedResponse<T>>`: Cấu trúc JSON thống nhất bao bọc kết quả, trả về `items`, `totalCount`, `pageIndex`, `pageSize`.
- **Người trình bày:** Hồ Đoàng Nguyên Khang
- **Bằng chứng ảnh:** `deliverables/evidence/05_swagger_endpoint.png`

---

### 4. Slide 10 – Xác thực và Phân quyền JWT Bearer (Security)
- **Nền tảng:** ASP.NET Core Middleware & Controller Authorization
- **Tập tin nguồn:** [backend/src/Visionary.Infrastructure/Services/JwtService.cs](file:///c:/Users/asus/Documents/Visionary%20API/backend/src/Visionary.Infrastructure/Services/JwtService.cs#L45-L55)
- **Hàm xử lý:** `GenerateToken(User user, IList<string> roles)`
- **Cơ chế:** Ký HMAC-SHA256 với Secret Key, đóng gói Claims `ClaimTypes.NameIdentifier` (UserId), `ClaimTypes.Email`, `ClaimTypes.Role`.
- **Đoạn mã (9 dòng thực tế):**
```csharp
var claims = new List<Claim> {
    new(ClaimTypes.NameIdentifier, user.Id.ToString()),
    new(ClaimTypes.Email, user.Email),
    new(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString())
};
claims.AddRange(roles.Select(role => new Claim(ClaimTypes.Role, role)));
var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_jwtSecret));
var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);
var token = new JwtSecurityToken(_issuer, _audience, claims, expires: DateTime.UtcNow.AddHours(4), signingCredentials: creds);
return new JwtSecurityTokenHandler().WriteToken(token);
```
- **Điểm chốt bảo mật:**
  - JWT không phải là chuỗi mã hóa bí mật (bất kỳ ai cũng giải mã Base64 đọc được Header và Payload).
  - Tính toàn vẹn được đảm bảo bởi **Chữ ký số (Signature)**. Khi client gửi header `Authorization: Bearer <token>`, middleware `UseAuthentication()` dùng Secret Key để xác thực chữ ký. Nếu người dùng tự ý đổi `roles` từ `Student` thành `Admin`, chữ ký sẽ sai lệch và server trả về mã **401 Unauthorized** ngay lập tức.
- **Người trình bày:** Hồ Đoàng Nguyên Khang
- **Bằng chứng ảnh:** `deliverables/evidence/13_401_response.png`, `deliverables/evidence/14_403_response.png`

---

### 5. Slide 12 & 13 – Windows Forms C# (.NET 8 Windows Desktop)
- **Nền tảng:** Windows Forms (.NET 8 LTS)
- **Tập tin nguồn:** [desktop/Visionary.Desktop/Forms/MainForm.cs](file:///c:/Users/asus/Documents/Visionary%20API/desktop/Visionary.Desktop/Forms/MainForm.cs#L590-L600)
- **Hàm xử lý:** `LoadEventRegistrationsAsync(Guid eventId)`
- **HTTP Method & Endpoint:** `GET /api/events/{id}/registrations`
- **Đoạn mã (9 dòng thực tế):**
```csharp
private async Task LoadEventRegistrationsAsync(Guid eventId)
{
    var list = await ApiClient.GetEventRegistrationsAsync(eventId);
    _dgvRegistrations.DataSource = null;
    _dgvRegistrations.DataSource = list.Select(r => new {
        MSSV = r.StudentId ?? "N/A",
        SinhVien = r.FullName,
        Email = r.Email,
        ThoiGianDangKy = r.RegisteredAt.ToLocalTime().ToString("dd/MM/yyyy HH:mm"),
        TrangThai = r.IsAttended ? "Đã điểm danh" : "Chưa điểm danh"
    }).ToList();
}
```
- **Giải thích kỹ thuật:**
  - `await`: Nhường quyền điều khiển cho luồng giao diện (UI Thread) trong lúc HttpClient gửi gói tin qua mạng, ngăn chặn hiện tượng đơ giật cửa sổ (`Not Responding`).
  - Tuyệt đối không dùng `.Result` hay `.Wait()`: Nếu gọi `.Result` trên UI thread, luồng giao diện sẽ bị khóa cứng trong khi Task đang chờ UI thread để hoàn tất -> gây **Deadlock** vĩnh viễn.
  - `_dgvRegistrations`: Điều khiển `DataGridView` chuẩn của Windows Forms, gán danh sách DTO đã được định dạng hiển thị.
- **Người trình bày:** Võ Ngọc Minh Đạt
- **Bằng chứng ảnh:** `deliverables/evidence/09_winforms_events.png`

---

### 6. Slide 15 – Sự cố thật và Quy trình Khắc phục
- **Sự cố 1:** Lỗi biên dịch `NETSDK1100` trong GitHub Actions Backend CI.
  - **Thông điệp lỗi nguyên văn:**
    ```text
    error NETSDK1100: To build a project targeting Windows on this operating system, set the EnableWindowsTargeting property to true. [/home/runner/work/visionary-api/desktop/Visionary.Desktop/Visionary.Desktop.csproj]
    ```
  - **Nguyên nhân gốc rễ:** File solution gốc `backend/Visionary.sln` chứa cả dự án `Visionary.Desktop.csproj` (`net8.0-windows`). Khi GitHub Actions chạy trên máy ảo Linux (`ubuntu-latest`), .NET SDK không cho phép build dự án Windows GUI.
  - **Khắc phục:** Tách thành `backend/Visionary.Backend.sln` độc lập chỉ chứa 4 dự án backend (`Core`, `Infrastructure`, `Api`, `Tests`). WinForms được build bằng workflow riêng `desktop.yml` trên máy ảo `windows-latest`.
- **Sự cố 2:** Lỗi bất đối xứng Generic Type Retrofit trên Android (`ApiResponse<List<T>>` vs `ApiResponse<PagedResponse<T>>`).
  - **Hiện tượng:** Màn hình English for IT và Opportunities trên Android bị văng app hoặc báo lỗi mạng.
  - **Nguyên nhân:** Backend trả về object phân trang `{ success: true, data: { items: [...], totalCount: 10 } }`, nhưng interface Android lại khai báo nhận mảng `List<T>`. Gson gặp object khi đang chờ array nên ném ngoại lệ `JsonParseException`.
  - **Khắc phục:** Cập nhật `VisionaryApiService.java` dùng đúng `ApiResponse<PagedResponse<LearningResourceItem>>` và truyền tham số `pageIndex`, `pageSize`.
- **Người trình bày:** Võ Ngọc Minh Đạt
- **Bằng chứng ảnh:** `deliverables/evidence/15_real_error_log.png`, `deliverables/evidence/16_error_fixed_test.png`
