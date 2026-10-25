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
    public class JobsController : ControllerBase
    {
        private readonly AppDbContext _context;

        public JobsController(AppDbContext context)
        {
            _context = context;
        }

        [HttpGet]
        public async Task<ActionResult<ApiResponse<PagedResponse<JobDto>>>> GetJobs(
            [FromQuery] JobType? jobType = null,
            [FromQuery] WorkplaceType? workplaceType = null,
            [FromQuery] string? search = null,
            [FromQuery] int pageIndex = 1,
            [FromQuery] int pageSize = 12)
        {
            var query = _context.Jobs.Where(j => j.IsVerified).AsQueryable();

            if (jobType.HasValue)
            {
                query = query.Where(j => j.JobType == jobType.Value);
            }

            if (workplaceType.HasValue)
            {
                query = query.Where(j => j.WorkplaceType == workplaceType.Value);
            }

            if (!string.IsNullOrWhiteSpace(search))
            {
                var s = search.Trim().ToLower();
                query = query.Where(j => j.Title.ToLower().Contains(s) || j.Company.ToLower().Contains(s) || j.Location.ToLower().Contains(s));
            }

            var total = await query.CountAsync();
            var list = await query
                .OrderByDescending(j => j.CreatedAt)
                .Skip((pageIndex - 1) * pageSize)
                .Take(pageSize)
                .Select(j => new JobDto
                {
                    Id = j.Id,
                    Title = j.Title,
                    Company = j.Company,
                    JobType = j.JobType.ToString(),
                    WorkplaceType = j.WorkplaceType.ToString(),
                    Location = j.Location,
                    ApplyUrl = j.ApplyUrl,
                    Requirements = j.Requirements,
                    EnglishRequired = j.EnglishRequired,
                    IsVerified = j.IsVerified,
                    CreatedAt = j.CreatedAt
                }).ToListAsync();

            return Ok(ApiResponse<PagedResponse<JobDto>>.Ok(new PagedResponse<JobDto>(list, total, pageIndex, pageSize)));
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<ApiResponse<JobDto>>> GetById(Guid id)
        {
            var j = await _context.Jobs.FindAsync(id);
            if (j == null) return NotFound(ApiResponse<JobDto>.Fail("Không tìm thấy tin tuyển dụng."));

            var dto = new JobDto
            {
                Id = j.Id,
                Title = j.Title,
                Company = j.Company,
                JobType = j.JobType.ToString(),
                WorkplaceType = j.WorkplaceType.ToString(),
                Location = j.Location,
                ApplyUrl = j.ApplyUrl,
                Requirements = j.Requirements,
                EnglishRequired = j.EnglishRequired,
                IsVerified = j.IsVerified,
                CreatedAt = j.CreatedAt
            };

            return Ok(ApiResponse<JobDto>.Ok(dto));
        }

        [Authorize(Roles = "Admin,Committee")]
        [HttpPost]
        public async Task<ActionResult<ApiResponse<JobDto>>> CreateJob([FromBody] CreateJobRequest request)
        {
            var job = new Job
            {
                Title = request.Title.Trim(),
                Company = request.Company.Trim(),
                JobType = request.JobType,
                WorkplaceType = request.WorkplaceType,
                Location = request.Location.Trim(),
                ApplyUrl = request.ApplyUrl.Trim(),
                Requirements = request.Requirements.Trim(),
                EnglishRequired = request.EnglishRequired,
                IsVerified = true
            };

            _context.Jobs.Add(job);
            await _context.SaveChangesAsync();

            return Ok(ApiResponse<JobDto>.Ok(new JobDto
            {
                Id = job.Id,
                Title = job.Title,
                Company = job.Company,
                JobType = job.JobType.ToString(),
                Location = job.Location,
                ApplyUrl = job.ApplyUrl
            }, "Đăng tin tuyển dụng thành công."));
        }
    }
}
