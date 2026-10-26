using System;
using System.Drawing;
using System.Threading;
using System.Windows.Forms;
using Visionary.Desktop.Services;

namespace Visionary.Desktop.Forms;

public class LoginForm : Form
{
    private TextBox _txtServerUrl = null!;
    private TextBox _txtEmail = null!;
    private TextBox _txtPassword = null!;
    private Button _btnLogin = null!;
    private Button _btnQuickAdmin = null!;
    private Button _btnQuickBcn = null!;
    private Label _lblStatus = null!;
    private ProgressBar _progressBar = null!;
    private readonly CancellationTokenSource _cts = new();

    public LoginForm()
    {
        InitializeComponent();
        FormClosed += (s, e) =>
        {
            // Hủy request đang chờ khi Form đóng để không giữ kết nối treo.
            _cts.Cancel();
            _cts.Dispose();
        };
    }

    private void InitializeComponent()
    {
        Text = "Đăng nhập Quản trị - VISIONARY Ecosystem";
        Size = new Size(460, 560);
        StartPosition = FormStartPosition.CenterScreen;
        FormBorderStyle = FormBorderStyle.FixedSingle;
        MaximizeBox = false;
        BackColor = Color.FromArgb(245, 247, 251);

        // Header Panel
        var pnlHeader = new Panel
        {
            Dock = DockStyle.Top,
            Height = 110,
            BackColor = Color.FromArgb(20, 45, 78) // Deep Navy
        };

        var lblLogo = new Label
        {
            Text = "VISIONARY",
            Font = new Font("Segoe UI", 18, FontStyle.Bold),
            ForeColor = Color.FromArgb(34, 166, 161), // Teal
            Location = new Point(25, 20),
            AutoSize = true
        };

        var lblSubtitle = new Label
        {
            Text = "Hệ thống Quản lý Hoạt động Hội nhập CLB Tiếng Anh DNTU\nPhần mềm Quản trị Desktop (Windows Forms C#)",
            Font = new Font("Segoe UI", 9),
            ForeColor = Color.FromArgb(203, 213, 225),
            Location = new Point(25, 55),
            AutoSize = true
        };

        pnlHeader.Controls.Add(lblLogo);
        pnlHeader.Controls.Add(lblSubtitle);

        // Body Content
        int startY = 130;

        // Server URL
        var lblServer = new Label
        {
            Text = "Địa chỉ Máy chủ Web API (ASP.NET Core):",
            Location = new Point(30, startY),
            AutoSize = true,
            Font = new Font("Segoe UI", 9, FontStyle.Bold),
            ForeColor = Color.FromArgb(51, 65, 85)
        };
        _txtServerUrl = new TextBox
        {
            Location = new Point(30, startY + 22),
            Size = new Size(385, 26),
            Font = new Font("Segoe UI", 9.5f),
            Text = AppState.ServerBaseUrl
        };

        // Email
        startY += 60;
        var lblEmail = new Label
        {
            Text = "Tài khoản Email sinh viên / Quản trị:",
            Location = new Point(30, startY),
            AutoSize = true,
            Font = new Font("Segoe UI", 9, FontStyle.Bold),
            ForeColor = Color.FromArgb(51, 65, 85)
        };
        _txtEmail = new TextBox
        {
            Location = new Point(30, startY + 22),
            Size = new Size(385, 26),
            Font = new Font("Segoe UI", 9.5f),
            Text = "quachkhoaduc@visionary.dntu.edu.vn"
        };

        // Password
        startY += 60;
        var lblPassword = new Label
        {
            Text = "Mật khẩu bảo mật:",
            Location = new Point(30, startY),
            AutoSize = true,
            Font = new Font("Segoe UI", 9, FontStyle.Bold),
            ForeColor = Color.FromArgb(51, 65, 85)
        };
        _txtPassword = new TextBox
        {
            Location = new Point(30, startY + 22),
            Size = new Size(385, 26),
            Font = new Font("Segoe UI", 9.5f),
            PasswordChar = '•'
        };

        // Progress bar & Status
        startY += 55;
        _progressBar = new ProgressBar
        {
            Location = new Point(30, startY),
            Size = new Size(385, 6),
            Style = ProgressBarStyle.Marquee,
            Visible = false
        };

        _lblStatus = new Label
        {
            Location = new Point(30, startY + 10),
            Size = new Size(385, 20),
            Font = new Font("Segoe UI", 8.5f),
            ForeColor = Color.FromArgb(220, 38, 38),
            TextAlign = ContentAlignment.MiddleCenter
        };

        // Login Button
        startY += 35;
        _btnLogin = new Button
        {
            Text = "ĐĂNG NHẬP HỆ THỐNG",
            Location = new Point(30, startY),
            Size = new Size(385, 40),
            BackColor = Color.FromArgb(34, 100, 172), // Visionary Blue
            ForeColor = Color.White,
            FlatStyle = FlatStyle.Flat,
            Font = new Font("Segoe UI", 10, FontStyle.Bold),
            Cursor = Cursors.Hand
        };
        _btnLogin.FlatAppearance.BorderSize = 0;
        _btnLogin.Click += OnLoginClick;

        // Quick login section
        startY += 50;
        var lblQuick = new Label
        {
            Text = "--- Tài khoản Mẫu Kiểm thử Nhanh ---",
            Location = new Point(30, startY),
            Size = new Size(385, 18),
            TextAlign = ContentAlignment.MiddleCenter,
            Font = new Font("Segoe UI", 8, FontStyle.Italic),
            ForeColor = Color.FromArgb(100, 116, 139)
        };

        startY += 25;
        _btnQuickAdmin = new Button
        {
            Text = "Quản trị viên (Đức)",
            Location = new Point(30, startY),
            Size = new Size(185, 32),
            BackColor = Color.White,
            ForeColor = Color.FromArgb(20, 45, 78),
            FlatStyle = FlatStyle.Flat,
            Font = new Font("Segoe UI", 8.5f),
            Cursor = Cursors.Hand
        };
        _btnQuickAdmin.FlatAppearance.BorderColor = Color.FromArgb(203, 213, 225);
        _btnQuickAdmin.Click += (s, e) =>
        {
            _txtEmail.Text = "quachkhoaduc@visionary.dntu.edu.vn";
            _txtPassword.Clear();
            _txtPassword.Focus();
            _lblStatus.Text = "Đã điền email Quản trị viên. Vui lòng nhập mật khẩu.";
        };

        _btnQuickBcn = new Button
        {
            Text = "Ban Chủ Nhiệm (Đạt)",
            Location = new Point(230, startY),
            Size = new Size(185, 32),
            BackColor = Color.White,
            ForeColor = Color.FromArgb(20, 45, 78),
            FlatStyle = FlatStyle.Flat,
            Font = new Font("Segoe UI", 8.5f),
            Cursor = Cursors.Hand
        };
        _btnQuickBcn.FlatAppearance.BorderColor = Color.FromArgb(203, 213, 225);
        _btnQuickBcn.Click += (s, e) =>
        {
            _txtEmail.Text = "vongocminhdat@visionary.dntu.edu.vn";
            _txtPassword.Clear();
            _txtPassword.Focus();
            _lblStatus.Text = "Đã điền email BCN. Vui lòng nhập mật khẩu.";
        };

        // Footer note
        var lblFooter = new Label
        {
            Text = "Phát triển bởi nhóm VISIONARY API - Học phần Web API TH71108 DNTU",
            Dock = DockStyle.Bottom,
            Height = 25,
            TextAlign = ContentAlignment.MiddleCenter,
            Font = new Font("Segoe UI", 7.5f),
            ForeColor = Color.FromArgb(148, 163, 184)
        };

        Controls.Add(pnlHeader);
        Controls.Add(lblServer);
        Controls.Add(_txtServerUrl);
        Controls.Add(lblEmail);
        Controls.Add(_txtEmail);
        Controls.Add(lblPassword);
        Controls.Add(_txtPassword);
        Controls.Add(_progressBar);
        Controls.Add(_lblStatus);
        Controls.Add(_btnLogin);
        Controls.Add(lblQuick);
        Controls.Add(_btnQuickAdmin);
        Controls.Add(_btnQuickBcn);
        Controls.Add(lblFooter);
    }

    private async void OnLoginClick(object? sender, EventArgs e)
    {
        var email = _txtEmail.Text.Trim();
        var pass = _txtPassword.Text.Trim();
        var server = _txtServerUrl.Text.Trim();

        if (string.IsNullOrEmpty(email) || string.IsNullOrEmpty(pass))
        {
            _lblStatus.ForeColor = Color.FromArgb(220, 38, 38);
            _lblStatus.Text = "Vui lòng nhập đầy đủ Email và Mật khẩu!";
            return;
        }

        if (!Uri.TryCreate(server, UriKind.Absolute, out var serverUri) ||
            (serverUri.Scheme != Uri.UriSchemeHttp && serverUri.Scheme != Uri.UriSchemeHttps))
        {
            _lblStatus.ForeColor = Color.FromArgb(220, 38, 38);
            _lblStatus.Text = "Địa chỉ máy chủ không hợp lệ. Ví dụ hợp lệ: http://localhost:5000";
            return;
        }

        AppState.ServerBaseUrl = server;

        // Chống bấm nút nhiều lần: vô hiệu hoá toàn bộ thao tác trong lúc đang xác thực.
        _btnLogin.Enabled = false;
        _btnQuickAdmin.Enabled = false;
        _btnQuickBcn.Enabled = false;
        _txtServerUrl.Enabled = false;
        _txtEmail.Enabled = false;
        _txtPassword.Enabled = false;
        _progressBar.Visible = true;
        _lblStatus.ForeColor = Color.FromArgb(34, 100, 172);
        _lblStatus.Text = "Đang kết nối và xác thực với ASP.NET Core API...";

        try
        {
            var auth = await ApiClient.Default.LoginAsync(email, pass, _cts.Token);
            _lblStatus.ForeColor = Color.FromArgb(22, 163, 74);
            _lblStatus.Text = $"Đăng nhập thành công! Xin chào {auth.User.FullName}";

            await Task.Delay(500, _cts.Token);

            var mainForm = new MainForm();
            mainForm.FormClosed += (s, args) => Close();
            Hide();
            mainForm.Show();
        }
        catch (OperationCanceledException)
        {
            // Form đã đóng trong lúc đang chờ -> không hiển thị lỗi.
            return;
        }
        catch (Exception ex)
        {
            _lblStatus.ForeColor = Color.FromArgb(220, 38, 38);

            // Với lỗi nghiệp vụ từ backend (sai email/mật khẩu) hiển thị đúng thông điệp
            // mà backend trả về; các lỗi kỹ thuật dùng thông điệp thân thiện.
            _lblStatus.Text = ex is Services.ApiException apiEx
                ? $"Lỗi: {(apiEx.Kind == Services.ApiErrorKind.Unauthorized || apiEx.Kind == Services.ApiErrorKind.Client
                    ? apiEx.Message
                    : apiEx.UserMessage)}"
                : $"Lỗi: {ex.Message}";
        }
        finally
        {
            _btnLogin.Enabled = true;
            _btnQuickAdmin.Enabled = true;
            _btnQuickBcn.Enabled = true;
            _txtServerUrl.Enabled = true;
            _txtEmail.Enabled = true;
            _txtPassword.Enabled = true;
            _progressBar.Visible = false;
        }
    }
}
