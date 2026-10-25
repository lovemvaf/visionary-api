package com.visionary.studentconnect.models;

import com.google.gson.annotations.SerializedName;
import java.util.List;

public class AuthModels {

    public static class LoginRequest {
        @SerializedName("email")
        private String email;

        @SerializedName("password")
        private String password;

        public LoginRequest(String email, String password) {
            this.email = email;
            this.password = password;
        }

        public String getEmail() { return email; }
        public String getPassword() { return password; }
    }

    public static class AuthResponse {
        @SerializedName("token")
        private String token;

        @SerializedName("expiresAt")
        private String expiresAt;

        @SerializedName("user")
        private UserProfile user;

        public String getToken() { return token; }
        public String getExpiresAt() { return expiresAt; }
        public UserProfile getUser() { return user; }
    }

    public static class UserProfile {
        @SerializedName("id")
        private String id;

        @SerializedName("email")
        private String email;

        @SerializedName("fullName")
        private String fullName;

        @SerializedName("studentId")
        private String studentId;

        @SerializedName("department")
        private String department;

        @SerializedName("roles")
        private List<String> roles;

        @SerializedName("isMember")
        private boolean isMember;

        @SerializedName("clubRole")
        private String clubRole;

        public String getId() { return id; }
        public String getEmail() { return email; }
        public String getFullName() { return fullName; }
        public String getStudentId() { return studentId; }
        public String getDepartment() { return department; }
        public List<String> getRoles() { return roles; }
        public boolean isMember() { return isMember; }
        public String getClubRole() { return clubRole; }
    }
}
