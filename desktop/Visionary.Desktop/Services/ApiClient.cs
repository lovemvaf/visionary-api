using System;
using System.Collections.Generic;
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using Visionary.Core.Common;
using Visionary.Core.DTOs;
using Visionary.Core.Enums;

namespace Visionary.Desktop.Services;

/// <summary>
/// Lớp giao tiếp với ASP.NET Core Web API của VISIONARY.
///
/// Mọi lỗi mạng/HTTP được chuẩn hoá thành <see cref="ApiException"/> để tầng UI hiển thị
/// thông báo thân thiện, phân biệt rõ timeout với lỗi HTTP, 401 (hết phiên),
/// 403 (không đủ quyền) và lỗi nghiệp vụ trả về từ backend.
///
/// Lớp có thể khởi tạo với HttpMessageHandler tùy ý để unit test không cần chạy server thật.
/// </summary>
public class ApiClient
{
    private static readonly JsonSerializerOptions _jsonOptions = new JsonSerializerOptions
    {
        PropertyNameCaseInsensitive = true
    };

    private readonly HttpClient _httpClient;

    /// <summary>
    /// Thời gian chờ tối đa cho mỗi request (giống HttpClient.Timeout mặc định 100s).
    /// </summary>
    public static readonly TimeSpan RequestTimeout = TimeSpan.FromSeconds(30);

    /// <summary>Instance dùng chung cho các Form (kết nối tới server thật).</summary>
    public static ApiClient Default { get; } = new(CreateDefaultHttpClient());

    public ApiClient(HttpClient httpClient)
    {
        _httpClient = httpClient ?? throw new ArgumentNullException(nameof(httpClient));
    }

    /// <summary>Tạo ApiClient với handler giả lập, dùng cho unit test.</summary>
    public ApiClient(HttpMessageHandler handler)
        : this(new HttpClient(handler, disposeHandler: false))
    {
    }

    private static HttpClient CreateDefaultHttpClient()
    {
        var client = new HttpClient
        {
            Timeout = RequestTimeout
        };
        return client;
    }

    #region Core helpers

    private static string GetUrl(string endpoint)
    {
        var baseUri = AppState.ServerBaseUrl.TrimEnd('/');
        return $"{baseUri}/{endpoint.TrimStart('/')}";
    }

    private static void SetAuthHeader(HttpRequestMessage request)
    {
        if (!string.IsNullOrEmpty(AppState.Token))
        {
            request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", AppState.Token);
        }
    }

    /// <summary>
    /// Gửi request và chuẩn hoá mọi lỗi (timeout / mạng / HTTP) thành ApiException.
    /// Phân biệt timeout do máy chủ không phản hồi với việc người dùng hủy thao tác.
    /// </summary>
    private async Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
    {
        try
        {
            return await _httpClient.SendAsync(request, cancellationToken).ConfigureAwait(false);
        }
        catch (OperationCanceledException) when (cancellationToken.IsCancellationRequested)
        {
            // Người dùng đóng Form hoặc hủy thao tác -> không phải lỗi hệ thống.
            throw;
        }
        catch (TaskCanceledException ex)
        {
            // HttpClient.Timeout kích hoạt: máy chủ không phản hồi trong thời gian chờ.
            throw new ApiException(
                ApiErrorKind.Timeout,
                $"Máy chủ không phản hồi sau {RequestTimeout.TotalSeconds:0} giây.",
                null,
                ex);
        }
        catch (HttpRequestException ex)
        {
            throw new ApiException(
                ApiErrorKind.Network,
                $"Không kết nối được tới máy chủ ({ex.Message}).",
                null,
                ex);
        }
    }

    /// <summary>
    /// Đọc nội dung phản hồi và ném ApiException tương ứng nếu HTTP không thành công.
    /// </summary>
    private async Task<string> ReadContentAsync(HttpResponseMessage response, CancellationToken cancellationToken)
    {
        try
        {
            return await response.Content.ReadAsStringAsync(cancellationToken).ConfigureAwait(false);
        }
        catch (Exception ex) when (ex is HttpRequestException or OperationCanceledException)
        {
            throw new ApiException(ApiErrorKind.Network, "Không đọc được dữ liệu phản hồi từ máy chủ.", null, ex);
        }
    }

    /// <summary>
    /// Chuyển HTTP status code thành ApiException với thông điệp thân thiện.
    /// 401 -> hết phiên đăng nhập, 403 -> không đủ quyền.
    /// </summary>
    private static ApiException BuildHttpError(HttpResponseMessage response, string content, string fallbackMessage)
    {
        var kind = response.StatusCode switch
        {
            HttpStatusCode.Unauthorized => ApiErrorKind.Unauthorized,
            HttpStatusCode.Forbidden => ApiErrorKind.Forbidden,
            _ => (int)response.StatusCode >= 500 ? ApiErrorKind.Server : ApiErrorKind.Client
        };

        var message = fallbackMessage;
        if (!string.IsNullOrWhiteSpace(content))
        {
            try
            {
                var errorPayload = JsonSerializer.Deserialize<ApiResponse<string>>(content, _jsonOptions);
                if (!string.IsNullOrWhiteSpace(errorPayload?.Message))
                {
                    message = errorPayload!.Message;
                }
            }
            catch (JsonException)
            {
                // Phản hồi không phải JSON (ví dụ trang lỗi của proxy) -> giữ thông điệp mặc định.
            }
        }

        return new ApiException(kind, message, (int)response.StatusCode);
    }

    /// <summary>
    /// Giải mã JSON phản hồi, chuẩn hoá lỗi JSON hỏng thành ApiErrorKind.InvalidResponse.
    /// </summary>
    private static ApiResponse<T> ParseEnvelope<T>(string content)
    {
        ApiResponse<T>? envelope;
        try
        {
            envelope = JsonSerializer.Deserialize<ApiResponse<T>>(content, _jsonOptions);
        }
        catch (JsonException ex)
        {
            throw new ApiException(
                ApiErrorKind.InvalidResponse,
                "Máy chủ trả về dữ liệu JSON không hợp lệ.",
                null,
                ex);
        }

        if (envelope == null)
        {
            throw new ApiException(ApiErrorKind.InvalidResponse, "Máy chủ trả về nội dung rỗng.");
        }

        return envelope;
    }

    /// <summary>
    /// Bọc lời gọi API chuẩn: gửi request, kiểm tra HTTP, giải mã envelope và trả về Data.
    /// Ném ApiException với thông điệp lấy từ backend khi có lỗi nghiệp vụ.
    /// </summary>
    private async Task<T> SendAsync<T>(
        HttpRequestMessage request,
        string errorFallback,
        CancellationToken cancellationToken,
        bool allowNullData = false,
        T? fallbackData = default)
    {
        var response = await SendAsync(request, cancellationToken).ConfigureAwait(false);
        var content = await ReadContentAsync(response, cancellationToken).ConfigureAwait(false);

        if (!response.IsSuccessStatusCode)
        {
            var error = BuildHttpError(response, content, errorFallback);
            if (error.IsSessionExpired)
            {
                AppState.Logout();
            }
            throw error;
        }

        var envelope = ParseEnvelope<T>(content);

        if (!envelope.Success && !string.IsNullOrWhiteSpace(envelope.Message))
        {
            // Backend trả 200 nhưng báo lỗi nghiệp vụ trong envelope.
            throw new ApiException(ApiErrorKind.Client, envelope.Message, (int)response.StatusCode);
        }

        if (envelope.Data == null)
        {
            if (allowNullData && fallbackData != null)
            {
                return fallbackData;
            }
            throw new ApiException(ApiErrorKind.InvalidResponse, errorFallback, (int)response.StatusCode);
        }

        return envelope.Data;
    }

    #endregion

    #region Auth

    public async Task<AuthResponse> LoginAsync(string email, string password, CancellationToken cancellationToken = default)
    {
        var request = new HttpRequestMessage(HttpMethod.Post, GetUrl("api/auth/login"))
        {
            Content = JsonContent.Create(new LoginRequest { Email = email, Password = password })
        };

        var auth = await SendAsync<AuthResponse>(
            request,
            "Không nhận được dữ liệu xác thực từ máy chủ.",
            cancellationToken).ConfigureAwait(false);

        if (string.IsNullOrWhiteSpace(auth.Token) || auth.User == null)
        {
            throw new ApiException(ApiErrorKind.InvalidResponse, "Máy chủ trả về phiên đăng nhập không hợp lệ.");
        }

        AppState.Token = auth.Token;
        AppState.CurrentUser = auth.User;
        AppState.TokenExpiresAt = auth.ExpiresAt == default ? null : auth.ExpiresAt;
        return auth;
    }

    public async Task<UserProfileDto> GetMeAsync(CancellationToken cancellationToken = default)
    {
        var request = new HttpRequestMessage(HttpMethod.Get, GetUrl("api/auth/me"));
        SetAuthHeader(request);

        var user = await SendAsync<UserProfileDto>(
            request,
            "Không tải được thông tin tài khoản.",
            cancellationToken).ConfigureAwait(false);

        AppState.CurrentUser = user;
        return user;
    }

    #endregion

    #region Admin

    public async Task<DashboardStatsDto> GetDashboardStatsAsync(CancellationToken cancellationToken = default)
    {
        var request = new HttpRequestMessage(HttpMethod.Get, GetUrl("api/admin/dashboard"));
        SetAuthHeader(request);

        return await SendAsync<DashboardStatsDto>(
            request,
            "Không tải được thống kê tổng quan.",
            cancellationToken,
            allowNullData: true,
            fallbackData: new DashboardStatsDto()).ConfigureAwait(false);
    }

    public async Task<List<ContentSourceDto>> GetSourcesAsync(CancellationToken cancellationToken = default)
    {
        var request = new HttpRequestMessage(HttpMethod.Get, GetUrl("api/admin/sources"));
        SetAuthHeader(request);

        return await SendAsync<List<ContentSourceDto>>(
            request,
            "Không tải được danh sách nguồn dữ liệu.",
            cancellationToken,
            allowNullData: true,
            fallbackData: new List<ContentSourceDto>()).ConfigureAwait(false);
    }

    public async Task<string> TriggerSourceAsync(Guid sourceId, CancellationToken cancellationToken = default)
    {
        var request = new HttpRequestMessage(HttpMethod.Post, GetUrl($"api/admin/sources/trigger/{sourceId}"));
        SetAuthHeader(request);

        var message = await SendAsync<string>(
            request,
            "Không kích hoạt được nguồn dữ liệu.",
            cancellationToken,
            allowNullData: true,
            fallbackData: string.Empty).ConfigureAwait(false);

        return string.IsNullOrWhiteSpace(message) ? "Đồng bộ nguồn dữ liệu thành công!" : message;
    }

    #endregion

    #region Club

    public async Task<PagedResponse<MemberDto>> GetMembersAsync(
        string? search = null,
        int pageIndex = 1,
        int pageSize = 50,
        CancellationToken cancellationToken = default)
    {
        var url = GetUrl($"api/club/members?pageIndex={pageIndex}&pageSize={pageSize}");
        if (!string.IsNullOrWhiteSpace(search))
        {
            url += $"&search={Uri.EscapeDataString(search.Trim())}";
        }

        var request = new HttpRequestMessage(HttpMethod.Get, url);
        SetAuthHeader(request);

        return await SendAsync<PagedResponse<MemberDto>>(
            request,
            "Không tải được danh sách thành viên.",
            cancellationToken,
            allowNullData: true,
            fallbackData: new PagedResponse<MemberDto>(new List<MemberDto>(), 0, pageIndex, pageSize)).ConfigureAwait(false);
    }

    public async Task<List<MembershipApplicationDto>> GetApplicationsAsync(
        MembershipStatus? status = null,
        CancellationToken cancellationToken = default)
    {
        var url = GetUrl("api/club/applications");
        if (status.HasValue)
        {
            url += $"?status={status.Value}";
        }

        var request = new HttpRequestMessage(HttpMethod.Get, url);
        SetAuthHeader(request);

        return await SendAsync<List<MembershipApplicationDto>>(
            request,
            "Không tải được danh sách đơn đăng ký.",
            cancellationToken,
            allowNullData: true,
            fallbackData: new List<MembershipApplicationDto>()).ConfigureAwait(false);
    }

    public async Task<string> ReviewApplicationAsync(
        Guid id,
        bool isApproved,
        string? clubRole,
        Guid? departmentId,
        string? notes,
        CancellationToken cancellationToken = default)
    {
        var request = new HttpRequestMessage(HttpMethod.Put, GetUrl($"api/club/applications/{id}/review"))
        {
            Content = JsonContent.Create(new ReviewApplicationRequest
            {
                IsApproved = isApproved,
                ClubRole = clubRole,
                DepartmentId = departmentId,
                ReviewNotes = notes
            })
        };
        SetAuthHeader(request);

        var message = await SendAsync<string>(
            request,
            "Không xử lý được đơn đăng ký.",
            cancellationToken,
            allowNullData: true,
            fallbackData: string.Empty).ConfigureAwait(false);

        return string.IsNullOrWhiteSpace(message)
            ? (isApproved ? "Phê duyệt thành công!" : "Từ chối thành công!")
            : message;
    }

    #endregion

    #region Events

    public async Task<PagedResponse<EventDto>> GetEventsAsync(
        string? search = null,
        int pageIndex = 1,
        int pageSize = 20,
        CancellationToken cancellationToken = default)
    {
        var url = GetUrl($"api/events?pageIndex={pageIndex}&pageSize={pageSize}");
        if (!string.IsNullOrWhiteSpace(search))
        {
            url += $"&search={Uri.EscapeDataString(search.Trim())}";
        }

        var request = new HttpRequestMessage(HttpMethod.Get, url);
        SetAuthHeader(request);

        return await SendAsync<PagedResponse<EventDto>>(
            request,
            "Không tải được danh sách sự kiện.",
            cancellationToken,
            allowNullData: true,
            fallbackData: new PagedResponse<EventDto>(new List<EventDto>(), 0, pageIndex, pageSize)).ConfigureAwait(false);
    }

    public async Task<EventDto> CreateEventAsync(CreateEventRequest req, CancellationToken cancellationToken = default)
    {
        var request = new HttpRequestMessage(HttpMethod.Post, GetUrl("api/events"))
        {
            Content = JsonContent.Create(req)
        };
        SetAuthHeader(request);

        return await SendAsync<EventDto>(
            request,
            "Không tạo được sự kiện.",
            cancellationToken).ConfigureAwait(false);
    }

    public async Task<List<EventRegistrationDto>> GetEventRegistrationsAsync(Guid eventId, CancellationToken cancellationToken = default)
    {
        var request = new HttpRequestMessage(HttpMethod.Get, GetUrl($"api/events/{eventId}/registrations"));
        SetAuthHeader(request);

        return await SendAsync<List<EventRegistrationDto>>(
            request,
            "Không tải được danh sách đăng ký.",
            cancellationToken,
            allowNullData: true,
            fallbackData: new List<EventRegistrationDto>()).ConfigureAwait(false);
    }

    public async Task<string> CheckInAttendeeAsync(Guid eventId, Guid userId, CancellationToken cancellationToken = default)
    {
        var request = new HttpRequestMessage(HttpMethod.Post, GetUrl($"api/events/{eventId}/attendance"))
        {
            Content = JsonContent.Create(new CheckInRequest
            {
                UserId = userId,
                Method = AttendanceMethod.ManualCheckIn
            })
        };
        SetAuthHeader(request);

        var message = await SendAsync<string>(
            request,
            "Không điểm danh được người tham gia.",
            cancellationToken,
            allowNullData: true,
            fallbackData: string.Empty).ConfigureAwait(false);

        return string.IsNullOrWhiteSpace(message) ? "Điểm danh thành công!" : message;
    }

    #endregion
}
