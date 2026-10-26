package com.visionary.studentconnect.api;

import java.io.IOException;
import java.net.ConnectException;
import java.net.SocketTimeoutException;
import java.net.UnknownHostException;
import okhttp3.MediaType;
import okhttp3.ResponseBody;
import org.junit.Assert;
import org.junit.Test;
import retrofit2.Response;

public class ApiErrorParserTest {

    @Test
    public void testParseErrorWithStructuredBackendErrorJson() {
        String errorJson = "{\n" +
                "  \"success\": false,\n" +
                "  \"message\": \"Thao tác không hợp lệ\",\n" +
                "  \"errors\": [\"Sự kiện này đã đạt giới hạn số lượng sinh viên đăng ký!\"],\n" +
                "  \"timestamp\": \"2026-10-26T11:00:00Z\"\n" +
                "}";

        ResponseBody body = ResponseBody.create(MediaType.parse("application/json"), errorJson);
        Response<Void> response = Response.error(400, body);

        String result = ApiErrorParser.parseError(response);
        Assert.assertEquals("Sự kiện này đã đạt giới hạn số lượng sinh viên đăng ký!", result);
    }

    @Test
    public void testParseErrorWithBackendMessageFallback() {
        String errorJson = "{\n" +
                "  \"success\": false,\n" +
                "  \"message\": \"Tài khoản của bạn chưa được cấp quyền tham gia\",\n" +
                "  \"errors\": []\n" +
                "}";

        ResponseBody body = ResponseBody.create(MediaType.parse("application/json"), errorJson);
        Response<Void> response = Response.error(403, body);

        String result = ApiErrorParser.parseError(response);
        Assert.assertEquals("Tài khoản của bạn chưa được cấp quyền tham gia", result);
    }

    @Test
    public void testParseErrorWithHtmlBodyFallbackToStatusCode() {
        String html502 = "<html><head><title>502 Bad Gateway</title></head><body>nginx</body></html>";
        ResponseBody body = ResponseBody.create(MediaType.parse("text/html"), html502);
        Response<Void> response = Response.error(502, body);

        String result = ApiErrorParser.parseError(response);
        Assert.assertTrue(result.contains("Cold Start") || result.contains("503") || result.contains("502"));
    }

    @Test
    public void testParseErrorHttpStatusCodes() {
        Assert.assertTrue(ApiErrorParser.getHttpStatusMessage(401).contains("Phiên đăng nhập đã hết hạn"));
        Assert.assertTrue(ApiErrorParser.getHttpStatusMessage(403).contains("không có quyền"));
        Assert.assertTrue(ApiErrorParser.getHttpStatusMessage(404).contains("Không tìm thấy"));
        Assert.assertTrue(ApiErrorParser.getHttpStatusMessage(500).contains("Lỗi máy chủ nội bộ"));
        Assert.assertTrue(ApiErrorParser.getHttpStatusMessage(503).contains("Cold Start"));
    }

    @Test
    public void testParseErrorSuccessfulResponseReturnsNull() {
        Response<String> successResponse = Response.success("OK");
        Assert.assertNull(ApiErrorParser.parseError(successResponse));
    }

    @Test
    public void testParseThrowableTimeout() {
        Throwable t = new SocketTimeoutException("connect timed out");
        String msg = ApiErrorParser.parseThrowable(t);
        Assert.assertTrue(msg.contains("Timeout") || msg.contains("Cold Start"));
    }

    @Test
    public void testParseThrowableUnknownHost() {
        Throwable t = new UnknownHostException("api.visionary.internal");
        String msg = ApiErrorParser.parseThrowable(t);
        Assert.assertTrue(msg.contains("URL") || msg.contains("máy chủ"));
    }

    @Test
    public void testParseThrowableConnectException() {
        Throwable t = new ConnectException("Connection refused");
        String msg = ApiErrorParser.parseThrowable(t);
        Assert.assertTrue(msg.contains("kết nối"));
    }

    @Test
    public void testParseThrowableGenericIOException() {
        Throwable t = new IOException("Broken pipe");
        String msg = ApiErrorParser.parseThrowable(t);
        Assert.assertTrue(msg.contains("Broken pipe"));
    }
}
