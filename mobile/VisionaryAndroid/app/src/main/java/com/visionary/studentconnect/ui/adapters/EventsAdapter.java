package com.visionary.studentconnect.ui.adapters;

import android.app.AlertDialog;
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import com.visionary.studentconnect.R;
import com.visionary.studentconnect.api.ApiClient;
import com.visionary.studentconnect.models.ApiResponse;
import com.visionary.studentconnect.models.EventModels.EventItem;
import java.util.ArrayList;
import java.util.List;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class EventsAdapter extends RecyclerView.Adapter<EventsAdapter.EventViewHolder> {
    private final Context context;
    private final List<EventItem> events = new ArrayList<>();

    public EventsAdapter(Context context) {
        this.context = context;
    }

    public void setEvents(List<EventItem> newEvents) {
        events.clear();
        if (newEvents != null) {
            events.addAll(newEvents);
        }
        notifyDataSetChanged();
    }

    @NonNull
    @Override
    public EventViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_event, parent, false);
        return new EventViewHolder(v);
    }

    @Override
    public void onBindViewHolder(@NonNull EventViewHolder holder, int position) {
        EventItem item = events.get(position);
        holder.tvTitle.setText(item.getTitle());
        holder.tvStatus.setText(item.getStatus());
        holder.tvDesc.setText(item.getDescription());

        String info = "📍 " + (item.getLocation() != null ? item.getLocation() : "DNTU") +
                " • 👥 " + item.getCurrentRegistrationsCount() + "/" + item.getMaxCapacity();
        holder.tvInfo.setText(info);

        if (item.isRegisteredByCurrentUser()) {
            holder.btnRegister.setText("Hủy đăng ký");
            holder.btnRegister.setBackgroundColor(androidx.core.content.ContextCompat.getColor(context, R.color.danger_red));
        } else {
            holder.btnRegister.setText("Đăng ký tham gia");
            holder.btnRegister.setBackgroundColor(androidx.core.content.ContextCompat.getColor(context, R.color.visionary_blue));
        }

        holder.btnRegister.setOnClickListener(v -> {
            if (item.isRegisteredByCurrentUser()) {
                cancelRegistration(item, holder);
            } else {
                registerForEvent(item, holder);
            }
        });

        holder.btnQrCode.setOnClickListener(v -> {
            String code = item.getQrCheckInCode() != null ? item.getQrCheckInCode() : "N/A";
            new AlertDialog.Builder(context)
                    .setTitle("Mã QR Điểm Danh Sự Kiện")
                    .setMessage("Sự kiện: " + item.getTitle() + "\n\nMã xác thực Check-in: " + code + "\n\nHãy xuất trình mã này tại bàn điểm danh của CLB.")
                    .setPositiveButton("Đã hiểu", null)
                    .show();
        });
    }

    private void registerForEvent(EventItem item, EventViewHolder holder) {
        holder.btnRegister.setEnabled(false);
        ApiClient.getService(context).registerForEvent(item.getId()).enqueue(new Callback<ApiResponse<String>>() {
            @Override
            public void onResponse(@NonNull Call<ApiResponse<String>> call, @NonNull Response<ApiResponse<String>> response) {
                holder.btnRegister.setEnabled(true);
                if (response.isSuccessful() && response.body() != null && response.body().isSuccess()) {
                    item.setRegisteredByCurrentUser(true);
                    notifyItemChanged(holder.getAdapterPosition());
                    Toast.makeText(context, "Đăng ký thành công!", Toast.LENGTH_SHORT).show();
                } else {
                    String msg = response.body() != null ? response.body().getMessage() : "Lỗi đăng ký";
                    Toast.makeText(context, msg, Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(@NonNull Call<ApiResponse<String>> call, @NonNull Throwable t) {
                holder.btnRegister.setEnabled(true);
                Toast.makeText(context, "Lỗi mạng: " + t.getMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void cancelRegistration(EventItem item, EventViewHolder holder) {
        holder.btnRegister.setEnabled(false);
        ApiClient.getService(context).cancelRegistration(item.getId()).enqueue(new Callback<ApiResponse<String>>() {
            @Override
            public void onResponse(@NonNull Call<ApiResponse<String>> call, @NonNull Response<ApiResponse<String>> response) {
                holder.btnRegister.setEnabled(true);
                if (response.isSuccessful() && response.body() != null && response.body().isSuccess()) {
                    item.setRegisteredByCurrentUser(false);
                    notifyItemChanged(holder.getAdapterPosition());
                    Toast.makeText(context, "Đã hủy đăng ký!", Toast.LENGTH_SHORT).show();
                } else {
                    String msg = response.body() != null ? response.body().getMessage() : "Lỗi hủy đăng ký";
                    Toast.makeText(context, msg, Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(@NonNull Call<ApiResponse<String>> call, @NonNull Throwable t) {
                holder.btnRegister.setEnabled(true);
                Toast.makeText(context, "Lỗi mạng: " + t.getMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }

    @Override
    public int getItemCount() {
        return events.size();
    }

    static class EventViewHolder extends RecyclerView.ViewHolder {
        TextView tvTitle, tvStatus, tvDesc, tvInfo;
        Button btnRegister, btnQrCode;

        public EventViewHolder(@NonNull View itemView) {
            super(itemView);
            tvTitle = itemView.findViewById(R.id.tvEventTitle);
            tvStatus = itemView.findViewById(R.id.tvEventStatus);
            tvDesc = itemView.findViewById(R.id.tvEventDesc);
            tvInfo = itemView.findViewById(R.id.tvEventInfo);
            btnRegister = itemView.findViewById(R.id.btnRegister);
            btnQrCode = itemView.findViewById(R.id.btnQrCode);
        }
    }
}
