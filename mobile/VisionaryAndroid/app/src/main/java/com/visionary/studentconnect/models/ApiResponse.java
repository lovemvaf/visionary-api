package com.visionary.studentconnect.models;

import com.google.gson.annotations.SerializedName;
import java.util.Collections;
import java.util.List;

public class ApiResponse<T> {
    @SerializedName("success")
    private boolean success;

    @SerializedName("message")
    private String message;

    @SerializedName("data")
    private T data;

    @SerializedName("errors")
    private List<String> errors;

    @SerializedName("timestamp")
    private String timestamp;

    public ApiResponse() {
    }

    public ApiResponse(boolean success, String message, T data, List<String> errors, String timestamp) {
        this.success = success;
        this.message = message;
        this.data = data;
        this.errors = errors;
        this.timestamp = timestamp;
    }

    public boolean isSuccess() {
        return success;
    }

    public String getMessage() {
        return message;
    }

    public T getData() {
        return data;
    }

    public List<String> getErrors() {
        return errors != null ? errors : Collections.emptyList();
    }

    public String getTimestamp() {
        return timestamp;
    }

    public String getFirstError() {
        if (errors != null && !errors.isEmpty()) {
            return errors.get(0);
        }
        return message;
    }
}
