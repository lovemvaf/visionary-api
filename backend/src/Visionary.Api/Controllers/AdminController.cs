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
    [Authorize(Roles = "Admin,Committee")]
    [ApiController]
    [Route("api/[controller]")]
    public class AdminController : ControllerBase
    {
        private readonly AppDbContext _context;
        private readonly IDataAutomationService _automationService;

        public AdminController(AppDbContext context, IDataAutomationService automationService)
        {
            _context = context;
            _automationService = automationService;
        }

        [HttpGet("dashboard")]
        public async Task<ActionResult<ApiResponse<DashboardStatsDto>>> GetDashboardStats()
        {
            var totalUsers = await _context.Users.CountAsync();
            var totalMembers = await _context.MemberProfiles.CountAsync(m => m.Status == "Active");
            var pendingApps = await _context.MembershipApplications.CountAsync(a => a.Status == MembershipStatus.Pending);
            var totalEvents = await _context.Events.CountAsync();
            var totalPosts = await _context.Posts.CountAsync();
            var totalAchievements = await _context.Achievements.CountAsync(a => a.IsVerified);
            var totalOpportunities = await _context.Opportunities.CountAsync();
            var totalJobs = await _context.Jobs.CountAsync();
            var totalTechResources = await _context.TechResources.CountAsync();

            var recentLogs = await _context.AuditLogs
                .Include(l => l.User)
                .OrderByDescending(l => l.Timestamp)
                .Take(5)
                .Select(l => new RecentActivityDto
                {
                    Action = l.Action,
                    Description = $"{l.Action} trên tài nguyên {l.Resource}",
                    Timestamp = l.Timestamp,
                    UserName = l.User != null ? l.User.FullName : "Hệ thống"
                }).ToListAsync();

            var stats = new DashboardStatsDto
            {
                TotalUsers = totalUsers,
                TotalMembers = totalMembers,
                PendingApplications = pendingApps,
                TotalEvents = totalEvents,
                TotalPosts = totalPosts,
                TotalAchievements = totalAchievements,
                TotalOpportunities = totalOpportunities,
                TotalJobs = totalJobs,
                TotalTechResources = totalTechResources,
                RecentActivities = recentLogs
            };

            return Ok(ApiResponse<DashboardStatsDto>.Ok(stats));
        }

        [HttpGet("sources")]
        public async Task<ActionResult<ApiResponse<List<ContentSourceDto>>>> GetSources()
        {
            var list = await _context.ContentSources
                .Select(s => new ContentSourceDto
                {
                    Id = s.Id,
                    Name = s.Name,
                    Type = s.Type,
                    EndpointUrl = s.EndpointUrl,
                    IntervalMinutes = s.IntervalMinutes,
                    IsEnabled = s.IsEnabled,
                    LastRunAt = s.LastRunAt,
                    LastStatus = s.LastStatus
                }).ToListAsync();

            return Ok(ApiResponse<List<ContentSourceDto>>.Ok(list));
        }

        [HttpPost("sources/trigger/{id}")]
        public async Task<ActionResult<ApiResponse<string>>> TriggerSource(Guid id)
        {
            var source = await _context.ContentSources.FindAsync(id);
            if (source == null) return NotFound(ApiResponse<string>.Fail("Nguồn không tồn tại."));

            if (source.Type == "GitHubApi")
            {
                await _automationService.SyncGitHubTrendingAsync();
            }
            else if (source.Type == "HuggingFaceApi")
            {
                await _automationService.SyncHuggingFaceModelsAsync();
            }
            else if (source.Type == "RssFeed")
            {
                await _automationService.SyncTechNewsAsync();
            }

            return Ok(ApiResponse<string>.Ok($"Đã thực thi thành công việc nạp dữ liệu từ nguồn: {source.Name}"));
        }

        [HttpGet("audit-logs")]
        public async Task<ActionResult<ApiResponse<List<AuditLogDto>>>> GetAuditLogs()
        {
            var list = await _context.AuditLogs
                .Include(a => a.User)
                .OrderByDescending(a => a.Timestamp)
                .Take(50)
                .Select(a => new AuditLogDto
                {
                    Id = a.Id,
                    Action = a.Action,
                    Resource = a.Resource,
                    ResourceId = a.ResourceId,
                    UserName = a.User != null ? a.User.FullName : "System",
                    IpAddress = a.IpAddress,
                    Timestamp = a.Timestamp,
                    Details = a.DetailsJson
                }).ToListAsync();

            return Ok(ApiResponse<List<AuditLogDto>>.Ok(list));
        }
    }
}
