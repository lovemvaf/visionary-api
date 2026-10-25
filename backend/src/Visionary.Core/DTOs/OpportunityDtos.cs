using System;
using Visionary.Core.Enums;

namespace Visionary.Core.DTOs
{
    public class OpportunityDto
    {
        public Guid Id { get; set; }
        public string Title { get; set; } = string.Empty;
        public string Organizer { get; set; } = string.Empty;
        public string Category { get; set; } = string.Empty;
        public string Scope { get; set; } = string.Empty;
        public string Format { get; set; } = string.Empty;
        public string OfficialUrl { get; set; } = string.Empty;
        public string Eligibility { get; set; } = string.Empty;
        public DateTime? RegistrationDeadline { get; set; }
        public string Status { get; set; } = string.Empty;
        public DateTime? VerifiedAt { get; set; }
        public string? VerifiedSource { get; set; }
    }

    public class CreateOpportunityRequest
    {
        public string Title { get; set; } = string.Empty;
        public string Organizer { get; set; } = string.Empty;
        public OpportunityCategory Category { get; set; } = OpportunityCategory.Hackathon;
        public string Scope { get; set; } = "Vietnam";
        public string Format { get; set; } = "Online";
        public string OfficialUrl { get; set; } = string.Empty;
        public string Eligibility { get; set; } = string.Empty;
        public DateTime? RegistrationDeadline { get; set; }
        public OpportunityStatus Status { get; set; } = OpportunityStatus.VerifiedOpen;
    }

    public class JobDto
    {
        public Guid Id { get; set; }
        public string Title { get; set; } = string.Empty;
        public string Company { get; set; } = string.Empty;
        public string JobType { get; set; } = string.Empty;
        public string WorkplaceType { get; set; } = string.Empty;
        public string Location { get; set; } = string.Empty;
        public string ApplyUrl { get; set; } = string.Empty;
        public string Requirements { get; set; } = string.Empty;
        public bool EnglishRequired { get; set; }
        public bool IsVerified { get; set; }
        public DateTime CreatedAt { get; set; }
    }

    public class CreateJobRequest
    {
        public string Title { get; set; } = string.Empty;
        public string Company { get; set; } = string.Empty;
        public JobType JobType { get; set; } = JobType.Internship;
        public WorkplaceType WorkplaceType { get; set; } = WorkplaceType.Hybrid;
        public string Location { get; set; } = "Dong Nai / HCM";
        public string ApplyUrl { get; set; } = string.Empty;
        public string Requirements { get; set; } = string.Empty;
        public bool EnglishRequired { get; set; } = true;
    }
}
