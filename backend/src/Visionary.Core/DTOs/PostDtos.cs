using System;
using System.Collections.Generic;
using Visionary.Core.Enums;

namespace Visionary.Core.DTOs
{
    public class PostCategoryDto
    {
        public Guid Id { get; set; }
        public string Name { get; set; } = string.Empty;
        public string Slug { get; set; } = string.Empty;
        public string? Description { get; set; }
        public int PostCount { get; set; }
    }

    public class PostDto
    {
        public Guid Id { get; set; }
        public Guid CategoryId { get; set; }
        public string CategoryName { get; set; } = string.Empty;
        public string AuthorName { get; set; } = string.Empty;
        public string Title { get; set; } = string.Empty;
        public string Slug { get; set; } = string.Empty;
        public string Summary { get; set; } = string.Empty;
        public string ContentMarkdown { get; set; } = string.Empty;
        public string ContentHtml { get; set; } = string.Empty;
        public string? ThumbnailUrl { get; set; }
        public string Status { get; set; } = string.Empty;
        public DateTime? PublishedAt { get; set; }
        public int ViewCount { get; set; }
        public List<string> Tags { get; set; } = new();
    }

    public class CreatePostRequest
    {
        public Guid CategoryId { get; set; }
        public string Title { get; set; } = string.Empty;
        public string Summary { get; set; } = string.Empty;
        public string ContentMarkdown { get; set; } = string.Empty;
        public string? ThumbnailUrl { get; set; }
        public List<string> Tags { get; set; } = new();
        public bool SubmitForReview { get; set; } = false;
    }

    public class UpdatePostRequest : CreatePostRequest
    {
        public PostStatus Status { get; set; }
    }
}
