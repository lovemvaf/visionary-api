package com.visionary.studentconnect.api;

import android.content.Context;
import com.visionary.studentconnect.utils.SessionManager;
import java.util.concurrent.TimeUnit;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.logging.HttpLoggingInterceptor;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class ApiClient {
    private static VisionaryApiService apiService;
    private static String currentBaseUrl;

    public static synchronized VisionaryApiService getService(Context context) {
        Context appContext = context != null ? context.getApplicationContext() : null;
        SessionManager session = new SessionManager(appContext != null ? appContext : context);
        String baseUrl = session.getBaseUrl();
        if (!baseUrl.endsWith("/")) {
            baseUrl += "/";
        }

        if (apiService == null || !baseUrl.equals(currentBaseUrl)) {
            currentBaseUrl = baseUrl;

            HttpLoggingInterceptor logging = new HttpLoggingInterceptor();
            // Log headers to avoid leaking sensitive credentials/tokens in request/response bodies in logcat
            logging.setLevel(HttpLoggingInterceptor.Level.HEADERS);

            OkHttpClient client = new OkHttpClient.Builder()
                    .connectTimeout(30, TimeUnit.SECONDS)
                    .readTimeout(30, TimeUnit.SECONDS)
                    .writeTimeout(30, TimeUnit.SECONDS)
                    .addInterceptor(chain -> {
                        Request original = chain.request();
                        Request.Builder builder = original.newBuilder();

                        String token = session.getToken();
                        if (token != null && !token.isEmpty()) {
                            builder.header("Authorization", "Bearer " + token);
                        }
                        builder.header("Accept", "application/json");

                        return chain.proceed(builder.build());
                    })
                    .addInterceptor(logging)
                    .build();

            Retrofit retrofit = new Retrofit.Builder()
                    .baseUrl(baseUrl)
                    .client(client)
                    .addConverterFactory(GsonConverterFactory.create())
                    .build();

            apiService = retrofit.create(VisionaryApiService.class);
        }

        return apiService;
    }

    public static synchronized void resetService() {
        apiService = null;
        currentBaseUrl = null;
    }
}
