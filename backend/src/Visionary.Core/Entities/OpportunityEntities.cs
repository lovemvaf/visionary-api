using System;
using Visionary.Core.Common;
using Visionary.Core.Enums;

namespace Visionary.Core.Entities
{
    public class Opportunity : BaseEntity
    {
        public string Title { get; set; } = string.Empty;
        public string Organizer { get; set; } = string.Empty;
        public OpportunityCategory Category { get; set; } = OpportunityCategory.Hackathon;
        public string Scope { get; set; } = "Vietnam"; // Vietnam, ASEAN, Global
        public string Format { get; set; } = "Online"; // Online, Offline, Hybrid
        public string OfficialUrl { get; set; } = string.Empty;
        public string Eligibility { get; set; } = string.Empty;
        public DateTime? RegistrationDeadline { get; set; }
        public OpportunityStatus Status { get; set; } = OpportunityStatus.VerifiedOpen;
        public DateTime? VerifiedAt { get; set; }
        public string? VerifiedSource { get; set; }
    }

    public class Job : BaseEntity
    {
        public string Title { get; set; } = string.Empty;
        public string Company { get; set; } = string.Empty;
        public JobType JobType { get; set; } = JobType.Internship;
        public WorkplaceType WorkplaceType { get; set; } = WorkplaceType.Hybrid;
        public string Location { get; set; } = "Dong Nai / HCM";
        public string ApplyUrl { get; set; } = string.Empty;
        public string Requirements { get; set; } = string.Empty;
        public bool EnglishRequired { get; set; } = true;
        public bool IsVerified { get; set; } = true;
    }
}
