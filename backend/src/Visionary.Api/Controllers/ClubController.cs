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
    public class ClubController : ControllerBase
    {
        private readonly AppDbContext _context;

        public ClubController(AppDbContext context)
        {
            _context = context;
        }

        [HttpGet("overview")]
        public async Task<ActionResult<ApiResponse<ClubOverviewDto>>> GetOverview()
        {
            var totalMembers = await _context.MemberProfiles.CountAsync(m => m.Status == "Active");
            var totalEvents = await _context.Events.CountAsync(e => e.Status != EventStatus.Draft);

            var departments = await _context.ClubDepartments
                .Select(d => new DepartmentDto
                {
                    Id = d.Id,
                    Name = d.Name,
                    Description = d.Description,
                    MemberCount = d.Members.Count(m => m.Status == "Active")
                }).ToListAsync();

            var currentTerm = await _context.CommitteeTerms
                .Include(t => t.Assignments)
                    .ThenInclude(a => a.User)
                .FirstOrDefaultAsync(t => t.IsCurrent);

            var committee = currentTerm?.Assignments.Select(a => new CommitteeMemberDto
            {
                UserId = a.UserId,
                FullName = a.User.FullName,
                Position = a.Position,
                AvatarUrl = a.User.AvatarUrl,
                Department = a.User.Department
            }).ToList() ?? new List<CommitteeMemberDto>();

            var overview = new ClubOverviewDto
            {
                TotalMembers = totalMembers,
                TotalEvents = totalEvents,
                Departments = departments,
                CurrentCommittee = committee
            };

            return Ok(ApiResponse<ClubOverviewDto>.Ok(overview));
        }

        [HttpGet("departments")]
        public async Task<ActionResult<ApiResponse<List<DepartmentDto>>>> GetDepartments()
        {
            var depts = await _context.ClubDepartments
                .Select(d => new DepartmentDto
                {
                    Id = d.Id,
                    Name = d.Name,
                    Description = d.Description,
                    MemberCount = d.Members.Count(m => m.Status == "Active")
                }).ToListAsync();

            return Ok(ApiResponse<List<DepartmentDto>>.Ok(depts));
        }

        [HttpGet("members")]
        public async Task<ActionResult<ApiResponse<PagedResponse<MemberDto>>>> GetMembers(
            [FromQuery] Guid? departmentId = null,
            [FromQuery] string? search = null,
            [FromQuery] int pageIndex = 1,
            [FromQuery] int pageSize = 12)
        {
            var query = _context.MemberProfiles
                .Include(m => m.User)
                .Include(m => m.Department)
                .Where(m => m.Status == "Active")
                .AsQueryable();

            if (departmentId.HasValue)
            {
                query = query.Where(m => m.DepartmentId == departmentId.Value);
            }

            if (!string.IsNullOrWhiteSpace(search))
            {
                var s = search.Trim().ToLower();
                query = query.Where(m => m.User.FullName.ToLower().Contains(s) ||
                                         (m.User.StudentId != null && m.User.StudentId.ToLower().Contains(s)) ||
                                         m.ClubRole.ToLower().Contains(s));
            }

            var total = await query.CountAsync();
            var items = await query
                .OrderBy(m => m.ClubRole)
                .ThenBy(m => m.User.FullName)
                .Skip((pageIndex - 1) * pageSize)
                .Take(pageSize)
                .Select(m => new MemberDto
                {
                    Id = m.Id,
                    UserId = m.UserId,
                    FullName = m.User.FullName,
                    Email = m.User.Email,
                    StudentId = m.User.StudentId,
                    DepartmentName = m.Department != null ? m.Department.Name : "Chung",
                    ClubRole = m.ClubRole,
                    Status = m.Status,
                    JoinedDate = m.JoinedDate,
                    EnglishLevel = m.EnglishLevel,
                    AvatarUrl = m.User.AvatarUrl
                }).ToListAsync();

            return Ok(ApiResponse<PagedResponse<MemberDto>>.Ok(new PagedResponse<MemberDto>(items, total, pageIndex, pageSize)));
        }

        [HttpGet("committee")]
        public async Task<ActionResult<ApiResponse<List<CommitteeMemberDto>>>> GetCommittee()
        {
            var term = await _context.CommitteeTerms
                .Include(t => t.Assignments)
                    .ThenInclude(a => a.User)
                .FirstOrDefaultAsync(t => t.IsCurrent);

            var members = term?.Assignments.Select(a => new CommitteeMemberDto
            {
                UserId = a.UserId,
                FullName = a.User.FullName,
                Position = a.Position,
                AvatarUrl = a.User.AvatarUrl,
                Department = a.User.Department
            }).ToList() ?? new List<CommitteeMemberDto>();

            return Ok(ApiResponse<List<CommitteeMemberDto>>.Ok(members));
        }

        [Authorize]
        [HttpPost("applications")]
        public async Task<ActionResult<ApiResponse<MembershipApplicationDto>>> ApplyMembership([FromBody] ApplyMembershipRequest request)
        {
            var userIdStr = User.FindFirstValue(ClaimTypes.NameIdentifier);
            if (!Guid.TryParse(userIdStr, out var userId)) return Unauthorized();

            var existingProfile = await _context.MemberProfiles.AnyAsync(m => m.UserId == userId && m.Status == "Active");
            if (existingProfile)
            {
                return BadRequest(ApiResponse<MembershipApplicationDto>.Fail("Bạn đã là thành viên chính thức của CLB."));
            }

            var pendingApp = await _context.MembershipApplications.AnyAsync(m => m.UserId == userId && m.Status == MembershipStatus.Pending);
            if (pendingApp)
            {
                return BadRequest(ApiResponse<MembershipApplicationDto>.Fail("Bạn đã có đơn đăng ký đang chờ xét duyệt."));
            }

            var app = new MembershipApplication
            {
                UserId = userId,
                PreferredDepartmentId = request.PreferredDepartmentId,
                SelfIntroduction = request.SelfIntroduction.Trim(),
                Motivation = request.Motivation.Trim(),
                EnglishProficiency = request.EnglishProficiency?.Trim(),
                Status = MembershipStatus.Pending
            };

            _context.MembershipApplications.Add(app);
            await _context.SaveChangesAsync();

            var user = await _context.Users.FindAsync(userId);
            var dept = request.PreferredDepartmentId.HasValue ? await _context.ClubDepartments.FindAsync(request.PreferredDepartmentId.Value) : null;

            var dto = new MembershipApplicationDto
            {
                Id = app.Id,
                UserId = app.UserId,
                ApplicantName = user?.FullName ?? "",
                ApplicantEmail = user?.Email ?? "",
                StudentId = user?.StudentId,
                PreferredDepartmentName = dept?.Name,
                SelfIntroduction = app.SelfIntroduction,
                Motivation = app.Motivation,
                EnglishProficiency = app.EnglishProficiency,
                Status = app.Status.ToString(),
                SubmittedAt = app.SubmittedAt
            };

            return Ok(ApiResponse<MembershipApplicationDto>.Ok(dto, "Nộp đơn đăng ký gia nhập CLB thành công."));
        }

        [Authorize(Roles = "Admin,Committee")]
        [HttpGet("applications")]
        public async Task<ActionResult<ApiResponse<List<MembershipApplicationDto>>>> GetApplications([FromQuery] MembershipStatus? status = null)
        {
            var query = _context.MembershipApplications
                .Include(a => a.User)
                .Include(a => a.PreferredDepartment)
                .AsQueryable();

            if (status.HasValue)
            {
                query = query.Where(a => a.Status == status.Value);
            }

            var list = await query
                .OrderByDescending(a => a.SubmittedAt)
                .Select(a => new MembershipApplicationDto
                {
                    Id = a.Id,
                    UserId = a.UserId,
                    ApplicantName = a.User.FullName,
                    ApplicantEmail = a.User.Email,
                    StudentId = a.User.StudentId,
                    PreferredDepartmentName = a.PreferredDepartment != null ? a.PreferredDepartment.Name : "Chưa chọn",
                    SelfIntroduction = a.SelfIntroduction,
                    Motivation = a.Motivation,
                    EnglishProficiency = a.EnglishProficiency,
                    Status = a.Status.ToString(),
                    ReviewNotes = a.ReviewNotes,
                    SubmittedAt = a.SubmittedAt
                }).ToListAsync();

            return Ok(ApiResponse<List<MembershipApplicationDto>>.Ok(list));
        }

        [Authorize(Roles = "Admin,Committee")]
        [HttpPut("applications/{id}/review")]
        public async Task<ActionResult<ApiResponse<string>>> ReviewApplication(Guid id, [FromBody] ReviewApplicationRequest request)
        {
            var reviewerIdStr = User.FindFirstValue(ClaimTypes.NameIdentifier);
            Guid.TryParse(reviewerIdStr, out var reviewerId);

            var app = await _context.MembershipApplications.Include(a => a.User).FirstOrDefaultAsync(a => a.Id == id);
            if (app == null) return NotFound(ApiResponse<string>.Fail("Đơn đăng ký không tồn tại."));

            if (app.Status != MembershipStatus.Pending)
            {
                return BadRequest(ApiResponse<string>.Fail("Đơn này đã được xử lý trước đó."));
            }

            app.Status = request.IsApproved ? MembershipStatus.Approved : MembershipStatus.Rejected;
            app.ReviewedByUserId = reviewerId;
            app.ReviewNotes = request.ReviewNotes?.Trim();
            app.ReviewedAt = DateTime.UtcNow;

            if (request.IsApproved)
            {
                // Create or activate MemberProfile
                var profile = await _context.MemberProfiles.FirstOrDefaultAsync(p => p.UserId == app.UserId);
                if (profile == null)
                {
                    profile = new MemberProfile
                    {
                        UserId = app.UserId,
                        DepartmentId = request.DepartmentId ?? app.PreferredDepartmentId,
                        ClubRole = string.IsNullOrWhiteSpace(request.ClubRole) ? "Thành viên" : request.ClubRole.Trim(),
                        EnglishLevel = app.EnglishProficiency,
                        JoinedDate = DateTime.UtcNow,
                        Status = "Active"
                    };
                    _context.MemberProfiles.Add(profile);
                }
                else
                {
                    profile.Status = "Active";
                    profile.DepartmentId = request.DepartmentId ?? app.PreferredDepartmentId;
                    profile.ClubRole = string.IsNullOrWhiteSpace(request.ClubRole) ? profile.ClubRole : request.ClubRole.Trim();
                }

                // Add ClubMember role
                var memberRole = await _context.Roles.FirstOrDefaultAsync(r => r.Name == AppRoles.ClubMember);
                if (memberRole != null && !await _context.UserRoles.AnyAsync(ur => ur.UserId == app.UserId && ur.RoleId == memberRole.Id))
                {
                    _context.UserRoles.Add(new UserRole { UserId = app.UserId, RoleId = memberRole.Id });
                }
            }

            await _context.SaveChangesAsync();
            return Ok(ApiResponse<string>.Ok(request.IsApproved ? "Đã phê duyệt đơn đăng ký và kết nạp thành viên mới." : "Đã từ chối đơn đăng ký."));
        }
    }
}
