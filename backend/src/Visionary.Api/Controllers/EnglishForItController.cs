using System;
using System.Collections.Generic;
using System.Linq;
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
    [Route("api/english-for-it")]
    public class EnglishForItController : ControllerBase
    {
        private readonly AppDbContext _context;

        public EnglishForItController(AppDbContext context)
        {
            _context = context;
        }

        [HttpGet]
        public async Task<ActionResult<ApiResponse<PagedResponse<LearningResourceDto>>>> GetResources(
            [FromQuery] EnglishLevel? level = null,
            [FromQuery] string? topic = null,
            [FromQuery] string? search = null,
            [FromQuery] int pageIndex = 1,
            [FromQuery] int pageSize = 12)
        {
            var query = _context.LearningResources.AsQueryable();

            if (level.HasValue)
            {
                query = query.Where(r => r.Level == level.Value);
            }

            if (!string.IsNullOrWhiteSpace(topic))
            {
                var t = topic.Trim().ToLower();
                query = query.Where(r => r.Topic.ToLower().Contains(t));
            }

            if (!string.IsNullOrWhiteSpace(search))
            {
                var s = search.Trim().ToLower();
                query = query.Where(r => r.Title.ToLower().Contains(s) || r.Summary.ToLower().Contains(s) || r.Content.ToLower().Contains(s));
            }

            var total = await query.CountAsync();
            var list = await query
                .OrderByDescending(r => r.CreatedAt)
                .Skip((pageIndex - 1) * pageSize)
                .Take(pageSize)
                .Select(r => new LearningResourceDto
                {
                    Id = r.Id,
                    Title = r.Title,
                    Slug = r.Slug,
                    Level = r.Level.ToString(),
                    Topic = r.Topic,
                    Summary = r.Summary,
                    Content = r.Content,
                    GlossaryJson = r.GlossaryJson,
                    ReferenceUrl = r.ReferenceUrl,
                    ViewCount = r.ViewCount,
                    CreatedAt = r.CreatedAt
                }).ToListAsync();

            return Ok(ApiResponse<PagedResponse<LearningResourceDto>>.Ok(new PagedResponse<LearningResourceDto>(list, total, pageIndex, pageSize)));
        }

        [HttpGet("{slug}")]
        public async Task<ActionResult<ApiResponse<LearningResourceDto>>> GetBySlug(string slug)
        {
            var r = await _context.LearningResources.FirstOrDefaultAsync(x => x.Slug == slug);
            if (r == null) return NotFound(ApiResponse<LearningResourceDto>.Fail("Không tìm thấy bài học English for IT."));

            r.ViewCount++;
            await _context.SaveChangesAsync();

            var dto = new LearningResourceDto
            {
                Id = r.Id,
                Title = r.Title,
                Slug = r.Slug,
                Level = r.Level.ToString(),
                Topic = r.Topic,
                Summary = r.Summary,
                Content = r.Content,
                GlossaryJson = r.GlossaryJson,
                ReferenceUrl = r.ReferenceUrl,
                ViewCount = r.ViewCount,
                CreatedAt = r.CreatedAt
            };

            return Ok(ApiResponse<LearningResourceDto>.Ok(dto));
        }

        [Authorize(Roles = "Admin,Committee,Collaborator")]
        [HttpPost]
        public async Task<ActionResult<ApiResponse<LearningResourceDto>>> CreateResource([FromBody] CreateLearningResourceRequest request)
        {
            var slug = "eng-" + Guid.NewGuid().ToString("N")[..8];
            var resource = new LearningResource
            {
                Title = request.Title.Trim(),
                Slug = slug,
                Level = request.Level,
                Topic = request.Topic.Trim(),
                Summary = request.Summary.Trim(),
                Content = request.Content.Trim(),
                GlossaryJson = request.GlossaryJson,
                ReferenceUrl = request.ReferenceUrl
            };

            _context.LearningResources.Add(resource);
            await _context.SaveChangesAsync();

            return Ok(ApiResponse<LearningResourceDto>.Ok(new LearningResourceDto
            {
                Id = resource.Id,
                Title = resource.Title,
                Slug = resource.Slug,
                Level = resource.Level.ToString(),
                Topic = resource.Topic,
                Summary = resource.Summary,
                Content = resource.Content
            }, "Thêm bài học English for IT thành công."));
        }
    }
}
