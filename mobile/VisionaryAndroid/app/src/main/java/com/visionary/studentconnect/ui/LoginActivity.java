package com.visionary.studentconnect.ui;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import com.google.android.material.textfield.TextInputEditText;
import com.visionary.studentconnect.R;
import com.visionary.studentconnect.api.ApiClient;
import com.visionary.studentconnect.api.ApiErrorParser;
import com.visionary.studentconnect.models.ApiResponse;
import com.visionary.studentconnect.models.AuthModels.AuthResponse;
import com.visionary.studentconnect.models.AuthModels.LoginRequest;
import com.visionary.studentconnect.utils.SessionManager;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class LoginActivity extends AppCompatActivity {
    private TextInputEditText etServerUrl, etEmail, etPassword;
    private Button btnLogin, btnQuickAdmin, btnQuickBcn;
    private ProgressBar progressBar;
    private TextView tvStatus;
    private SessionManager session;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        session = new SessionManager(this);

        if (session.isLoggedIn()) {
            startMainActivity();
            return;
        }

        setContentView(R.layout.activity_login);

        etServerUrl = findViewById(R.id.etServerUrl);
        etEmail = findViewById(R.id.etEmail);
        etPassword = findViewById(R.id.etPassword);
        btnLogin = findViewById(R.id.btnLogin);
        btnQuickAdmin = findViewById(R.id.btnQuickAdmin);
        btnQuickBcn = findViewById(R.id.btnQuickBcn);
        progressBar = findViewById(R.id.progressBar);
        tvStatus = findViewById(R.id.tvStatus);

        etServerUrl.setText(session.getBaseUrl());

        btnLogin.setOnClickListener(v -> performLogin());

        btnQuickAdmin.setOnClickListener(v -> {
            etEmail.setText("quachkhoaduc@visionary.dntu.edu.vn");
            etPassword.setText("");
            etPassword.requestFocus();
            tvStatus.setVisibility(View.GONE);
        });

        btnQuickBcn.setOnClickListener(v -> {
            etEmail.setText("vongocminhdat@visionary.dntu.edu.vn");
            etPassword.setText("");
            etPassword.requestFocus();
            tvStatus.setVisibility(View.GONE);
        });
    }

    private void performLogin() {
        String server = etServerUrl.getText() != null ? etServerUrl.getText().toString().trim() : "";
        String email = etEmail.getText() != null ? etEmail.getText().toString().trim() : "";
        String password = etPassword.getText() != null ? etPassword.getText().toString().trim() : "";

        if (email.isEmpty() || password.isEmpty()) {
            tvStatus.setVisibility(View.VISIBLE);
            tvStatus.setText("Vui lòng nhập email và mật khẩu.");
            return;
        }

        if (!server.isEmpty()) {
            session.saveBaseUrl(server);
            ApiClient.resetService();
        }

        progressBar.setVisibility(View.VISIBLE);
        btnLogin.setEnabled(false);
        tvStatus.setVisibility(View.GONE);

        LoginRequest req = new LoginRequest(email, password);
        ApiClient.getService(this).login(req).enqueue(new Callback<ApiResponse<AuthResponse>>() {
            @Override
            public void onResponse(@NonNull Call<ApiResponse<AuthResponse>> call, @NonNull Response<ApiResponse<AuthResponse>> response) {
                if (isFinishing() || isDestroyed()) return;
                progressBar.setVisibility(View.GONE);
                btnLogin.setEnabled(true);

                if (response.isSuccessful() && response.body() != null && response.body().isSuccess()) {
                    AuthResponse auth = response.body().getData();
                    if (auth != null) {
                        session.saveAuth(auth.getToken(), auth.getUser());
                        Toast.makeText(LoginActivity.this, "Đăng nhập thành công!", Toast.LENGTH_SHORT).show();
                        startMainActivity();
                    } else {
                        tvStatus.setVisibility(View.VISIBLE);
                        tvStatus.setText("Lỗi: Dữ liệu phản hồi xác thực không hợp lệ từ máy chủ.");
                    }
                } else {
                    String msg = ApiErrorParser.parseError(response);
                    tvStatus.setVisibility(View.VISIBLE);
                    tvStatus.setText("Lỗi: " + msg);
                }
            }

            @Override
            public void onFailure(@NonNull Call<ApiResponse<AuthResponse>> call, @NonNull Throwable t) {
                if (isFinishing() || isDestroyed()) return;
                progressBar.setVisibility(View.GONE);
                btnLogin.setEnabled(true);
                tvStatus.setVisibility(View.VISIBLE);
                tvStatus.setText(ApiErrorParser.parseThrowable(t));
            }
        });
    }

    private void startMainActivity() {
        Intent intent = new Intent(this, MainActivity.class);
        startActivity(intent);
        finish();
    }
}
