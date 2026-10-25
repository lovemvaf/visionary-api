using System;
using System.Collections.Generic;
using Visionary.Core.Common;

namespace Visionary.Core.Entities
{
    public class User : BaseEntity
    {
        public string Email { get; set; } = string.Empty;
        public string? PasswordHash { get; set; }
        public string FullName { get; set; } = string.Empty;
        public string? StudentId { get; set; } // MSSV
        public string? Department { get; set; } // Khoa CNTT, Ngoại ngữ...
        public string? AvatarUrl { get; set; }
        public string? Bio { get; set; }
        public bool IsActive { get; set; } = true;
        public bool EmailConfirmed { get; set; } = false;
        public string? GoogleId { get; set; }

        public ICollection<UserRole> UserRoles { get; set; } = new List<UserRole>();
        public MemberProfile? MemberProfile { get; set; }
        public ICollection<MembershipApplication> Applications { get; set; } = new List<MembershipApplication>();
        public ICollection<EventRegistration> Registrations { get; set; } = new List<EventRegistration>();
        public ICollection<EventAttendance> Attendances { get; set; } = new List<EventAttendance>();
        public ICollection<Post> Posts { get; set; } = new List<Post>();
        public ICollection<Achievement> Achievements { get; set; } = new List<Achievement>();
    }

    public class Role
    {
        public Guid Id { get; set; } = Guid.NewGuid();
        public string Name { get; set; } = string.Empty;
        public string? Description { get; set; }

        public ICollection<UserRole> UserRoles { get; set; } = new List<UserRole>();
    }

    public class UserRole
    {
        public Guid UserId { get; set; }
        public User User { get; set; } = null!;

        public Guid RoleId { get; set; }
        public Role Role { get; set; } = null!;

        public DateTime AssignedAt { get; set; } = DateTime.UtcNow;
    }
}
