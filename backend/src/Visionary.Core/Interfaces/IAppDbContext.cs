using System.Threading;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using Visionary.Core.Entities;

namespace Visionary.Core.Interfaces
{
    public interface IAppDbContext
    {
        DbSet<User> Users { get; }
        DbSet<Role> Roles { get; }
        DbSet<UserRole> UserRoles { get; }
        DbSet<ClubDepartment> ClubDepartments { get; }
        DbSet<MemberProfile> MemberProfiles { get; }
        DbSet<MembershipApplication> MembershipApplications { get; }
        DbSet<CommitteeTerm> CommitteeTerms { get; }
        DbSet<CommitteeAssignment> CommitteeAssignments { get; }
        DbSet<Event> Events { get; }
        DbSet<EventRegistration> EventRegistrations { get; }
        DbSet<EventAttendance> EventAttendances { get; }
        DbSet<PostCategory> PostCategories { get; }
        DbSet<Post> Posts { get; }
        DbSet<Tag> Tags { get; }
        DbSet<PostTag> PostTags { get; }
        DbSet<AchievementCategory> AchievementCategories { get; }
        DbSet<Achievement> Achievements { get; }
        DbSet<LearningResource> LearningResources { get; }
        DbSet<TechResource> TechResources { get; }
        DbSet<Opportunity> Opportunities { get; }
        DbSet<Job> Jobs { get; }
        DbSet<ContentSource> ContentSources { get; }
        DbSet<ImportRun> ImportRuns { get; }
        DbSet<AuditLog> AuditLogs { get; }

        Task<int> SaveChangesAsync(CancellationToken cancellationToken = default);
    }
}
