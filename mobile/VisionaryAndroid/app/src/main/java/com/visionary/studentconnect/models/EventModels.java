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

        public EventItem() {
        }

        public EventItem(String id, String title, String slug, String description, String location,
                         String startTime, String endTime, int maxCapacity, int currentRegistrationsCount,
                         String status, boolean isRegisteredByCurrentUser, String qrCheckInCode) {
            this.id = id;
            this.title = title;
            this.slug = slug;
            this.description = description;
            this.location = location;
            this.startTime = startTime;
            this.endTime = endTime;
            this.maxCapacity = maxCapacity;
            this.currentRegistrationsCount = currentRegistrationsCount;
            this.status = status;
            this.isRegisteredByCurrentUser = isRegisteredByCurrentUser;
            this.qrCheckInCode = qrCheckInCode;
        }

        public String getId() { return id; }
        public String getTitle() { return title; }
        public String getSlug() { return slug; }
        public String getDescription() { return description; }
        public String getLocation() { return location != null ? location : "DNTU"; }
        public String getStartTime() { return startTime; }
        public String getEndTime() { return endTime; }
        public int getMaxCapacity() { return maxCapacity; }
        public int getCurrentRegistrationsCount() { return currentRegistrationsCount; }
        public String getStatus() { return status != null ? status : "Active"; }
        public boolean isRegisteredByCurrentUser() { return isRegisteredByCurrentUser; }
        public String getQrCheckInCode() { return qrCheckInCode; }

        public void setRegisteredByCurrentUser(boolean registered) {
            this.isRegisteredByCurrentUser = registered;
        }
    }
}
