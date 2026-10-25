package com.visionary.studentconnect.models;

import com.google.gson.annotations.SerializedName;

public class EventModels {

    public static class EventItem {
        @SerializedName("id")
        private String id;

        @SerializedName("title")
        private String title;

        @SerializedName("slug")
        private String slug;

        @SerializedName("description")
        private String description;

        @SerializedName("location")
        private String location;

        @SerializedName("startTime")
        private String startTime;

        @SerializedName("endTime")
        private String endTime;

        @SerializedName("maxCapacity")
        private int maxCapacity;

        @SerializedName("currentRegistrationsCount")
        private int currentRegistrationsCount;

        @SerializedName("status")
        private String status;

        @SerializedName("isRegisteredByCurrentUser")
        private boolean isRegisteredByCurrentUser;

        @SerializedName("qrCheckInCode")
        private String qrCheckInCode;

        public String getId() { return id; }
        public String getTitle() { return title; }
        public String getSlug() { return slug; }
        public String getDescription() { return description; }
        public String getLocation() { return location; }
        public String getStartTime() { return startTime; }
        public String getEndTime() { return endTime; }
        public int getMaxCapacity() { return maxCapacity; }
        public int getCurrentRegistrationsCount() { return currentRegistrationsCount; }
        public String getStatus() { return status; }
        public boolean isRegisteredByCurrentUser() { return isRegisteredByCurrentUser; }
        public String getQrCheckInCode() { return qrCheckInCode; }

        public void setRegisteredByCurrentUser(boolean registered) {
            this.isRegisteredByCurrentUser = registered;
        }
    }
}
