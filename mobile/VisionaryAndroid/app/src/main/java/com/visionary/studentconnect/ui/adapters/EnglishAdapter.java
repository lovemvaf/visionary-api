package com.visionary.studentconnect.ui.adapters;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import com.visionary.studentconnect.R;
import com.visionary.studentconnect.models.ContentModels.LearningResourceItem;
import java.util.ArrayList;
import java.util.List;

public class EnglishAdapter extends RecyclerView.Adapter<EnglishAdapter.EnglishViewHolder> {
    private final List<LearningResourceItem> items = new ArrayList<>();

    public void setItems(List<LearningResourceItem> newItems) {
        items.clear();
        if (newItems != null) {
            items.addAll(newItems);
        }
        notifyDataSetChanged();
    }

    @NonNull
    @Override
    public EnglishViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_english, parent, false);
        return new EnglishViewHolder(v);
    }

    @Override
    public void onBindViewHolder(@NonNull EnglishViewHolder holder, int position) {
        LearningResourceItem item = items.get(position);
        holder.tvTerm.setText(item.getTitle() != null ? item.getTitle() : "");
        String category = item.getCategory() != null ? item.getCategory() : "English for IT";
        String level = item.getLevel() != null ? item.getLevel() : "General";
        holder.tvCategory.setText(category + " • " + level);
        holder.tvDefinition.setText(item.getContentMarkdown() != null ? item.getContentMarkdown() : "");
        holder.tvExample.setText(item.getSampleSentence() != null ? "Ví dụ: " + item.getSampleSentence() : "");
    }

    @Override
    public int getItemCount() {
        return items.size();
    }

    static class EnglishViewHolder extends RecyclerView.ViewHolder {
        TextView tvTerm, tvCategory, tvDefinition, tvExample;

        public EnglishViewHolder(@NonNull View itemView) {
            super(itemView);
            tvTerm = itemView.findViewById(R.id.tvTerm);
            tvCategory = itemView.findViewById(R.id.tvCategory);
            tvDefinition = itemView.findViewById(R.id.tvDefinition);
            tvExample = itemView.findViewById(R.id.tvExample);
        }
    }
}
