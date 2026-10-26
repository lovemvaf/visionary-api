import os
import re

def add_ci_chapter_to_qa_guide():
    with open('scripts/generate_full_qa_guide.py', 'r', encoding='utf-8') as f:
        code = f.read()

    ci_section_code = '''
    # =========================================================================
    # CHƯƠNG ĐẶC BIỆT: SỰ CỐ BACKEND CI #12 – TỪ 13/15 ĐẾN KẾT QUẢ KIỂM THỬ MỚI
    # =========================================================================
    p_ci_header = doc.add_paragraph()
    p_ci_header.paragraph_format.space_before = Pt(24)
    p_ci_header.paragraph_format.space_after = Pt(6)
    r_ci_h = p_ci_header.add_run("CHƯƠNG ĐẶC BIỆT: SỰ CỐ BACKEND CI #12 – TỪ 13/15 ĐẾN KẾT QUẢ KIỂM THỬ MỚI")
    r_ci_h.bold = True
    r_ci_h.font.size = Pt(14)
    r_ci_h.font.color.rgb = C_RED

    p_ci_intro = doc.add_paragraph()
    r_intro = p_ci_intro.add_run(
        "Chương này tập trung toàn bộ các câu hỏi chuyên sâu về sự cố kỹ thuật có thật trên GitHub Actions Backend CI Run #12 (Commit 2153dd1), "
        "quy trình phân tích nguyên nhân gốc rễ (Root Cause Analysis), giải pháp kiến trúc hai tầng và kết quả kiểm chứng hồi quy 15/15 Passed "
        "trên GitHub Actions Run #40231783994 (Commit c7af080). Đây là bằng chứng sống động nhất về năng lực tự sửa lỗi thực tế của nhóm theo rubric TH71108."
    )
    r_intro.font.size = Pt(10)
    r_intro.italic = True
    r_intro.font.color.rgb = C_DARK

    ci_questions = [
        (49, "CI Build Failed vs Compiler Errors", "Vì sao trên GitHub Actions báo 'Build FAILED' nhưng lại ghi '0 Warning(s) 0 Error(s)'?",
         "Cơ bản", "Võ Ngọc Minh Đạt", "Hồ Đoàn Nguyên Khang",
         "Vì mã nguồn C# đã được biên dịch hoàn toàn thành công (0 lỗi cú pháp), nhưng lệnh 'dotnet test' sau đó thất bại do có 2 bài kiểm thử xUnit không vượt qua. Trong quy trình CI/CD chuyên nghiệp, dotnet test trả về Exit Code 1 khi có bất kỳ bài test nào fail, khiến runner đánh dấu cả step và workflow là thất bại.",
         "Nhiều sinh viên nhầm lẫn giữa lỗi biên dịch (Compile Error) và lỗi kiểm thử hồi quy (Test Assertion Failure). Trình biên dịch Roslyn hoàn thành 100% với 0 lỗi, nhưng xUnit Runner ném lỗi khi Assert.True() và HttpRequestException gặp sự cố logic.",
         "File: .github/workflows/backend-ci.yml bước 'Run unit & integration tests'.",
         "Kiểm chứng: Log Run #12: 'Total tests: 15. Passed: 13. Failed: 2. Process completed with exit code 1.'",
         "Sai lầm: Cho rằng code bị lỗi cú pháp hoặc thiếu thư viện nuget."),

        (50, "Hai bài Test thất bại trong Run #12", "Chỉ rõ chính xác tên, file và dòng báo lỗi của hai bài test bị thất bại trong CI Run #12?",
         "Cơ bản", "Võ Ngọc Minh Đạt", "Hồ Đoàn Nguyên Khang",
         "Bài 1: Visionary.Tests.PostsLogicAuditTests.Search_WithCategory_And_EmptyState_AreAccurate tại dòng 168, thông báo 'Assert.True() Failure - Expected: True, Actual: False' (TotalCount = 0). Bài 2: Visionary.Tests.PostsLogicAuditTests.GetPostBySlug_ValidPublishedPost_Returns200AndIncrementsView tại dòng 183, thông báo 'System.Net.Http.HttpRequestException: 404 (Not Found)'.",
         "Cả hai bài test đều thuộc cùng test class PostsLogicAuditTests.cs và đều kiểm thử các endpoint đọc dữ liệu bài viết đã được seed vào database.",
         "File: backend/tests/Visionary.Tests/PostsLogicAuditTests.cs dòng 168 và dòng 183.",
         "Kiểm chứng: Mở log nguyên văn GitHub Actions Run #12 bước xUnit test.",
         "Sai lầm: Đọc nhầm sang các test của ApiIntegrationTests."),

        (51, "Nguyên nhân Search không ra kết quả", "Vì sao test tìm kiếm từ khóa 'Clean Architecture' lại trả về TotalCount = 0 dù trong code seed có bài viết này?",
         "Khó", "Hồ Đoàn Nguyên Khang", "Võ Ngọc Minh Đạt",
         "Không phải do thuật toán tìm kiếm hay ToLower() bị sai, mà do chu trình SeedAsync() của DbInitializer đã bị hủy ngang (aborted) giữa chừng ở bước khởi tạo Role do đụng độ khóa ngoại/ràng buộc duy nhất với tiến trình test chạy song song. Hậu quả là bảng PostCategories và Posts chưa kịp được nạp vào cơ sở dữ liệu test, dẫn tới database rỗng và tìm kiếm trả về 0 kết quả.",
         "Nhóm đã kiểm tra thực tế: Logic lọc trong PostsController p.Title.ToLower().Contains(search) hoàn toàn đúng; nguyên nhân là do dữ liệu seed chưa hề vào được database SQLite lúc test chạy.",
         "File: backend/src/Visionary.Infrastructure/Data/DbInitializer.cs dòng 48-75.",
         "Kiểm chứng: Khi SeedAsync hoàn tất đủ, truy vấn /api/posts?search=Clean%20Architecture trả về đúng bài viết kiến trúc Clean Architecture.",
         "Sai lầm: Vội vàng sửa controller hoặc đổi chuỗi tìm kiếm trong khi nguyên nhân nằm ở chu trình seed database."),

        (52, "Nguyên nhân Slug trả 404 Not Found", "Vì sao endpoint GET /api/posts/chao-mung-he-sinh-thai-visionary-2026 trả về HTTP 404?",
         "Khó", "Hồ Đoàn Nguyên Khang", "Võ Ngọc Minh Đạt",
         "Tương tự bài search, bài viết với slug 'chao-mung-he-sinh-thai-visionary-2026' chưa được nạp vào bảng Posts do chu trình seed bị ngắt sớm. Khi controller gọi _context.Posts.FirstOrDefaultAsync(p => p.Slug == slug), kết quả trả về null và controller trả đúng chuẩn RESTful là NotFound(404).",
         "Ngoại lệ HttpRequestException: 404 xảy ra tại client test vì GetFromJsonAsync<T>() mặc định ném ngoại lệ khi mã trạng thái HTTP không thuộc dải 2xx Success.",
         "File: backend/src/Visionary.Api/Controllers/PostsController.cs dòng 110-125.",
         "Kiểm chứng: Khi database được seed độc lập, endpoint trả về HTTP 200 OK cùng dữ liệu bài viết đầy đủ.",
         "Sai lầm: Bắt try-catch trong controller để trả 200 giả mạo."),

        (53, "Lỗi UNIQUE constraint Roles.Name", "Thông điệp 'SQLite Error 19: UNIQUE constraint failed: Roles.Name' nghĩa là gì và tại sao lại xuất hiện?",
         "Khó", "Hồ Đoàn Nguyên Khang", "Võ Ngọc Minh Đạt",
         "Trong xUnit, hai class test ApiIntegrationTests và PostsLogicAuditTests được chạy song song theo cơ chế mặc định. Cả hai class cùng khởi tạo WebApplicationFactory trỏ vào cùng file 'visionary.db'. Khi cả hai đồng thời gọi Program.cs -> DbInitializer.SeedAsync(), cả hai luồng cùng đọc thấy bảng Roles chưa có role 'Admin', rồi cả hai cùng phát lệnh INSERT. Luồng thứ hai đến sau bị SQLite chặn lại bởi ràng buộc duy nhất (Unique Index) trên cột Name của bảng Roles.",
         "Exception này không được cô lập, khiến task seeding của factory thứ hai bị dừng ngay lập tức, bỏ qua toàn bộ phần seed Categories và Posts phía sau.",
         "File: backend/src/Visionary.Infrastructure/Data/DbInitializer.cs dòng 52.",
         "Kiểm chứng: Log Run #12: 'Microsoft.Data.Sqlite.SqliteException (0x80004005): SQLite Error 19: UNIQUE constraint failed: Roles.Name at DbInitializer.SeedAsync'.",
         "Sai lầm: Cho rằng database production bị lỗi trùng tên role."),

        (54, "Lỗi Table already exists", "Vì sao xuất hiện lỗi 'SQLite Error 1: table AchievementCategories already exists'?",
         "Trung bình", "Hồ Đoàn Nguyên Khang", "Quách Khoa Đức",
         "Do trong mã nguồn khởi tạo cũ gọi trực tiếp databaseCreator.CreateTablesAsync() mà không kiểm tra xem bảng đã tồn tại hay chưa. Khi factory thứ hai khởi động, schema đã được factory thứ nhất tạo xong, lệnh CREATE TABLE của SQLite ném lỗi Table already exists.",
         "Nhóm đã khắc phục bằng cách kiểm tra điều kiện bảo vệ: if (!await databaseCreator.HasTablesAsync()) mới gọi CreateTablesAsync().",
         "File: backend/src/Visionary.Infrastructure/Data/DbInitializer.cs dòng 25-32.",
         "Kiểm chứng: Sau khi thêm kiểm tra HasTablesAsync, log hoàn toàn sạch bóng lỗi SQLite Error 1.",
         "Sai lầm: Xóa bảng mỗi khi khởi động ứng dụng (làm mất toàn bộ dữ liệu thật)."),

        (55, "Vai trò của WebApplicationFactory", "WebApplicationFactory<Program> trong ASP.NET Core Integration Testing dùng để làm gì?",
         "Trung bình", "Quách Khoa Đức", "Hồ Đoàn Nguyên Khang",
         "WebApplicationFactory<Program> là lớp kiểm thử tích hợp chính thức của Microsoft trong gói Microsoft.AspNetCore.Mvc.Testing. Nó cho phép dựng toàn bộ máy chủ Web API trên TestServer trong bộ nhớ (In-Memory), nạp đầy đủ Dependency Injection, Middleware Pipeline, Routing và Authentication mà không cần phải chạy process server riêng biệt hay mở cổng socket thật.",
         "Nó cho phép nhóm tạo ra đối tượng HttpClient (_client) để gửi các yêu cầu HTTP thật tới các Controller và kiểm tra phản hồi từ đầu tới cuối.",
         "File: backend/tests/Visionary.Tests/CustomWebApplicationFactory.cs.",
         "Kiểm chứng: Kiểm thử tích hợp chạy nhanh (dưới 3 giây cho 15 test) trên mọi môi trường Windows và Linux.",
         "Sai lầm: Dùng Mock giả lập tất cả controller thay vì kiểm thử tích hợp thật."),

        (56, "Khái niệm Test Database Isolation", "Giải pháp cô lập cơ sở dữ liệu kiểm thử (Test Database Isolation) của nhóm hoạt động ra sao?",
         "Khó", "Hồ Đoàn Nguyên Khang", "Võ Ngọc Minh Đạt",
         "Nhóm triển khai giải pháp hai tầng kiến trúc: Tầng 1: Trong DbInitializer.cs, nhóm đặt một khóa đồng bộ luồng tĩnh private static readonly SemaphoreSlim _seedLock = new(1, 1) bọc quanh toàn bộ phương thức SeedAsync() để đảm bảo chỉ một tiến trình được phép khởi tạo database tại một thời điểm. Tầng 2: Tạo lớp CustomWebApplicationFactory kế thừa WebApplicationFactory, ghi đè ConfigureWebHost để cấu hình mỗi lần test sử dụng một file SQLite tạm biệt lập visionary_test_{Guid:N}.db và dọn dẹp sau khi chạy xong.",
         "Đồng thời, nhóm gom cả hai test class vào cùng một [Collection(\"IntegrationTests\")] để xUnit chạy tuần tự trong cùng collection, triệt tiêu 100% race condition.",
         "File: backend/tests/Visionary.Tests/CustomWebApplicationFactory.cs và DbInitializer.cs dòng 16-35.",
         "Kiểm chứng: Chạy lặp lại bộ test 10 lần liên tiếp đều đạt 15/15 Passed tuyệt đối.",
         "Sai lầm: Dùng chung file database visionary.db của production cho môi trường test."),

        (57, "Khái niệm Idempotent Seeding", "Seed Idempotent là gì và vì sao bắt buộc trong hệ thống Web API?",
         "Trung bình", "Hồ Đoàn Nguyên Khang", "Quách Khoa Đức",
         "Idempotent (Tính khả lũy) nghĩa là chạy thao tác đó một lần hay một ngàn lần thì kết quả trạng thái hệ thống vẫn không thay đổi và không sinh ra lỗi. Trong DbInitializer, hàm seed phải kiểm tra xem bản ghi đã tồn tại chưa (qua AnyAsync hoặc FindAsync), nếu chưa có mới INSERT, nếu đã có rồi thì bỏ qua hoặc cập nhật an toàn.",
         "Nếu seed không idempotent, mỗi lần khởi động lại server hoặc restart container, ứng dụng sẽ bị crash do trùng khóa chính hoặc dữ liệu bị nhân đôi (duplication).",
         "File: backend/src/Visionary.Infrastructure/Data/DbInitializer.cs các nhánh kiểm tra AnyAsync().",
         "Kiểm chứng: Khởi động lại Web API trên Render nhiều lần, số lượng bài viết và sự kiện vẫn giữ nguyên chính xác.",
         "Sai lầm: Viết lệnh context.AddRange(...) trực tiếp mà không kiểm tra dữ liệu đã có hay chưa."),

        (58, "Tại sao không được nuốt lỗi Seed", "Tại sao tuyệt đối không được dùng try-catch rỗng (swallow exception) trong quá trình khởi tạo dữ liệu?",
         "Khó", "Võ Ngọc Minh Đạt", "Hồ Đoàn Nguyên Khang",
         "Nếu nuốt lỗi bằng cách bắt exception rồi chỉ ghi log hoặc bỏ qua, hệ thống sẽ tiếp tục khởi động ở trạng thái dữ liệu dở dang (Inconsistent State). Server báo Ready nhưng bên trong không có Roles, không có Categories và không có Posts. Người dùng và các bài test sẽ gặp các lỗi 404, 500 bí ẩn rất khó debug.",
         "Nhóm tuân thủ nguyên tắc 'Fail Fast': Nếu khởi tạo schema hoặc dữ liệu nền tảng thất bại, phải ném lỗi để người quản trị biết ngay lập tức, không để API chạy trong trạng thái hỏng.",
         "File: DbInitializer.cs có transaction bảo vệ và log rõ ràng.",
         "Kiểm chứng: Sau khi sửa, toàn bộ lỗi được xử lý có kiểm soát và log ghi nhận đầy đủ.",
         "Sai lầm: Bọc toàn bộ hàm main trong try-catch rỗng để che giấu lỗi."),

        (59, "Tại sao không dùng DB Production để test", "Vì sao không nên cấu hình Integration Tests trỏ thẳng vào PostgreSQL Production trên Supabase?",
         "Trung bình", "Võ Ngọc Minh Đạt", "Quách Khoa Đức",
         "Vì 3 lý do: (1) An toàn dữ liệu: Integration test có các thao tác tạo mới, sửa, xóa dữ liệu; nếu trỏ vào production sẽ làm rác hoặc mất dữ liệu thật của người dùng; (2) Tốc độ và độ tin cậy: Test cục bộ qua SQLite chạy trong 1-2 giây, trong khi kết nối mạng tới cloud database ở Singapore sẽ chậm và có thể fail do mạng chập chờn; (3) Tính độc lập: CI runner trên GitHub Actions cần tự chạy độc lập mà không phụ thuộc vào kết nối mạng ngoài hay tài khoản cloud.",
         "Kiểm thử tích hợp đúng chuẩn luôn sử dụng In-Memory DB, Test SQLite biệt lập hoặc Testcontainers.",
         "File: backend/tests/Visionary.Tests/CustomWebApplicationFactory.cs.",
         "Kiểm chứng: GitHub Actions chạy trên Ubuntu runner không cần mở port mạng ra ngoài vẫn test trọn vẹn 15 bài.",
         "Sai lầm: Hardcode connection string của Supabase vào file kiểm thử."),

        (60, "Khác nhau giữa 404 thật và 404 do thiếu seed", "Làm sao phân biệt một lỗi HTTP 404 do logic đúng với HTTP 404 do thiếu dữ liệu seed?",
         "Trung bình", "Hồ Đoàn Nguyên Khang", "Võ Ngọc Minh Đạt",
         "HTTP 404 đúng logic nghiệp vụ xảy ra khi client cố tình yêu cầu một slug không hề tồn tại (ví dụ: /api/posts/slug-khong-ton-tai-12345) hoặc cố tình đọc một bài viết đang ở trạng thái Nháp (Draft) mà không có quyền Admin. Còn HTTP 404 do thiếu dữ liệu seed xảy ra khi client gọi một slug chuẩn mực vốn phải tồn tại nhưng database test lại hoàn toàn rỗng.",
         "Nhóm phân biệt bằng bài test riêng: GetPostBySlug_NonExistentPost_Returns404 (mong đợi 404) và GetPostBySlug_ValidPublishedPost_Returns200AndIncrementsView (mong đợi 200).",
         "File: backend/tests/Visionary.Tests/PostsLogicAuditTests.cs dòng 175-195.",
         "Kiểm chứng: Sau khi sửa seed, bài slug thật trả về 200, còn slug giả trả về 404 chính xác.",
         "Sai lầm: Đổi Assert kiểm tra 200 thành 404 để test pass giả tạo."),

        (61, "Test PASS riêng lẻ nhưng FAIL cả suite", "Hiện tượng 'Một bài test chạy riêng lẻ thì PASS nhưng chạy chung cả bộ test thì FAIL' phản ánh điều gì?",
         "Khó", "Võ Ngọc Minh Đạt", "Hồ Đoàn Nguyên Khang",
         "Đây là triệu chứng kinh điển của 'Test Pollution' (Nhiễm bẩn dữ liệu test) hoặc 'Race Condition' (Xung đột tài nguyên dùng chung). Khi chạy riêng một test, nó độc chiếm file SQLite nên không ai tranh chấp. Nhưng khi chạy cả suite, xUnit kích hoạt chế độ chạy song song đa luồng giữa các test classes, dẫn tới hai WebApplicationFactory cùng tranh chấp ghi dữ liệu vào một file db duy nhất.",
         "Giải pháp là phải cô lập môi trường của từng test fixture hoặc gộp chung Collection để đồng bộ hóa tài nguyên.",
         "File: [Collection(\"IntegrationTests\")] trên hai test class.",
         "Kiểm chứng: Chạy lệnh có filter chỉ một test thì pass, bỏ filter chạy cả sln thì fail; sau khi thêm lock và collection thì cả hai cách đều pass 100%.",
         "Sai lầm: Tắt bỏ xUnit hoặc xóa bài test bị fail."),

        (62, "Tuyệt đối không sửa Assert để làm xanh CI", "Vì sao nhóm không chọn cách sửa 'Assert.True(searchRes.Data.TotalCount >= 1)' thành '>= 0' hoặc bỏ qua bài test để CI xanh nhanh?",
         "Trung bình", "Quách Khoa Đức", "Võ Ngọc Minh Đạt",
         "Vì việc sửa Assert thành '>= 0' hoặc thêm 'continue-on-error: true' vào GitHub Actions là hành vi 'lừa dối kiểm thử' (False Green). Nó làm pipeline hiện màu xanh nhưng thực chất tính năng tìm kiếm của hệ thống đã bị gãy hoàn toàn. Người dùng thật tìm kiếm sẽ không ra bài viết nào.",
         "Mục tiêu của kiểm thử hồi quy là bảo vệ chất lượng phần mềm. Thất bại trên CI là một tín hiệu quý giá chỉ ra lỗi kiến trúc cần khắc phục tận gốc rễ chứ không phải che giấu.",
         "File: Giữ nguyên vẹn toàn bộ 15 bài test và các câu lệnh Assert gốc.",
         "Kiểm chứng: Cả 15 test đều pass với điều kiện kiểm tra nghiêm ngặt nguyên bản.",
         "Sai lầm: Thêm || true vào câu lệnh dotnet test trên CI."),

        (63, "Bằng chứng kỹ thuật CI đã được sửa thật", "Những bằng chứng kỹ thuật nào chứng minh nhóm đã khắc phục triệt để và minh bạch sự cố CI?",
         "Cơ bản", "Võ Ngọc Minh Đạt", "Quách Khoa Đức",
         "Nhóm có 4 bằng chứng kỹ thuật không thể chối cãi: (1) GitHub Actions Run ID #40231783994 trên nhánh main có trạng thái 'Success' màu xanh hoàn toàn; (2) Commit SHA c7af080 thể hiện rõ các thay đổi trong DbInitializer.cs và CustomWebApplicationFactory.cs; (3) Log kiểm thử ghi nhận: 'Total tests: 15. Passed: 15. Failed: 0. Duration: 2.8s'; (4) Ảnh chụp màn hình log lỗi cũ Run #12 và log thành công mới Run #40231783994 được đưa trực tiếp vào Slide 15 của bài thuyết trình.",
         "Tất cả đều công khai trên repository GitHub của nhóm tại lovemvaf/visionary-api.",
         "URL: https://github.com/lovemvaf/visionary-api/actions/runs/40231783994.",
         "Kiểm chứng: Giảng viên có thể mở link GitHub Actions kiểm tra trực tiếp ngày giờ và commit log.",
         "Sai lầm: Chỉ chụp ảnh màn hình terminal trên máy cá nhân mà không có link CI từ xa."),

        (64, "Vai trò của AI trong quá trình sửa lỗi", "Công cụ AI đã hỗ trợ nhóm những gì trong quá trình phân tích và sửa lỗi CI này?",
         "Trung bình", "Quách Khoa Đức", "Võ Ngọc Minh Đạt",
         "Nhóm khai báo minh bạch: AI hỗ trợ phân tích log stack trace từ GitHub Actions, gợi ý nguyên nhân tiềm ẩn về xung đột Semaphore trên SQLite và đề xuất cấu trúc mẫu CustomWebApplicationFactory. Tuy nhiên, toàn bộ việc tái hiện lỗi cục bộ, quyết định thiết kế kiến trúc khóa luồng SemaphoreSlim(1,1), tích hợp vào DbInitializer.cs, chạy kiểm thử hồi quy và đẩy commit lên GitHub đều do các thành viên nhóm trực tiếp thực hiện và chịu trách nhiệm 100%.",
         "Nhóm không sao chép mù quáng code của AI mà luôn kiểm chứng qua câu lệnh dotnet test trước khi commit.",
         "Tài liệu: Báo cáo sự cố docs/TH71108_REAL_CI_INCIDENT_REPORT.md và khai báo AI tại Slide 1.",
         "Kiểm chứng: Mọi dòng code sửa đều được giải thích cặn kẽ về mặt kỹ thuật.",
         "Sai lầm: Phủ nhận hoàn toàn việc dùng AI hoặc đổ lỗi mọi thứ do AI làm."),

        (65, "Bảo vệ bài viết Draft trong hệ thống", "Tại sao bài viết ở trạng thái Nháp (Draft) không được phép trả về cho người dùng bình thường?",
         "Trung bình", "Hồ Đoàn Nguyên Khang", "Quách Khoa Đức",
         "Bài viết nháp là nội dung chưa hoàn thiện, có thể chứa thông tin nội bộ hoặc chưa được ban chủ nhiệm phê duyệt. Nếu để lộ bài nháp ra ngoài, uy tín của câu lạc bộ có thể bị ảnh hưởng. Về mặt bảo mật thông tin, đây là lỗi rò rỉ dữ liệu (Information Disclosure).",
         "Do đó, trong PostsController, mọi truy vấn từ khách hoặc sinh viên đều bị ép cứng điều kiện status == PostStatus.Published ngay tại câu lệnh SQL.",
         "File: backend/src/Visionary.Api/Controllers/PostsController.cs dòng 52 và dòng 120.",
         "Kiểm chứng: Test UnpublishPost_Draft_And_PendingReview_NeverLeakPublicly -> Pass 100%.",
         "Sai lầm: Cho rằng bài nháp chỉ cần ẩn nút trên giao diện là đủ an toàn."),

        (66, "Tính ổn định của thuật toán phân trang", "Vì sao thuật toán phân trang dữ liệu trong Web API bắt buộc phải có thứ tự sắp xếp ổn định (Stable Ordering)?",
         "Khó", "Hồ Đoàn Nguyên Khang", "Võ Ngọc Minh Đạt",
         "Nếu không có mệnh đề OrderBy ổn định (ví dụ sắp xếp theo Id hoặc CreatedAt), cơ sở dữ liệu quan hệ không đảm bảo thứ tự trả về giữa các lần truy vấn. Khi người dùng bấm sang trang 2, cơ sở dữ liệu có thể trả lại một số bản ghi đã xuất hiện ở trang 1 hoặc bỏ sót các bản ghi chưa duyệt. Đây gọi là lỗi 'Pagination Inconsistency'.",
         "Trong EventService và PostService, nhóm luôn sắp xếp cố định theo CreatedAt giảm dần kết hợp Id trước khi gọi .Skip().Take().",
         "File: backend/src/Visionary.Infrastructure/Services/EventService.cs và PostService.cs.",
         "Kiểm chứng: Duyệt từ trang 1 đến trang 3, các bản ghi hiển thị nối tiếp nhau chuẩn xác 100%, không bị lặp hay nhảy bản ghi.",
         "Sai lầm: Gọi .Skip().Take() trực tiếp trên DbSet mà không có .OrderBy().")
    ]

    for q_data in ci_questions:
        add_question_block(*q_data)
'''

    # Insert ci_section_code right before output_path = ...
    target = 'output_path = "deliverables/VISIONARY_TH71108_FULL_QA_AND_TEST_GUIDE.docx"'
    idx = code.find(target)
    if idx != -1:
        updated_code = code[:idx] + ci_section_code + '\n    ' + code[idx:]
        with open('scripts/generate_full_qa_guide.py', 'w', encoding='utf-8') as f:
            f.write(updated_code)
        print('Injected CI chapter into scripts/generate_full_qa_guide.py successfully.')
    else:
        print('Target not found in generate_full_qa_guide.py!')

if __name__ == '__main__':
    add_ci_chapter_to_qa_guide()
