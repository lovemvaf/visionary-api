using System;
using System.Collections.Generic;
using Visionary.Core.Common;
using Visionary.Core.Enums;

namespace Visionary.Core.Entities
{
    public class PostCategory : BaseEntity
    {
        public string Name { get; set; } = string.Empty;
        public string Slug { get; set; } = string.Empty;
        public string? Description { get; set; }

        public ICollection<Post> Posts { get; set; } = new List<Post>();
    }

    public class Tag : BaseEntity
    {
        public string Name { get; set; } = string.Empty;
        public string Slug { get; set; } = string.Empty;

        public ICollection<PostTag> PostTags { get; set; } = new List<PostTag>();
    }

    public class PostTag
    {
        public Guid PostId { get; set; }
        public Post Post { get; set; } = null!;

        public Guid TagId { get; set; }
        public Tag Tag { get; set; } = null!;
    }

    public class Post : BaseEntity
    {
        public Guid CategoryId { get; set; }
        public PostCategory Category { get; set; } = null!;

        public Guid AuthorUserId { get; set; }
        public User AuthorUser { get; set; } = null!;

        public string Title { get; set; } = string.Empty;
        public string Slug { get; set; } = string.Empty;
        public string Summary { get; set; } = string.Empty;
        public string ContentMarkdown { get; set; } = string.Empty;
        public string ContentHtml { get; set; } = string.Empty;
        public string? ThumbnailUrl { get; set; }
        public PostStatus Status { get; set; } = PostStatus.Published;
        public DateTime? PublishedAt { get; set; }
        public int ViewCount { get; set; } = 0;

        public ICollection<PostTag> PostTags { get; set; } = new List<PostTag>();
    }
}
