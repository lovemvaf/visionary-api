package com.visionary.studentconnect.models;

import com.google.gson.annotations.SerializedName;

public class ContentModels {

    public static class LearningResourceItem {
        @SerializedName("id")
        private String id;

        @SerializedName("title")
        private String title;

        @SerializedName("category")
        private String category;

        @SerializedName("level")
        private String level;

        @SerializedName("contentMarkdown")
        private String contentMarkdown;

        @SerializedName("sampleSentence")
        private String sampleSentence;

        public String getId() { return id; }
        public String getTitle() { return title; }
        public String getCategory() { return category; }
        public String getLevel() { return level; }
        public String getContentMarkdown() { return contentMarkdown; }
        public String getSampleSentence() { return sampleSentence; }
    }

    public static class OpportunityItem {
        @SerializedName("id")
        private String id;

        @SerializedName("title")
        private String title;

        @SerializedName("organizer")
        private String organizer;

        @SerializedName("category")
        private String category;

        @SerializedName("description")
        private String description;

        @SerializedName("deadline")
        private String deadline;

        @SerializedName("location")
        private String location;

        @SerializedName("officialUrl")
        private String officialUrl;

        public String getId() { return id; }
        public String getTitle() { return title; }
        public String getOrganizer() { return organizer; }
        public String getCategory() { return category; }
        public String getDescription() { return description; }
        public String getDeadline() { return deadline; }
        public String getLocation() { return location; }
        public String getOfficialUrl() { return officialUrl; }
    }
}
