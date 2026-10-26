using System;
using Visionary.Core.DTOs;
using Visionary.Core.Enums;

namespace Visionary.Desktop.Services;

/// <summary>
/// Global application state for Windows Forms desktop client.
/// Stores current session token, user details, and active server base URL.
/// </summary>
public static class AppState
{
    public static string ServerBaseUrl { get; set; } = "http://localhost:5000";
    public static string? Token { get; set; }
    public static UserProfileDto? CurrentUser { get; set; }

    /// <summary>Thời điểm JWT hết hạn (nếu backend trả về).</summary>
    public static DateTime? TokenExpiresAt { get; set; }

    public static bool IsAuthenticated => !string.IsNullOrEmpty(Token) && CurrentUser != null;

    /// <summary>
    /// Phiên đã hết hạn nếu backend đã cung cấp mốc hết hạn và thời điểm đó đã qua.
    /// Dùng để chủ động đăng xuất thay vì chờ tới lúc API trả về 401.
    /// </summary>
    public static bool IsSessionExpired =>
        TokenExpiresAt.HasValue && TokenExpiresAt.Value.ToUniversalTime() <= DateTime.UtcNow;

    public static bool IsAdmin => HasAnyRole(AppRoles.Admin, "System Administrator");

    public static bool IsCommittee => HasAnyRole(AppRoles.Admin, AppRoles.Committee, "Club Committee", "BCN");

    /// <summary>
    /// Kiểm tra tài khoản hiện tại có một trong các role được liệt kê hay không.
    /// So sánh không phân biệt hoa thường để không phụ thuộc cách backend trả về tên role.
    /// </summary>
    public static bool HasAnyRole(params string[] roles)
    {
        var userRoles = CurrentUser?.Roles;
        if (userRoles == null || roles.Length == 0)
        {
            return false;
        }

        foreach (var userRole in userRoles)
        {
            if (string.IsNullOrWhiteSpace(userRole))
            {
                continue;
            }

            foreach (var role in roles)
            {
                if (string.Equals(userRole.Trim(), role, StringComparison.OrdinalIgnoreCase))
                {
                    return true;
                }
            }
        }

        return false;
    }

    public static void Logout()
    {
        Token = null;
        CurrentUser = null;
        TokenExpiresAt = null;
    }
}
