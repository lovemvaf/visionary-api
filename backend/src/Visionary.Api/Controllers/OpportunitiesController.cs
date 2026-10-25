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
    [Route("api/[controller]")]
    public class OpportunitiesController : ControllerBase
    {
        private readonly AppDbContext _context;

        public OpportunitiesController(AppDbContext context)
        {
            _context = context;
        }

        [HttpGet]
        public async Task<ActionResult<ApiResponse<PagedResponse<OpportunityDto>>>> GetOpportunities(
            [FromQuery] OpportunityCategory? category = null,
            [FromQuery] string? scope = null,
            [FromQuery] string? search = null,
            [FromQuery] int pageIndex = 1,
            [FromQuery] int pageSize = 12)
        {
            var query = _context.Opportunities.AsQueryable();

            if (category.HasValue)
            {
                query = query.Where(o => o.Category == category.Value);
            }

            if (!string.IsNullOrWhiteSpace(scope))
            {
                query = query.Where(o => o.Scope.ToLower() == scope.Trim().ToLower());
            }

            if (!string.IsNullOrWhiteSpace(search))
            {
                var s = search.Trim().ToLower();
                query = query.Where(o => o.Title.ToLower().Contains(s) || o.Organizer.ToLower().Contains(s) || o.Eligibility.ToLower().Contains(s));
            }

            var total = await query.CountAsync();
            var list = await query
                .OrderByDescending(o => o.CreatedAt)
                .Skip((pageIndex - 1) * pageSize)
                .Take(pageSize)
                .Select(o => new OpportunityDto
                {
                    Id = o.Id,
                    Title = o.Title,
                    Organizer = o.Organizer,
                    Category = o.Category.ToString(),
                    Scope = o.Scope,
                    Format = o.Format,
                    OfficialUrl = o.OfficialUrl,
                    Eligibility = o.Eligibility,
                    RegistrationDeadline = o.RegistrationDeadline,
                    Status = o.Status.ToString(),
                    VerifiedAt = o.VerifiedAt,
                    VerifiedSource = o.VerifiedSource
                }).ToListAsync();

            return Ok(ApiResponse<PagedResponse<OpportunityDto>>.Ok(new PagedResponse<OpportunityDto>(list, total, pageIndex, pageSize)));
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<ApiResponse<OpportunityDto>>> GetById(Guid id)
        {
            var o = await _context.Opportunities.FindAsync(id);
            if (o == null) return NotFound(ApiResponse<OpportunityDto>.Fail("Không tìm thấy cơ hội."));

            var dto = new OpportunityDto
            {
                Id = o.Id,
                Title = o.Title,
                Organizer = o.Organizer,
                Category = o.Category.ToString(),
                Scope = o.Scope,
                Format = o.Format,
                OfficialUrl = o.OfficialUrl,
                Eligibility = o.Eligibility,
                RegistrationDeadline = o.RegistrationDeadline,
                Status = o.Status.ToString(),
                VerifiedAt = o.VerifiedAt,
                VerifiedSource = o.VerifiedSource
            };

            return Ok(ApiResponse<OpportunityDto>.Ok(dto));
        }

        [Authorize(Roles = "Admin,Committee")]
        [HttpPost]
        public async Task<ActionResult<ApiResponse<OpportunityDto>>> CreateOpportunity([FromBody] CreateOpportunityRequest request)
        {
            var opp = new Opportunity
            {
                Title = request.Title.Trim(),
                Organizer = request.Organizer.Trim(),
                Category = request.Category,
                Scope = request.Scope.Trim(),
                Format = request.Format.Trim(),
                OfficialUrl = request.OfficialUrl.Trim(),
                Eligibility = request.Eligibility.Trim(),
                RegistrationDeadline = request.RegistrationDeadline,
                Status = request.Status,
                VerifiedAt = DateTime.UtcNow,
                VerifiedSource = "VISIONARY Verified"
            };

            _context.Opportunities.Add(opp);
            await _context.SaveChangesAsync();

            return Ok(ApiResponse<OpportunityDto>.Ok(new OpportunityDto
            {
                Id = opp.Id,
                Title = opp.Title,
                Organizer = opp.Organizer,
                Category = opp.Category.ToString(),
                Scope = opp.Scope,
                OfficialUrl = opp.OfficialUrl,
                Status = opp.Status.ToString()
            }, "Thêm cơ hội thành công."));
        }
    }
}
