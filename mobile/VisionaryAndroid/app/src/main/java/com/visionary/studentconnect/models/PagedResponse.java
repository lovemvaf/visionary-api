package com.visionary.studentconnect.models;

import com.google.gson.annotations.SerializedName;
import java.util.List;

public class PagedResponse<T> {
    @SerializedName("items")
    private List<T> items;

    @SerializedName("totalCount")
    private int totalCount;

    @SerializedName("pageIndex")
    private int pageIndex;

    @SerializedName("pageSize")
    private int pageSize;

    public List<T> getItems() {
        return items;
    }

    public int getTotalCount() {
        return totalCount;
    }

    public int getPageIndex() {
        return pageIndex;
    }

    public int getPageSize() {
        return pageSize;
    }
}
