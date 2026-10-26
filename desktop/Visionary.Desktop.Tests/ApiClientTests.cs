using System.Net;
using System.Text.Json;
using Visionary.Core.DTOs;
using Visionary.Desktop.Services;

namespace Visionary.Desktop.Tests;

/// <summary>
/// Kiểm thử tầng giao tiếp API của Desktop client:
/// phân biệt timeout / lỗi mạng / lỗi HTTP, xử lý JSON hỏng, 401, 403 và lỗi nghiệp vụ.
/// </summary>
[Collection("AppState")]
public class ApiClientTests : IDisposable
{
    private readonly string _originalBaseUrl = AppState.ServerBaseUrl;

    public ApiClientTests()
    {
        AppState.ServerBaseUrl = "http://localhost:5000";
        AppState.Logout();
    }

    public void Dispose()
    {
        AppState.ServerBaseUrl = _originalBaseUrl;
        AppState.Logout();
        GC.SuppressFinalize(this);
    }

    private static ApiClient CreateClient(StubHttpMessageHandler handler)
        => new(new HttpClient(handler) { Timeout = TimeSpan.FromSeconds(2) });

    private static string OkJson<T>(T data, string message = "Success")
        => JsonSerializer.Serialize(new
        {
            success = true,
            message,
            data,
            errors = Array.Empty<string>(),
            timestamp = DateTime.UtcNow
        });

    [Fact]
    public async Task LoginAsync_ValidCredentials_ReturnsAuthResponseAndStoresSession()
    {
        var payload = OkJson(new
        {
            token = "jwt-token-abc",
            expiresAt = DateTime.UtcNow.AddHours(2),
            user = new { id = Guid.NewGuid(), email = "vongocminhdat@visionary.dntu.edu.vn", fullName = "Võ Ngọc Minh Đạt", roles = new[] { "Committee" } }
        });

        var client = CreateClient(StubHttpMessageHandler.Json(HttpStatusCode.OK, payload));

        var auth = await client.LoginAsync("vongocminhdat@visionary.dntu.edu.vn", "mat-khau");

        Assert.Equal("jwt-token-abc", auth.Token);
        Assert.Equal("Võ Ngọc Minh Đạt", auth.User.FullName);
        Assert.Equal("jwt-token-abc", AppState.Token);
        Assert.Equal("Võ Ngọc Minh Đạt", AppState.CurrentUser?.FullName);
        Assert.True(AppState.IsAuthenticated);
    }

    [Fact]
    public async Task LoginAsync_InvalidCredentials_ThrowsClientErrorWithBackendMessage()
    {
        var payload = JsonSerializer.Serialize(new
        {
            success = false,
            message = "Email hoặc mật khẩu không đúng.",
            data = (object?)null,
            errors = new[] { "Email hoặc mật khẩu không đúng." },
            timestamp = DateTime.UtcNow
        });

        var client = CreateClient(StubHttpMessageHandler.Json(HttpStatusCode.Unauthorized, payload));

        var ex = await Assert.ThrowsAsync<ApiException>(() => client.LoginAsync("a@b.c", "sai"));

        Assert.Equal(ApiErrorKind.Unauthorized, ex.Kind);
        Assert.Equal("Email hoặc mật khẩu không đúng.", ex.Message);
    }

    [Fact]
    public async Task LoginAsync_ServerUnreachable_ThrowsNetworkErrorNotTimeout()
    {
        var client = CreateClient(StubHttpMessageHandler.NetworkFailure());

        var ex = await Assert.ThrowsAsync<ApiException>(() => client.LoginAsync("a@b.c", "x"));

        Assert.Equal(ApiErrorKind.Network, ex.Kind);
        Assert.False(ex.IsTimeout);
    }

    [Fact]
    public async Task LoginAsync_ServerNeverResponds_ThrowsTimeoutError()
    {
        var client = CreateClient(StubHttpMessageHandler.NeverRespond());

        var ex = await Assert.ThrowsAsync<ApiException>(() => client.LoginAsync("a@b.c", "x"));

        Assert.Equal(ApiErrorKind.Timeout, ex.Kind);
        Assert.True(ex.IsTimeout);
    }

    [Fact]
    public async Task GetMembersAsync_InvalidJson_ThrowsInvalidResponseError()
    {
        var client = CreateClient(StubHttpMessageHandler.Json(HttpStatusCode.OK, "{ this is not json "));

        var ex = await Assert.ThrowsAsync<ApiException>(() => client.GetMembersAsync());

        Assert.Equal(ApiErrorKind.InvalidResponse, ex.Kind);
    }

    [Fact]
    public async Task GetMembersAsync_EmptyData_ReturnsEmptyPageInsteadOfNull()
    {
        var payload = OkJson(new { items = Array.Empty<object>(), pageIndex = 1, pageSize = 50, totalCount = 0 });

        var client = CreateClient(StubHttpMessageHandler.Json(HttpStatusCode.OK, payload));

        var page = await client.GetMembersAsync();

        Assert.NotNull(page);
        Assert.Empty(page.Items);
    }

    [Fact]
    public async Task GetMembersAsync_SearchTerm_IsUrlEncoded()
    {
        string? requestedUrl = null;
        var handler = new StubHttpMessageHandler(async (request, _) =>
        {
            // AbsoluteUri giữ nguyên phần đã escape, ToString() sẽ giải mã lại.
            requestedUrl = request.RequestUri?.AbsoluteUri;
            return new HttpResponseMessage(HttpStatusCode.OK)
            {
                Content = new StringContent(OkJson(new { items = Array.Empty<object>(), pageIndex = 1, pageSize = 50, totalCount = 0 }))
            };
        });

        var client = CreateClient(handler);

        await client.GetMembersAsync("Nguyễn Văn A");

        Assert.NotNull(requestedUrl);
        Assert.Contains("search=" + Uri.EscapeDataString("Nguyễn Văn A"), requestedUrl);
    }

    [Fact]
    public async Task GetDashboardStatsAsync_Forbidden_ThrowsForbiddenError()
    {
        var client = CreateClient(StubHttpMessageHandler.Json(HttpStatusCode.Forbidden, "{}"));

        var ex = await Assert.ThrowsAsync<ApiException>(() => client.GetDashboardStatsAsync());

        Assert.Equal(ApiErrorKind.Forbidden, ex.Kind);
        Assert.True(ex.IsForbidden);
    }

    [Fact]
    public async Task GetDashboardStatsAsync_ServerError_ThrowsServerError()
    {
        var client = CreateClient(StubHttpMessageHandler.Json(HttpStatusCode.InternalServerError, "{}"));

        var ex = await Assert.ThrowsAsync<ApiException>(() => client.GetDashboardStatsAsync());

        Assert.Equal(ApiErrorKind.Server, ex.Kind);
    }

    [Fact]
    public async Task GetApplicationsAsync_TokenExpired_ClearsSessionAndReportsUnauthorized()
    {
        AppState.Token = "expired-token";
        AppState.CurrentUser = new UserProfileDto { FullName = "Test" };

        var client = CreateClient(StubHttpMessageHandler.Json(HttpStatusCode.Unauthorized, "{}"));

        var ex = await Assert.ThrowsAsync<ApiException>(() => client.GetApplicationsAsync());

        Assert.Equal(ApiErrorKind.Unauthorized, ex.Kind);
        Assert.True(ex.IsSessionExpired);
        Assert.Null(AppState.Token);
        Assert.Null(AppState.CurrentUser);
    }

    [Fact]
    public async Task GetApplicationsAsync_BusinessErrorInEnvelope_ThrowsClientError()
    {
        var payload = JsonSerializer.Serialize(new
        {
            success = false,
            message = "Ứng viên đã tồn tại trong danh sách.",
            data = (object?)null,
            errors = new[] { "Ứng viên đã tồn tại trong danh sách." },
            timestamp = DateTime.UtcNow
        });

        var client = CreateClient(StubHttpMessageHandler.Json(HttpStatusCode.OK, payload));

        var ex = await Assert.ThrowsAsync<ApiException>(() => client.GetApplicationsAsync());

        Assert.Equal(ApiErrorKind.Client, ex.Kind);
        Assert.Equal("Ứng viên đã tồn tại trong danh sách.", ex.Message);
    }

    [Fact]
    public async Task CheckInAttendeeAsync_SendsBearerTokenAndEventId()
    {
        string? authHeader = null;
        string? url = null;
        var handler = new StubHttpMessageHandler(async (request, _) =>
        {
            authHeader = request.Headers.Authorization?.ToString();
            url = request.RequestUri?.ToString();
            return new HttpResponseMessage(HttpStatusCode.OK)
            {
                Content = new StringContent(OkJson("Điểm danh thành công!"))
            };
        });

        AppState.Token = "jwt-token-abc";

        var client = CreateClient(handler);
        var eventId = Guid.NewGuid();
        var userId = Guid.NewGuid();

        var message = await client.CheckInAttendeeAsync(eventId, userId);

        Assert.Equal("Điểm danh thành công!", message);
        Assert.Equal("Bearer jwt-token-abc", authHeader);
        Assert.NotNull(url);
        Assert.Contains(eventId.ToString(), url);
    }

    [Fact]
    public async Task GetEventsAsync_CancellationRequested_PropagatesCancellation()
    {
        var client = CreateClient(StubHttpMessageHandler.NeverRespond());

        using var cts = new CancellationTokenSource();
        cts.CancelAfter(TimeSpan.FromMilliseconds(100));

        await Assert.ThrowsAnyAsync<OperationCanceledException>(
            () => client.GetEventsAsync(cancellationToken: cts.Token));
    }
}
