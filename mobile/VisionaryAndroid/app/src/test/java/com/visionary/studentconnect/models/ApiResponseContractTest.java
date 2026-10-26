package com.visionary.studentconnect.models;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import com.visionary.studentconnect.models.AuthModels.AuthResponse;
import com.visionary.studentconnect.models.EventModels.EventItem;
import java.lang.reflect.Type;
import org.junit.Assert;
import org.junit.Test;

public class ApiResponseContractTest {
    private final Gson gson = new Gson();

    @Test
    public void testAuthResponseDeserialization() {
        String json = "{\n" +
                "  \"success\": true,\n" +
                "  \"message\": \"Đăng nhập thành công\",\n" +
                "  \"data\": {\n" +
                "    \"token\": \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.dummy_token\",\n" +
                "    \"expiresAt\": \"2026-10-27T00:00:00Z\",\n" +
                "    \"user\": {\n" +
                "      \"id\": \"user-001\",\n" +
                "      \"email\": \"trikhang@dntu.edu.vn\",\n" +
                "      \"fullName\": \"Đào Trí Khang\",\n" +
                "      \"studentId\": \"22001122\",\n" +
                "      \"department\": \"Công nghệ Thông tin\",\n" +
                "      \"roles\": [\"Student\", \"ClubMember\"],\n" +
                "      \"isMember\": true,\n" +
                "      \"clubRole\": \"Member\"\n" +
                "    }\n" +
                "  },\n" +
                "  \"errors\": [],\n" +
                "  \"timestamp\": \"2026-10-26T11:00:00Z\"\n" +
                "}";

        Type type = new TypeToken<ApiResponse<AuthResponse>>() {}.getType();
        ApiResponse<AuthResponse> response = gson.fromJson(json, type);

        Assert.assertNotNull(response);
        Assert.assertTrue(response.isSuccess());
        Assert.assertEquals("Đăng nhập thành công", response.getMessage());
        Assert.assertEquals("2026-10-26T11:00:00Z", response.getTimestamp());
        Assert.assertNotNull(response.getData());
        Assert.assertEquals("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.dummy_token", response.getData().getToken());
        Assert.assertNotNull(response.getData().getUser());
        Assert.assertEquals("Đào Trí Khang", response.getData().getUser().getFullName());
        Assert.assertEquals("22001122", response.getData().getUser().getStudentId());
        Assert.assertTrue(response.getData().getUser().isMember());
        Assert.assertEquals(2, response.getData().getUser().getRoles().size());
        Assert.assertTrue(response.getErrors().isEmpty());
    }

    @Test
    public void testPagedEventsResponseDeserialization() {
        String json = "{\n" +
                "  \"success\": true,\n" +
                "  \"message\": \"Success\",\n" +
                "  \"data\": {\n" +
                "    \"items\": [\n" +
                "      {\n" +
                "        \"id\": \"evt-001\",\n" +
                "        \"title\": \"Workshop Mobile App Development\",\n" +
                "        \"slug\": \"workshop-mobile-app\",\n" +
                "        \"description\": \"Xây dựng ứng dụng Android kết nối REST API\",\n" +
                "        \"location\": \"Phòng Lab CNTT\",\n" +
                "        \"startTime\": \"2026-11-05T08:00:00Z\",\n" +
                "        \"endTime\": \"2026-11-05T11:30:00Z\",\n" +
                "        \"maxCapacity\": 80,\n" +
                "        \"currentRegistrationsCount\": 45,\n" +
                "        \"status\": \"Published\",\n" +
                "        \"isRegisteredByCurrentUser\": true,\n" +
                "        \"qrCheckInCode\": \"QR-MOBILE-001\"\n" +
                "      }\n" +
                "    ],\n" +
                "    \"totalCount\": 25,\n" +
                "    \"pageIndex\": 1,\n" +
                "    \"pageSize\": 20,\n" +
                "    \"totalPages\": 2,\n" +
                "    \"hasNextPage\": true,\n" +
                "    \"hasPreviousPage\": false\n" +
                "  },\n" +
                "  \"errors\": [],\n" +
                "  \"timestamp\": \"2026-10-26T11:00:00Z\"\n" +
                "}";

        Type type = new TypeToken<ApiResponse<PagedResponse<EventItem>>>() {}.getType();
        ApiResponse<PagedResponse<EventItem>> response = gson.fromJson(json, type);

        Assert.assertNotNull(response);
        Assert.assertTrue(response.isSuccess());
        Assert.assertNotNull(response.getData());

        PagedResponse<EventItem> paged = response.getData();
        Assert.assertEquals(25, paged.getTotalCount());
        Assert.assertEquals(1, paged.getPageIndex());
        Assert.assertEquals(20, paged.getPageSize());
        Assert.assertEquals(2, paged.getTotalPages());
        Assert.assertTrue(paged.hasNextPage());
        Assert.assertFalse(paged.hasPreviousPage());
        Assert.assertEquals(1, paged.getSafeItems().size());

        EventItem item = paged.getSafeItems().get(0);
        Assert.assertEquals("evt-001", item.getId());
        Assert.assertEquals("Workshop Mobile App Development", item.getTitle());
        Assert.assertEquals("Phòng Lab CNTT", item.getLocation());
        Assert.assertEquals(80, item.getMaxCapacity());
        Assert.assertEquals(45, item.getCurrentRegistrationsCount());
        Assert.assertTrue(item.isRegisteredByCurrentUser());
        Assert.assertEquals("QR-MOBILE-001", item.getQrCheckInCode());
    }

    @Test
    public void testErrorResponseDeserializationWithErrorsList() {
        String json = "{\n" +
                "  \"success\": false,\n" +
                "  \"message\": \"Xác thực thất bại\",\n" +
                "  \"data\": null,\n" +
                "  \"errors\": [\n" +
                "    \"Mật khẩu không chính xác\",\n" +
                "    \"Vui lòng thử lại sau ít phút\"\n" +
                "  ],\n" +
                "  \"timestamp\": \"2026-10-26T11:00:00Z\"\n" +
                "}";

        Type type = new TypeToken<ApiResponse<Void>>() {}.getType();
        ApiResponse<Void> response = gson.fromJson(json, type);

        Assert.assertNotNull(response);
        Assert.assertFalse(response.isSuccess());
        Assert.assertEquals("Xác thực thất bại", response.getMessage());
        Assert.assertEquals(2, response.getErrors().size());
        Assert.assertEquals("Mật khẩu không chính xác", response.getFirstError());
    }

    @Test
    public void testPagedResponseNullSafety() {
        PagedResponse<EventItem> emptyPaged = new PagedResponse<>();
        Assert.assertNotNull(emptyPaged.getSafeItems());
        Assert.assertTrue(emptyPaged.getSafeItems().isEmpty());
    }
}
