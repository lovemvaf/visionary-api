package com.visionary.studentconnect.models;

import com.google.gson.annotations.SerializedName;
import java.util.Collections;
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

    @SerializedName("totalPages")
    private int totalPages;

    @SerializedName("hasNextPage")
    private boolean hasNextPage;

    @SerializedName("hasPreviousPage")
    private boolean hasPreviousPage;

    public PagedResponse() {
    }

    public PagedResponse(List<T> items, int totalCount, int pageIndex, int pageSize, int totalPages, boolean hasNextPage, boolean hasPreviousPage) {
        this.items = items;
        this.totalCount = totalCount;
        this.pageIndex = pageIndex;
        this.pageSize = pageSize;
        this.totalPages = totalPages;
        this.hasNextPage = hasNextPage;
        this.hasPreviousPage = hasPreviousPage;
    }

    public List<T> getItems() {
        return items;
    }

    public List<T> getSafeItems() {
        return items != null ? items : Collections.emptyList();
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

    public int getTotalPages() {
        return totalPages;
    }

    public boolean hasNextPage() {
        return hasNextPage;
    }

    public boolean hasPreviousPage() {
        return hasPreviousPage;
    }
}
