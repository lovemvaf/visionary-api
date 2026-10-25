# THIẾT KẾ CƠ SỞ DỮ LIỆU TẬP TRUNG (DATABASE SCHEMA SPECIFICATION)
**Hệ quản trị CSDL:** PostgreSQL (Tương thích Supabase) & Entity Framework Core 8  
**Kiến trúc:** Bảng dữ liệu chuẩn hóa 3NF, Khóa ngoại (Foreign Keys), Chỉ mục (Indexes), Ràng buộc (Constraints), và Audit Trail.

---

## 1. Danh sách Thực thể và Nhóm Bảng (Entities & Table Groups)

### Nhóm 1: Danh tính, Tài khoản & Tổ chức CLB (Identity & Club Structure)
1. **Users**
   - `Id` (UUID/Guid, PK)
   - `Email` (VARCHAR(256), UNIQUE, NOT NULL)
   - `PasswordHash` (VARCHAR(512), NULL - hỗ trợ tài khoản Google)
   - `FullName` (VARCHAR(150), NOT NULL)
   - `StudentId` (VARCHAR(30), NULL - MSSV tại DNTU)
   - `Department` (VARCHAR(100), NULL - Khoa / Viện)
   - `AvatarUrl` (VARCHAR(500), NULL)
   - `Bio` (TEXT, NULL)
   - `IsActive` (BOOLEAN, DEFAULT TRUE)
   - `EmailConfirmed` (BOOLEAN, DEFAULT FALSE)
   - `GoogleId` (VARCHAR(128), NULL, UNIQUE)
   - `CreatedAt` (TIMESTAMPTZ, NOT NULL)
   - `UpdatedAt` (TIMESTAMPTZ, NOT NULL)

2. **Roles**
   - `Id` (UUID/Guid, PK)
   - `Name` (VARCHAR(50), UNIQUE, NOT NULL) - ['Admin', 'Supervisor', 'Committee', 'Collaborator', 'ClubMember', 'Student', 'Guest']
   - `Description` (VARCHAR(255), NULL)

3. **UserRoles**
   - `UserId` (Guid, FK -> Users.Id, PK)
   - `RoleId` (Guid, FK -> Roles.Id, PK)
   - `AssignedAt` (TIMESTAMPTZ, NOT NULL)

4. **ClubDepartments**
   - `Id` (UUID/Guid, PK)
   - `Name` (VARCHAR(100), NOT NULL) - Ban Học thuật, Ban Truyền thông, Ban Sự kiện, Ban Đối ngoại
   - `Description` (TEXT, NULL)
   - `LeaderUserId` (Guid, FK -> Users.Id, NULL)

5. **MemberProfiles**
   - `Id` (UUID/Guid, PK)
   - `UserId` (Guid, FK -> Users.Id, UNIQUE, NOT NULL)
   - `DepartmentId` (Guid, FK -> ClubDepartments.Id, NULL)
   - `ClubRole` (VARCHAR(100), NOT NULL) - Ví dụ: Chủ nhiệm, Phó Chủ nhiệm, Trưởng ban, Thành viên
   - `JoinedDate` (DATE, NOT NULL)
   - `Status` (VARCHAR(50), NOT NULL) - Active, Inactive, Alumni
   - `EnglishLevel` (VARCHAR(50), NULL) - TOEIC, IELTS, CEFR B1, B2...
   - `TechSkills` (TEXT[], NULL)

6. **MembershipApplications**
   - `Id` (UUID/Guid, PK)
   - `UserId` (Guid, FK -> Users.Id, NOT NULL)
   - `PreferredDepartmentId` (Guid, FK -> ClubDepartments.Id, NULL)
   - `SelfIntroduction` (TEXT, NOT NULL)
   - `Motivation` (TEXT, NOT NULL)
   - `EnglishProficiency` (VARCHAR(100), NULL)
   - `Status` (VARCHAR(50), NOT NULL) - Pending, Approved, Rejected
   - `ReviewedByUserId` (Guid, FK -> Users.Id, NULL)
   - `ReviewNotes` (TEXT, NULL)
   - `ReviewedAt` (TIMESTAMPTZ, NULL)
   - `SubmittedAt` (TIMESTAMPTZ, NOT NULL)

7. **CommitteeTerms**
   - `Id` (UUID/Guid, PK)
   - `Name` (VARCHAR(100), NOT NULL) - Ví dụ: "Nhiệm kỳ 2024 - 2025", "Nhiệm kỳ 2025 - 2026"
   - `StartDate` (DATE, NOT NULL)
   - `EndDate` (DATE, NULL)
   - `IsCurrent` (BOOLEAN, DEFAULT FALSE)

8. **CommitteeAssignments**
   - `Id` (UUID/Guid, PK)
   - `TermId` (Guid, FK -> CommitteeTerms.Id, NOT NULL)
   - `UserId` (Guid, FK -> Users.Id, NOT NULL)
   - `Position` (VARCHAR(100), NOT NULL) - Chủ nhiệm, Phó chủ nhiệm, v.v.
   - `Notes` (TEXT, NULL)

---

### Nhóm 2: Sự kiện, Hoạt động & Điểm danh (Activities & Events)
9. **Events**
   - `Id` (UUID/Guid, PK)
   - `Title` (VARCHAR(250), NOT NULL)
   - `Slug` (VARCHAR(250), UNIQUE, NOT NULL)
   - `Description` (TEXT, NOT NULL)
   - `Location` (VARCHAR(250), NOT NULL) - Phòng A101 / Online Google Meet
   - `StartTime` (TIMESTAMPTZ, NOT NULL)
   - `EndTime` (TIMESTAMPTZ, NOT NULL)
   - `RegistrationDeadline` (TIMESTAMPTZ, NOT NULL)
   - `MaxCapacity` (INT, DEFAULT 100)
   - `BannerUrl` (VARCHAR(500), NULL)
   - `Status` (VARCHAR(50), NOT NULL) - Draft, Published, Ongoing, Completed, Cancelled
   - `CreatedByUserId` (Guid, FK -> Users.Id, NOT NULL)
   - `QrCheckInCode` (VARCHAR(100), NULL)
   - `CreatedAt` (TIMESTAMPTZ, NOT NULL)
   - `UpdatedAt` (TIMESTAMPTZ, NOT NULL)

10. **EventRegistrations**
    - `Id` (UUID/Guid, PK)
    - `EventId` (Guid, FK -> Events.Id, NOT NULL)
    - `UserId` (Guid, FK -> Users.Id, NOT NULL)
    - `RegisteredAt` (TIMESTAMPTZ, NOT NULL)
    - `Status` (VARCHAR(50), NOT NULL) - Registered, Cancelled, Waitlist
    - `Notes` (VARCHAR(255), NULL)
    - *UNIQUE CONSTRAINT (EventId, UserId)*

11. **EventAttendances**
    - `Id` (UUID/Guid, PK)
    - `EventId` (Guid, FK -> Events.Id, NOT NULL)
    - `UserId` (Guid, FK -> Users.Id, NOT NULL)
    - `CheckInTime` (TIMESTAMPTZ, NOT NULL)
    - `VerifiedByUserId` (Guid, FK -> Users.Id, NULL)
    - `Method` (VARCHAR(50), NOT NULL) - ManualCheckIn, DynamicQRCode
    - *UNIQUE CONSTRAINT (EventId, UserId)*

---

### Nhóm 3: Cổng Nội dung & CMS (Content & CMS)
12. **PostCategories**
    - `Id` (UUID/Guid, PK)
    - `Name` (VARCHAR(100), NOT NULL)
    - `Slug` (VARCHAR(100), UNIQUE, NOT NULL)
    - `Description` (VARCHAR(255), NULL)

13. **Posts**
    - `Id` (UUID/Guid, PK)
    - `CategoryId` (Guid, FK -> PostCategories.Id, NOT NULL)
    - `AuthorUserId` (Guid, FK -> Users.Id, NOT NULL)
    - `Title` (VARCHAR(255), NOT NULL)
    - `Slug` (VARCHAR(255), UNIQUE, NOT NULL)
    - `Summary` (VARCHAR(500), NOT NULL)
    - `ContentMarkdown` (TEXT, NOT NULL)
    - `ContentHtml` (TEXT, NOT NULL)
    - `ThumbnailUrl` (VARCHAR(500), NULL)
    - `Status` (VARCHAR(50), NOT NULL) - Draft, PendingReview, Published, Archived
    - `PublishedAt` (TIMESTAMPTZ, NULL)
    - `ViewCount` (INT, DEFAULT 0)
    - `CreatedAt` (TIMESTAMPTZ, NOT NULL)
    - `UpdatedAt` (TIMESTAMPTZ, NOT NULL)

14. **Tags** & **PostTags**
    - `Id` (UUID/Guid, PK), `Name`, `Slug`
    - Quan hệ Many-to-Many giữa `Posts` và `Tags`.

---

### Nhóm 4: Bảng vàng Thành tích (Hall of Achievement)
15. **AchievementCategories**
    - `Id` (UUID/Guid, PK)
    - `Name` (VARCHAR(100), NOT NULL) - Academic Excellence, Technology & Innovation, English Achievement, Global Engagement, Community Contribution
    - `Slug` (VARCHAR(100), UNIQUE, NOT NULL)

16. **Achievements**
    - `Id` (UUID/Guid, PK)
    - `CategoryId` (Guid, FK -> AchievementCategories.Id, NOT NULL)
    - `RecipientUserId` (Guid, FK -> Users.Id, NOT NULL)
    - `Title` (VARCHAR(255), NOT NULL)
    - `Description` (TEXT, NOT NULL)
    - `AwardedDate` (DATE, NOT NULL)
    - `EvidenceUrl` (VARCHAR(500), NULL) - Ảnh bằng chứng nhận, link bài báo, giải thưởng
    - `IsVerified` (BOOLEAN, DEFAULT FALSE)
    - `VerifiedByUserId` (Guid, FK -> Users.Id, NULL)
    - `CreatedAt` (TIMESTAMPTZ, NOT NULL)

---

### Nhóm 5: English for IT & Technology Radar (Knowledge Center)
17. **LearningResources (English for IT)**
    - `Id` (UUID/Guid, PK)
    - `Title` (VARCHAR(255), NOT NULL)
    - `Slug` (VARCHAR(255), UNIQUE, NOT NULL)
    - `Level` (VARCHAR(50), NOT NULL) - Beginner, Intermediate, Advanced, Professional
    - `Topic` (VARCHAR(100), NOT NULL) - Programming English, REST API, AI/ML, Cloud & DevOps, CV & Interview
    - `Summary` (TEXT, NOT NULL)
    - `Content` (TEXT, NOT NULL)
    - `GlossaryJson` (JSONB, NULL) - Danh mục từ vựng, phiên âm, định nghĩa và ngữ cảnh
    - `ReferenceUrl` (VARCHAR(500), NULL)
    - `CreatedAt` (TIMESTAMPTZ, NOT NULL)
    - `UpdatedAt` (TIMESTAMPTZ, NOT NULL)

18. **TechResources (Technology Radar & Open Source)**
    - `Id` (UUID/Guid, PK)
    - `Name` (VARCHAR(255), NOT NULL)
    - `SourceType` (VARCHAR(50), NOT NULL) - GitHubRepository, HuggingFaceModel, ResearchPaper, Framework
    - `ExternalId` (VARCHAR(255), NULL) - e.g. "dotnet/aspnetcore"
    - `OfficialUrl` (VARCHAR(500), NOT NULL)
    - `Description` (TEXT, NOT NULL)
    - `PrimaryLanguage` (VARCHAR(50), NULL)
    - `License` (VARCHAR(100), NULL)
    - `MetricsJson` (JSONB, NULL) - Stars, Forks, Downloads, Likes
    - `LearningSuitability` (VARCHAR(50), NULL) - BeginnerFriendly, Intermediate, Advanced
    - `LastCheckedAt` (TIMESTAMPTZ, NOT NULL)
    - `IsVerified` (BOOLEAN, DEFAULT TRUE)

---

### Nhóm 6: Cuộc thi & Cơ hội Việc làm (Opportunities & Careers)
19. **Opportunities**
    - `Id` (UUID/Guid, PK)
    - `Title` (VARCHAR(255), NOT NULL)
    - `Organizer` (VARCHAR(255), NOT NULL)
    - `Category` (VARCHAR(100), NOT NULL) - Hackathon, AI Challenge, Algorithm ICPC, Cybersecurity CTF, Scholarship, Exchange
    - `Scope` (VARCHAR(50), NOT NULL) - Vietnam, ASEAN, Global
    - `Format` (VARCHAR(50), NOT NULL) - Online, Offline, Hybrid
    - `OfficialUrl` (VARCHAR(500), NOT NULL)
    - `Eligibility` (TEXT, NOT NULL)
    - `RegistrationDeadline` (TIMESTAMPTZ, NULL)
    - `Status` (VARCHAR(50), NOT NULL) - VerifiedOpen, VerifiedClosed, Unverified
    - `VerifiedAt` (TIMESTAMPTZ, NULL)
    - `CreatedAt` (TIMESTAMPTZ, NOT NULL)

20. **Jobs (Career Gateway)**
    - `Id` (UUID/Guid, PK)
    - `Title` (VARCHAR(255), NOT NULL)
    - `Company` (VARCHAR(255), NOT NULL)
    - `JobType` (VARCHAR(50), NOT NULL) - Internship, Fresher, Junior
    - `WorkplaceType` (VARCHAR(50), NOT NULL) - Remote, Hybrid, Onsite
    - `Location` (VARCHAR(255), NOT NULL) - Dong Nai, Ho Chi Minh, Vietnam, Global
    - `ApplyUrl` (VARCHAR(500), NOT NULL)
    - `Requirements` (TEXT, NOT NULL)
    - `EnglishRequired` (BOOLEAN, DEFAULT TRUE)
    - `IsVerified` (BOOLEAN, DEFAULT TRUE)
    - `CreatedAt` (TIMESTAMPTZ, NOT NULL)

---

### Nhóm 7: Tự động hóa & Hệ thống (Ingestion & System)
21. **ContentSources**
    - `Id` (UUID/Guid, PK)
    - `Name` (VARCHAR(150), NOT NULL)
    - `Type` (VARCHAR(50), NOT NULL) - GitHubApi, HuggingFaceApi, RssFeed, ExternalJobFeed
    - `EndpointUrl` (VARCHAR(500), NOT NULL)
    - `IntervalMinutes` (INT, DEFAULT 360)
    - `IsEnabled` (BOOLEAN, DEFAULT TRUE)
    - `LastRunAt` (TIMESTAMPTZ, NULL)
    - `LastStatus` (VARCHAR(50), NULL)

22. **ImportRuns**
    - `Id` (UUID/Guid, PK)
    - `SourceId` (Guid, FK -> ContentSources.Id, NOT NULL)
    - `StartTime` (TIMESTAMPTZ, NOT NULL)
    - `EndTime` (TIMESTAMPTZ, NULL)
    - `ItemsFetched` (INT, DEFAULT 0)
    - `ItemsInserted` (INT, DEFAULT 0)
    - `Status` (VARCHAR(50), NOT NULL) - Success, Failed, Partial
    - `ErrorMessage` (TEXT, NULL)

23. **AuditLogs**
    - `Id` (UUID/Guid, PK)
    - `UserId` (Guid, FK -> Users.Id, NULL)
    - `Action` (VARCHAR(100), NOT NULL)
    - `Resource` (VARCHAR(100), NOT NULL)
    - `ResourceId` (VARCHAR(100), NULL)
    - `IpAddress` (VARCHAR(50), NULL)
    - `Timestamp` (TIMESTAMPTZ, NOT NULL)
    - `DetailsJson` (TEXT, NULL)
