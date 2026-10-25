package com.visionary.studentconnect.ui;

import android.os.Bundle;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;
import com.google.android.material.bottomnavigation.BottomNavigationView;
import com.visionary.studentconnect.R;
import com.visionary.studentconnect.ui.fragments.EnglishForItFragment;
import com.visionary.studentconnect.ui.fragments.EventsFragment;
import com.visionary.studentconnect.ui.fragments.HomeFragment;
import com.visionary.studentconnect.ui.fragments.OpportunitiesFragment;
import com.visionary.studentconnect.ui.fragments.ProfileFragment;
import com.visionary.studentconnect.utils.SessionManager;

public class MainActivity extends AppCompatActivity {
    private BottomNavigationView bottomNav;
    private TextView tvUserShort;
    private SessionManager session;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        session = new SessionManager(this);

        bottomNav = findViewById(R.id.bottom_navigation);
        tvUserShort = findViewById(R.id.tvUserShort);

        String userDisplay = session.getFullName();
        if (session.getRoles() != null && !session.getRoles().isEmpty()) {
            userDisplay += " [" + session.getRoles().split(",")[0].trim() + "]";
        }
        tvUserShort.setText(userDisplay);

        bottomNav.setOnItemSelectedListener(item -> {
            Fragment selectedFragment = null;
            int itemId = item.getItemId();

            if (itemId == R.id.nav_home) {
                selectedFragment = new HomeFragment();
            } else if (itemId == R.id.nav_events) {
                selectedFragment = new EventsFragment();
            } else if (itemId == R.id.nav_english) {
                selectedFragment = new EnglishForItFragment();
            } else if (itemId == R.id.nav_opportunities) {
                selectedFragment = new OpportunitiesFragment();
            } else if (itemId == R.id.nav_profile) {
                selectedFragment = new ProfileFragment();
            }

            if (selectedFragment != null) {
                getSupportFragmentManager().beginTransaction()
                        .replace(R.id.fragment_container, selectedFragment)
                        .commit();
                return true;
            }
            return false;
        });

        // Default screen: HomeFragment
        if (savedInstanceState == null) {
            getSupportFragmentManager().beginTransaction()
                    .replace(R.id.fragment_container, new HomeFragment())
                    .commit();
        }
    }
}
