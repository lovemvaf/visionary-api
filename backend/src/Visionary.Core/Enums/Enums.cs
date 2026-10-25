namespace Visionary.Core.Enums
{
    public static class AppRoles
    {
        public const string Admin = "Admin";
        public const string Supervisor = "Supervisor";
        public const string Committee = "Committee";
        public const string Collaborator = "Collaborator";
        public const string ClubMember = "ClubMember";
        public const string Student = "Student";
        public const string Guest = "Guest";
    }

    public enum MembershipStatus
    {
        Pending,
        Approved,
        Rejected
    }

    public enum EventStatus
    {
        Draft,
        Published,
        Ongoing,
        Completed,
        Cancelled
    }

    public enum RegistrationStatus
    {
        Registered,
        Waitlist,
        Cancelled
    }

    public enum AttendanceMethod
    {
        ManualCheckIn,
        DynamicQRCode
    }

    public enum PostStatus
    {
        Draft,
        PendingReview,
        Published,
        Archived
    }

    public enum EnglishLevel
    {
        Beginner,
        Intermediate,
        Advanced,
        Professional
    }

    public enum TechSourceType
    {
        GitHubRepository,
        HuggingFaceModel,
        ResearchPaper,
        Framework
    }

    public enum OpportunityCategory
    {
        Hackathon,
        AiChallenge,
        AlgorithmIcpc,
        CybersecurityCtf,
        Scholarship,
        ExchangeProgram
    }

    public enum OpportunityStatus
    {
        VerifiedOpen,
        VerifiedClosed,
        Unverified
    }

    public enum JobType
    {
        Internship,
        Fresher,
        Junior
    }

    public enum WorkplaceType
    {
        Remote,
        Hybrid,
        Onsite
    }
}
