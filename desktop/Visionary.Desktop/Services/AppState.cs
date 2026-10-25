using System;
using Visionary.Core.DTOs;

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

    public static bool IsAuthenticated => !string.IsNullOrEmpty(Token) && CurrentUser != null;

    public static bool IsAdmin => CurrentUser?.Roles != null && 
        (CurrentUser.Roles.Contains("Admin") || CurrentUser.Roles.Contains("System Administrator"));

    public static bool IsCommittee => CurrentUser?.Roles != null && 
        (IsAdmin || CurrentUser.Roles.Contains("Club Committee") || CurrentUser.Roles.Contains("BCN"));

    public static void Logout()
    {
        Token = null;
        CurrentUser = null;
    }
}
