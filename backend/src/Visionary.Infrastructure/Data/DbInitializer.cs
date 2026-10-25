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
        public static async Task SeedAsync(AppDbContext context, IPasswordHasher passwordHasher)
        {
            try
            {
                var databaseCreator = Microsoft.EntityFrameworkCore.Infrastructure.AccessorExtensions.GetService<Microsoft.EntityFrameworkCore.Storage.IDatabaseCreator>(context.Database) as Microsoft.EntityFrameworkCore.Storage.RelationalDatabaseCreator;
                if (databaseCreator != null)
                {
                    await databaseCreator.CreateTablesAsync();
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
            await context.SaveChangesAsync();

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
            if (!await context.PostCategories.AnyAsync())
            {
                var catNews = new PostCategory { Name = "Tin Hội nhập Quốc tế", Slug = "tin-hoi-nhap", Description = "Các chương trình giao lưu, văn hóa và tin tức thế giới." };
                var catTech = new PostCategory { Name = "Công nghệ & AI", Slug = "cong-nghe-ai", Description = "Xu hướng công nghệ, mô hình AI mới và kiến trúc phần mềm." };
                var catEnglish = new PostCategory { Name = "Tiếng Anh Chuyên ngành", Slug = "tieng-anh-chuyen-nganh", Description = "Phương pháp học, thuật ngữ và bài giảng English for IT." };
                var catClub = new PostCategory { Name = "Hoạt động CLB", Slug = "hoat-dong-clb", Description = "Thông báo, lịch trình sinh hoạt và sự kiện của CLB Tiếng Anh DNTU." };

                context.PostCategories.AddRange(catNews, catTech, catEnglish, catClub);
                await context.SaveChangesAsync();

                context.Posts.Add(new Post
                {
                    CategoryId = catTech.Id,
                    AuthorUserId = duc.Id,
                    Title = "Chào mừng đến với Hệ sinh thái VISIONARY DNTU 2026",
                    Slug = "chao-mung-he-sinh-thai-visionary-2026",
                    Summary = "VISIONARY là nền tảng tích hợp quản lý CLB Tiếng Anh, trung tâm học tập English for IT, radar công nghệ và cổng cơ hội quốc tế.",
                    ContentMarkdown = "### VISIONARY – Nơi kết nối Sinh viên, Công nghệ và Cơ hội Quốc tế\n\nĐược phát triển bởi nhóm **VISIONARY API** (Quách Khoa Đức, Võ Ngọc Minh Đạt, Hồ Đoàng Nguyên Khang, Đào Trí Khang), nền tảng hướng đến mục tiêu chuẩn hóa nghiệp vụ và tạo đột phá trong năng lực hội nhập cho sinh viên DNTU.",
                    ContentHtml = "<h3>VISIONARY – Nơi kết nối Sinh viên, Công nghệ và Cơ hội Quốc tế</h3><p>Được phát triển bởi nhóm <strong>VISIONARY API</strong>, nền tảng hướng đến mục tiêu chuẩn hóa nghiệp vụ và tạo đột phá trong năng lực hội nhập cho sinh viên DNTU.</p>",
                    Status = PostStatus.Published,
                    PublishedAt = DateTime.UtcNow
                });
                await context.SaveChangesAsync();
            }

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
    }
}
