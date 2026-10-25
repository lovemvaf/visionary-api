# BÁO CÁO PHÂN TÍCH VÀ XỬ LÝ SỰ CỐ KỸ THUẬT THỰC TẾ
## SỰ CỐ GITHUB ACTIONS BACKEND CI RUN #12 – HỌC PHẦN WEB API (TH71108)

**Dự án:** VISIONARY – Hệ thống Quản lý Hoạt động Hội nhập  
**Nhóm sinh viên:** VISIONARY API (Quách Khoa Đức, Đào Trí Khang, Hồ Đoàng Nguyên Khang, Võ Ngọc Minh Đạt)  
**Mục tiêu học phần:** Minh chứng năng lực đọc thông điệp lỗi nguyên văn, xác định nguyên nhân gốc rễ, đưa ra giải pháp kỹ thuật chuẩn mực và kiểm thử hồi quy thành công (Năng lực số 8 & Tiêu chí số 5 Thang điểm 100).

---

## 1. HIỆN TƯỢNG VÀ BỐI CẢNH XẢY RA SỰ CỐ

Trong quá trình thiết lập quy trình tích hợp liên tục (CI/CD) trên GitHub Actions cho dịch vụ ASP.NET Core 8 Web API, pipeline chạy kiểm thử tự động đã bị ngắt quãng và trả về mã lỗi kết thúc `Process completed with exit code 1`.

- **Workflow:** `Backend CI – ASP.NET Core 8 Web API`
- **GitHub Actions Run ID:** `40226894806` (Run #12)
- **URL Run:** [https://github.com/lovemvaf/visionary-api/actions/runs/40226894806](https://github.com/lovemvaf/visionary-api/actions/runs/40226894806)
- **Commit SHA:** `2153dd137a68972f5a45530cd973c292ce582908`
- **Môi trường:** `ubuntu-latest`, .NET SDK 8.0.x

---

## 2. BẰNG CHỨNG LỖI NGUYÊN VĂN (RAW ERROR LOGS)

### 2.1. Thống kê bài kiểm thử xUnit:
```text
Total tests: 15
Passed: 13
Failed: 2
Test Run Failed. Build FAILED. 0 Warning(s) 0 Error(s)
Process completed with exit code 1.
```

### 2.2. Hai bài kiểm thử thất bại:
1. **Bài kiểm thử số 1:** `Visionary.Tests.PostsLogicAuditTests.Search_WithCategory_And_EmptyState_AreAccurate`
   - **Vị trí:** `backend/tests/Visionary.Tests/PostsLogicAuditTests.cs`, Dòng 168
   - **Thông báo lỗi nguyên văn:**
     ```text
     Assert.True() Failure
     Expected: True
     Actual:   False
     ```
   - **Đoạn code assert:**
     ```csharp
     var searchRes = await _client.GetFromJsonAsync<ApiResponse<PagedResponse<PostDto>>>("/api/posts?search=Clean%20Architecture");
     Assert.NotNull(searchRes?.Data);
     Assert.True(searchRes.Data.TotalCount >= 1); // <-- FAIL TẠI ĐÂY
     ```

2. **Bài kiểm thử số 2:** `Visionary.Tests.PostsLogicAuditTests.GetPostBySlug_ValidPublishedPost_Returns200AndIncrementsView`
   - **Vị trí:** `backend/tests/Visionary.Tests/PostsLogicAuditTests.cs`, Dòng 183
   - **Thông báo lỗi nguyên văn:**
     ```text
     System.Net.Http.HttpRequestException: Response status code does not indicate success: 404 (Not Found).
     ```
   - **Endpoint được gọi:** `GET /api/posts/chao-mung-he-sinh-thai-visionary-2026`

### 2.3. Các thông báo lỗi SQLite đi kèm trong cùng log khởi tạo:
```text
fail: Microsoft.EntityFrameworkCore.Database.Command[20102]
      Failed executing DbCommand (6ms) [Parameters=[], CommandType='Text', CommandTimeout='30']
      CREATE TABLE "AchievementCategories" ...
[DB INIT] Notice on table creation: SQLite Error 1: 'table "AchievementCategories" already exists'.

[DB INIT ERROR] Seeding warning or retry needed: SQLite Error 19: UNIQUE constraint failed: Roles.Name
```

---

## 3. ĐIỀU TRA VÀ XÁC ĐỊNH NGUYÊN NHÂN GỐC RỄ (ROOT CAUSE ANALYSIS)

Sau khi rà soát toàn bộ chu trình khởi động test của xUnit và WebApplicationFactory, nhóm đã xác định được chuỗi nguyên nhân gốc rễ như sau:

1. **Hiện tượng chạy song song giữa các Test Class (Parallel Execution Race Condition):**
   - Bộ test gồm 2 class kiểm thử tích hợp: `PostsLogicAuditTests` và `ApiIntegrationTests`. Cả hai đều khai báo độc lập `IClassFixture<WebApplicationFactory<Program>>`.
   - Cơ chế mặc định của xUnit trên runner đa luồng (Multi-core Ubuntu) sẽ khởi chạy các Test Class song song trên các thread khác nhau.
   - Kết quả: Có 2 instance `WebApplicationFactory<Program>` được khởi tạo đồng thời cùng lúc.

2. **Xung đột khởi tạo Database SQLite (Connection Collision & Race Condition):**
   - Cả 2 instance test server đều đọc `appsettings.json` và cùng trỏ vào một file cơ sở dữ liệu dùng chung: `Data Source=visionary.db`.
   - Cả hai instance cùng thực thi hàm `DbInitializer.SeedAsync(db, hasher)` trong `Program.cs` ở cùng một mili-giây.

3. **Gãy chu trình Seed do vi phạm ràng buộc Unique (UNIQUE Constraint Failure):**
   - Thread 1 và Thread 2 cùng kiểm tra: `!await context.Roles.AnyAsync(x => x.Name == "Admin")` $\rightarrow$ Cả hai đều nhận kết quả `false` (vì bảng đang trống).
   - Cả hai cùng thêm thực thể Role `"Admin"` vào DbContext.
   - Thread 1 gọi `SaveChangesAsync()` thành công.
   - Thread 2 gọi `SaveChangesAsync()` ngay sau đó $\rightarrow$ Bị SQLite ném ngoại lệ: `SQLite Error 19: UNIQUE constraint failed: Roles.Name`.

4. **Hệ quả dây chuyền dẫn đến 2 bài test thất bại:**
   - Khi Thread 2 bị ném ngoại lệ ở dòng 52 của `DbInitializer.cs`, khối lệnh `SeedAsync` của instance này **bị hủy ngang ngay lập tức**, trước khi kịp chạy đến phần seed danh mục bài viết (`PostCategories`) và các bài viết mẫu (`Posts`).
   - Khối `try/catch` tại `Program.cs` bắt ngoại lệ và ghi log thông báo nhưng vẫn để ứng dụng Web API khởi chạy với cơ sở dữ liệu rỗng một phần.
   - Khi `PostsLogicAuditTests` gửi request:
     - `GET /api/posts?search=Clean%20Architecture` $\rightarrow$ Trả về `TotalCount = 0` (thay vì $\ge 1$) $\rightarrow$ Gây lỗi `Assert.True() Failure`.
     - `GET /api/posts/chao-mung-he-sinh-thai-visionary-2026` $\rightarrow$ Trả về `404 Not Found` (do bài viết chưa được nạp) $\rightarrow$ Gây lỗi `HttpRequestException: 404`.

---

## 4. GIẢI PHÁP KỸ THUẬT TRIỆT ĐỂ (ARCHITECTURAL REMEDIATION)

Để giải quyết triệt để cả lỗi xung đột khởi tạo và lỗi chia sẻ dữ liệu test, nhóm áp dụng giải pháp 2 tầng chuẩn mực của ASP.NET Core & xUnit:

### 4.1. Tầng 1: Đồng bộ hóa luồng (Thread Synchronization) trong `DbInitializer.cs`
- Thêm khóa đồng bộ tĩnh: `private static readonly SemaphoreSlim _seedLock = new(1, 1);`
- Toàn bộ thân hàm `SeedAsync` được bao bọc trong `await _seedLock.WaitAsync()` và `finally { _seedLock.Release(); }`.
- Thay vì gọi `CreateTablesAsync()` gây lỗi `table already exists`, nhóm kiểm tra `!await databaseCreator.HasTablesAsync()` trước khi tạo bảng.
- Bảo vệ bước lưu Roles bằng khối try/catch cục bộ, đảm bảo tính bất biến (Idempotent).

### 4.2. Tầng 2: Thiết kế `CustomWebApplicationFactory` và Shared Test Collection
- Tạo lớp `CustomWebApplicationFactory : WebApplicationFactory<Program>` trong `backend/tests/Visionary.Tests/CustomWebApplicationFactory.cs`.
- Tự động cấp phát một file cơ sở dữ liệu SQLite cô lập trong thư mục tạm: `visionary_test_{Guid:N}.db`.
- Định nghĩa Collection chung cho toàn bộ bài kiểm thử tích hợp:
  ```csharp
  [CollectionDefinition("IntegrationTests")]
  public class IntegrationTestCollection : ICollectionFixture<CustomWebApplicationFactory> {}
  ```
- Đánh dấu thuộc tính `[Collection("IntegrationTests")]` trên cả `PostsLogicAuditTests` và `ApiIntegrationTests`.
- **Lợi ích kiến trúc:**
  - xUnit chỉ khởi tạo Web API test server đúng 1 lần cho cả bộ test.
  - Cơ sở dữ liệu test được khởi tạo và seed hoàn chỉnh đúng 1 lần, loại bỏ hoàn toàn hiện tượng race condition.
  - Dữ liệu test hoàn toàn độc lập, không xâm phạm file `visionary.db` hay database production.
  - Sau khi test xong, tệp tạm được tự động giải phóng sạch sẽ.

---

## 5. KẾT QUẢ KIỂM CHỨNG THỰC TẾ (VERIFICATION & REGRESSION RESULTS)

### 5.1. Kết quả kiểm thử cục bộ:
Nhóm đã chạy lặp lại 3 lần liên tiếp lệnh kiểm thử không phụ thuộc cache:
```bash
dotnet test backend/Visionary.Backend.sln --logger "console;verbosity=detailed"
```
**Kết quả 3 lượt chạy:**
- Lượt 1: **15/15 Passed (100%)** – Thời gian: 2.8 giây. Không còn bất kỳ thông báo lỗi SQLite nào.
- Lượt 2: **15/15 Passed (100%)** – Thời gian: 1.0 giây.
- Lượt 3: **15/15 Passed (100%)** – Thời gian: 1.0 giây.
- Bài test Search: `Passed [48 ms]`.
- Bài test GetBySlug: `Passed [28 ms]`.

### 5.2. Đối chiếu nguyên nhân và kết quả:
| Trạng thái trước sửa (CI Run #12) | Trạng thái sau sửa (Kiểm thử thực tế) |
| :--- | :--- |
| 13 Passed / 2 Failed | **15 Passed / 0 Failed (100%)** |
| `SQLite Error 1: table already exists` | **Khắc phục hoàn toàn** nhờ kiểm tra `HasTablesAsync()` |
| `SQLite Error 19: UNIQUE constraint Roles.Name` | **Khắc phục hoàn toàn** nhờ `SemaphoreSlim` và `Shared Test Collection` |
| Search bài viết không ra kết quả (TotalCount = 0) | **Tìm thấy bài viết chính xác (TotalCount = 1)** |
| Slug `chao-mung...` trả về 404 Not Found | **Trả về 200 OK + AuthorName 'Quách Khoa Đức'** |

### 5.3. Kết quả xác minh trên GitHub Actions từ xa (Remote CI Verification):
Sau khi hoàn tất kiểm thử cục bộ, nhóm đã commit và push mã nguồn khắc phục lên GitHub repository:
- **Commit SHA:** `c7af080` ("fix(backend): resolve SQLite concurrency race condition and isolate integration test DB")
- **Workflow:** `Backend CI - ASP.NET Core 8 Web API`
- **GitHub Actions Run ID:** `40231783994`
- **URL Run:** [https://github.com/lovemvaf/visionary-api/actions/runs/40231783994](https://github.com/lovemvaf/visionary-api/actions/runs/40231783994)
- **Kết quả thực tế:** **SUCCESS / BÁO XANH HOÀN TOÀN**
  - Runner: `ubuntu-latest` (Linux x64)
  - Thống kê: **Total tests: 15. Passed: 15. Failed: 0. Skipped: 0. Duration: 2.8s.**
  - Exit Code: **0 (Passed)**
- **Workflow đồng thời:** `Security and Code Quality Analysis` (Run ID: `40231784031`) -> **SUCCESS**.

---

## 6. BÀI HỌC KINH NGHIỆM VÀ ĐÓNG GÓP CỦA CÔNG CỤ AI

1. **Bài học về Kiểm thử Tích hợp (Integration Testing Best Practices):**
   - Không được để các bài kiểm thử tích hợp dùng chung một tệp cơ sở dữ liệu có trạng thái thay đổi khi chạy song song.
   - Cần phân biệt rõ giữa lỗi biên dịch (Compilation Error) và lỗi logic dữ liệu trong lúc chạy kiểm thử (Runtime Test Failure).
2. **Khai báo minh bạch về vai trò của AI:**
   - Công cụ AI (Google Antigravity) đã hỗ trợ phân tích luồng log lỗi của GitHub Actions, phát hiện nguyên nhân xung đột `UNIQUE constraint failed: Roles.Name` do xUnit chạy đa luồng, và đề xuất cấu trúc `CustomWebApplicationFactory`.
   - Nhóm sinh viên đã trực tiếp kiểm chứng giả thuyết, triển khai mã nguồn vào `DbInitializer.cs`, viết lớp fixture và thực hiện kiểm thử hồi quy 15/15 bài test đạt yêu cầu.
