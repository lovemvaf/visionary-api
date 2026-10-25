using System;
using Visionary.Core.Common;
using Visionary.Core.Enums;

namespace Visionary.Core.Entities
{
    public class LearningResource : BaseEntity
    {
        public string Title { get; set; } = string.Empty;
        public string Slug { get; set; } = string.Empty;
        public EnglishLevel Level { get; set; } = EnglishLevel.Intermediate;
        public string Topic { get; set; } = "Programming English"; // Web Dev, AI/ML, Cloud & DevOps, CV & Interview...
        public string Summary { get; set; } = string.Empty;
        public string Content { get; set; } = string.Empty;
        public string? GlossaryJson { get; set; } // JSON array of terminology, phonetic, meaning, example
        public string? ReferenceUrl { get; set; }
        public int ViewCount { get; set; } = 0;
    }

    public class TechResource : BaseEntity
    {
        public string Name { get; set; } = string.Empty; // e.g. "dotnet/aspnetcore", "meta-llama/Llama-3-8B"
        public TechSourceType SourceType { get; set; } = TechSourceType.GitHubRepository;
        public string? ExternalId { get; set; }
        public string OfficialUrl { get; set; } = string.Empty;
        public string Description { get; set; } = string.Empty;
        public string? PrimaryLanguage { get; set; }
        public string? License { get; set; }
        public string? MetricsJson { get; set; } // Stars, Forks, Downloads, Likes
        public string? LearningSuitability { get; set; } // BeginnerFriendly, Intermediate, Advanced
        public DateTime LastCheckedAt { get; set; } = DateTime.UtcNow;
        public bool IsVerified { get; set; } = true;
    }
}
