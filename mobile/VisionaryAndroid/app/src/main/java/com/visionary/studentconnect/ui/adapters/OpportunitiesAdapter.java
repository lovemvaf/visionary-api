package com.visionary.studentconnect.ui.adapters;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import com.visionary.studentconnect.R;
import com.visionary.studentconnect.models.ContentModels.OpportunityItem;
import java.util.ArrayList;
import java.util.List;

public class OpportunitiesAdapter extends RecyclerView.Adapter<OpportunitiesAdapter.OpportunityViewHolder> {
    private final List<OpportunityItem> items = new ArrayList<>();

    public void setItems(List<OpportunityItem> newItems) {
        items.clear();
        if (newItems != null) {
            items.addAll(newItems);
        }
        notifyDataSetChanged();
    }

    @NonNull
    @Override
    public OpportunityViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_opportunity, parent, false);
        return new OpportunityViewHolder(v);
    }

    @Override
    public void onBindViewHolder(@NonNull OpportunityViewHolder holder, int position) {
        OpportunityItem item = items.get(position);
        holder.tvTitle.setText(item.getTitle());
        holder.tvCategory.setText(item.getCategory());
        holder.tvOrganizer.setText("Đơn vị: " + item.getOrganizer());
        holder.tvDesc.setText(item.getDescription());

        String deadline = "📅 Hạn: " + (item.getDeadline() != null ? item.getDeadline().split("T")[0] : "Đang mở") +
                " • 📍 " + (item.getLocation() != null ? item.getLocation() : "Online");
        holder.tvDeadline.setText(deadline);
    }

    @Override
    public int getItemCount() {
        return items.size();
    }

    static class OpportunityViewHolder extends RecyclerView.ViewHolder {
        TextView tvTitle, tvCategory, tvOrganizer, tvDesc, tvDeadline;

        public OpportunityViewHolder(@NonNull View itemView) {
            super(itemView);
            tvTitle = itemView.findViewById(R.id.tvOppTitle);
            tvCategory = itemView.findViewById(R.id.tvOppCategory);
            tvOrganizer = itemView.findViewById(R.id.tvOppOrganizer);
            tvDesc = itemView.findViewById(R.id.tvOppDesc);
            tvDeadline = itemView.findViewById(R.id.tvOppDeadline);
        }
    }
}
