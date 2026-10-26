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
    public class EventsController : ControllerBase
    {
        private readonly AppDbContext _context;

        public EventsController(AppDbContext context)
        {
            _context = context;
        }

        [HttpGet]
        public async Task<ActionResult<ApiResponse<PagedResponse<EventDto>>>> GetEvents(
            [FromQuery] EventStatus? status = null,
            [FromQuery] string? search = null,
            [FromQuery] int pageIndex = 1,
            [FromQuery] int pageSize = 10)
        {
            if (pageIndex < 1) pageIndex = 1;
            if (pageSize < 1) pageSize = 10;
            if (pageSize > 100) pageSize = 100;

            var currentUserIdStr = User.FindFirstValue(ClaimTypes.NameIdentifier);
            Guid.TryParse(currentUserIdStr, out var currentUserId);

            var query = _context.Events
                .Include(e => e.Registrations)
                .Include(e => e.Attendances)
                .AsQueryable();

            if (status.HasValue)
            {
                query = query.Where(e => e.Status == status.Value);
            }
            else
            {
                // Default: show published, ongoing, completed
                query = query.Where(e => e.Status != EventStatus.Draft);
            }

            if (!string.IsNullOrWhiteSpace(search))
            {
                var s = search.Trim().ToLower();
                query = query.Where(e => e.Title.ToLower().Contains(s) || e.Description.ToLower().Contains(s) || e.Location.ToLower().Contains(s));
            }

            var total = await query.CountAsync();
            var list = await query
                .OrderByDescending(e => e.StartTime)
                .Skip((pageIndex - 1) * pageSize)
                .Take(pageSize)
                .Select(e => new EventDto
                {
                    Id = e.Id,
                    Title = e.Title,
                    Slug = e.Slug,
                    Description = e.Description,
                    Location = e.Location,
                    StartTime = e.StartTime,
                    EndTime = e.EndTime,
                    RegistrationDeadline = e.RegistrationDeadline,
                    MaxCapacity = e.MaxCapacity,
                    CurrentRegistrationsCount = e.Registrations.Count(r => r.Status == RegistrationStatus.Registered),
                    BannerUrl = e.BannerUrl,
                    Status = e.Status.ToString(),
                    IsRegisteredByCurrentUser = currentUserId != Guid.Empty && e.Registrations.Any(r => r.UserId == currentUserId && r.Status == RegistrationStatus.Registered),
                    IsCheckedInByCurrentUser = currentUserId != Guid.Empty && e.Attendances.Any(a => a.UserId == currentUserId),
                    QrCheckInCode = e.QrCheckInCode
                }).ToListAsync();

            return Ok(ApiResponse<PagedResponse<EventDto>>.Ok(new PagedResponse<EventDto>(list, total, pageIndex, pageSize)));
        }

        [HttpGet("{slug}")]
        public async Task<ActionResult<ApiResponse<EventDto>>> GetEventBySlug(string slug)
        {
            var currentUserIdStr = User.FindFirstValue(ClaimTypes.NameIdentifier);
            Guid.TryParse(currentUserIdStr, out var currentUserId);

            var e = await _context.Events
                .Include(ev => ev.Registrations)
                .Include(ev => ev.Attendances)
                .FirstOrDefaultAsync(ev => ev.Slug == slug);

            if (e == null) return NotFound(ApiResponse<EventDto>.Fail("Không tìm thấy sự kiện."));

            var dto = new EventDto
            {
                Id = e.Id,
                Title = e.Title,
                Slug = e.Slug,
                Description = e.Description,
                Location = e.Location,
                StartTime = e.StartTime,
                EndTime = e.EndTime,
                RegistrationDeadline = e.RegistrationDeadline,
                MaxCapacity = e.MaxCapacity,
                CurrentRegistrationsCount = e.Registrations.Count(r => r.Status == RegistrationStatus.Registered),
                BannerUrl = e.BannerUrl,
                Status = e.Status.ToString(),
                IsRegisteredByCurrentUser = currentUserId != Guid.Empty && e.Registrations.Any(r => r.UserId == currentUserId && r.Status == RegistrationStatus.Registered),
                IsCheckedInByCurrentUser = currentUserId != Guid.Empty && e.Attendances.Any(a => a.UserId == currentUserId),
                QrCheckInCode = e.QrCheckInCode
            };

            return Ok(ApiResponse<EventDto>.Ok(dto));
        }

        [Authorize(Roles = "Admin,Committee")]
        [HttpPost]
        public async Task<ActionResult<ApiResponse<EventDto>>> CreateEvent([FromBody] CreateEventRequest request)
        {
            var userIdStr = User.FindFirstValue(ClaimTypes.NameIdentifier);
            Guid.TryParse(userIdStr, out var userId);

            var slug = "event-" + Guid.NewGuid().ToString("N")[..8];
            var ev = new Event
            {
                Title = request.Title.Trim(),
                Slug = slug,
                Description = request.Description.Trim(),
                Location = request.Location.Trim(),
                StartTime = request.StartTime,
                EndTime = request.EndTime,
                RegistrationDeadline = request.RegistrationDeadline,
                MaxCapacity = request.MaxCapacity > 0 ? request.MaxCapacity : 100,
                BannerUrl = request.BannerUrl,
                Status = EventStatus.Published,
                CreatedByUserId = userId,
                QrCheckInCode = "VIS-QR-" + Guid.NewGuid().ToString("N")[..8].ToUpper()
            };

            _context.Events.Add(ev);
            await _context.SaveChangesAsync();

            return Ok(ApiResponse<EventDto>.Ok(new EventDto
            {
                Id = ev.Id,
                Title = ev.Title,
                Slug = ev.Slug,
                Description = ev.Description,
                Location = ev.Location,
                StartTime = ev.StartTime,
                EndTime = ev.EndTime,
                RegistrationDeadline = ev.RegistrationDeadline,
                MaxCapacity = ev.MaxCapacity,
                Status = ev.Status.ToString(),
                QrCheckInCode = ev.QrCheckInCode
            }, "Tạo sự kiện mới thành công."));
        }

        [Authorize(Roles = "Admin,Committee")]
        [HttpPut("{id}")]
        public async Task<ActionResult<ApiResponse<string>>> UpdateEvent(Guid id, [FromBody] UpdateEventRequest request)
        {
            var ev = await _context.Events.FindAsync(id);
            if (ev == null) return NotFound(ApiResponse<string>.Fail("Sự kiện không tồn tại."));

            ev.Title = request.Title.Trim();
            ev.Description = request.Description.Trim();
            ev.Location = request.Location.Trim();
            ev.StartTime = request.StartTime;
            ev.EndTime = request.EndTime;
            ev.RegistrationDeadline = request.RegistrationDeadline;
            ev.MaxCapacity = request.MaxCapacity;
            ev.BannerUrl = request.BannerUrl;
            ev.Status = request.Status;
            ev.UpdatedAt = DateTime.UtcNow;

            await _context.SaveChangesAsync();
            return Ok(ApiResponse<string>.Ok("Cập nhật sự kiện thành công."));
        }

        [Authorize(Roles = "Admin,Committee")]
        [HttpDelete("{id}")]
        public async Task<ActionResult<ApiResponse<string>>> DeleteEvent(Guid id)
        {
            var ev = await _context.Events.FindAsync(id);
            if (ev == null) return NotFound(ApiResponse<string>.Fail("Sự kiện không tồn tại."));

            ev.Status = EventStatus.Cancelled;
            await _context.SaveChangesAsync();

            return Ok(ApiResponse<string>.Ok("Đã hủy sự kiện."));
        }

        [Authorize]
        [HttpPost("{id}/register")]
        public async Task<ActionResult<ApiResponse<string>>> RegisterForEvent(Guid id)
        {
            var userIdStr = User.FindFirstValue(ClaimTypes.NameIdentifier);
            if (!Guid.TryParse(userIdStr, out var userId)) return Unauthorized();

            var ev = await _context.Events
                .Include(e => e.Registrations)
                .FirstOrDefaultAsync(e => e.Id == id);

            if (ev == null) return NotFound(ApiResponse<string>.Fail("Sự kiện không tồn tại."));

            if (ev.Status != EventStatus.Published && ev.Status != EventStatus.Ongoing)
            {
                return BadRequest(ApiResponse<string>.Fail("Sự kiện hiện không mở đăng ký."));
            }

            if (DateTime.UtcNow > ev.RegistrationDeadline)
            {
                return BadRequest(ApiResponse<string>.Fail("Đã hết hạn đăng ký tham gia sự kiện."));
            }

            var existingReg = ev.Registrations.FirstOrDefault(r => r.UserId == userId);
            if (existingReg != null)
            {
                if (existingReg.Status == RegistrationStatus.Registered)
                {
                    return BadRequest(ApiResponse<string>.Fail("Bạn đã đăng ký sự kiện này rồi."));
                }
                existingReg.Status = RegistrationStatus.Registered;
                existingReg.RegisteredAt = DateTime.UtcNow;
            }
            else
            {
                var activeCount = ev.Registrations.Count(r => r.Status == RegistrationStatus.Registered);
                var reg = new EventRegistration
                {
                    EventId = id,
                    UserId = userId,
                    RegisteredAt = DateTime.UtcNow,
                    Status = activeCount >= ev.MaxCapacity ? RegistrationStatus.Waitlist : RegistrationStatus.Registered
                };
                _context.EventRegistrations.Add(reg);
            }

            await _context.SaveChangesAsync();
            return Ok(ApiResponse<string>.Ok("Đăng ký tham gia sự kiện thành công!"));
        }

        [Authorize]
        [HttpPost("{id}/cancel")]
        public async Task<ActionResult<ApiResponse<string>>> CancelRegistration(Guid id)
        {
            var userIdStr = User.FindFirstValue(ClaimTypes.NameIdentifier);
            if (!Guid.TryParse(userIdStr, out var userId)) return Unauthorized();

            var reg = await _context.EventRegistrations.FirstOrDefaultAsync(r => r.EventId == id && r.UserId == userId);
            if (reg == null || reg.Status == RegistrationStatus.Cancelled)
            {
                return BadRequest(ApiResponse<string>.Fail("Bạn chưa đăng ký sự kiện này."));
            }

            reg.Status = RegistrationStatus.Cancelled;
            await _context.SaveChangesAsync();

            return Ok(ApiResponse<string>.Ok("Hủy đăng ký thành công."));
        }

        [Authorize(Roles = "Admin,Committee")]
        [HttpGet("{id}/registrations")]
        public async Task<ActionResult<ApiResponse<List<EventRegistrationDto>>>> GetRegistrations(Guid id)
        {
            var list = await _context.EventRegistrations
                .Include(r => r.User)
                .Where(r => r.EventId == id)
                .Select(r => new EventRegistrationDto
                {
                    Id = r.Id,
                    EventId = r.EventId,
                    UserId = r.UserId,
                    FullName = r.User.FullName,
                    Email = r.User.Email,
                    StudentId = r.User.StudentId,
                    RegisteredAt = r.RegisteredAt,
                    Status = r.Status.ToString(),
                    IsAttended = _context.EventAttendances.Any(a => a.EventId == id && a.UserId == r.UserId),
                    CheckInTime = _context.EventAttendances
                        .Where(a => a.EventId == id && a.UserId == r.UserId)
                        .Select(a => (DateTime?)a.CheckInTime)
                        .FirstOrDefault()
                }).ToListAsync();

            return Ok(ApiResponse<List<EventRegistrationDto>>.Ok(list));
        }

        [Authorize(Roles = "Admin,Committee")]
        [HttpPost("{id}/attendance")]
        public async Task<ActionResult<ApiResponse<string>>> CheckIn(Guid id, [FromBody] CheckInRequest request)
        {
            var reviewerIdStr = User.FindFirstValue(ClaimTypes.NameIdentifier);
            Guid.TryParse(reviewerIdStr, out var reviewerId);

            var ev = await _context.Events.FindAsync(id);
            if (ev == null) return NotFound(ApiResponse<string>.Fail("Sự kiện không tồn tại."));

            var user = await _context.Users.FindAsync(request.UserId);
            if (user == null) return NotFound(ApiResponse<string>.Fail("Sinh viên không tồn tại."));

            var existingAttendance = await _context.EventAttendances
                .FirstOrDefaultAsync(a => a.EventId == id && a.UserId == request.UserId);

            if (existingAttendance != null)
            {
                return BadRequest(ApiResponse<string>.Fail("Sinh viên này đã được điểm danh trước đó."));
            }

            var attendance = new EventAttendance
            {
                EventId = id,
                UserId = request.UserId,
                CheckInTime = DateTime.UtcNow,
                Method = request.Method,
                VerifiedByUserId = reviewerId
            };

            _context.EventAttendances.Add(attendance);
            await _context.SaveChangesAsync();

            return Ok(ApiResponse<string>.Ok($"Điểm danh thành công cho sinh viên {user.FullName}."));
        }

        [Authorize]
        [HttpGet("my-events")]
        public async Task<ActionResult<ApiResponse<List<EventDto>>>> GetMyEvents()
        {
            var userIdStr = User.FindFirstValue(ClaimTypes.NameIdentifier);
            if (!Guid.TryParse(userIdStr, out var userId)) return Unauthorized();

            var events = await _context.EventRegistrations
                .Include(r => r.Event)
                    .ThenInclude(e => e.Registrations)
                .Include(r => r.Event)
                    .ThenInclude(e => e.Attendances)
                .Where(r => r.UserId == userId && r.Status == RegistrationStatus.Registered)
                .Select(r => new EventDto
                {
                    Id = r.Event.Id,
                    Title = r.Event.Title,
                    Slug = r.Event.Slug,
                    Description = r.Event.Description,
                    Location = r.Event.Location,
                    StartTime = r.Event.StartTime,
                    EndTime = r.Event.EndTime,
                    RegistrationDeadline = r.Event.RegistrationDeadline,
                    MaxCapacity = r.Event.MaxCapacity,
                    CurrentRegistrationsCount = r.Event.Registrations.Count(reg => reg.Status == RegistrationStatus.Registered),
                    BannerUrl = r.Event.BannerUrl,
                    Status = r.Event.Status.ToString(),
                    IsRegisteredByCurrentUser = true,
                    IsCheckedInByCurrentUser = r.Event.Attendances.Any(a => a.UserId == userId),
                    QrCheckInCode = r.Event.QrCheckInCode
                }).ToListAsync();

            return Ok(ApiResponse<List<EventDto>>.Ok(events));
        }
    }
}
