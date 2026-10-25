using System;
using System.Collections.Generic;
using Visionary.Core.Common;
using Visionary.Core.Enums;

namespace Visionary.Core.Entities
{
    public class ClubDepartment : BaseEntity
    {
        public string Name { get; set; } = string.Empty;
        public string? Description { get; set; }
        public Guid? LeaderUserId { get; set; }
        public User? LeaderUser { get; set; }

        public ICollection<MemberProfile> Members { get; set; } = new List<MemberProfile>();
    }

    public class MemberProfile : BaseEntity
    {
        public Guid UserId { get; set; }
        public User User { get; set; } = null!;

        public Guid? DepartmentId { get; set; }
        public ClubDepartment? Department { get; set; }

        public string ClubRole { get; set; } = "Thành viên";
        public DateTime JoinedDate { get; set; } = DateTime.UtcNow;
        public string Status { get; set; } = "Active"; // Active, Inactive, Alumni
        public string? EnglishLevel { get; set; } // TOEIC 750, IELTS 6.5, etc.
        public string? TechSkills { get; set; } // Comma separated or JSON
    }

    public class MembershipApplication : BaseEntity
    {
        public Guid UserId { get; set; }
        public User User { get; set; } = null!;

        public Guid? PreferredDepartmentId { get; set; }
        public ClubDepartment? PreferredDepartment { get; set; }

        public string SelfIntroduction { get; set; } = string.Empty;
        public string Motivation { get; set; } = string.Empty;
        public string? EnglishProficiency { get; set; }
        public MembershipStatus Status { get; set; } = MembershipStatus.Pending;

        public Guid? ReviewedByUserId { get; set; }
        public User? ReviewedByUser { get; set; }
        public string? ReviewNotes { get; set; }
        public DateTime? ReviewedAt { get; set; }
        public DateTime SubmittedAt { get; set; } = DateTime.UtcNow;
    }

    public class CommitteeTerm : BaseEntity
    {
        public string Name { get; set; } = string.Empty; // e.g. "Nhiệm kỳ 2024 - 2025"
        public DateTime StartDate { get; set; }
        public DateTime? EndDate { get; set; }
        public bool IsCurrent { get; set; } = false;

        public ICollection<CommitteeAssignment> Assignments { get; set; } = new List<CommitteeAssignment>();
    }

    public class CommitteeAssignment : BaseEntity
    {
        public Guid TermId { get; set; }
        public CommitteeTerm Term { get; set; } = null!;

        public Guid UserId { get; set; }
        public User User { get; set; } = null!;

        public string Position { get; set; } = string.Empty; // Chủ nhiệm, Phó Chủ nhiệm, Trưởng ban...
        public string? Notes { get; set; }
    }
}
