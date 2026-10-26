package com.visionary.studentconnect.api;

import com.google.gson.Gson;
import com.visionary.studentconnect.models.ApiResponse;
import java.io.IOException;
import java.net.ConnectException;
import java.net.SocketTimeoutException;
import java.net.UnknownHostException;
import okhttp3.ResponseBody;
import retrofit2.Response;

public class ApiErrorParser {
    private static final Gson gson = new Gson();

    /**
     * Extracts a user-friendly error message from a Retrofit Response.
     */
    public static String parseError(Response<?> response) {
        if (response == null) {
            return "Phản hồi máy chủ không xác định.";
        }

        if (response.isSuccessful()) {
            return null;
        }

        // Try extracting structured error from response errorBody
        ResponseBody errorBody = response.errorBody();
        if (errorBody != null) {
            try {
                String errorJson = errorBody.string();
                if (errorJson != null && !errorJson.trim().isEmpty()) {
                    ApiResponse<?> parsed = gson.fromJson(errorJson, ApiResponse.class);
                    if (parsed != null) {
                        String firstError = parsed.getFirstError();
                        if (firstError != null && !firstError.trim().isEmpty()) {
                            return firstError.trim();
                        }
                        if (parsed.getMessage() != null && !parsed.getMessage().trim().isEmpty()) {
                            return parsed.getMessage().trim();
                        }
                    }
                }
            } catch (Exception ignored) {
                // If body wasn't JSON (e.g. HTML gateway error), fall back to HTTP status code message
            }
        }

        // Fallback to HTTP status code classification
        return getHttpStatusMessage(response.code());
    }

    /**
     * Map HTTP status codes to user-friendly Vietnamese messages.
     */
    public static String getHttpStatusMessage(int statusCode) {
        switch (statusCode) {
            case 400:
                return "Dữ liệu yêu cầu không hợp lệ (400 Bad Request).";
            case 401:
                return "Phiên đăng nhập đã hết hạn hoặc không hợp lệ. Vui lòng đăng nhập lại (401).";
            case 403:
                return "Bạn không có quyền thực hiện thao tác này (403 Forbidden).";
            case 404:
                return "Không tìm thấy dữ liệu yêu cầu trên máy chủ (404 Not Found).";
            case 408:
                return "Yêu cầu mạng bị quá thời gian chờ (408 Request Timeout).";
            case 409:
                return "Dữ liệu bị xung đột hoặc đã tồn tại trên hệ thống (409 Conflict).";
            case 429:
                return "Bạn đã gửi quá nhiều yêu cầu. Vui lòng thử lại sau giây lát (429 Too Many Requests).";
            case 500:
                return "Lỗi máy chủ nội bộ. Vui lòng liên hệ ban quản trị hoặc thử lại sau (500).";
            case 502:
            case 503:
            case 504:
                return "Máy chủ đang khởi động hoặc tạm thời gián đoạn (Cold Start / 503). Vui lòng thử lại sau 30 giây.";
            default:
                return "Máy chủ phản hồi mã lỗi HTTP " + statusCode + ".";
        }
    }

    /**
     * Classifies Network / IO throwables into user-friendly messages.
     */
    public static String parseThrowable(Throwable t) {
        if (t == null) {
            return "Lỗi kết nối không xác định.";
        }

        if (t instanceof SocketTimeoutException) {
            return "Quá thời gian kết nối (Timeout). Máy chủ backend có thể đang khởi động (Cold Start), vui lòng thử lại sau ít phút.";
        }

        if (t instanceof UnknownHostException) {
            return "Không thể phân giải địa chỉ máy chủ. Vui lòng kiểm tra lại URL máy chủ hoặc kết nối mạng.";
        }

        if (t instanceof ConnectException) {
            return "Không thể kết nối đến máy chủ API. Vui lòng kiểm tra máy chủ backend có đang hoạt động hay không.";
        }

        if (t instanceof IOException) {
            return "Lỗi truyền thông mạng: " + t.getLocalizedMessage();
        }

        return "Đã xảy ra lỗi: " + t.getLocalizedMessage();
    }
}
