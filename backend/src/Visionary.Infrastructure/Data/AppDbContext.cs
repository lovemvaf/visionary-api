using System;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using Visionary.Core.Entities;
using Visionary.Core.Interfaces;

namespace Visionary.Infrastructure.Data
{
    public class AppDbContext : DbContext, IAppDbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
        {
        }

        public DbSet<User> Users => Set<User>();
        public DbSet<Role> Roles => Set<Role>();
        public DbSet<UserRole> UserRoles => Set<UserRole>();
        public DbSet<ClubDepartment> ClubDepartments => Set<ClubDepartment>();
        public DbSet<MemberProfile> MemberProfiles => Set<MemberProfile>();
        public DbSet<MembershipApplication> MembershipApplications => Set<MembershipApplication>();
        public DbSet<CommitteeTerm> CommitteeTerms => Set<CommitteeTerm>();
        public DbSet<CommitteeAssignment> CommitteeAssignments => Set<CommitteeAssignment>();
        public DbSet<Event> Events => Set<Event>();
        public DbSet<EventRegistration> EventRegistrations => Set<EventRegistration>();
        public DbSet<EventAttendance> EventAttendances => Set<EventAttendance>();
        public DbSet<PostCategory> PostCategories => Set<PostCategory>();
        public DbSet<Post> Posts => Set<Post>();
        public DbSet<Tag> Tags => Set<Tag>();
        public DbSet<PostTag> PostTags => Set<PostTag>();
        public DbSet<AchievementCategory> AchievementCategories => Set<AchievementCategory>();
        public DbSet<Achievement> Achievements => Set<Achievement>();
        public DbSet<LearningResource> LearningResources => Set<LearningResource>();
        public DbSet<TechResource> TechResources => Set<TechResource>();
        public DbSet<Opportunity> Opportunities => Set<Opportunity>();
        public DbSet<Job> Jobs => Set<Job>();
        public DbSet<ContentSource> ContentSources => Set<ContentSource>();
        public DbSet<ImportRun> ImportRuns => Set<ImportRun>();
        public DbSet<AuditLog> AuditLogs => Set<AuditLog>();

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // User
            modelBuilder.Entity<User>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.HasIndex(e => e.Email).IsUnique();
                entity.Property(e => e.Email).IsRequired().HasMaxLength(256);
                entity.Property(e => e.FullName).IsRequired().HasMaxLength(150);
            });

            // Role
            modelBuilder.Entity<Role>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.HasIndex(e => e.Name).IsUnique();
                entity.Property(e => e.Name).IsRequired().HasMaxLength(50);
            });

            // UserRole (Composite Key)
            modelBuilder.Entity<UserRole>(entity =>
            {
                entity.HasKey(ur => new { ur.UserId, ur.RoleId });
                entity.HasOne(ur => ur.User)
                      .WithMany(u => u.UserRoles)
                      .HasForeignKey(ur => ur.UserId)
                      .OnDelete(DeleteBehavior.Cascade);
                entity.HasOne(ur => ur.Role)
                      .WithMany(r => r.UserRoles)
                      .HasForeignKey(ur => ur.RoleId)
                      .OnDelete(DeleteBehavior.Cascade);
            });

            // MemberProfile (1-1 with User)
            modelBuilder.Entity<MemberProfile>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.HasOne(mp => mp.User)
                      .WithOne(u => u.MemberProfile)
                      .HasForeignKey<MemberProfile>(mp => mp.UserId)
                      .OnDelete(DeleteBehavior.Cascade);
                entity.HasOne(mp => mp.Department)
                      .WithMany(d => d.Members)
                      .HasForeignKey(mp => mp.DepartmentId)
                      .OnDelete(DeleteBehavior.SetNull);
            });

            // MembershipApplication
            modelBuilder.Entity<MembershipApplication>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.HasOne(ma => ma.User)
                      .WithMany(u => u.Applications)
                      .HasForeignKey(ma => ma.UserId)
                      .OnDelete(DeleteBehavior.Cascade);
            });

            // Event
            modelBuilder.Entity<Event>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.HasIndex(e => e.Slug).IsUnique();
                entity.Property(e => e.Title).IsRequired().HasMaxLength(250);
            });

            // EventRegistration
            modelBuilder.Entity<EventRegistration>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.HasIndex(e => new { e.EventId, e.UserId }).IsUnique();
                entity.HasOne(er => er.Event)
                      .WithMany(e => e.Registrations)
                      .HasForeignKey(er => er.EventId)
                      .OnDelete(DeleteBehavior.Cascade);
                entity.HasOne(er => er.User)
                      .WithMany(u => u.Registrations)
                      .HasForeignKey(er => er.UserId)
                      .OnDelete(DeleteBehavior.Cascade);
            });

            // EventAttendance
            modelBuilder.Entity<EventAttendance>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.HasIndex(e => new { e.EventId, e.UserId }).IsUnique();
                entity.HasOne(ea => ea.Event)
                      .WithMany(e => e.Attendances)
                      .HasForeignKey(ea => ea.EventId)
                      .OnDelete(DeleteBehavior.Cascade);
                entity.HasOne(ea => ea.User)
                      .WithMany(u => u.Attendances)
                      .HasForeignKey(ea => ea.UserId)
                      .OnDelete(DeleteBehavior.Cascade);
            });

            // Post & PostCategory
            modelBuilder.Entity<PostCategory>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.HasIndex(e => e.Slug).IsUnique();
            });

            modelBuilder.Entity<Post>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.HasIndex(e => e.Slug).IsUnique();
                entity.HasOne(p => p.Category)
                      .WithMany(c => c.Posts)
                      .HasForeignKey(p => p.CategoryId)
                      .OnDelete(DeleteBehavior.Restrict);
                entity.HasOne(p => p.AuthorUser)
                      .WithMany(u => u.Posts)
                      .HasForeignKey(p => p.AuthorUserId)
                      .OnDelete(DeleteBehavior.Cascade);
            });

            // PostTag (Composite Key)
            modelBuilder.Entity<PostTag>(entity =>
            {
                entity.HasKey(pt => new { pt.PostId, pt.TagId });
                entity.HasOne(pt => pt.Post)
                      .WithMany(p => p.PostTags)
                      .HasForeignKey(pt => pt.PostId)
                      .OnDelete(DeleteBehavior.Cascade);
                entity.HasOne(pt => pt.Tag)
                      .WithMany(t => t.PostTags)
                      .HasForeignKey(pt => pt.TagId)
                      .OnDelete(DeleteBehavior.Cascade);
            });

            // Achievement
            modelBuilder.Entity<Achievement>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.HasOne(a => a.Category)
                      .WithMany()
                      .HasForeignKey(a => a.CategoryId)
                      .OnDelete(DeleteBehavior.Restrict);
                entity.HasOne(a => a.RecipientUser)
                      .WithMany(u => u.Achievements)
                      .HasForeignKey(a => a.RecipientUserId)
                      .OnDelete(DeleteBehavior.Cascade);
            });

            // LearningResource
            modelBuilder.Entity<LearningResource>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.HasIndex(e => e.Slug).IsUnique();
            });

            // TechResource
            modelBuilder.Entity<TechResource>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.HasIndex(e => e.Name);
            });

            // Opportunity
            modelBuilder.Entity<Opportunity>(entity =>
            {
                entity.HasKey(e => e.Id);
            });

            // Job
            modelBuilder.Entity<Job>(entity =>
            {
                entity.HasKey(e => e.Id);
            });
        }
    }
}
