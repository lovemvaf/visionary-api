using System;

namespace Visionary.Desktop.Services;

/// <summary>
/// Phân loại lỗi khi giao tiếp với ASP.NET Core Web API.
/// Cho phép Desktop phân biệt rõ: timeout, lỗi mạng, token hết hạn,
/// không đủ quyền và lỗi nghiệp vụ từ backend.
/// </summary>
public enum ApiErrorKind
{
    /// <summary>Máy chủ không phản hồi trong thời gian chờ (timeout).</summary>
    Timeout = 0,

    /// <summary>Không kết nối được tới máy chủ (DNS, socket, máy chủ chưa chạy).</summary>
    Network = 1,

    /// <summary>HTTP 401 - token thiếu, sai hoặc đã hết hạn.</summary>
    Unauthorized = 2,

    /// <summary>HTTP 403 - tài khoản không đủ quyền (thiếu role Admin/Committee).</summary>
    Forbidden = 3,

    /// <summary>Lỗi phía người dùng (HTTP 4xx khác) hoặc lỗi nghiệp vụ trả về bởi backend.</summary>
    Client = 4,

    /// <summary>Lỗi phía máy chủ (HTTP 5xx).</summary>
    Server = 5,

    /// <summary>Phản hồi HTTP 200 nhưng nội dung JSON không hợp lệ hoặc thiếu dữ liệu.</summary>
    InvalidResponse = 6
}

/// <summary>
/// Lỗi có cấu trúc từ tầng giao tiếp API của Desktop client.
/// </summary>
public class ApiException : Exception
{
    public ApiException(ApiErrorKind kind, string message, int? statusCode = null, Exception? innerException = null)
        : base(message, innerException)
    {
        Kind = kind;
        StatusCode = statusCode;
    }

    /// <summary>Loại lỗi để UI quyết định cách hiển thị thông báo.</summary>
    public ApiErrorKind Kind { get; }

    /// <summary>Mã HTTP gốc (nếu có).</summary>
    public int? StatusCode { get; }

    /// <summary>True nếu đây là timeout (không phải lỗi HTTP).</summary>
    public bool IsTimeout => Kind == ApiErrorKind.Timeout;

    /// <summary>True nếu phiên đăng nhập đã hết hạn cần đăng nhập lại.</summary>
    public bool IsSessionExpired => Kind == ApiErrorKind.Unauthorized;

    /// <summary>True nếu tài khoản không đủ quyền thao tác.</summary>
    public bool IsForbidden => Kind == ApiErrorKind.Forbidden;

    /// <summary>
    /// Thông điệp thân thiện dành cho người dùng cuối (quản trị viên CLB).
    /// </summary>
    public string UserMessage => Kind switch
    {
        ApiErrorKind.Timeout =>
            "Hết thời gian chờ phản hồi từ máy chủ. Máy chủ backend có thể đang khởi động hoặc mạng đang chậm, vui lòng thử lại.",
        ApiErrorKind.Network =>
            "Không kết nối được tới máy chủ API. Kiểm tra lại địa chỉ máy chủ và đảm bảo backend đang chạy.",
        ApiErrorKind.Unauthorized =>
            "Phiên đăng nhập đã hết hạn hoặc không hợp lệ. Vui lòng đăng nhập lại.",
        ApiErrorKind.Forbidden =>
            "Tài khoản hiện tại không có quyền thực hiện thao tác này (cần quyền BCN hoặc Quản trị viên).",
        ApiErrorKind.Server =>
            "Máy chủ backend đang gặp lỗi (lỗi nội bộ của hệ thống). Vui lòng liên hệ quản trị viên hoặc thử lại sau.",
        ApiErrorKind.InvalidResponse =>
            "Dữ liệu phản hồi từ máy chủ không hợp lệ, không thể hiển thị.",
        _ => Message
    };
}
