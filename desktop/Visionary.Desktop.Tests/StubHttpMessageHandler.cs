using System.Net;

namespace Visionary.Desktop.Tests;

/// <summary>
/// HttpMessageHandler giả lập để kiểm thử ApiClient mà không cần chạy backend thật.
/// </summary>
public sealed class StubHttpMessageHandler : HttpMessageHandler
{
    private readonly Func<HttpRequestMessage, CancellationToken, Task<HttpResponseMessage>> _responder;

    public StubHttpMessageHandler(Func<HttpRequestMessage, CancellationToken, Task<HttpResponseMessage>> responder)
    {
        _responder = responder;
    }

    public StubHttpMessageHandler(HttpStatusCode statusCode, string content)
        : this((_, _) => Task.FromResult(new HttpResponseMessage(statusCode)
        {
            Content = new StringContent(content)
        }))
    {
    }

    public static StubHttpMessageHandler Json(HttpStatusCode statusCode, string json)
        => new(statusCode, json);

    /// <summary>Handler luôn ném lỗi mạng (ví dụ máy chủ không chạy).</summary>
    public static StubHttpMessageHandler NetworkFailure()
        => new((_, _) => throw new HttpRequestException("Không thể kết nối tới máy chủ"));

    /// <summary>Handler bị treo cho tới khi token hủy (mô phỏng máy chủ không phản hồi).</summary>
    public static StubHttpMessageHandler NeverRespond()
        => new(async (_, ct) =>
        {
            await Task.Delay(Timeout.Infinite, ct);
            return new HttpResponseMessage(HttpStatusCode.OK);
        });

    protected override Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
        => _responder(request, cancellationToken);
}
