package com.visionary.studentconnect.ui.fragments;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Toast;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout;
import com.visionary.studentconnect.R;
import com.visionary.studentconnect.api.ApiClient;
import com.visionary.studentconnect.models.ApiResponse;
import com.visionary.studentconnect.models.EventModels.EventItem;
import com.visionary.studentconnect.models.PagedResponse;
import com.visionary.studentconnect.ui.adapters.EventsAdapter;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class EventsFragment extends Fragment {
    private EventsAdapter adapter;
    private SwipeRefreshLayout swipeRefresh;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View v = inflater.inflate(R.layout.fragment_events, container, false);

        swipeRefresh = v.findViewById(R.id.swipeRefresh);
        RecyclerView rv = v.findViewById(R.id.rvEvents);
        rv.setLayoutManager(new LinearLayoutManager(getContext()));

        adapter = new EventsAdapter(requireContext());
        rv.setAdapter(adapter);

        swipeRefresh.setOnRefreshListener(this::loadEvents);

        loadEvents();
        return v;
    }

    private void loadEvents() {
        if (getContext() == null) return;
        swipeRefresh.setRefreshing(true);

        ApiClient.getService(getContext()).getEvents(1, 20).enqueue(new Callback<ApiResponse<PagedResponse<EventItem>>>() {
            @Override
            public void onResponse(@NonNull Call<ApiResponse<PagedResponse<EventItem>>> call, @NonNull Response<ApiResponse<PagedResponse<EventItem>>> response) {
                swipeRefresh.setRefreshing(false);
                if (response.isSuccessful() && response.body() != null && response.body().isSuccess()) {
                    PagedResponse<EventItem> paged = response.body().getData();
                    if (paged != null) {
                        adapter.setEvents(paged.getItems());
                    }
                } else {
                    Toast.makeText(getContext(), "Không thể tải danh sách sự kiện", Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(@NonNull Call<ApiResponse<PagedResponse<EventItem>>> call, @NonNull Throwable t) {
                swipeRefresh.setRefreshing(false);
                Toast.makeText(getContext(), "Lỗi mạng: " + t.getMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }
}
