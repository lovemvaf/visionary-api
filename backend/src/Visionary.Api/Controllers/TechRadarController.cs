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
using Visionary.Core.Interfaces;
using Visionary.Infrastructure.Data;

namespace Visionary.Api.Controllers
{
    [ApiController]
    [Route("api/tech-radar")]
    public class TechRadarController : ControllerBase
    {
        private readonly AppDbContext _context;
        private readonly IDataAutomationService _automationService;

        public TechRadarController(AppDbContext context, IDataAutomationService automationService)
        {
            _context = context;
            _automationService = automationService;
        }

        [HttpGet]
        public async Task<ActionResult<ApiResponse<PagedResponse<TechResourceDto>>>> GetResources(
            [FromQuery] TechSourceType? sourceType = null,
            [FromQuery] string? search = null,
            [FromQuery] int pageIndex = 1,
            [FromQuery] int pageSize = 12)
        {
            var query = _context.TechResources.AsQueryable();

            if (sourceType.HasValue)
            {
                query = query.Where(r => r.SourceType == sourceType.Value);
            }

            if (!string.IsNullOrWhiteSpace(search))
            {
                var s = search.Trim().ToLower();
                query = query.Where(r => r.Name.ToLower().Contains(s) || r.Description.ToLower().Contains(s) || (r.PrimaryLanguage != null && r.PrimaryLanguage.ToLower().Contains(s)));
            }

            var total = await query.CountAsync();
            var list = await query
                .OrderByDescending(r => r.LastCheckedAt)
                .Skip((pageIndex - 1) * pageSize)
                .Take(pageSize)
                .Select(r => new TechResourceDto
                {
                    Id = r.Id,
                    Name = r.Name,
                    SourceType = r.SourceType.ToString(),
                    ExternalId = r.ExternalId,
                    OfficialUrl = r.OfficialUrl,
                    Description = r.Description,
                    PrimaryLanguage = r.PrimaryLanguage,
                    License = r.License,
                    MetricsJson = r.MetricsJson,
                    LearningSuitability = r.LearningSuitability,
                    LastCheckedAt = r.LastCheckedAt,
                    IsVerified = r.IsVerified
                }).ToListAsync();

            return Ok(ApiResponse<PagedResponse<TechResourceDto>>.Ok(new PagedResponse<TechResourceDto>(list, total, pageIndex, pageSize)));
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<ApiResponse<TechResourceDto>>> GetById(Guid id)
        {
            var r = await _context.TechResources.FindAsync(id);
            if (r == null) return NotFound(ApiResponse<TechResourceDto>.Fail("Không tìm thấy tài nguyên công nghệ."));

            var dto = new TechResourceDto
            {
                Id = r.Id,
                Name = r.Name,
                SourceType = r.SourceType.ToString(),
                ExternalId = r.ExternalId,
                OfficialUrl = r.OfficialUrl,
                Description = r.Description,
                PrimaryLanguage = r.PrimaryLanguage,
                License = r.License,
                MetricsJson = r.MetricsJson,
                LearningSuitability = r.LearningSuitability,
                LastCheckedAt = r.LastCheckedAt,
                IsVerified = r.IsVerified
            };

            return Ok(ApiResponse<TechResourceDto>.Ok(dto));
        }

        [Authorize(Roles = "Admin,Committee")]
        [HttpPost("sync")]
        public async Task<ActionResult<ApiResponse<string>>> SyncResources([FromBody] SyncTechResourcesRequest request)
        {
            if (request.Source == "GitHub" || request.Source == "All")
            {
                await _automationService.SyncGitHubTrendingAsync();
            }
            if (request.Source == "HuggingFace" || request.Source == "All")
            {
                await _automationService.SyncHuggingFaceModelsAsync();
            }

            return Ok(ApiResponse<string>.Ok("Đã kích hoạt đồng bộ dữ liệu công nghệ thành công."));
        }
    }
}
