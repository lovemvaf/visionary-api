using Visionary.Desktop.Services;

namespace Visionary.Desktop.Tests;

/// <summary>
/// AppState là static dùng chung cho toàn bộ ứng dụng, nên các test liên quan tới nó
/// phải chạy tuần tự để không tranh chấp trạng thái.
/// </summary>
[CollectionDefinition("AppState", DisableParallelization = true)]
public class AppStateCollection
{
}

/// <summary>
/// Kiểm thử logic phân quyền và quản lý phiên đăng nhập trên Desktop.
/// </summary>
[Collection("AppState")]
public class AppStateTests : IDisposable
{
    public AppStateTests()
    {
        AppState.Logout();
    }

    public void Dispose()
    {
        AppState.Logout();
        GC.SuppressFinalize(this);
    }

    private static void SetUser(params string[] roles)
    {
        AppState.Token = "token";
        AppState.CurrentUser = new Visionary.Core.DTOs.UserProfileDto
        {
            FullName = "Test User",
            Roles = roles.ToList()
        };
    }

    [Fact]
    public void IsAdmin_AdminRole_ReturnsTrue()
    {
        SetUser("Admin");

        Assert.True(AppState.IsAdmin);
        Assert.True(AppState.IsCommittee);
    }

    [Fact]
    public void IsCommittee_CommitteeRole_ReturnsTrueButIsAdminFalse()
    {
        SetUser("Committee");

        Assert.True(AppState.IsCommittee);
        Assert.False(AppState.IsAdmin);
    }

    [Fact]
    public void IsCommittee_StudentRole_ReturnsFalse()
    {
        SetUser("Student");

        Assert.False(AppState.IsCommittee);
        Assert.False(AppState.IsAdmin);
    }

    [Fact]
    public void HasAnyRole_CaseInsensitiveAndTrimmed_Matches()
    {
        SetUser("  committee  ");

        Assert.True(AppState.HasAnyRole("Committee"));
    }

    [Fact]
    public void IsAuthenticated_WithoutToken_ReturnsFalse()
    {
        AppState.CurrentUser = new Visionary.Core.DTOs.UserProfileDto { FullName = "Test" };

        Assert.False(AppState.IsAuthenticated);
    }

    [Fact]
    public void Logout_ClearsTokenUserAndExpiry()
    {
        SetUser("Admin");
        AppState.TokenExpiresAt = DateTime.UtcNow.AddHours(1);

        AppState.Logout();

        Assert.Null(AppState.Token);
        Assert.Null(AppState.CurrentUser);
        Assert.Null(AppState.TokenExpiresAt);
        Assert.False(AppState.IsAuthenticated);
    }

    [Fact]
    public void IsSessionExpired_WhenExpiryInPast_ReturnsTrue()
    {
        SetUser("Admin");
        AppState.TokenExpiresAt = DateTime.UtcNow.AddMinutes(-1);

        Assert.True(AppState.IsSessionExpired);
    }

    [Fact]
    public void IsSessionExpired_WhenNoExpiry_ReturnsFalse()
    {
        SetUser("Admin");

        Assert.False(AppState.IsSessionExpired);
    }
}
