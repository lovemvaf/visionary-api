using System;
using System.Collections.Generic;

namespace Visionary.Core.DTOs
{
    public class DashboardStatsDto
    {
        public int TotalUsers { get; set; }
        public int TotalMembers { get; set; }
        public int PendingApplications { get; set; }
        public int TotalEvents { get; set; }
        public int TotalPosts { get; set; }
        public int TotalAchievements { get; set; }
        public int TotalOpportunities { get; set; }
        public int TotalJobs { get; set; }
        public int TotalTechResources { get; set; }
        public List<RecentActivityDto> RecentActivities { get; set; } = new();
    }

    public class RecentActivityDto
    {
        public string Action { get; set; } = string.Empty;
        public string Description { get; set; } = string.Empty;
        public DateTime Timestamp { get; set; }
        public string? UserName { get; set; }
    }

    public class ContentSourceDto
    {
        public Guid Id { get; set; }
        public string Name { get; set; } = string.Empty;
        public string Type { get; set; } = string.Empty;
        public string EndpointUrl { get; set; } = string.Empty;
        public int IntervalMinutes { get; set; }
        public bool IsEnabled { get; set; }
        public DateTime? LastRunAt { get; set; }
        public string? LastStatus { get; set; }
    }

    public class AuditLogDto
    {
        public Guid Id { get; set; }
        public string Action { get; set; } = string.Empty;
        public string Resource { get; set; } = string.Empty;
        public string? ResourceId { get; set; }
        public string? UserName { get; set; }
        public string? IpAddress { get; set; }
        public DateTime Timestamp { get; set; }
        public string? Details { get; set; }
    }
}
