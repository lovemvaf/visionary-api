using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Text.Json;
using System.Threading.Tasks;
using Visionary.Core.Common;
using Visionary.Core.DTOs;
using Visionary.Core.Enums;

namespace Visionary.Desktop.Services;

public class ApiClient
{
    private static readonly HttpClient _httpClient = new HttpClient
    {
        Timeout = TimeSpan.FromSeconds(15)
    };

    private static readonly JsonSerializerOptions _jsonOptions = new JsonSerializerOptions
    {
        PropertyNameCaseInsensitive = true
    };

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

    public static async Task<AuthResponse> LoginAsync(string email, string password)
    {
        var request = new HttpRequestMessage(HttpMethod.Post, GetUrl("api/auth/login"))
        {
            Content = JsonContent.Create(new LoginRequest { Email = email, Password = password })
        };

        var response = await _httpClient.SendAsync(request);
        var content = await response.Content.ReadAsStringAsync();

        if (!response.IsSuccessStatusCode)
        {
            var errorObj = JsonSerializer.Deserialize<ApiResponse<AuthResponse>>(content, _jsonOptions);
            throw new Exception(errorObj?.Message ?? $"Lỗi đăng nhập (Mã HTTP {response.StatusCode})");
        }

        var result = JsonSerializer.Deserialize<ApiResponse<AuthResponse>>(content, _jsonOptions);
        if (result?.Data == null) throw new Exception("Không nhận được dữ liệu xác thực từ máy chủ.");

        AppState.Token = result.Data.Token;
        AppState.CurrentUser = result.Data.User;
        return result.Data;
    }

    public static async Task<UserProfileDto> GetMeAsync()
    {
        var request = new HttpRequestMessage(HttpMethod.Get, GetUrl("api/auth/me"));
        SetAuthHeader(request);

        var response = await _httpClient.SendAsync(request);
        var content = await response.Content.ReadAsStringAsync();

        if (!response.IsSuccessStatusCode)
        {
            throw new Exception($"Không thể tải thông tin tài khoản (HTTP {response.StatusCode})");
        }

        var result = JsonSerializer.Deserialize<ApiResponse<UserProfileDto>>(content, _jsonOptions);
        if (result?.Data != null)
        {
            AppState.CurrentUser = result.Data;
            return result.Data;
        }

        throw new Exception("Dữ liệu hồ sơ rỗng.");
    }

    public static async Task<DashboardStatsDto> GetDashboardStatsAsync()
    {
        var request = new HttpRequestMessage(HttpMethod.Get, GetUrl("api/admin/dashboard"));
        SetAuthHeader(request);

        var response = await _httpClient.SendAsync(request);
        var content = await response.Content.ReadAsStringAsync();

        if (!response.IsSuccessStatusCode)
        {
            throw new Exception($"Lỗi tải thống kê (HTTP {response.StatusCode}): {content}");
        }

        var result = JsonSerializer.Deserialize<ApiResponse<DashboardStatsDto>>(content, _jsonOptions);
        return result?.Data ?? new DashboardStatsDto();
    }

    public static async Task<PagedResponse<MemberDto>> GetMembersAsync(string? search = null, int pageIndex = 1, int pageSize = 50)
    {
        var url = GetUrl($"api/club/members?pageIndex={pageIndex}&pageSize={pageSize}");
        if (!string.IsNullOrWhiteSpace(search))
        {
            url += $"&search={Uri.EscapeDataString(search.Trim())}";
        }

        var request = new HttpRequestMessage(HttpMethod.Get, url);
        SetAuthHeader(request);

        var response = await _httpClient.SendAsync(request);
        var content = await response.Content.ReadAsStringAsync();

        if (!response.IsSuccessStatusCode)
        {
            throw new Exception($"Lỗi tải danh sách thành viên (HTTP {response.StatusCode})");
        }

        var result = JsonSerializer.Deserialize<ApiResponse<PagedResponse<MemberDto>>>(content, _jsonOptions);
        return result?.Data ?? new PagedResponse<MemberDto>(new List<MemberDto>(), 0, 1, pageSize);
    }

    public static async Task<List<MembershipApplicationDto>> GetApplicationsAsync(MembershipStatus? status = null)
    {
        var url = GetUrl("api/club/applications");
        if (status.HasValue)
        {
            url += $"?status={status.Value}";
        }

        var request = new HttpRequestMessage(HttpMethod.Get, url);
        SetAuthHeader(request);

        var response = await _httpClient.SendAsync(request);
        var content = await response.Content.ReadAsStringAsync();

        if (!response.IsSuccessStatusCode)
        {
            throw new Exception($"Lỗi tải đơn đăng ký (HTTP {response.StatusCode})");
        }

        var result = JsonSerializer.Deserialize<ApiResponse<List<MembershipApplicationDto>>>(content, _jsonOptions);
        return result?.Data ?? new List<MembershipApplicationDto>();
    }

    public static async Task<string> ReviewApplicationAsync(Guid id, bool isApproved, string? clubRole, Guid? departmentId, string? notes)
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

        var response = await _httpClient.SendAsync(request);
        var content = await response.Content.ReadAsStringAsync();

        if (!response.IsSuccessStatusCode)
        {
            var err = JsonSerializer.Deserialize<ApiResponse<string>>(content, _jsonOptions);
            throw new Exception(err?.Message ?? $"Lỗi xử lý đơn (HTTP {response.StatusCode})");
        }

        var result = JsonSerializer.Deserialize<ApiResponse<string>>(content, _jsonOptions);
        return result?.Message ?? (isApproved ? "Phê duyệt thành công!" : "Từ chối thành công!");
    }

    public static async Task<PagedResponse<EventDto>> GetEventsAsync(string? search = null, int pageIndex = 1, int pageSize = 20)
    {
        var url = GetUrl($"api/events?pageIndex={pageIndex}&pageSize={pageSize}");
        if (!string.IsNullOrWhiteSpace(search))
        {
            url += $"&search={Uri.EscapeDataString(search.Trim())}";
        }

        var request = new HttpRequestMessage(HttpMethod.Get, url);
        SetAuthHeader(request);

        var response = await _httpClient.SendAsync(request);
        var content = await response.Content.ReadAsStringAsync();

        if (!response.IsSuccessStatusCode)
        {
            throw new Exception($"Lỗi tải danh sách sự kiện (HTTP {response.StatusCode})");
        }

        var result = JsonSerializer.Deserialize<ApiResponse<PagedResponse<EventDto>>>(content, _jsonOptions);
        return result?.Data ?? new PagedResponse<EventDto>(new List<EventDto>(), 0, 1, pageSize);
    }

    public static async Task<EventDto> CreateEventAsync(CreateEventRequest req)
    {
        var request = new HttpRequestMessage(HttpMethod.Post, GetUrl("api/events"))
        {
            Content = JsonContent.Create(req)
        };
        SetAuthHeader(request);

        var response = await _httpClient.SendAsync(request);
        var content = await response.Content.ReadAsStringAsync();

        if (!response.IsSuccessStatusCode)
        {
            var err = JsonSerializer.Deserialize<ApiResponse<EventDto>>(content, _jsonOptions);
            throw new Exception(err?.Message ?? $"Lỗi tạo sự kiện (HTTP {response.StatusCode})");
        }

        var result = JsonSerializer.Deserialize<ApiResponse<EventDto>>(content, _jsonOptions);
        return result?.Data ?? throw new Exception("Không nhận được dữ liệu phản hồi.");
    }

    public static async Task<List<EventRegistrationDto>> GetEventRegistrationsAsync(Guid eventId)
    {
        var request = new HttpRequestMessage(HttpMethod.Get, GetUrl($"api/events/{eventId}/registrations"));
        SetAuthHeader(request);

        var response = await _httpClient.SendAsync(request);
        var content = await response.Content.ReadAsStringAsync();

        if (!response.IsSuccessStatusCode)
        {
            throw new Exception($"Lỗi tải danh sách đăng ký (HTTP {response.StatusCode})");
        }

        var result = JsonSerializer.Deserialize<ApiResponse<List<EventRegistrationDto>>>(content, _jsonOptions);
        return result?.Data ?? new List<EventRegistrationDto>();
    }

    public static async Task<string> CheckInAttendeeAsync(Guid eventId, Guid userId)
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

        var response = await _httpClient.SendAsync(request);
        var content = await response.Content.ReadAsStringAsync();

        if (!response.IsSuccessStatusCode)
        {
            var err = JsonSerializer.Deserialize<ApiResponse<string>>(content, _jsonOptions);
            throw new Exception(err?.Message ?? $"Lỗi điểm danh (HTTP {response.StatusCode})");
        }

        var result = JsonSerializer.Deserialize<ApiResponse<string>>(content, _jsonOptions);
        return result?.Message ?? "Điểm danh thành công!";
    }

    public static async Task<List<ContentSourceDto>> GetSourcesAsync()
    {
        var request = new HttpRequestMessage(HttpMethod.Get, GetUrl("api/admin/sources"));
        SetAuthHeader(request);

        var response = await _httpClient.SendAsync(request);
        var content = await response.Content.ReadAsStringAsync();

        if (!response.IsSuccessStatusCode)
        {
            throw new Exception($"Lỗi tải danh sách nguồn tự động (HTTP {response.StatusCode})");
        }

        var result = JsonSerializer.Deserialize<ApiResponse<List<ContentSourceDto>>>(content, _jsonOptions);
        return result?.Data ?? new List<ContentSourceDto>();
    }

    public static async Task<string> TriggerSourceAsync(Guid sourceId)
    {
        var request = new HttpRequestMessage(HttpMethod.Post, GetUrl($"api/admin/sources/trigger/{sourceId}"));
        SetAuthHeader(request);

        var response = await _httpClient.SendAsync(request);
        var content = await response.Content.ReadAsStringAsync();

        if (!response.IsSuccessStatusCode)
        {
            var err = JsonSerializer.Deserialize<ApiResponse<string>>(content, _jsonOptions);
            throw new Exception(err?.Message ?? $"Lỗi đồng bộ nguồn (HTTP {response.StatusCode})");
        }

        var result = JsonSerializer.Deserialize<ApiResponse<string>>(content, _jsonOptions);
        return result?.Message ?? "Đồng bộ thành công!";
    }
}
