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
import com.visionary.studentconnect.api.ApiErrorParser;
import com.visionary.studentconnect.models.ApiResponse;
import com.visionary.studentconnect.models.ContentModels.LearningResourceItem;
import com.visionary.studentconnect.models.PagedResponse;
import com.visionary.studentconnect.ui.adapters.EnglishAdapter;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class EnglishForItFragment extends Fragment {
    private EnglishAdapter adapter;
    private SwipeRefreshLayout swipeRefresh;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View v = inflater.inflate(R.layout.fragment_english, container, false);

        swipeRefresh = v.findViewById(R.id.swipeRefresh);
        RecyclerView rv = v.findViewById(R.id.rvEnglish);
        rv.setLayoutManager(new LinearLayoutManager(getContext()));

        adapter = new EnglishAdapter();
        rv.setAdapter(adapter);

        swipeRefresh.setOnRefreshListener(this::loadResources);

        loadResources();
        return v;
    }

    private void loadResources() {
        if (!isAdded() || getContext() == null) return;
        swipeRefresh.setRefreshing(true);

        ApiClient.getService(requireContext()).getEnglishResources(1, 20).enqueue(new Callback<ApiResponse<PagedResponse<LearningResourceItem>>>() {
            @Override
            public void onResponse(@NonNull Call<ApiResponse<PagedResponse<LearningResourceItem>>> call, @NonNull Response<ApiResponse<PagedResponse<LearningResourceItem>>> response) {
                if (!isAdded() || getContext() == null) return;
                swipeRefresh.setRefreshing(false);
                if (response.isSuccessful() && response.body() != null && response.body().isSuccess() && response.body().getData() != null) {
                    adapter.setItems(response.body().getData().getSafeItems());
                } else {
                    String msg = ApiErrorParser.parseError(response);
                    Toast.makeText(getContext(), msg != null ? msg : "Không thể tải danh sách tài liệu", Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(@NonNull Call<ApiResponse<PagedResponse<LearningResourceItem>>> call, @NonNull Throwable t) {
                if (!isAdded() || getContext() == null) return;
                swipeRefresh.setRefreshing(false);
                Toast.makeText(getContext(), ApiErrorParser.parseThrowable(t), Toast.LENGTH_SHORT).show();
            }
        });
    }
}
