using System;
using Visionary.Core.Common;

namespace Visionary.Core.Entities
{
    public class ContentSource : BaseEntity
    {
        public string Name { get; set; } = string.Empty;
        public string Type { get; set; } = "GitHubApi"; // GitHubApi, HuggingFaceApi, RssFeed, ExternalJobFeed
        public string EndpointUrl { get; set; } = string.Empty;
        public int IntervalMinutes { get; set; } = 360;
        public bool IsEnabled { get; set; } = true;
        public DateTime? LastRunAt { get; set; }
        public string? LastStatus { get; set; }
    }

    public class ImportRun : BaseEntity
    {
        public Guid SourceId { get; set; }
        public ContentSource Source { get; set; } = null!;

        public DateTime StartTime { get; set; } = DateTime.UtcNow;
        public DateTime? EndTime { get; set; }
        public int ItemsFetched { get; set; } = 0;
        public int ItemsInserted { get; set; } = 0;
        public string Status { get; set; } = "Success"; // Success, Failed, Partial
        public string? ErrorMessage { get; set; }
    }

    public class AuditLog : BaseEntity
    {
        public Guid? UserId { get; set; }
        public User? User { get; set; }

        public string Action { get; set; } = string.Empty; // LOGIN, REGISTER, APPROVE_MEMBER, CREATE_EVENT, etc.
        public string Resource { get; set; } = string.Empty;
        public string? ResourceId { get; set; }
        public string? IpAddress { get; set; }
        public DateTime Timestamp { get; set; } = DateTime.UtcNow;
        public string? DetailsJson { get; set; }
    }
}
