using System;
using Visionary.Core.Enums;

namespace Visionary.Core.DTOs
{
    public class LearningResourceDto
    {
        public Guid Id { get; set; }
        public string Title { get; set; } = string.Empty;
        public string Slug { get; set; } = string.Empty;
        public string Level { get; set; } = string.Empty;
        public string Topic { get; set; } = string.Empty;
        public string Summary { get; set; } = string.Empty;
        public string Content { get; set; } = string.Empty;
        public string? GlossaryJson { get; set; }
        public string? ReferenceUrl { get; set; }
        public int ViewCount { get; set; }
        public DateTime CreatedAt { get; set; }
    }

    public class CreateLearningResourceRequest
    {
        public string Title { get; set; } = string.Empty;
        public EnglishLevel Level { get; set; } = EnglishLevel.Intermediate;
        public string Topic { get; set; } = "Programming English";
        public string Summary { get; set; } = string.Empty;
        public string Content { get; set; } = string.Empty;
        public string? GlossaryJson { get; set; }
        public string? ReferenceUrl { get; set; }
    }

    public class TechResourceDto
    {
        public Guid Id { get; set; }
        public string Name { get; set; } = string.Empty;
        public string SourceType { get; set; } = string.Empty;
        public string? ExternalId { get; set; }
        public string OfficialUrl { get; set; } = string.Empty;
        public string Description { get; set; } = string.Empty;
        public string? PrimaryLanguage { get; set; }
        public string? License { get; set; }
        public string? MetricsJson { get; set; }
        public string? LearningSuitability { get; set; }
        public DateTime LastCheckedAt { get; set; }
        public bool IsVerified { get; set; }
    }

    public class SyncTechResourcesRequest
    {
        public string Source { get; set; } = "All"; // "GitHub", "HuggingFace", "All"
    }
}
