using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using Visionary.Core.Entities;
using Visionary.Core.Enums;
using Visionary.Core.Interfaces;

namespace Visionary.Infrastructure.Data
{
    public static class DbInitializer
    {
        private static readonly System.Threading.SemaphoreSlim _seedLock = new(1, 1);

        public static async Task SeedAsync(AppDbContext context, IPasswordHasher passwordHasher)
        {
            await _seedLock.WaitAsync();
            try
            {
                try
                {
                    var databaseCreator = Microsoft.EntityFrameworkCore.Infrastructure.AccessorExtensions.GetService<Microsoft.EntityFrameworkCore.Storage.IDatabaseCreator>(context.Database) as Microsoft.EntityFrameworkCore.Storage.RelationalDatabaseCreator;
                    if (databaseCreator != null)
                    {
                        if (!await databaseCreator.HasTablesAsync())
                        {
                            await databaseCreator.CreateTablesAsync();
                        }
                    }
                    else
                    {
                        await context.Database.EnsureCreatedAsync();
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"[DB INIT] Notice on table creation: {ex.Message}");
                }

                // 1. Seed Roles
                var roles = new List<Role>
                {
                    new() { Name = AppRoles.Admin, Description = "Quản trị viên toàn quyền hệ thống" },
                    new() { Name = AppRoles.Supervisor, Description = "Giảng viên phụ trách và cố vấn CLB" },
                    new() { Name = AppRoles.Committee, Description = "Ban Chủ Nhiệm CLB Tiếng Anh DNTU" },
                    new() { Name = AppRoles.Collaborator, Description = "Cộng tác viên biên tập nội dung & sự kiện" },
                    new() { Name = AppRoles.ClubMember, Description = "Thành viên chính thức CLB Tiếng Anh" },
                    new() { Name = AppRoles.Student, Description = "Sinh viên DNTU đã đăng ký tài khoản" },
                    new() { Name = AppRoles.Guest, Description = "Khách vãng lai" }
                };

                foreach (var r in roles)
                {
                    if (!await context.Roles.AnyAsync(x => x.Name == r.Name))
                    {
                        context.Roles.Add(r);
                    }
                }

                try
                {
                    await context.SaveChangesAsync();
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"[DB INIT] Notice on saving roles: {ex.Message}");
                }

            var adminRole = await context.Roles.FirstAsync(r => r.Name == AppRoles.Admin);
            var committeeRole = await context.Roles.FirstAsync(r => r.Name == AppRoles.Committee);
            var memberRole = await context.Roles.FirstAsync(r => r.Name == AppRoles.ClubMember);
            var collabRole = await context.Roles.FirstAsync(r => r.Name == AppRoles.Collaborator);
            var studentRole = await context.Roles.FirstAsync(r => r.Name == AppRoles.Student);

            // 2. Seed Core Team Users (Development team credentials - distinct from club officers)
            var rawSeedPassword = Environment.GetEnvironmentVariable("ADMIN_SEED_PASSWORD") ?? "Visionary@2026";
            var defaultPassword = passwordHasher.HashPassword(rawSeedPassword);

            // Quách Khoa Đức - Principal Software Architect & Full-Stack Lead
            var duc = await context.Users.FirstOrDefaultAsync(u => u.Email == "quachkhoaduc@visionary.dntu.edu.vn");
            if (duc == null)
            {
                duc = new User
                {
                    Email = "quachkhoaduc@visionary.dntu.edu.vn",
                    FullName = "Quách Khoa Đức",
                    PasswordHash = defaultPassword,
                    StudentId = "1923040025",
                    Department = "Công nghệ Thông tin",
                    Bio = "Principal Software Architect & Lead. Nhóm phát triển VISIONARY API.",
                    EmailConfirmed = true,
                    IsActive = true
                };
                context.Users.Add(duc);
                await context.SaveChangesAsync();

                context.UserRoles.Add(new UserRole { UserId = duc.Id, RoleId = adminRole.Id });
                context.UserRoles.Add(new UserRole { UserId = duc.Id, RoleId = committeeRole.Id });
                context.UserRoles.Add(new UserRole { UserId = duc.Id, RoleId = studentRole.Id });
            }

            // Võ Ngọc Minh Đạt - Desktop Software Engineer
            var dat = await context.Users.FirstOrDefaultAsync(u => u.Email == "vongocminhdat@visionary.dntu.edu.vn");
            if (dat == null)
            {
                dat = new User
                {
                    Email = "vongocminhdat@visionary.dntu.edu.vn",
                    FullName = "Võ Ngọc Minh Đạt",
                    PasswordHash = defaultPassword,
                    Department = "Công nghệ Thông tin",
                    Bio = "Desktop Software Engineer (WinForms) & Club Operations. Nhóm phát triển VISIONARY API.",
                    EmailConfirmed = true,
                    IsActive = true
                };
                context.Users.Add(dat);
                await context.SaveChangesAsync();

                context.UserRoles.Add(new UserRole { UserId = dat.Id, RoleId = committeeRole.Id });
                context.UserRoles.Add(new UserRole { UserId = dat.Id, RoleId = memberRole.Id });
            }

            // Hồ Đoàng Nguyên Khang - Data Pipeline Specialist
            var khangH = await context.Users.FirstOrDefaultAsync(u => u.Email == "hodoangnguyenkhang@visionary.dntu.edu.vn");
            if (khangH == null)
            {
                khangH = new User
                {
                    Email = "hodoangnguyenkhang@visionary.dntu.edu.vn",
                    FullName = "Hồ Đoàng Nguyên Khang",
                    PasswordHash = defaultPassword,
                    Department = "Công nghệ Thông tin",
                    Bio = "Data Pipeline & Opportunities Specialist. Nhóm phát triển VISIONARY API.",
                    EmailConfirmed = true,
                    IsActive = true
                };
                context.Users.Add(khangH);
                await context.SaveChangesAsync();

                context.UserRoles.Add(new UserRole { UserId = khangH.Id, RoleId = committeeRole.Id });
                context.UserRoles.Add(new UserRole { UserId = khangH.Id, RoleId = collabRole.Id });
            }

            // Đào Trí Khang - Mobile Software Engineer & QA Lead
            var khangD = await context.Users.FirstOrDefaultAsync(u => u.Email == "daotrikhang@visionary.dntu.edu.vn");
            if (khangD == null)
            {
                khangD = new User
                {
                    Email = "daotrikhang@visionary.dntu.edu.vn",
                    FullName = "Đào Trí Khang",
                    PasswordHash = defaultPassword,
                    Department = "Công nghệ Thông tin",
                    Bio = "Mobile Software Engineer (Android Native) & QA Lead. Nhóm phát triển VISIONARY API.",
                    EmailConfirmed = true,
                    IsActive = true
                };
                context.Users.Add(khangD);
                await context.SaveChangesAsync();

                context.UserRoles.Add(new UserRole { UserId = khangD.Id, RoleId = committeeRole.Id });
                context.UserRoles.Add(new UserRole { UserId = khangD.Id, RoleId = memberRole.Id });
            }

            await context.SaveChangesAsync();

            // 3. Seed Club Departments
            if (!await context.ClubDepartments.AnyAsync())
            {
                var deptAcademic = new ClubDepartment { Name = "Ban Chuyên môn & Học thuật", Description = "Phụ trách tổ chức lớp học English for IT, rèn luyện kỹ năng phỏng vấn và học thuật quốc tế." };
                var deptMedia = new ClubDepartment { Name = "Ban Truyền thông & Sự kiện", Description = "Phụ trách cổng tin tức, fanpage, hình ảnh sự kiện và tổ chức các buổi hội thảo sinh viên." };
                var deptExternal = new ClubDepartment { Name = "Ban Đối ngoại & Kết nối Doanh nghiệp", Description = "Kết nối các cơ hội học bổng, cuộc thi hackathon và cơ hội thực tập quốc tế." };

                context.ClubDepartments.AddRange(deptAcademic, deptMedia, deptExternal);
                await context.SaveChangesAsync();

                // Assign Duc & Dat to departments with appropriate technical club roles
                if (duc.MemberProfile == null)
                {
                    context.MemberProfiles.Add(new MemberProfile
                    {
                        UserId = duc.Id,
                        DepartmentId = deptAcademic.Id,
                        ClubRole = "Trưởng ban Chuyên môn & Kỹ thuật",
                        EnglishLevel = "IELTS 7.5 / Professional IT",
                        Status = "Active"
                    });
                }
                if (dat.MemberProfile == null)
                {
                    context.MemberProfiles.Add(new MemberProfile
                    {
                        UserId = dat.Id,
                        DepartmentId = deptMedia.Id,
                        ClubRole = "Phụ trách Kỹ thuật & Hoạt động",
                        EnglishLevel = "TOEIC 800",
                        Status = "Active"
                    });
                }
                await context.SaveChangesAsync();
            }

            // 4. Seed Committee Term (Technical & Operational assignments)
            if (!await context.CommitteeTerms.AnyAsync())
            {
                var currentTerm = new CommitteeTerm
                {
                    Name = "Nhiệm kỳ 2025 - 2026",
                    StartDate = new DateTime(2025, 9, 1, 0, 0, 0, DateTimeKind.Utc),
                    IsCurrent = true
                };
                context.CommitteeTerms.Add(currentTerm);
                await context.SaveChangesAsync();

                context.CommitteeAssignments.AddRange(
                    new CommitteeAssignment { TermId = currentTerm.Id, UserId = duc.Id, Position = "Phụ trách Công nghệ & Nền tảng" },
                    new CommitteeAssignment { TermId = currentTerm.Id, UserId = dat.Id, Position = "Phụ trách Kỹ thuật & Sự kiện" },
                    new CommitteeAssignment { TermId = currentTerm.Id, UserId = khangH.Id, Position = "Phụ trách Dữ liệu Cơ hội & Học bổng" },
                    new CommitteeAssignment { TermId = currentTerm.Id, UserId = khangD.Id, Position = "Phụ trách Nền tảng Di động & Đảm bảo Chất lượng" }
                );
                await context.SaveChangesAsync();
            }

            // 5. Seed Post Categories & Posts
            var catNews = await context.PostCategories.FirstOrDefaultAsync(c => c.Slug == "tin-hoi-nhap");
            if (catNews == null)
            {
                catNews = new PostCategory { Name = "Tin Hội nhập Quốc tế", Slug = "tin-hoi-nhap", Description = "Các chương trình giao lưu, văn hóa và tin tức thế giới." };
                context.PostCategories.Add(catNews);
            }

            var catTech = await context.PostCategories.FirstOrDefaultAsync(c => c.Slug == "cong-nghe-ai");
            if (catTech == null)
            {
                catTech = new PostCategory { Name = "Công nghệ & AI", Slug = "cong-nghe-ai", Description = "Xu hướng công nghệ, mô hình AI mới và kiến trúc phần mềm." };
                context.PostCategories.Add(catTech);
            }

            var catEnglish = await context.PostCategories.FirstOrDefaultAsync(c => c.Slug == "tieng-anh-chuyen-nganh");
            if (catEnglish == null)
            {
                catEnglish = new PostCategory { Name = "Tiếng Anh Chuyên ngành", Slug = "tieng-anh-chuyen-nganh", Description = "Phương pháp học, thuật ngữ và bài giảng English for IT." };
                context.PostCategories.Add(catEnglish);
            }

            var catClub = await context.PostCategories.FirstOrDefaultAsync(c => c.Slug == "hoat-dong-clb");
            if (catClub == null)
            {
                catClub = new PostCategory { Name = "Hoạt động CLB", Slug = "hoat-dong-clb", Description = "Thông báo, lịch trình sinh hoạt và sự kiện của CLB Tiếng Anh DNTU." };
                context.PostCategories.Add(catClub);
            }
            await context.SaveChangesAsync();

            // Seed 23 Published posts (8 Tech, 6 English, 5 News, 4 Club) + 2 Unpublished (1 Draft, 1 PendingReview)
            var baseTime = new DateTime(2026, 10, 25, 12, 0, 0, DateTimeKind.Utc);
            var seedPosts = new List<Post>
            {
                // --- NHÓM 1: CÔNG NGHỆ & AI (8 BÀI PUBLISHED) ---
                new Post
                {
                    CategoryId = catTech.Id,
                    AuthorUserId = duc.Id,
                    Title = "Chào mừng đến với Hệ sinh thái VISIONARY DNTU 2026",
                    Slug = "chao-mung-he-sinh-thai-visionary-2026",
                    Summary = "VISIONARY là nền tảng tích hợp quản lý CLB Tiếng Anh, trung tâm học tập English for IT, radar công nghệ và cổng cơ hội quốc tế.",
                    ContentMarkdown = "### VISIONARY – Nơi kết nối Sinh viên, Công nghệ và Cơ hội Quốc tế\n\nĐược phát triển bởi nhóm **VISIONARY API** (Quách Khoa Đức, Võ Ngọc Minh Đạt, Hồ Đoàng Nguyên Khang, Đào Trí Khang), nền tảng hướng đến mục tiêu chuẩn hóa nghiệp vụ và tạo đột phá trong năng lực hội nhập cho sinh viên DNTU.",
                    ContentHtml = "<h3>VISIONARY – Nơi kết nối Sinh viên, Công nghệ và Cơ hội Quốc tế</h3><p>Được phát triển bởi nhóm <strong>VISIONARY API</strong>, nền tảng hướng đến mục tiêu chuẩn hóa nghiệp vụ và tạo đột phá trong năng lực hội nhập cho sinh viên DNTU.</p>",
                    Status = PostStatus.Published,
                    PublishedAt = baseTime.AddHours(-1)
                },
                new Post
                {
                    CategoryId = catTech.Id,
                    AuthorUserId = duc.Id,
                    Title = "Thực hành Kiến trúc Clean Architecture với ASP.NET Core Web API và Next.js",
                    Slug = "kien-truc-clean-architecture-aspnet-core",
                    Summary = "Hướng dẫn phân tách tầng Core, Infrastructure và Api để xây dựng backend phân tán hiệu năng cao phục vụ đa nền tảng Web, Desktop và Mobile.",
                    ContentMarkdown = "Clean Architecture giúp hệ thống độc lập với cơ sở dữ liệu, framework bên ngoài và dễ dàng kiểm thử tự động với xUnit.",
                    ContentHtml = "<p>Clean Architecture giúp hệ thống độc lập với cơ sở dữ liệu, framework bên ngoài và dễ dàng kiểm thử tự động với xUnit.</p>",
                    Status = PostStatus.Published,
                    PublishedAt = baseTime.AddHours(-2)
                },
                new Post
                {
                    CategoryId = catTech.Id,
                    AuthorUserId = duc.Id,
                    Title = "Ứng dụng RAG (Retrieval-Augmented Generation) trong tra cứu tài liệu học thuật",
                    Slug = "ung-dung-rag-trong-tra-cuu-tai-lieu-hoc-thuat",
                    Summary = "Phương pháp kết hợp cơ sở dữ liệu vector và mô hình ngôn ngữ lớn để trả lời câu hỏi chính xác dựa trên giáo trình và tài liệu nghiên cứu.",
                    ContentMarkdown = "Kỹ thuật RAG giải quyết triệt để hiện tượng ảo tưởng (hallucination) của LLMs trong môi trường giáo dục đại học.",
                    ContentHtml = "<p>Kỹ thuật RAG giải quyết triệt để hiện tượng ảo tưởng của LLMs trong môi trường giáo dục đại học.</p>",
                    Status = PostStatus.Published,
                    PublishedAt = baseTime.AddHours(-3)
                },
                new Post
                {
                    CategoryId = catTech.Id,
                    AuthorUserId = dat.Id,
                    Title = "Phân tích hiệu năng Entity Framework Core và Dapper trong hệ thống lớn",
                    Slug = "so-sanh-giai-phap-orm-ef-core-va-dapper",
                    Summary = "So sánh chi tiết tốc độ truy vấn, mức chiếm dụng bộ nhớ và tính dễ bảo trì giữa ORM toàn diện EF Core và micro-ORM Dapper.",
                    ContentMarkdown = "Việc sử dụng AsNoTracking() và Compiled Queries trên EF Core 8 mang lại tốc độ tiệm cận với Dapper thuần.",
                    ContentHtml = "<p>Việc sử dụng AsNoTracking() và Compiled Queries trên EF Core 8 mang lại tốc độ tiệm cận với Dapper thuần.</p>",
                    Status = PostStatus.Published,
                    PublishedAt = baseTime.AddHours(-4)
                },
                new Post
                {
                    CategoryId = catTech.Id,
                    AuthorUserId = khangH.Id,
                    Title = "Lộ trình làm chủ Cloud-Native và Container hóa với Docker và Kubernetes",
                    Slug = "lo-trinh-hoc-lap-trinh-cloud-native-2026",
                    Summary = "Các bước thực tiễn từ đóng gói ứng dụng .NET vào Docker image siêu nhẹ đến cấu hình auto-deploy trên môi trường đám mây.",
                    ContentMarkdown = "Container hóa đảm bảo tính nhất quán 100% giữa môi trường phát triển local và máy chủ production trên Render/Cloud Run.",
                    ContentHtml = "<p>Container hóa đảm bảo tính nhất quán 100% giữa môi trường phát triển local và máy chủ production trên Render/Cloud Run.</p>",
                    Status = PostStatus.Published,
                    PublishedAt = baseTime.AddHours(-5)
                },
                new Post
                {
                    CategoryId = catTech.Id,
                    AuthorUserId = khangD.Id,
                    Title = "Triển khai mô hình AI trên thiết bị di động với TensorFlow Lite và ONNX",
                    Slug = "xay-dung-mo-hinh-ai-edge-tren-thiet-bi-di-dong",
                    Summary = "Tối ưu hóa mô hình học sâu để chạy trực tiếp (Edge AI) trên ứng dụng Android Native Java mà không phụ thuộc vào kết nối mạng liên tục.",
                    ContentMarkdown = "Kỹ thuật lượng tử hóa (Quantization) giúp giảm dung lượng model xuống 4 lần mà chỉ giảm dưới 1% độ chính xác.",
                    ContentHtml = "<p>Kỹ thuật lượng tử hóa giúp giảm dung lượng model xuống 4 lần mà chỉ giảm dưới 1% độ chính xác.</p>",
                    Status = PostStatus.Published,
                    PublishedAt = baseTime.AddHours(-6)
                },
                new Post
                {
                    CategoryId = catTech.Id,
                    AuthorUserId = khangD.Id,
                    Title = "Tự động hóa kiểm thử End-to-End với Playwright và CI/CD Pipeline",
                    Slug = "tu-dong-hoa-kiem-thu-voi-playwright-va-github-actions",
                    Summary = "Xây dựng kịch bản kiểm thử giao diện người dùng tự động đa trình duyệt, chụp ảnh bằng chứng và báo cáo lỗi tức thì trên GitHub Actions.",
                    ContentMarkdown = "Playwright hỗ trợ kiểm thử song song, mô phỏng network throttling và tự động retry khi gặp transient errors.",
                    ContentHtml = "<p>Playwright hỗ trợ kiểm thử song song, mô phỏng network throttling và tự động retry khi gặp transient errors.</p>",
                    Status = PostStatus.Published,
                    PublishedAt = baseTime.AddHours(-7)
                },
                new Post
                {
                    CategoryId = catTech.Id,
                    AuthorUserId = dat.Id,
                    Title = "Kỹ thuật tối ưu hóa chỉ mục và Connection Pooling trên PostgreSQL Supabase",
                    Slug = "toi-uu-truy-van-postgresql-voi-supabase-pooler",
                    Summary = "Kinh nghiệm thực chiến khi cấu hình Supabase IPv4 Pooler cổng 5432 và đánh chỉ mục B-tree/GIN cho các trường tìm kiếm thường xuyên.",
                    ContentMarkdown = "Sử dụng PgBouncer Session Mode giúp duy trì kết nối ổn định từ các máy chủ container mà không làm cạn kiệt tài nguyên database.",
                    ContentHtml = "<p>Sử dụng PgBouncer Session Mode giúp duy trì kết nối ổn định từ các máy chủ container mà không làm cạn kiệt tài nguyên database.</p>",
                    Status = PostStatus.Published,
                    PublishedAt = baseTime.AddHours(-8)
                },

                // --- NHÓM 2: TIẾNG ANH CHUYÊN NGÀNH (6 BÀI PUBLISHED) ---
                new Post
                {
                    CategoryId = catEnglish.Id,
                    AuthorUserId = duc.Id,
                    Title = "50 thuật ngữ tiếng Anh cốt lõi khi thiết kế và làm việc với RESTful Web API",
                    Slug = "thuat-ngu-tieng-anh-chuyen-sau-restful-api",
                    Summary = "Tổng hợp các khái niệm Idempotency, Statelessness, Payload, Query Parameter, Rate Limiting và Bearer Token theo tiêu chuẩn quốc tế.",
                    ContentMarkdown = "Nắm vững thuật ngữ chuẩn giúp kỹ sư tự tin đọc RFCs và thảo luận kỹ thuật với các nhóm kỹ sư nước ngoài.",
                    ContentHtml = "<p>Nắm vững thuật ngữ chuẩn giúp kỹ sư tự tin đọc RFCs và thảo luận kỹ thuật với các nhóm kỹ sư nước ngoài.</p>",
                    Status = PostStatus.Published,
                    PublishedAt = baseTime.AddHours(-9)
                },
                new Post
                {
                    CategoryId = catEnglish.Id,
                    AuthorUserId = dat.Id,
                    Title = "Cẩm nang trả lời phỏng vấn kỹ thuật bằng tiếng Anh cho vị trí Software Engineer",
                    Slug = "ky-nang-tra-loi-phong-van-ky-thuat-bang-tieng-anh",
                    Summary = "Cấu trúc trả lời theo phương pháp STAR (Situation, Task, Action, Result) và bộ câu hỏi mẫu khi giải thích thuật toán và kiến trúc hệ thống.",
                    ContentMarkdown = "Tập trung giải thích mạch lạc tư duy giải quyết vấn đề (problem-solving mindset) thay vì chỉ đọc thuộc lòng code.",
                    ContentHtml = "<p>Tập trung giải thích mạch lạc tư duy giải quyết vấn đề thay vì chỉ đọc thuộc lòng code.</p>",
                    Status = PostStatus.Published,
                    PublishedAt = baseTime.AddHours(-10)
                },
                new Post
                {
                    CategoryId = catEnglish.Id,
                    AuthorUserId = khangH.Id,
                    Title = "Hướng dẫn viết Git Commit Message và Pull Request chuẩn Convention quốc tế",
                    Slug = "cach-viet-git-commit-message-chuan-quoc-te",
                    Summary = "Quy tắc Conventional Commits (feat, fix, refactor, chore) và cấu trúc PR description chuyên nghiệp giúp tăng tốc độ review mã nguồn.",
                    ContentMarkdown = "Mỗi commit message là một thông điệp kỹ thuật rõ ràng giúp duy trì lịch sử dự án minh bạch cho cả nhóm.",
                    ContentHtml = "<p>Mỗi commit message là một thông điệp kỹ thuật rõ ràng giúp duy trì lịch sử dự án minh bạch cho cả nhóm.</p>",
                    Status = PostStatus.Published,
                    PublishedAt = baseTime.AddHours(-11)
                },
                new Post
                {
                    CategoryId = catEnglish.Id,
                    AuthorUserId = duc.Id,
                    Title = "Phương pháp đọc hiểu tài liệu kỹ thuật quốc tế và chuẩn RFC không cần từ điển",
                    Slug = "doc-hieu-tai-lieu-ky-thuat-chuyen-sau-rfcs",
                    Summary = "Chiến lược phân tích cấu trúc tài liệu MSDN, AWS Architecture Center và IETF RFC để nắm bắt thông số kỹ thuật nhanh chóng.",
                    ContentMarkdown = "Xây dựng vốn từ theo sơ đồ ngữ nghĩa (semantic network) giúp ghi nhớ thuật ngữ tự nhiên theo ngữ cảnh bài toán.",
                    ContentHtml = "<p>Xây dựng vốn từ theo sơ đồ ngữ nghĩa giúp ghi nhớ thuật ngữ tự nhiên theo ngữ cảnh bài toán.</p>",
                    Status = PostStatus.Published,
                    PublishedAt = baseTime.AddHours(-12)
                },
                new Post
                {
                    CategoryId = catEnglish.Id,
                    AuthorUserId = khangD.Id,
                    Title = "Tiếng Anh giao tiếp hàng ngày trong quy trình Agile Scrum tại các công ty đa quốc gia",
                    Slug = "tieng-anh-giao-tiep-trong-mo-hinh-agile-scrum",
                    Summary = "Các mẫu câu chuẩn trong buổi Daily Stand-up, Sprint Planning, Retrospective và cách báo cáo blocker một cách tự tin và chuyên nghiệp.",
                    ContentMarkdown = "Sử dụng ngôn ngữ súc tích, hướng đến giải pháp giúp giảm thiểu hiểu lầm trong các nhóm làm việc từ xa đa quốc gia.",
                    ContentHtml = "<p>Sử dụng ngôn ngữ súc tích, hướng đến giải pháp giúp giảm thiểu hiểu lầm trong các nhóm làm việc từ xa đa quốc gia.</p>",
                    Status = PostStatus.Published,
                    PublishedAt = baseTime.AddHours(-13)
                },
                new Post
                {
                    CategoryId = catEnglish.Id,
                    AuthorUserId = khangH.Id,
                    Title = "Nắm vững thuật ngữ AI, Machine Learning và Prompt Engineering tiếng Anh",
                    Slug = "thuat-ngu-ai-prompt-engineering-chuyen-nghiep",
                    Summary = "Giải mã các thuật ngữ Zero-shot, Few-shot, Chain-of-Thought, Temperature, Top-p và Fine-tuning trong kỷ nguyên Trí tuệ nhân tạo tạo sinh.",
                    ContentMarkdown = "Hiểu rõ các tham số bằng tiếng Anh là nền tảng để tinh chỉnh và kiểm soát hành vi của các mô hình ngôn ngữ lớn.",
                    ContentHtml = "<p>Hiểu rõ các tham số bằng tiếng Anh là nền tảng để tinh chỉnh và kiểm soát hành vi của các mô hình ngôn ngữ lớn.</p>",
                    Status = PostStatus.Published,
                    PublishedAt = baseTime.AddHours(-14)
                },

                // --- NHÓM 3: TIN HỘI NHẬP QUỐC TẾ (5 BÀI PUBLISHED) ---
                new Post
                {
                    CategoryId = catNews.Id,
                    AuthorUserId = khangH.Id,
                    Title = "Tổng hợp chương trình học bổng ASEAN và cơ hội trao đổi sinh viên quốc tế 2026",
                    Slug = "co-hoi-hoc-bong-asean-va-chuong-trinh-trao-doi-2026",
                    Summary = "Danh sách các chương trình học bổng toàn phần, giao lưu văn hóa và thực tập ngắn hạn tại các trường đại học đối tác trong khu vực.",
                    ContentMarkdown = "Sinh viên DNTU sở hữu nền tảng tiếng Anh tốt và các dự án thực tế luôn có lợi thế cạnh tranh vượt trội.",
                    ContentHtml = "<p>Sinh viên DNTU sở hữu nền tảng tiếng Anh tốt và các dự án thực tế luôn có lợi thế cạnh tranh vượt trội.</p>",
                    Status = PostStatus.Published,
                    PublishedAt = baseTime.AddHours(-15)
                },
                new Post
                {
                    CategoryId = catNews.Id,
                    AuthorUserId = duc.Id,
                    Title = "Kinh nghiệm thực chiến tại các cuộc thi Google Cloud AI Hackathon và Devpost",
                    Slug = "kinh-nghiem-tham-gia-hackathon-quoc-te-google-cloud",
                    Summary = "Chiến lược lập đội thi, phân chia vai trò Full-stack / AI Engineer và cách làm video demo thuyết phục ban giám khảo quốc tế.",
                    ContentMarkdown = "Ý tưởng giải quyết bài toán thực tiễn gắn với mục tiêu phát triển bền vững luôn nhận được đánh giá cao tại các kỳ Hackathon toàn cầu.",
                    ContentHtml = "<p>Ý tưởng giải quyết bài toán thực tiễn gắn với mục tiêu phát triển bền vững luôn nhận được đánh giá cao tại các kỳ Hackathon toàn cầu.</p>",
                    Status = PostStatus.Published,
                    PublishedAt = baseTime.AddHours(-16)
                },
                new Post
                {
                    CategoryId = catNews.Id,
                    AuthorUserId = dat.Id,
                    Title = "Đại học Công nghệ Đồng Nai mở rộng hợp tác đào tạo và hội nhập công nghệ số",
                    Slug = "dntu-mo-rong-hop-tac-dao-tao-chuan-quoc-te",
                    Summary = "DNTU tiếp tục ký kết các biên bản ghi nhớ hợp tác chiến lược với các tập đoàn công nghệ hàng đầu nhằm nâng cao chất lượng chuẩn đầu ra.",
                    ContentMarkdown = "Chương trình đào tạo gắn liền với thực tiễn doanh nghiệp giúp sinh viên sẵn sàng tiếp cận môi trường làm việc toàn cầu ngay khi tốt nghiệp.",
                    ContentHtml = "<p>Chương trình đào tạo gắn liền với thực tiễn doanh nghiệp giúp sinh viên sẵn sàng tiếp cận môi trường làm việc toàn cầu ngay khi tốt nghiệp.</p>",
                    Status = PostStatus.Published,
                    PublishedAt = baseTime.AddHours(-17)
                },
                new Post
                {
                    CategoryId = catNews.Id,
                    AuthorUserId = khangH.Id,
                    Title = "Hướng dẫn chuẩn bị hồ sơ ứng tuyển chương trình thực tập công nghệ tại Singapore",
                    Slug = "chuan-bi-ho-so-ung-tuyen-thuc-tap-tai-singapore",
                    Summary = "Các lưu ý khi viết CV tiếng Anh chuẩn ATS, viết thư nguyện vọng (Cover Letter) và xây dựng Portfolio dự án GitHub nổi bật.",
                    ContentMarkdown = "Một portfolio minh bạch với mã nguồn sạch và tài liệu hướng dẫn chi tiết là bằng chứng rõ ràng nhất về năng lực kỹ thuật.",
                    ContentHtml = "<p>Một portfolio minh bạch với mã nguồn sạch và tài liệu hướng dẫn chi tiết là bằng chứng rõ ràng nhất về năng lực kỹ thuật.</p>",
                    Status = PostStatus.Published,
                    PublishedAt = baseTime.AddHours(-18)
                },
                new Post
                {
                    CategoryId = catNews.Id,
                    AuthorUserId = khangD.Id,
                    Title = "Nghệ thuật thuyết trình dự án công nghệ trước hội đồng giám khảo quốc tế",
                    Slug = "ky-nang-thuyet-trinh-du-an-cong-nghe-tai-hoi-nghi-toan-cau",
                    Summary = "Bí quyết thiết kế slide thuyết trình tối giản, diễn đạt súc tích phần Demo kỹ thuật và làm chủ thời gian hỏi đáp (Q&A) bằng tiếng Anh.",
                    ContentMarkdown = "Tập trung làm nổi bật giá trị cốt lõi và kết quả định lượng mà hệ thống đem lại cho người dùng cuối.",
                    ContentHtml = "<p>Tập trung làm nổi bật giá trị cốt lõi và kết quả định lượng mà hệ thống đem lại cho người dùng cuối.</p>",
                    Status = PostStatus.Published,
                    PublishedAt = baseTime.AddHours(-19)
                },

                // --- NHÓM 4: HOẠT ĐỘNG CLB (4 BÀI PUBLISHED) ---
                new Post
                {
                    CategoryId = catClub.Id,
                    AuthorUserId = dat.Id,
                    Title = "Kế hoạch hoạt động và lịch sinh hoạt định kỳ CLB Tiếng Anh DNTU năm học 2025 - 2026",
                    Slug = "ke-hoach-hoat-dong-clb-tieng-anh-dntu-2025-2026",
                    Summary = "Lộ trình các buổi sinh hoạt chuyên đề, rèn luyện speaking hàng tuần và chương trình chuẩn bị cho các cuộc thi học thuật quốc tế.",
                    ContentMarkdown = "Ban Chủ Nhiệm CLB thông báo thời gian biểu và hình thức sinh hoạt kết hợp trực tiếp và trực tuyến cho toàn thể hội viên.",
                    ContentHtml = "<p>Ban Chủ Nhiệm CLB thông báo thời gian biểu và hình thức sinh hoạt kết hợp trực tiếp và trực tuyến cho toàn thể hội viên.</p>",
                    Status = PostStatus.Published,
                    PublishedAt = baseTime.AddHours(-20)
                },
                new Post
                {
                    CategoryId = catClub.Id,
                    AuthorUserId = dat.Id,
                    Title = "Tổng kết chuỗi hoạt động Speaking Club: Giao lưu công nghệ và kỹ năng ngoại ngữ",
                    Slug = "tong-ket-chuong-trinh-speaking-club-thang-10",
                    Summary = "Ghi nhận sự tham gia sôi nổi của hơn 100 sinh viên tại các phiên thảo luận chuyên đề về AI và xu hướng phát triển phần mềm.",
                    ContentMarkdown = "Chương trình đã tạo môi trường cởi mở giúp các bạn sinh viên tự tin thể hiện quan điểm kỹ thuật hoàn toàn bằng tiếng Anh.",
                    ContentHtml = "<p>Chương trình đã tạo môi trường cởi mở giúp các bạn sinh viên tự tin thể hiện quan điểm kỹ thuật hoàn toàn bằng tiếng Anh.</p>",
                    Status = PostStatus.Published,
                    PublishedAt = baseTime.AddHours(-21)
                },
                new Post
                {
                    CategoryId = catClub.Id,
                    AuthorUserId = duc.Id,
                    Title = "Phát động Cuộc thi Hùng biện Tiếng Anh Công nghệ \"VISIONARY Voice 2026\"",
                    Slug = "phat-dong-cuoc-thi-hung-bien-tieng-anh-cong-nghe",
                    Summary = "Sân chơi học thuật thường niên dành cho sinh viên đam mê công nghệ trình bày các giải pháp chuyển đổi số và hội nhập quốc tế.",
                    ContentMarkdown = "Cuộc thi mang đến nhiều giải thưởng giá trị cùng cơ hội nhận học bổng và thư giới thiệu thực tập tại các đối tác doanh nghiệp.",
                    ContentHtml = "<p>Cuộc thi mang đến nhiều giải thưởng giá trị cùng cơ hội nhận học bổng và thư giới thiệu thực tập tại các đối tác doanh nghiệp.</p>",
                    Status = PostStatus.Published,
                    PublishedAt = baseTime.AddHours(-22)
                },
                new Post
                {
                    CategoryId = catClub.Id,
                    AuthorUserId = khangD.Id,
                    Title = "Thông báo tuyển Cộng tác viên Ban Chuyên môn & Kỹ thuật VISIONARY",
                    Slug = "thong-bao-tuyen-cong-tac-vien-ban-chuyen-mon-ky-thuat",
                    Summary = "Cơ hội tham gia trực tiếp vào quá trình phát triển hệ sinh thái VISIONARY, rèn luyện kỹ năng Web API, Next.js và quản trị sự kiện.",
                    ContentMarkdown = "Các bạn ứng viên quan tâm vui lòng nộp đơn trực tiếp qua cổng thành viên trên website VISIONARY trước ngày 15/11/2026.",
                    ContentHtml = "<p>Các bạn ứng viên quan tâm vui lòng nộp đơn trực tiếp qua cổng thành viên trên website VISIONARY trước ngày 15/11/2026.</p>",
                    Status = PostStatus.Published,
                    PublishedAt = baseTime.AddHours(-23)
                },

                // --- BẢN NHÁP & CHỜ DUYỆT (2 BÀI - KHÔNG ĐƯỢC XUẤT HIỆN CÔNG KHAI) ---
                new Post
                {
                    CategoryId = catTech.Id,
                    AuthorUserId = duc.Id,
                    Title = "[Bản nháp] Kế hoạch tổ chức Workshop GenAI cho tân sinh viên",
                    Slug = "draft-ke-hoach-workshop-ai-thang-11",
                    Summary = "Nội dung dự thảo chương trình thực hành Prompt Engineering và ứng dụng AI trong học tập dành cho sinh viên khóa mới.",
                    ContentMarkdown = "Tài liệu nội bộ đang soạn thảo. Chưa được xuất bản công khai.",
                    ContentHtml = "<p>Tài liệu nội bộ đang soạn thảo. Chưa được xuất bản công khai.</p>",
                    Status = PostStatus.Draft,
                    PublishedAt = null
                },
                new Post
                {
                    CategoryId = catClub.Id,
                    AuthorUserId = dat.Id,
                    Title = "[Chờ duyệt] Báo cáo dự toán kinh phí hoạt động CLB Quý 3/2026",
                    Slug = "pending-bao-cao-tai-chinh-clb-quy-3",
                    Summary = "Bảng kê chi tiết kinh phí tổ chức các buổi tọa đàm và chi phí vận hành hệ thống đám mây VISIONARY gửi Ban Cố vấn.",
                    ContentMarkdown = "Báo cáo đang chờ phê duyệt từ Giảng viên phụ trách. Nghiêm cấm công khai.",
                    ContentHtml = "<p>Báo cáo đang chờ phê duyệt từ Giảng viên phụ trách. Nghiêm cấm công khai.</p>",
                    Status = PostStatus.PendingReview,
                    PublishedAt = null
                }
            };

            foreach (var post in seedPosts)
            {
                var existing = await context.Posts.FirstOrDefaultAsync(p => p.Slug == post.Slug);
                if (existing == null)
                {
                    context.Posts.Add(post);
                }
                else
                {
                    // Ensure existing posts have verified published status and correct category
                    existing.CategoryId = post.CategoryId;
                    existing.Status = post.Status;
                    existing.PublishedAt = post.PublishedAt;
                    existing.Title = post.Title;
                    existing.Summary = post.Summary;
                    existing.ContentMarkdown = post.ContentMarkdown;
                    existing.ContentHtml = post.ContentHtml;
                }
            }
            await context.SaveChangesAsync();

            // 6. Seed Events
            if (!await context.Events.AnyAsync())
            {
                context.Events.Add(new Event
                {
                    Title = "VISIONARY Tech & English Talk 2026: Lộ trình làm chủ AI và Hội nhập Toàn cầu",
                    Slug = "visionary-tech-english-talk-2026",
                    Description = "Buổi tọa đàm chuyên sâu về cách kết hợp năng lực tiếng Anh chuyên ngành với các công nghệ AI hiện đại (LLMs, RAG, Web API) để tự tin ứng tuyển các tập đoàn công nghệ đa quốc gia.",
                    Location = "Hội trường Edison, Trường Đại học Công nghệ Đồng Nai & Online MS Teams",
                    StartTime = DateTime.UtcNow.AddDays(7),
                    EndTime = DateTime.UtcNow.AddDays(7).AddHours(3),
                    RegistrationDeadline = DateTime.UtcNow.AddDays(6),
                    MaxCapacity = 150,
                    CreatedByUserId = duc.Id,
                    Status = EventStatus.Published,
                    QrCheckInCode = "VIS-EVENT-TALK2026-QR"
                });
                await context.SaveChangesAsync();
            }

            // 7. Seed English for IT (Learning Resources)
            if (!await context.LearningResources.AnyAsync())
            {
                context.LearningResources.AddRange(
                    new LearningResource
                    {
                        Title = "Essential REST API Terminology for Backend Engineers",
                        Slug = "essential-rest-api-terminology",
                        Level = EnglishLevel.Intermediate,
                        Topic = "REST API & Backend",
                        Summary = "Bộ thuật ngữ và mẫu câu phỏng vấn chuẩn quốc tế về RESTful API, HTTP Status Codes, Idempotency và JWT Authentication.",
                        Content = "### Key Concepts:\n- **Idempotency:** An HTTP method is idempotent if the intended effect on the server of making a single request is the same as making several identical requests (e.g. GET, PUT, DELETE).\n- **Statelessness:** The server does not store any client context between requests.",
                        GlossaryJson = "[{\"term\":\"Idempotency\",\"phonetic\":\"/ˌaɪ.dɛmˈpoʊ.təns/\",\"meaning\":\"Tính bất biến khi gọi nhiều lần cùng một request\",\"example\":\"PUT and DELETE methods must be idempotent.\"}]"
                    },
                    new LearningResource
                    {
                        Title = "Demystifying AI & LLM Terminology: RAG, Embeddings, Tokens",
                        Slug = "demystifying-ai-llm-terminology",
                        Level = EnglishLevel.Advanced,
                        Topic = "AI & Machine Learning",
                        Summary = "Hiểu sâu thuật ngữ tiếng Anh trong kỷ nguyên GenAI: Retrieval-Augmented Generation (RAG), Vector Embeddings, và Context Window.",
                        Content = "### Key Concepts:\n- **Retrieval-Augmented Generation (RAG):** The process of optimizing the output of an LLM by referencing an authoritative knowledge base outside of its training data sources.\n- **Vector Embeddings:** Numerical representations of concepts converted to number sequences.",
                        GlossaryJson = "[{\"term\":\"RAG\",\"phonetic\":\"/ræɡ/\",\"meaning\":\"Tạo sinh tăng cường truy xuất\",\"example\":\"RAG prevents hallucinations by grounding responses in verified documents.\"}]"
                    }
                );
                await context.SaveChangesAsync();
            }

            // 8. Seed Tech Resources (Radar)
            if (!await context.TechResources.AnyAsync())
            {
                context.TechResources.AddRange(
                    new TechResource
                    {
                        Name = "dotnet/aspnetcore",
                        SourceType = TechSourceType.GitHubRepository,
                        ExternalId = "dotnet/aspnetcore",
                        OfficialUrl = "https://github.com/dotnet/aspnetcore",
                        Description = "ASP.NET Core is a cross-platform, high-performance, open-source framework for building modern, cloud-enabled, Internet-connected apps.",
                        PrimaryLanguage = "C#",
                        License = "MIT",
                        MetricsJson = "{\"stars\": 36800, \"forks\": 9600}",
                        LearningSuitability = "Advanced",
                        LastCheckedAt = DateTime.UtcNow
                    },
                    new TechResource
                    {
                        Name = "vercel/next.js",
                        SourceType = TechSourceType.GitHubRepository,
                        ExternalId = "vercel/next.js",
                        OfficialUrl = "https://github.com/vercel/next.js",
                        Description = "The React Framework for the Web. Used by some of the world's largest companies, Next.js enables you to create full-stack Web applications.",
                        PrimaryLanguage = "JavaScript/TypeScript",
                        License = "MIT",
                        MetricsJson = "{\"stars\": 127000, \"forks\": 27000}",
                        LearningSuitability = "Intermediate",
                        LastCheckedAt = DateTime.UtcNow
                    }
                );
                await context.SaveChangesAsync();
            }

            // 9. Seed Opportunities (Hackathons & Competitions)
            if (!await context.Opportunities.AnyAsync())
            {
                context.Opportunities.AddRange(
                    new Opportunity
                    {
                        Title = "ICPC Vietnam National Programming Contest 2026",
                        Organizer = "Hội Tin học Việt Nam (VAIP) & ICPC Asia Pacific",
                        Category = OpportunityCategory.AlgorithmIcpc,
                        Scope = "Vietnam",
                        Format = "Offline",
                        OfficialUrl = "https://icpc.ptit.edu.vn",
                        Eligibility = "Sinh viên đang theo học tại các trường đại học tại Việt Nam, tối đa 3 thành viên một đội.",
                        RegistrationDeadline = DateTime.UtcNow.AddMonths(2),
                        Status = OpportunityStatus.VerifiedOpen,
                        VerifiedAt = DateTime.UtcNow,
                        VerifiedSource = "ICPC Official Registry"
                    },
                    new Opportunity
                    {
                        Title = "Google Cloud AI Hackathon 2026",
                        Organizer = "Google Cloud & Devpost",
                        Category = OpportunityCategory.Hackathon,
                        Scope = "Global",
                        Format = "Online",
                        OfficialUrl = "https://googlecloud.devpost.com",
                        Eligibility = "Sinh viên toàn cầu từ 18 tuổi trở lên, phát triển ứng dụng ứng dụng Gemini API hoặc Vertex AI.",
                        RegistrationDeadline = DateTime.UtcNow.AddMonths(1),
                        Status = OpportunityStatus.VerifiedOpen,
                        VerifiedAt = DateTime.UtcNow,
                        VerifiedSource = "Devpost Verified Contest"
                    }
                );
                await context.SaveChangesAsync();
            }

            // 10. Seed Jobs (Career Gateway)
            if (!await context.Jobs.AnyAsync())
            {
                context.Jobs.AddRange(
                    new Job
                    {
                        Title = "Software Engineering Intern (.NET / C#)",
                        Company = "FPT Software Global Delivery",
                        JobType = JobType.Internship,
                        WorkplaceType = WorkplaceType.Hybrid,
                        Location = "Dong Nai / HCM",
                        ApplyUrl = "https://career.fpt-software.com",
                        Requirements = "Nắm vững C#, OOP, ASP.NET Core Web API cơ bản. Tiếng Anh giao tiếp hoặc đọc hiểu tài liệu chuyên ngành tốt.",
                        EnglishRequired = true,
                        IsVerified = true
                    },
                    new Job
                    {
                        Title = "Frontend Engineer Fresher (Next.js / TypeScript)",
                        Company = "VNG Corporation",
                        JobType = JobType.Fresher,
                        WorkplaceType = WorkplaceType.Onsite,
                        Location = "Ho Chi Minh City",
                        ApplyUrl = "https://careers.vng.com.vn",
                        Requirements = "Kinh nghiệm với React, Next.js App Router, Tailwind CSS. Năng động, tư duy hội nhập và khả năng làm việc nhóm tốt.",
                        EnglishRequired = true,
                        IsVerified = true
                    }
                );
                await context.SaveChangesAsync();
            }

            // 11. Seed Content Sources for Automation
            if (!await context.ContentSources.AnyAsync())
            {
                context.ContentSources.AddRange(
                    new ContentSource
                    {
                        Name = "GitHub Trending Repositories",
                        Type = "GitHubApi",
                        EndpointUrl = "https://api.github.com/search/repositories?q=stars:>1000+topic:ai&sort=stars",
                        IntervalMinutes = 360,
                        IsEnabled = true
                    },
                    new ContentSource
                    {
                        Name = "Hugging Face Trending Models",
                        Type = "HuggingFaceApi",
                        EndpointUrl = "https://huggingface.co/api/models?sort=likes7d&direction=-1&limit=20",
                        IntervalMinutes = 360,
                        IsEnabled = true
                    },
                    new ContentSource
                    {
                        Name = "Dev.to Tech Articles Feed",
                        Type = "RssFeed",
                        EndpointUrl = "https://dev.to/api/articles?tag=programming&per_page=15",
                        IntervalMinutes = 360,
                        IsEnabled = true
                    }
                );
                await context.SaveChangesAsync();
            }
            }
            finally
            {
                _seedLock.Release();
            }
        }
    }
}
