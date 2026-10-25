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
using Visionary.Infrastructure.Data;

namespace Visionary.Api.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class AchievementsController : ControllerBase
    {
        private readonly AppDbContext _context;

        public AchievementsController(AppDbContext context)
        {
            _context = context;
        }

        [HttpGet]
        public async Task<ActionResult<ApiResponse<List<AchievementDto>>>> GetAchievements([FromQuery] Guid? categoryId = null)
        {
            var query = _context.Achievements
                .Include(a => a.Category)
                .Include(a => a.RecipientUser)
                .Where(a => a.IsVerified)
                .AsQueryable();

            if (categoryId.HasValue)
            {
                query = query.Where(a => a.CategoryId == categoryId.Value);
            }

            var list = await query
                .OrderByDescending(a => a.AwardedDate)
                .Select(a => new AchievementDto
                {
                    Id = a.Id,
                    CategoryId = a.CategoryId,
                    CategoryName = a.Category.Name,
                    RecipientUserId = a.RecipientUserId,
                    RecipientName = a.RecipientUser.FullName,
                    StudentId = a.RecipientUser.StudentId,
                    Department = a.RecipientUser.Department,
                    Title = a.Title,
                    Description = a.Description,
                    AwardedDate = a.AwardedDate,
                    EvidenceUrl = a.EvidenceUrl,
                    IsVerified = a.IsVerified
                }).ToListAsync();

            return Ok(ApiResponse<List<AchievementDto>>.Ok(list));
        }

        [Authorize]
        [HttpPost("nominate")]
        public async Task<ActionResult<ApiResponse<string>>> NominateAchievement([FromBody] NominateAchievementRequest request)
        {
            var achievement = new Achievement
            {
                CategoryId = request.CategoryId,
                RecipientUserId = request.RecipientUserId,
                Title = request.Title.Trim(),
                Description = request.Description.Trim(),
                AwardedDate = request.AwardedDate,
                EvidenceUrl = request.EvidenceUrl?.Trim(),
                IsVerified = false
            };

            _context.Achievements.Add(achievement);
            await _context.SaveChangesAsync();

            return Ok(ApiResponse<string>.Ok("Đề xuất thành tích thành công. Ban phụ trách sẽ tiến hành xác minh minh chứng."));
        }

        [Authorize(Roles = "Admin,Supervisor,Committee")]
        [HttpPut("{id}/verify")]
        public async Task<ActionResult<ApiResponse<string>>> VerifyAchievement(Guid id, [FromBody] VerifyAchievementRequest request)
        {
            var reviewerIdStr = User.FindFirstValue(ClaimTypes.NameIdentifier);
            Guid.TryParse(reviewerIdStr, out var reviewerId);

            var a = await _context.Achievements.FindAsync(id);
            if (a == null) return NotFound(ApiResponse<string>.Fail("Không tìm thấy thành tích."));

            a.IsVerified = request.IsVerified;
            a.VerifiedByUserId = reviewerId;
            await _context.SaveChangesAsync();

            return Ok(ApiResponse<string>.Ok(request.IsVerified ? "Đã xác minh và công bố vinh danh thành tích." : "Đã từ chối vinh danh thành tích."));
        }
    }
}
