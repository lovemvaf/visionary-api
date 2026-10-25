using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Claims;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Visionary.Core.Common;
using Visionary.Core.DTOs;
using Visionary.Core.Entities;
using Visionary.Core.Enums;
using Visionary.Infrastructure.Data;

namespace Visionary.Api.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class PostsController : ControllerBase
    {
        private readonly AppDbContext _context;

        public PostsController(AppDbContext context)
        {
            _context = context;
        }

        [HttpGet]
        public async Task<ActionResult<ApiResponse<PagedResponse<PostDto>>>> GetPosts(
            [FromQuery] Guid? categoryId = null,
            [FromQuery] string? search = null,
            [FromQuery] int pageIndex = 1,
            [FromQuery] int pageSize = 10)
        {
            var query = _context.Posts
                .Include(p => p.Category)
                .Include(p => p.AuthorUser)
                .Include(p => p.PostTags).ThenInclude(pt => pt.Tag)
                .Where(p => p.Status == PostStatus.Published)
                .AsQueryable();

            if (categoryId.HasValue)
            {
                query = query.Where(p => p.CategoryId == categoryId.Value);
            }

            if (!string.IsNullOrWhiteSpace(search))
            {
                var s = search.Trim().ToLower();
                query = query.Where(p => p.Title.ToLower().Contains(s) || p.Summary.ToLower().Contains(s));
            }

            var total = await query.CountAsync();
            var items = await query
                .OrderByDescending(p => p.PublishedAt ?? p.CreatedAt)
                .Skip((pageIndex - 1) * pageSize)
                .Take(pageSize)
                .Select(p => new PostDto
                {
                    Id = p.Id,
                    CategoryId = p.CategoryId,
                    CategoryName = p.Category.Name,
                    AuthorName = p.AuthorUser.FullName,
                    Title = p.Title,
                    Slug = p.Slug,
                    Summary = p.Summary,
                    ContentMarkdown = p.ContentMarkdown,
                    ContentHtml = p.ContentHtml,
                    ThumbnailUrl = p.ThumbnailUrl,
                    Status = p.Status.ToString(),
                    PublishedAt = p.PublishedAt,
                    ViewCount = p.ViewCount,
                    Tags = p.PostTags.Select(pt => pt.Tag.Name).ToList()
                }).ToListAsync();

            return Ok(ApiResponse<PagedResponse<PostDto>>.Ok(new PagedResponse<PostDto>(items, total, pageIndex, pageSize)));
        }

        [HttpGet("{slug}")]
        public async Task<ActionResult<ApiResponse<PostDto>>> GetPostBySlug(string slug)
        {
            var p = await _context.Posts
                .Include(post => post.Category)
                .Include(post => post.AuthorUser)
                .Include(post => post.PostTags).ThenInclude(pt => pt.Tag)
                .FirstOrDefaultAsync(post => post.Slug == slug);

            if (p == null) return NotFound(ApiResponse<PostDto>.Fail("Không tìm thấy bài viết."));

            p.ViewCount++;
            await _context.SaveChangesAsync();

            var dto = new PostDto
            {
                Id = p.Id,
                CategoryId = p.CategoryId,
                CategoryName = p.Category.Name,
                AuthorName = p.AuthorUser.FullName,
                Title = p.Title,
                Slug = p.Slug,
                Summary = p.Summary,
                ContentMarkdown = p.ContentMarkdown,
                ContentHtml = p.ContentHtml,
                ThumbnailUrl = p.ThumbnailUrl,
                Status = p.Status.ToString(),
                PublishedAt = p.PublishedAt,
                ViewCount = p.ViewCount,
                Tags = p.PostTags.Select(pt => pt.Tag.Name).ToList()
            };

            return Ok(ApiResponse<PostDto>.Ok(dto));
        }

        [HttpGet("categories")]
        public async Task<ActionResult<ApiResponse<List<PostCategoryDto>>>> GetCategories()
        {
            var list = await _context.PostCategories
                .Select(c => new PostCategoryDto
                {
                    Id = c.Id,
                    Name = c.Name,
                    Slug = c.Slug,
                    Description = c.Description,
                    PostCount = c.Posts.Count(p => p.Status == PostStatus.Published)
                }).ToListAsync();

            return Ok(ApiResponse<List<PostCategoryDto>>.Ok(list));
        }

        [Authorize(Roles = "Admin,Committee,Collaborator")]
        [HttpPost]
        public async Task<ActionResult<ApiResponse<PostDto>>> CreatePost([FromBody] CreatePostRequest request)
        {
            var userIdStr = User.FindFirstValue(ClaimTypes.NameIdentifier);
            if (!Guid.TryParse(userIdStr, out var userId)) return Unauthorized();

            var isManager = User.IsInRole(AppRoles.Admin) || User.IsInRole(AppRoles.Committee);
            var initialStatus = isManager && !request.SubmitForReview ? PostStatus.Published : PostStatus.PendingReview;

            var slug = "post-" + Guid.NewGuid().ToString("N")[..8];
            var post = new Post
            {
                CategoryId = request.CategoryId,
                AuthorUserId = userId,
                Title = request.Title.Trim(),
                Slug = slug,
                Summary = request.Summary.Trim(),
                ContentMarkdown = request.ContentMarkdown,
                ContentHtml = request.ContentMarkdown, // Simplification for editor
                ThumbnailUrl = request.ThumbnailUrl,
                Status = initialStatus,
                PublishedAt = initialStatus == PostStatus.Published ? DateTime.UtcNow : null
            };

            _context.Posts.Add(post);
            await _context.SaveChangesAsync();

            return Ok(ApiResponse<PostDto>.Ok(new PostDto
            {
                Id = post.Id,
                CategoryId = post.CategoryId,
                Title = post.Title,
                Slug = post.Slug,
                Summary = post.Summary,
                Status = post.Status.ToString()
            }, "Tạo bài viết thành công."));
        }

        [Authorize(Roles = "Admin,Committee")]
        [HttpPut("{id}/status")]
        public async Task<ActionResult<ApiResponse<string>>> UpdateStatus(Guid id, [FromQuery] PostStatus status)
        {
            var post = await _context.Posts.FindAsync(id);
            if (post == null) return NotFound(ApiResponse<string>.Fail("Bài viết không tồn tại."));

            post.Status = status;
            if (status == PostStatus.Published && post.PublishedAt == null)
            {
                post.PublishedAt = DateTime.UtcNow;
            }
            await _context.SaveChangesAsync();

            return Ok(ApiResponse<string>.Ok($"Đã cập nhật trạng thái bài viết thành {status}."));
        }

        [Authorize(Roles = "Admin,Committee")]
        [HttpDelete("{id}")]
        public async Task<ActionResult<ApiResponse<string>>> DeletePost(Guid id)
        {
            var post = await _context.Posts.FindAsync(id);
            if (post == null) return NotFound(ApiResponse<string>.Fail("Bài viết không tồn tại."));

            post.Status = PostStatus.Archived;
            await _context.SaveChangesAsync();

            return Ok(ApiResponse<string>.Ok("Đã gỡ bài viết."));
        }
    }
}
