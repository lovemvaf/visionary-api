package com.visionary.studentconnect.ui.fragments;

import android.content.Intent;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import com.visionary.studentconnect.R;
import com.visionary.studentconnect.ui.LoginActivity;
import com.visionary.studentconnect.utils.SessionManager;

public class ProfileFragment extends Fragment {

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View v = inflater.inflate(R.layout.fragment_profile, container, false);

        SessionManager session = new SessionManager(requireContext());

        TextView tvName = v.findViewById(R.id.tvProfileName);
        TextView tvEmail = v.findViewById(R.id.tvProfileEmail);
        TextView tvRoles = v.findViewById(R.id.tvProfileRoles);
        Button btnLogout = v.findViewById(R.id.btnLogout);

        tvName.setText(session.getFullName());
        tvEmail.setText(session.getEmail());
        tvRoles.setText("Vai trò: " + session.getRoles());

        btnLogout.setOnClickListener(view -> {
            session.clear();
            Intent intent = new Intent(getActivity(), LoginActivity.class);
            intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
            startActivity(intent);
        });

        return v;
    }
}
