package com.visionary.studentconnect.models;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import com.visionary.studentconnect.models.ContentModels.LearningResourceItem;
import com.visionary.studentconnect.models.ContentModels.OpportunityItem;
import java.lang.reflect.Type;
import org.junit.Assert;
import org.junit.Test;

public class ContentModelsContractTest {
    private final Gson gson = new Gson();

    @Test
    public void testEnglishForItResourceDeserialization() {
        String json = "{\n" +
                "  \"id\": \"eng-001\",\n" +
                "  \"title\": \"RESTful API\",\n" +
                "  \"category\": \"Web Services\",\n" +
                "  \"level\": \"Intermediate\",\n" +
                "  \"contentMarkdown\": \"An architectural style for network applications using HTTP verbs.\",\n" +
                "  \"sampleSentence\": \"Our team builds a RESTful API with ASP.NET Core 8.\"\n" +
                "}";

        LearningResourceItem item = gson.fromJson(json, LearningResourceItem.class);
        Assert.assertNotNull(item);
        Assert.assertEquals("eng-001", item.getId());
        Assert.assertEquals("RESTful API", item.getTitle());
        Assert.assertEquals("Web Services", item.getCategory());
        Assert.assertEquals("Intermediate", item.getLevel());
        Assert.assertEquals("An architectural style for network applications using HTTP verbs.", item.getContentMarkdown());
        Assert.assertEquals("Our team builds a RESTful API with ASP.NET Core 8.", item.getSampleSentence());
    }

    @Test
    public void testOpportunityItemDeserialization() {
        String json = "{\n" +
                "  \"id\": \"opp-001\",\n" +
                "  \"title\": \"Google Summer of Code 2026\",\n" +
                "  \"organizer\": \"Google Open Source\",\n" +
                "  \"category\": \"Global Internship\",\n" +
                "  \"description\": \"Chương trình thực tập phát triển nguồn mở quốc tế\",\n" +
                "  \"deadline\": \"2026-04-15T23:59:59Z\",\n" +
                "  \"location\": \"Remote / Toàn cầu\",\n" +
                "  \"officialUrl\": \"https://summerofcode.withgoogle.com\"\n" +
                "}";

        OpportunityItem item = gson.fromJson(json, OpportunityItem.class);
        Assert.assertNotNull(item);
        Assert.assertEquals("opp-001", item.getId());
        Assert.assertEquals("Google Summer of Code 2026", item.getTitle());
        Assert.assertEquals("Google Open Source", item.getOrganizer());
        Assert.assertEquals("Global Internship", item.getCategory());
        Assert.assertEquals("2026-04-15T23:59:59Z", item.getDeadline());
        Assert.assertEquals("Remote / Toàn cầu", item.getLocation());
        Assert.assertEquals("https://summerofcode.withgoogle.com", item.getOfficialUrl());
    }
}
