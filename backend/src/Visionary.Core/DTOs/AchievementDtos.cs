using System;

namespace Visionary.Core.DTOs
{
    public class AchievementDto
    {
        public Guid Id { get; set; }
        public Guid CategoryId { get; set; }
        public string CategoryName { get; set; } = string.Empty;
        public Guid RecipientUserId { get; set; }
        public string RecipientName { get; set; } = string.Empty;
        public string? StudentId { get; set; }
        public string? Department { get; set; }
        public string Title { get; set; } = string.Empty;
        public string Description { get; set; } = string.Empty;
        public DateTime AwardedDate { get; set; }
        public string? EvidenceUrl { get; set; }
        public bool IsVerified { get; set; }
    }

    public class NominateAchievementRequest
    {
        public Guid CategoryId { get; set; }
        public Guid RecipientUserId { get; set; }
        public string Title { get; set; } = string.Empty;
        public string Description { get; set; } = string.Empty;
        public DateTime AwardedDate { get; set; }
        public string? EvidenceUrl { get; set; }
    }

    public class VerifyAchievementRequest
    {
        public bool IsVerified { get; set; }
    }
}
