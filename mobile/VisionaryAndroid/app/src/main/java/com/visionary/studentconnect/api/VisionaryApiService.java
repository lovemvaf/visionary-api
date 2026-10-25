package com.visionary.studentconnect.api;

import com.visionary.studentconnect.models.ApiResponse;
import com.visionary.studentconnect.models.AuthModels.AuthResponse;
import com.visionary.studentconnect.models.AuthModels.LoginRequest;
import com.visionary.studentconnect.models.AuthModels.UserProfile;
import com.visionary.studentconnect.models.ContentModels.LearningResourceItem;
import com.visionary.studentconnect.models.ContentModels.OpportunityItem;
import com.visionary.studentconnect.models.EventModels.EventItem;
import com.visionary.studentconnect.models.PagedResponse;

import java.util.List;
import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.POST;
import retrofit2.http.Path;
import retrofit2.http.Query;

public interface VisionaryApiService {

    @POST("api/auth/login")
    Call<ApiResponse<AuthResponse>> login(@Body LoginRequest request);

    @GET("api/auth/me")
    Call<ApiResponse<UserProfile>> getMe();

    @GET("api/events")
    Call<ApiResponse<PagedResponse<EventItem>>> getEvents(
            @Query("pageIndex") int pageIndex,
            @Query("pageSize") int pageSize
    );

    @POST("api/events/{id}/register")
    Call<ApiResponse<String>> registerForEvent(@Path("id") String eventId);

    @POST("api/events/{id}/cancel")
    Call<ApiResponse<String>> cancelRegistration(@Path("id") String eventId);

    @GET("api/english-for-it")
    Call<ApiResponse<PagedResponse<LearningResourceItem>>> getEnglishResources(
            @Query("pageIndex") int pageIndex,
            @Query("pageSize") int pageSize
    );

    @GET("api/opportunities")
    Call<ApiResponse<PagedResponse<OpportunityItem>>> getOpportunities(
            @Query("pageIndex") int pageIndex,
            @Query("pageSize") int pageSize
    );
}
