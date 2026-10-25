package com.visionary.studentconnect.utils;

import android.content.Context;
import android.content.SharedPreferences;
import com.visionary.studentconnect.models.AuthModels.UserProfile;

public class SessionManager {
    private static final String PREF_NAME = "visionary_session";
    private static final String KEY_TOKEN = "jwt_token";
    private static final String KEY_BASE_URL = "base_url";
    private static final String KEY_FULL_NAME = "full_name";
    private static final String KEY_EMAIL = "email";
    private static final String KEY_ROLES = "roles";
    private static final String KEY_IS_MEMBER = "is_member";

    private final SharedPreferences prefs;

    public SessionManager(Context context) {
        prefs = context.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE);
    }

    public void saveBaseUrl(String url) {
        prefs.edit().putString(KEY_BASE_URL, url).apply();
    }

    public String getBaseUrl() {
        return prefs.getString(KEY_BASE_URL, "http://10.0.2.2:5000/");
    }

    public void saveAuth(String token, UserProfile user) {
        SharedPreferences.Editor editor = prefs.edit();
        editor.putString(KEY_TOKEN, token);
        if (user != null) {
            editor.putString(KEY_FULL_NAME, user.getFullName());
            editor.putString(KEY_EMAIL, user.getEmail());
            editor.putString(KEY_ROLES, user.getRoles() != null ? String.join(", ", user.getRoles()) : "");
            editor.putBoolean(KEY_IS_MEMBER, user.isMember());
        }
        editor.apply();
    }

    public String getToken() {
        return prefs.getString(KEY_TOKEN, null);
    }

    public boolean isLoggedIn() {
        return getToken() != null && !getToken().isEmpty();
    }

    public String getFullName() {
        return prefs.getString(KEY_FULL_NAME, "Sinh viên");
    }

    public String getEmail() {
        return prefs.getString(KEY_EMAIL, "");
    }

    public String getRoles() {
        return prefs.getString(KEY_ROLES, "Student");
    }

    public void clear() {
        prefs.edit().remove(KEY_TOKEN).remove(KEY_FULL_NAME).remove(KEY_EMAIL).remove(KEY_ROLES).apply();
    }
}
