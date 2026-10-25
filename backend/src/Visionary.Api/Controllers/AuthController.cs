using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Claims;
using System.Threading.Tasks;
using Google.Apis.Auth;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Visionary.Core.Common;
using Visionary.Core.DTOs;
using Visionary.Core.Entities;
using Visionary.Core.Enums;
using Visionary.Core.Interfaces;
using Visionary.Infrastructure.Data;

namespace Visionary.Api.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class AuthController : ControllerBase
    {
        private readonly AppDbContext _context;
        private readonly IJwtService _jwtService;
        private readonly IPasswordHasher _passwordHasher;
        private readonly IConfiguration _configuration;
        private readonly ILogger<AuthController> _logger;

        public AuthController(
            AppDbContext context,
            IJwtService jwtService,
            IPasswordHasher passwordHasher,
            IConfiguration configuration,
            ILogger<AuthController> logger)
        {
            _context = context;
            _jwtService = jwtService;
            _passwordHasher = passwordHasher;
            _configuration = configuration;
            _logger = logger;
        }

        [HttpPost("register")]
        public async Task<ActionResult<ApiResponse<AuthResponse>>> Register([FromBody] RegisterRequest request)
        {
            if (string.IsNullOrWhiteSpace(request.Email) || string.IsNullOrWhiteSpace(request.Password))
            {
                return BadRequest(ApiResponse<AuthResponse>.Fail("Email và mật khẩu không được để trống."));
            }

            var normalizedEmail = request.Email.Trim().ToLowerInvariant();
            if (await _context.Users.AnyAsync(u => u.Email.ToLower() == normalizedEmail))
            {
                return BadRequest(ApiResponse<AuthResponse>.Fail("Email đã được sử dụng bởi tài khoản khác."));
            }

            var studentRole = await _context.Roles.FirstOrDefaultAsync(r => r.Name == AppRoles.Student);
            if (studentRole == null)
            {
                studentRole = new Role { Name = AppRoles.Student, Description = "Sinh viên DNTU" };
                _context.Roles.Add(studentRole);
                await _context.SaveChangesAsync();
            }

            var user = new User
            {
                Email = normalizedEmail,
                FullName = request.FullName.Trim(),
                PasswordHash = _passwordHasher.HashPassword(request.Password),
                StudentId = request.StudentId?.Trim(),
                Department = request.Department?.Trim(),
                IsActive = true,
                EmailConfirmed = false
            };

            _context.Users.Add(user);
            await _context.SaveChangesAsync();

            _context.UserRoles.Add(new UserRole
            {
                UserId = user.Id,
                RoleId = studentRole.Id
            });

            _context.AuditLogs.Add(new AuditLog
            {
                UserId = user.Id,
                Action = "REGISTER",
                Resource = "User",
                ResourceId = user.Id.ToString(),
                IpAddress = HttpContext.Connection.RemoteIpAddress?.ToString(),
                DetailsJson = $"{{\"email\":\"{normalizedEmail}\"}}"
            });

            await _context.SaveChangesAsync();

            var roles = new List<string> { AppRoles.Student };
            var token = _jwtService.GenerateToken(user, roles);

            var profile = new UserProfileDto
            {
                Id = user.Id,
                Email = user.Email,
                FullName = user.FullName,
                StudentId = user.StudentId,
                Department = user.Department,
                Roles = roles,
                IsMember = false
            };

            return Ok(ApiResponse<AuthResponse>.Ok(new AuthResponse
            {
                Token = token,
                ExpiresAt = DateTime.UtcNow.AddHours(24),
                User = profile
            }, "Đăng ký tài khoản thành công."));
        }

        [HttpPost("login")]
        public async Task<ActionResult<ApiResponse<AuthResponse>>> Login([FromBody] LoginRequest request)
        {
            if (string.IsNullOrWhiteSpace(request.Email) || string.IsNullOrWhiteSpace(request.Password))
            {
                return BadRequest(ApiResponse<AuthResponse>.Fail("Vui lòng nhập email và mật khẩu."));
            }

            var normalizedEmail = request.Email.Trim().ToLowerInvariant();
            var user = await _context.Users
                .Include(u => u.UserRoles)
                    .ThenInclude(ur => ur.Role)
                .Include(u => u.MemberProfile)
                .FirstOrDefaultAsync(u => u.Email.ToLower() == normalizedEmail);

            if (user == null || string.IsNullOrEmpty(user.PasswordHash) ||
                !_passwordHasher.VerifyPassword(request.Password, user.PasswordHash))
            {
                return Unauthorized(ApiResponse<AuthResponse>.Fail("Email hoặc mật khẩu không chính xác."));
            }

            if (!user.IsActive)
            {
                return Unauthorized(ApiResponse<AuthResponse>.Fail("Tài khoản của bạn đã bị vô hiệu hóa."));
            }

            var roles = user.UserRoles.Select(ur => ur.Role.Name).ToList();
            if (!roles.Any()) roles.Add(AppRoles.Student);

            var token = _jwtService.GenerateToken(user, roles);

            _context.AuditLogs.Add(new AuditLog
            {
                UserId = user.Id,
                Action = "LOGIN",
                Resource = "User",
                ResourceId = user.Id.ToString(),
                IpAddress = HttpContext.Connection.RemoteIpAddress?.ToString()
            });
            await _context.SaveChangesAsync();

            var profile = new UserProfileDto
            {
                Id = user.Id,
                Email = user.Email,
                FullName = user.FullName,
                StudentId = user.StudentId,
                Department = user.Department,
                AvatarUrl = user.AvatarUrl,
                Bio = user.Bio,
                Roles = roles,
                IsMember = user.MemberProfile != null,
                ClubRole = user.MemberProfile?.ClubRole
            };

            return Ok(ApiResponse<AuthResponse>.Ok(new AuthResponse
            {
                Token = token,
                ExpiresAt = DateTime.UtcNow.AddHours(24),
                User = profile
            }, "Đăng nhập thành công."));
        }

        [HttpPost("google")]
        public async Task<ActionResult<ApiResponse<AuthResponse>>> GoogleLogin([FromBody] GoogleLoginRequest request)
        {
            if (string.IsNullOrWhiteSpace(request.IdToken))
            {
                return BadRequest(ApiResponse<AuthResponse>.Fail("Google IdToken không được để trống."));
            }

            string email;
            string name;
            string? picture = null;
            string? googleSubject = null;

            try
            {
                // Verify Google IdToken with official Google Auth
                var googleClientId = _configuration["Authentication:Google:ClientId"];
                GoogleJsonWebSignature.Payload payload;

                if (!string.IsNullOrEmpty(googleClientId))
                {
                    var settings = new GoogleJsonWebSignature.ValidationSettings
                    {
                        Audience = new[] { googleClientId }
                    };
                    payload = await GoogleJsonWebSignature.ValidateAsync(request.IdToken, settings);
                }
                else
                {
                    // Fallback for development without configured Google Client ID
                    payload = await GoogleJsonWebSignature.ValidateAsync(request.IdToken);
                }

                email = payload.Email.ToLowerInvariant();
                name = payload.Name ?? payload.Email;
                picture = payload.Picture;
                googleSubject = payload.Subject;
            }
            catch (Exception ex)
            {
                _logger.LogWarning(ex, "Google token validation failed: {Msg}", ex.Message);
                return Unauthorized(ApiResponse<AuthResponse>.Fail("Mã xác thực Google không hợp lệ hoặc đã hết hạn."));
            }

            var user = await _context.Users
                .Include(u => u.UserRoles)
                    .ThenInclude(ur => ur.Role)
                .Include(u => u.MemberProfile)
                .FirstOrDefaultAsync(u => u.Email.ToLower() == email);

            if (user == null)
            {
                var studentRole = await _context.Roles.FirstOrDefaultAsync(r => r.Name == AppRoles.Student);
                if (studentRole == null)
                {
                    studentRole = new Role { Name = AppRoles.Student, Description = "Sinh viên DNTU" };
                    _context.Roles.Add(studentRole);
                    await _context.SaveChangesAsync();
                }

                user = new User
                {
                    Email = email,
                    FullName = name,
                    AvatarUrl = picture,
                    GoogleId = googleSubject,
                    EmailConfirmed = true,
                    IsActive = true
                };
                _context.Users.Add(user);
                await _context.SaveChangesAsync();

                _context.UserRoles.Add(new UserRole { UserId = user.Id, RoleId = studentRole.Id });
                await _context.SaveChangesAsync();

                user = await _context.Users
                    .Include(u => u.UserRoles)
                        .ThenInclude(ur => ur.Role)
                    .FirstAsync(u => u.Id == user.Id);
            }
            else
            {
                if (string.IsNullOrEmpty(user.GoogleId))
                {
                    user.GoogleId = googleSubject;
                }
                if (string.IsNullOrEmpty(user.AvatarUrl) && !string.IsNullOrEmpty(picture))
                {
                    user.AvatarUrl = picture;
                }
                await _context.SaveChangesAsync();
            }

            var roles = user.UserRoles.Select(ur => ur.Role.Name).ToList();
            if (!roles.Any()) roles.Add(AppRoles.Student);

            var token = _jwtService.GenerateToken(user, roles);

            var profile = new UserProfileDto
            {
                Id = user.Id,
                Email = user.Email,
                FullName = user.FullName,
                StudentId = user.StudentId,
                Department = user.Department,
                AvatarUrl = user.AvatarUrl,
                Bio = user.Bio,
                Roles = roles,
                IsMember = user.MemberProfile != null,
                ClubRole = user.MemberProfile?.ClubRole
            };

            return Ok(ApiResponse<AuthResponse>.Ok(new AuthResponse
            {
                Token = token,
                ExpiresAt = DateTime.UtcNow.AddHours(24),
                User = profile
            }, "Đăng nhập Google thành công."));
        }

        [Authorize]
        [HttpGet("me")]
        public async Task<ActionResult<ApiResponse<UserProfileDto>>> GetMe()
        {
            var userIdStr = User.FindFirstValue(ClaimTypes.NameIdentifier) ?? User.FindFirstValue("sub");
            if (!Guid.TryParse(userIdStr, out var userId))
            {
                return Unauthorized(ApiResponse<UserProfileDto>.Fail("Phiên đăng nhập không hợp lệ."));
            }

            var user = await _context.Users
                .Include(u => u.UserRoles)
                    .ThenInclude(ur => ur.Role)
                .Include(u => u.MemberProfile)
                .FirstOrDefaultAsync(u => u.Id == userId);

            if (user == null)
            {
                return NotFound(ApiResponse<UserProfileDto>.Fail("Không tìm thấy thông tin tài khoản."));
            }

            var roles = user.UserRoles.Select(ur => ur.Role.Name).ToList();

            var profile = new UserProfileDto
            {
                Id = user.Id,
                Email = user.Email,
                FullName = user.FullName,
                StudentId = user.StudentId,
                Department = user.Department,
                AvatarUrl = user.AvatarUrl,
                Bio = user.Bio,
                Roles = roles,
                IsMember = user.MemberProfile != null,
                ClubRole = user.MemberProfile?.ClubRole
            };

            return Ok(ApiResponse<UserProfileDto>.Ok(profile));
        }

        [Authorize]
        [HttpPut("profile")]
        public async Task<ActionResult<ApiResponse<UserProfileDto>>> UpdateProfile([FromBody] UpdateProfileRequest request)
        {
            var userIdStr = User.FindFirstValue(ClaimTypes.NameIdentifier);
            if (!Guid.TryParse(userIdStr, out var userId))
            {
                return Unauthorized(ApiResponse<UserProfileDto>.Fail("Phiên làm việc hết hạn."));
            }

            var user = await _context.Users
                .Include(u => u.UserRoles).ThenInclude(ur => ur.Role)
                .Include(u => u.MemberProfile)
                .FirstOrDefaultAsync(u => u.Id == userId);

            if (user == null) return NotFound(ApiResponse<UserProfileDto>.Fail("Người dùng không tồn tại."));

            user.FullName = string.IsNullOrWhiteSpace(request.FullName) ? user.FullName : request.FullName.Trim();
            user.StudentId = request.StudentId?.Trim() ?? user.StudentId;
            user.Department = request.Department?.Trim() ?? user.Department;
            user.Bio = request.Bio?.Trim() ?? user.Bio;
            user.AvatarUrl = request.AvatarUrl?.Trim() ?? user.AvatarUrl;
            user.UpdatedAt = DateTime.UtcNow;

            await _context.SaveChangesAsync();

            var profile = new UserProfileDto
            {
                Id = user.Id,
                Email = user.Email,
                FullName = user.FullName,
                StudentId = user.StudentId,
                Department = user.Department,
                AvatarUrl = user.AvatarUrl,
                Bio = user.Bio,
                Roles = user.UserRoles.Select(r => r.Role.Name).ToList(),
                IsMember = user.MemberProfile != null,
                ClubRole = user.MemberProfile?.ClubRole
            };

            return Ok(ApiResponse<UserProfileDto>.Ok(profile, "Cập nhật hồ sơ thành công."));
        }

        [Authorize]
        [HttpPost("change-password")]
        public async Task<ActionResult<ApiResponse<string>>> ChangePassword([FromBody] ChangePasswordRequest request)
        {
            var userIdStr = User.FindFirstValue(ClaimTypes.NameIdentifier);
            if (!Guid.TryParse(userIdStr, out var userId))
            {
                return Unauthorized(ApiResponse<string>.Fail("Phiên làm việc hết hạn."));
            }

            var user = await _context.Users.FirstOrDefaultAsync(u => u.Id == userId);
            if (user == null) return NotFound(ApiResponse<string>.Fail("Người dùng không tồn tại."));

            if (!string.IsNullOrEmpty(user.PasswordHash) &&
                !_passwordHasher.VerifyPassword(request.CurrentPassword, user.PasswordHash))
            {
                return BadRequest(ApiResponse<string>.Fail("Mật khẩu hiện tại không chính xác."));
            }

            if (string.IsNullOrWhiteSpace(request.NewPassword) || request.NewPassword.Length < 6)
            {
                return BadRequest(ApiResponse<string>.Fail("Mật khẩu mới phải có tối thiểu 6 ký tự."));
            }

            user.PasswordHash = _passwordHasher.HashPassword(request.NewPassword);
            user.UpdatedAt = DateTime.UtcNow;
            await _context.SaveChangesAsync();

            return Ok(ApiResponse<string>.Ok("Đổi mật khẩu thành công."));
        }
    }
}
