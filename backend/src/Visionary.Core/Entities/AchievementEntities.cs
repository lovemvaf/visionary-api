using System;
using Visionary.Core.Common;

namespace Visionary.Core.Entities
{
    public class AchievementCategory : BaseEntity
    {
        public string Name { get; set; } = string.Empty; // Academic Excellence, Technology & Innovation, English Achievement, Global Engagement, Community Contribution
        public string Slug { get; set; } = string.Empty;
        public string? Description { get; set; }
    }

    public class Achievement : BaseEntity
    {
        public Guid CategoryId { get; set; }
        public AchievementCategory Category { get; set; } = null!;

        public Guid RecipientUserId { get; set; }
        public User RecipientUser { get; set; } = null!;

        public string Title { get; set; } = string.Empty;
        public string Description { get; set; } = string.Empty;
        public DateTime AwardedDate { get; set; }
        public string? EvidenceUrl { get; set; }
        public bool IsVerified { get; set; } = false;

        public Guid? VerifiedByUserId { get; set; }
        public User? VerifiedByUser { get; set; }
    }
}
