using System;
using System.Collections.Generic;

namespace Visionary.Core.DTOs
{
    public class ClubOverviewDto
    {
        public string Name { get; set; } = "Câu lạc bộ Tiếng Anh DNTU (VISIONARY)";
        public string Description { get; set; } = "Kết nối sinh viên, phát triển kỹ năng ngoại ngữ gắn với công nghệ và mở rộng cơ hội hội nhập toàn cầu.";
        public string Mission { get; set; } = "Connecting Students, Technology and Global Opportunities.";
        public int TotalMembers { get; set; }
        public int TotalEvents { get; set; }
        public List<DepartmentDto> Departments { get; set; } = new();
        public List<CommitteeMemberDto> CurrentCommittee { get; set; } = new();
        public string ContactEmail { get; set; } = "visionary.dntu@gmail.com";
    }

    public class DepartmentDto
    {
        public Guid Id { get; set; }
        public string Name { get; set; } = string.Empty;
        public string? Description { get; set; }
        public int MemberCount { get; set; }
    }

    public class MemberDto
    {
        public Guid Id { get; set; }
        public Guid UserId { get; set; }
        public string FullName { get; set; } = string.Empty;
        public string Email { get; set; } = string.Empty;
        public string? StudentId { get; set; }
        public string? DepartmentName { get; set; }
        public string ClubRole { get; set; } = string.Empty;
        public string Status { get; set; } = string.Empty;
        public DateTime JoinedDate { get; set; }
        public string? EnglishLevel { get; set; }
        public string? AvatarUrl { get; set; }
    }

    public class CommitteeMemberDto
    {
        public Guid UserId { get; set; }
        public string FullName { get; set; } = string.Empty;
        public string Position { get; set; } = string.Empty;
        public string? AvatarUrl { get; set; }
        public string? Department { get; set; }
    }

    public class ApplyMembershipRequest
    {
        public Guid? PreferredDepartmentId { get; set; }
        public string SelfIntroduction { get; set; } = string.Empty;
        public string Motivation { get; set; } = string.Empty;
        public string? EnglishProficiency { get; set; }
    }

    public class MembershipApplicationDto
    {
        public Guid Id { get; set; }
        public Guid UserId { get; set; }
        public string ApplicantName { get; set; } = string.Empty;
        public string ApplicantEmail { get; set; } = string.Empty;
        public string? StudentId { get; set; }
        public string? PreferredDepartmentName { get; set; }
        public string SelfIntroduction { get; set; } = string.Empty;
        public string Motivation { get; set; } = string.Empty;
        public string? EnglishProficiency { get; set; }
        public string Status { get; set; } = string.Empty;
        public string? ReviewNotes { get; set; }
        public DateTime SubmittedAt { get; set; }
    }

    public class ReviewApplicationRequest
    {
        public bool IsApproved { get; set; }
        public string? ClubRole { get; set; } // default "Thành viên"
        public Guid? DepartmentId { get; set; }
        public string? ReviewNotes { get; set; }
    }
}
