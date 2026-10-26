using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;
using Visionary.Core.DTOs;
using Visionary.Core.Enums;
using Visionary.Desktop.Services;

namespace Visionary.Desktop.Forms;

public class MainForm : Form
{
    private Panel _pnlSidebar = null!;
    private Panel _pnlHeader = null!;
    private Panel _pnlContent = null!;
    private Label _lblHeaderUser = null!;
    private Button _btnNavDashboard = null!;
    private Button _btnNavMembers = null!;
    private Button _btnNavApplications = null!;
    private Button _btnNavEvents = null!;
    private Button _btnNavSync = null!;
    private Button _btnNavAbout = null!;

    // Active View Panels
    private Panel _viewDashboard = null!;
    private Panel _viewMembers = null!;
    private Panel _viewApplications = null!;
    private Panel _viewEvents = null!;
    private Panel _viewSync = null!;
    private Panel _viewAbout = null!;

    // Dashboard controls
    private Label _lblCardMembers = null!;
    private Label _lblCardPending = null!;
    private Label _lblCardEvents = null!;
    private Label _lblCardSources = null!;
    private ListBox _lstRecentActivities = null!;

    // Members controls
    private DataGridView _dgvMembers = null!;
    private TextBox _txtMemberSearch = null!;

    // Applications controls
    private DataGridView _dgvApplications = null!;
    private ComboBox _cboAppStatus = null!;
    private List<MembershipApplicationDto> _cachedApplications = new();

    // Events controls
    private DataGridView _dgvEvents = null!;
    private DataGridView _dgvRegistrations = null!;
    private Label _lblSelectedEvent = null!;
    private Guid _currentEventId = Guid.Empty;
    private Button _btnCreateEventDashboard = null!;
    private Button _btnCreateEventEvents = null!;
    private Button _btnCheckIn = null!;

    // Sync controls
    private DataGridView _dgvSources = null!;
    private Label _lblSyncStatus = null!;

    // Global status strip (hiển thị lỗi/thông báo chung cho toàn bộ màn hình)
    private Label _lblGlobalStatus = null!;

    // Hủy các request đang chờ khi Form đóng
    private readonly CancellationTokenSource _cts = new();

    // Cờ chống thao tác trùng lặp (double-click) trong lúc request đang chạy
    private bool _isLoadingInitialData;
    private bool _isCheckingIn;
    private bool _isReviewing;
    private bool _isSyncing;
    private bool _isCreatingEvent;

    public MainForm()
    {
        InitializeComponent();
        ApplyPermissionVisibility();

        FormClosed += (s, e) =>
        {
            _cts.Cancel();
            _cts.Dispose();
        };

        // Nạp dữ liệu sau khi Form đã hiển thị để không chặn UI thread khi khởi tạo.
        Shown += async (s, e) => await LoadInitialDataAsync();
    }

    private void InitializeComponent()
    {
        Text = "VISIONARY – Club Administration | Quản lý Hoạt động Hội nhập CLB Tiếng Anh DNTU";
        Size = new Size(1200, 780);
        MinimumSize = new Size(1000, 650);
        StartPosition = FormStartPosition.CenterScreen;
        BackColor = Color.FromArgb(245, 247, 251);

        // Header Panel
        _pnlHeader = new Panel
        {
            Dock = DockStyle.Top,
            Height = 65,
            BackColor = Color.FromArgb(20, 45, 78) // Deep Navy
        };

        var lblBrand = new Label
        {
            Text = "VISIONARY CLUB ADMIN",
            Font = new Font("Segoe UI", 13, FontStyle.Bold),
            ForeColor = Color.FromArgb(34, 166, 161), // Teal
            Location = new Point(20, 20),
            AutoSize = true
        };

        _lblHeaderUser = new Label
        {
            Text = $"Tài khoản: {AppState.CurrentUser?.FullName ?? "N/A"} [{string.Join(", ", AppState.CurrentUser?.Roles ?? new List<string>())}]",
            Font = new Font("Segoe UI", 9.5f),
            ForeColor = Color.White,
            Location = new Point(320, 22),
            AutoSize = true
        };

        var btnLogout = new Button
        {
            Text = "Đăng xuất",
            Anchor = AnchorStyles.Top | AnchorStyles.Right,
            Location = new Point(1080, 16),
            Size = new Size(95, 32),
            BackColor = Color.FromArgb(220, 38, 38),
            ForeColor = Color.White,
            FlatStyle = FlatStyle.Flat,
            Font = new Font("Segoe UI", 9, FontStyle.Bold),
            Cursor = Cursors.Hand
        };
        btnLogout.FlatAppearance.BorderSize = 0;
        btnLogout.Click += (s, e) =>
        {
            AppState.Logout();
            new LoginForm().Show();
            Close();
        };

        _lblGlobalStatus = new Label
        {
            Text = string.Empty,
            Font = new Font("Segoe UI", 8.5f),
            ForeColor = Color.FromArgb(203, 213, 225),
            Location = new Point(320, 42),
            Size = new Size(740, 18),
            TextAlign = ContentAlignment.MiddleLeft
        };

        _pnlHeader.Controls.Add(lblBrand);
        _pnlHeader.Controls.Add(_lblHeaderUser);
        _pnlHeader.Controls.Add(_lblGlobalStatus);
        _pnlHeader.Controls.Add(btnLogout);

        // Sidebar Panel
        _pnlSidebar = new Panel
        {
            Dock = DockStyle.Left,
            Width = 240,
            BackColor = Color.FromArgb(15, 23, 42) // Dark Navy Slate
        };

        int navY = 20;
        _btnNavDashboard = CreateNavButton("📊  Tổng quan (Dashboard)", navY, () => SwitchView(_viewDashboard, _btnNavDashboard));
        navY += 50;
        _btnNavMembers = CreateNavButton("👥  Thành viên CLB", navY, () => SwitchView(_viewMembers, _btnNavMembers));
        navY += 50;
        _btnNavApplications = CreateNavButton("📝  Duyệt đơn gia nhập", navY, () => SwitchView(_viewApplications, _btnNavApplications));
        navY += 50;
        _btnNavEvents = CreateNavButton("📅  Sự kiện & Điểm danh", navY, () => SwitchView(_viewEvents, _btnNavEvents));
        navY += 50;
        _btnNavSync = CreateNavButton("⚡  Dữ liệu & Sync", navY, () => SwitchView(_viewSync, _btnNavSync));
        navY += 50;
        _btnNavAbout = CreateNavButton("ℹ️  Về VISIONARY", navY, () => SwitchView(_viewAbout, _btnNavAbout));

        var lblSidebarFooter = new Label
        {
            Text = "Nhóm VISIONARY API\nTH71108 - Web API DNTU",
            Dock = DockStyle.Bottom,
            Height = 45,
            TextAlign = ContentAlignment.MiddleCenter,
            ForeColor = Color.FromArgb(148, 163, 184),
            Font = new Font("Segoe UI", 8)
        };
        _pnlSidebar.Controls.Add(lblSidebarFooter);

        // Content Host Panel
        _pnlContent = new Panel
        {
            Dock = DockStyle.Fill,
            BackColor = Color.FromArgb(245, 247, 251),
            Padding = new Padding(20)
        };

        // Initialize All Subviews
        InitDashboardView();
        InitMembersView();
        InitApplicationsView();
        InitEventsView();
        InitSyncView();
        InitAboutView();

        Controls.Add(_pnlContent);
        Controls.Add(_pnlSidebar);
        Controls.Add(_pnlHeader);

        // Default view: Dashboard
        SwitchView(_viewDashboard, _btnNavDashboard);
    }

    private Button CreateNavButton(string text, int y, Action onClick)
    {
        var btn = new Button
        {
            Text = text,
            Location = new Point(10, y),
            Size = new Size(220, 42),
            BackColor = Color.Transparent,
            ForeColor = Color.FromArgb(203, 213, 225),
            FlatStyle = FlatStyle.Flat,
            TextAlign = ContentAlignment.MiddleLeft,
            Font = new Font("Segoe UI", 9.5f),
            Cursor = Cursors.Hand,
            Padding = new Padding(10, 0, 0, 0)
        };
        btn.FlatAppearance.BorderSize = 0;
        btn.Click += (s, e) => onClick();
        _pnlSidebar.Controls.Add(btn);
        return btn;
    }

    private void SwitchView(Panel targetView, Button activeButton)
    {
        _pnlContent.Controls.Clear();
        targetView.Dock = DockStyle.Fill;
        _pnlContent.Controls.Add(targetView);

        foreach (Control c in _pnlSidebar.Controls)
        {
            if (c is Button b)
            {
                b.BackColor = Color.Transparent;
                b.ForeColor = Color.FromArgb(203, 213, 225);
                b.Font = new Font("Segoe UI", 9.5f, FontStyle.Regular);
            }
        }

        activeButton.BackColor = Color.FromArgb(34, 100, 172); // Visionary Blue
        activeButton.ForeColor = Color.White;
        activeButton.Font = new Font("Segoe UI", 9.5f, FontStyle.Bold);
    }

    #region View 1: Dashboard
    private void InitDashboardView()
    {
        _viewDashboard = new Panel { AutoScroll = true };

        var lblTitle = new Label
        {
            Text = "TỔNG QUAN HỆ THỐNG & HOẠT ĐỘNG CLB",
            Font = new Font("Segoe UI", 14, FontStyle.Bold),
            ForeColor = Color.FromArgb(20, 45, 78),
            Location = new Point(0, 0),
            AutoSize = true
        };
        _viewDashboard.Controls.Add(lblTitle);

        // 4 Stat Cards
        int cardW = 200, gap = 20;
        var pnlCard1 = CreateStatCard("Thành viên chính thức", "...", Color.FromArgb(34, 100, 172), 0, 40, out _lblCardMembers);
        var pnlCard2 = CreateStatCard("Đơn chờ xét duyệt", "...", Color.FromArgb(234, 88, 12), (cardW + gap), 40, out _lblCardPending);
        var pnlCard3 = CreateStatCard("Sự kiện hoạt động", "...", Color.FromArgb(22, 163, 74), (cardW + gap) * 2, 40, out _lblCardEvents);
        var pnlCard4 = CreateStatCard("Nguồn dữ liệu tự động", "...", Color.FromArgb(147, 51, 234), (cardW + gap) * 3, 40, out _lblCardSources);

        _viewDashboard.Controls.Add(pnlCard1);
        _viewDashboard.Controls.Add(pnlCard2);
        _viewDashboard.Controls.Add(pnlCard3);
        _viewDashboard.Controls.Add(pnlCard4);

        // Quick Actions
        var lblQuick = new Label
        {
            Text = "Thao tác Nhanh:",
            Font = new Font("Segoe UI", 11, FontStyle.Bold),
            ForeColor = Color.FromArgb(51, 65, 85),
            Location = new Point(0, 155),
            AutoSize = true
        };
        _viewDashboard.Controls.Add(lblQuick);

        var btnCreateEv = new Button
        {
            Text = "➕ Tạo Sự kiện Mới",
            Location = new Point(0, 185),
            Size = new Size(180, 36),
            BackColor = Color.FromArgb(34, 100, 172),
            ForeColor = Color.White,
            FlatStyle = FlatStyle.Flat,
            Font = new Font("Segoe UI", 9, FontStyle.Bold),
            Cursor = Cursors.Hand
        };
        btnCreateEv.FlatAppearance.BorderSize = 0;
        btnCreateEv.Click += (s, e) => ShowCreateEventDialog();
        _btnCreateEventDashboard = btnCreateEv;

        var btnViewApps = new Button
        {
            Text = "📋 Duyệt Đơn Chờ Ngay",
            Location = new Point(190, 185),
            Size = new Size(190, 36),
            BackColor = Color.FromArgb(234, 88, 12),
            ForeColor = Color.White,
            FlatStyle = FlatStyle.Flat,
            Font = new Font("Segoe UI", 9, FontStyle.Bold),
            Cursor = Cursors.Hand
        };
        btnViewApps.FlatAppearance.BorderSize = 0;
        btnViewApps.Click += (s, e) => SwitchView(_viewApplications, _btnNavApplications);

        var btnRefreshDash = new Button
        {
            Text = "🔄 Làm mới Thống kê",
            Location = new Point(390, 185),
            Size = new Size(160, 36),
            BackColor = Color.White,
            ForeColor = Color.FromArgb(20, 45, 78),
            FlatStyle = FlatStyle.Flat,
            Font = new Font("Segoe UI", 9),
            Cursor = Cursors.Hand
        };
        btnRefreshDash.FlatAppearance.BorderColor = Color.FromArgb(203, 213, 225);
        btnRefreshDash.Click += async (s, e) => await LoadDashboardStatsAsync();

        _viewDashboard.Controls.Add(btnCreateEv);
        _viewDashboard.Controls.Add(btnViewApps);
        _viewDashboard.Controls.Add(btnRefreshDash);

        // Recent Activity Box
        var lblActivities = new Label
        {
            Text = "Nhật ký Hoạt động Quản trị gần đây:",
            Font = new Font("Segoe UI", 11, FontStyle.Bold),
            ForeColor = Color.FromArgb(51, 65, 85),
            Location = new Point(0, 240),
            AutoSize = true
        };
        _viewDashboard.Controls.Add(lblActivities);

        _lstRecentActivities = new ListBox
        {
            Location = new Point(0, 270),
            Size = new Size(860, 280),
            Font = new Font("Consolas", 9.5f),
            BackColor = Color.White,
            BorderStyle = BorderStyle.FixedSingle,
            IntegralHeight = false
        };
        _viewDashboard.Controls.Add(_lstRecentActivities);
    }

    private Panel CreateStatCard(string title, string value, Color accentColor, int x, int y, out Label lblVal)
    {
        var pnl = new Panel
        {
            Location = new Point(x, y),
            Size = new Size(200, 95),
            BackColor = Color.White,
            BorderStyle = BorderStyle.FixedSingle
        };

        var pnlAccent = new Panel
        {
            Dock = DockStyle.Left,
            Width = 5,
            BackColor = accentColor
        };

        var lblT = new Label
        {
            Text = title,
            Font = new Font("Segoe UI", 8.5f),
            ForeColor = Color.FromArgb(100, 116, 139),
            Location = new Point(15, 12),
            Size = new Size(175, 20)
        };

        lblVal = new Label
        {
            Text = value,
            Font = new Font("Segoe UI", 18, FontStyle.Bold),
            ForeColor = Color.FromArgb(20, 45, 78),
            Location = new Point(15, 35),
            Size = new Size(175, 45)
        };

        pnl.Controls.Add(pnlAccent);
        pnl.Controls.Add(lblT);
        pnl.Controls.Add(lblVal);
        return pnl;
    }
    #endregion

    #region View 2: Members
    private void InitMembersView()
    {
        _viewMembers = new Panel();

        var lblTitle = new Label
        {
            Text = "DANH SÁCH THÀNH VIÊN CLB TIẾNG ANH DNTU",
            Font = new Font("Segoe UI", 14, FontStyle.Bold),
            ForeColor = Color.FromArgb(20, 45, 78),
            Location = new Point(0, 0),
            AutoSize = true
        };

        _txtMemberSearch = new TextBox
        {
            Location = new Point(0, 40),
            Size = new Size(300, 26),
            Font = new Font("Segoe UI", 9.5f),
            PlaceholderText = "Tìm theo họ tên, MSSV, vai trò..."
        };

        var btnSearch = new Button
        {
            Text = "🔍 Tìm kiếm",
            Location = new Point(310, 39),
            Size = new Size(100, 28),
            BackColor = Color.FromArgb(34, 100, 172),
            ForeColor = Color.White,
            FlatStyle = FlatStyle.Flat,
            Font = new Font("Segoe UI", 9, FontStyle.Bold),
            Cursor = Cursors.Hand
        };
        btnSearch.FlatAppearance.BorderSize = 0;
        btnSearch.Click += async (s, e) => await LoadMembersAsync(_txtMemberSearch.Text.Trim());

        var btnRefresh = new Button
        {
            Text = "🔄 Làm mới",
            Location = new Point(420, 39),
            Size = new Size(90, 28),
            BackColor = Color.White,
            FlatStyle = FlatStyle.Flat,
            Font = new Font("Segoe UI", 9),
            Cursor = Cursors.Hand
        };
        btnRefresh.FlatAppearance.BorderColor = Color.FromArgb(203, 213, 225);
        btnRefresh.Click += async (s, e) =>
        {
            _txtMemberSearch.Text = string.Empty;
            await LoadMembersAsync();
        };

        _dgvMembers = new DataGridView
        {
            Location = new Point(0, 80),
            Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right,
            Size = new Size(920, 520),
            BackgroundColor = Color.White,
            BorderStyle = BorderStyle.None,
            ReadOnly = true,
            AllowUserToAddRows = false,
            SelectionMode = DataGridViewSelectionMode.FullRowSelect,
            AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill
        };

        _viewMembers.Controls.Add(lblTitle);
        _viewMembers.Controls.Add(_txtMemberSearch);
        _viewMembers.Controls.Add(btnSearch);
        _viewMembers.Controls.Add(btnRefresh);
        _viewMembers.Controls.Add(_dgvMembers);
    }
    #endregion

    #region View 3: Applications
    private void InitApplicationsView()
    {
        _viewApplications = new Panel();

        var lblTitle = new Label
        {
            Text = "XÉT DUYỆT ĐƠN GIA NHẬP CLB TIẾNG ANH",
            Font = new Font("Segoe UI", 14, FontStyle.Bold),
            ForeColor = Color.FromArgb(20, 45, 78),
            Location = new Point(0, 0),
            AutoSize = true
        };

        var lblFilter = new Label
        {
            Text = "Trạng thái đơn:",
            Location = new Point(0, 42),
            AutoSize = true,
            Font = new Font("Segoe UI", 9, FontStyle.Bold)
        };

        _cboAppStatus = new ComboBox
        {
            Location = new Point(100, 39),
            Size = new Size(180, 26),
            DropDownStyle = ComboBoxStyle.DropDownList,
            Font = new Font("Segoe UI", 9)
        };
        _cboAppStatus.Items.Add("Tất cả đơn");
        _cboAppStatus.Items.Add("Chờ duyệt (Pending)");
        _cboAppStatus.Items.Add("Đã chấp thuận (Approved)");
        _cboAppStatus.Items.Add("Đã từ chối (Rejected)");
        _cboAppStatus.SelectedIndex = 1; // Default: Pending
        _cboAppStatus.SelectedIndexChanged += async (s, e) => await LoadApplicationsAsync();

        var btnReview = new Button
        {
            Text = "✏️ Xem & Xét Duyệt Đơn",
            Location = new Point(300, 38),
            Size = new Size(180, 30),
            BackColor = Color.FromArgb(34, 100, 172),
            ForeColor = Color.White,
            FlatStyle = FlatStyle.Flat,
            Font = new Font("Segoe UI", 9, FontStyle.Bold),
            Cursor = Cursors.Hand
        };
        btnReview.FlatAppearance.BorderSize = 0;
        btnReview.Click += OnReviewApplicationClick;

        var btnRefresh = new Button
        {
            Text = "🔄 Làm mới",
            Location = new Point(490, 38),
            Size = new Size(90, 30),
            BackColor = Color.White,
            FlatStyle = FlatStyle.Flat,
            Font = new Font("Segoe UI", 9),
            Cursor = Cursors.Hand
        };
        btnRefresh.FlatAppearance.BorderColor = Color.FromArgb(203, 213, 225);
        btnRefresh.Click += async (s, e) => await LoadApplicationsAsync();

        _dgvApplications = new DataGridView
        {
            Location = new Point(0, 80),
            Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right,
            Size = new Size(920, 520),
            BackgroundColor = Color.White,
            BorderStyle = BorderStyle.None,
            ReadOnly = true,
            AllowUserToAddRows = false,
            SelectionMode = DataGridViewSelectionMode.FullRowSelect,
            AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill
        };

        _viewApplications.Controls.Add(lblTitle);
        _viewApplications.Controls.Add(lblFilter);
        _viewApplications.Controls.Add(_cboAppStatus);
        _viewApplications.Controls.Add(btnReview);
        _viewApplications.Controls.Add(btnRefresh);
        _viewApplications.Controls.Add(_dgvApplications);
    }
    #endregion

    #region View 4: Events & Attendance
    private void InitEventsView()
    {
        _viewEvents = new Panel();

        var lblTitle = new Label
        {
            Text = "QUẢN LÝ SỰ KIỆN & ĐIỂM DANH THAM GIA",
            Font = new Font("Segoe UI", 14, FontStyle.Bold),
            ForeColor = Color.FromArgb(20, 45, 78),
            Location = new Point(0, 0),
            AutoSize = true
        };

        var btnCreate = new Button
        {
            Text = "➕ Tạo Sự kiện Mới",
            Location = new Point(0, 40),
            Size = new Size(160, 32),
            BackColor = Color.FromArgb(34, 100, 172),
            ForeColor = Color.White,
            FlatStyle = FlatStyle.Flat,
            Font = new Font("Segoe UI", 9, FontStyle.Bold),
            Cursor = Cursors.Hand
        };
        btnCreate.FlatAppearance.BorderSize = 0;
        btnCreate.Click += (s, e) => ShowCreateEventDialog();
        _btnCreateEventEvents = btnCreate;

        var btnRefresh = new Button
        {
            Text = "🔄 Làm mới",
            Location = new Point(170, 40),
            Size = new Size(90, 32),
            BackColor = Color.White,
            FlatStyle = FlatStyle.Flat,
            Font = new Font("Segoe UI", 9),
            Cursor = Cursors.Hand
        };
        btnRefresh.FlatAppearance.BorderColor = Color.FromArgb(203, 213, 225);
        btnRefresh.Click += async (s, e) => await LoadEventsAsync();

        // Split Panel: Top = Events, Bottom = Registrations & Checkin
        var lblEvList = new Label
        {
            Text = "Danh sách Sự kiện CLB:",
            Font = new Font("Segoe UI", 10, FontStyle.Bold),
            ForeColor = Color.FromArgb(51, 65, 85),
            Location = new Point(0, 80),
            AutoSize = true
        };

        _dgvEvents = new DataGridView
        {
            Location = new Point(0, 105),
            Anchor = AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Right,
            Size = new Size(920, 200),
            BackgroundColor = Color.White,
            BorderStyle = BorderStyle.FixedSingle,
            ReadOnly = true,
            AllowUserToAddRows = false,
            SelectionMode = DataGridViewSelectionMode.FullRowSelect,
            AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill
        };
        _dgvEvents.SelectionChanged += async (s, e) =>
        {
            if (_dgvEvents.SelectedRows.Count > 0)
            {
                var row = _dgvEvents.SelectedRows[0];
                if (row.DataBoundItem is EventDto ev)
                {
                    _currentEventId = ev.Id;
                    _lblSelectedEvent.Text = $"Người đăng ký & Điểm danh sự kiện: {ev.Title} (Giới hạn: {ev.MaxCapacity})";

                    // Danh sách đăng ký/điểm danh chỉ dành cho Admin/Committee.
                    if (AppState.IsCommittee)
                    {
                        await LoadEventRegistrationsAsync(ev.Id);
                    }
                }
            }
        };

        _lblSelectedEvent = new Label
        {
            Text = "Chọn một sự kiện ở trên để xem danh sách đăng ký và điểm danh:",
            Font = new Font("Segoe UI", 10, FontStyle.Bold),
            ForeColor = Color.FromArgb(34, 100, 172),
            Location = new Point(0, 320),
            AutoSize = true
        };

        var btnCheckIn = new Button
        {
            Text = "✅ Xác nhận Điểm danh (Check-in)",
            Location = new Point(700, 315),
            Anchor = AnchorStyles.Top | AnchorStyles.Right,
            Size = new Size(220, 30),
            BackColor = Color.FromArgb(22, 163, 74),
            ForeColor = Color.White,
            FlatStyle = FlatStyle.Flat,
            Font = new Font("Segoe UI", 9, FontStyle.Bold),
            Cursor = Cursors.Hand
        };
        btnCheckIn.FlatAppearance.BorderSize = 0;
        btnCheckIn.Click += OnCheckInClick;
        _btnCheckIn = btnCheckIn;

        _dgvRegistrations = new DataGridView
        {
            Location = new Point(0, 355),
            Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right,
            Size = new Size(920, 240),
            BackgroundColor = Color.White,
            BorderStyle = BorderStyle.FixedSingle,
            ReadOnly = true,
            AllowUserToAddRows = false,
            SelectionMode = DataGridViewSelectionMode.FullRowSelect,
            AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill
        };

        _viewEvents.Controls.Add(lblTitle);
        _viewEvents.Controls.Add(btnCreate);
        _viewEvents.Controls.Add(btnRefresh);
        _viewEvents.Controls.Add(lblEvList);
        _viewEvents.Controls.Add(_dgvEvents);
        _viewEvents.Controls.Add(_lblSelectedEvent);
        _viewEvents.Controls.Add(btnCheckIn);
        _viewEvents.Controls.Add(_dgvRegistrations);
    }
    #endregion

    #region View 5: Data Sync
    private void InitSyncView()
    {
        _viewSync = new Panel();

        var lblTitle = new Label
        {
            Text = "ĐIỀU KHIỂN NGUỒN DỮ LIỆU TỰ ĐỘNG (DATA AUTOMATION)",
            Font = new Font("Segoe UI", 14, FontStyle.Bold),
            ForeColor = Color.FromArgb(20, 45, 78),
            Location = new Point(0, 0),
            AutoSize = true
        };

        var btnTrigger = new Button
        {
            Text = "⚡ Kích hoạt Nạp Dữ liệu Ngay (Trigger Sync)",
            Location = new Point(0, 40),
            Size = new Size(260, 34),
            BackColor = Color.FromArgb(147, 51, 234),
            ForeColor = Color.White,
            FlatStyle = FlatStyle.Flat,
            Font = new Font("Segoe UI", 9, FontStyle.Bold),
            Cursor = Cursors.Hand
        };
        btnTrigger.FlatAppearance.BorderSize = 0;
        btnTrigger.Click += OnTriggerSyncClick;

        var btnRefresh = new Button
        {
            Text = "🔄 Làm mới nguồn",
            Location = new Point(270, 40),
            Size = new Size(130, 34),
            BackColor = Color.White,
            FlatStyle = FlatStyle.Flat,
            Font = new Font("Segoe UI", 9),
            Cursor = Cursors.Hand
        };
        btnRefresh.FlatAppearance.BorderColor = Color.FromArgb(203, 213, 225);
        btnRefresh.Click += async (s, e) => await LoadSourcesAsync();

        _lblSyncStatus = new Label
        {
            Location = new Point(420, 47),
            Size = new Size(490, 24),
            Font = new Font("Segoe UI", 9, FontStyle.Italic),
            ForeColor = Color.FromArgb(100, 116, 139)
        };

        _dgvSources = new DataGridView
        {
            Location = new Point(0, 90),
            Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right,
            Size = new Size(920, 500),
            BackgroundColor = Color.White,
            BorderStyle = BorderStyle.None,
            ReadOnly = true,
            AllowUserToAddRows = false,
            SelectionMode = DataGridViewSelectionMode.FullRowSelect,
            AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill
        };

        _viewSync.Controls.Add(lblTitle);
        _viewSync.Controls.Add(btnTrigger);
        _viewSync.Controls.Add(btnRefresh);
        _viewSync.Controls.Add(_lblSyncStatus);
        _viewSync.Controls.Add(_dgvSources);
    }
    #endregion

    #region View 6: About Visionary
    private void InitAboutView()
    {
        _viewAbout = new Panel { AutoScroll = true };

        var lblTitle = new Label
        {
            Text = "VỀ DỰ ÁN VISIONARY & NHÓM PHÁT TRIỂN VISIONARY API",
            Font = new Font("Segoe UI", 15, FontStyle.Bold),
            ForeColor = Color.FromArgb(20, 45, 78),
            Location = new Point(0, 0),
            AutoSize = true
        };
        _viewAbout.Controls.Add(lblTitle);

        var pnlCard = new Panel
        {
            Location = new Point(0, 40),
            Size = new Size(900, 560),
            BackColor = Color.White,
            BorderStyle = BorderStyle.FixedSingle,
            Padding = new Padding(25)
        };

        var lblIntro = new Label
        {
            Text = "HỆ THỐNG QUẢN LÝ HOẠT ĐỘNG HỘI NHẬP CLB TIẾNG ANH DNTU\n" +
                   "VISIONARY – English, Technology & Global Integration Platform",
            Font = new Font("Segoe UI", 12, FontStyle.Bold),
            ForeColor = Color.FromArgb(34, 100, 172),
            Location = new Point(25, 20),
            AutoSize = true
        };
        pnlCard.Controls.Add(lblIntro);

        var lblDesc = new Label
        {
            Text = "VISIONARY là nền tảng số hóa quản lý hoạt động Câu lạc bộ Tiếng Anh Trường Đại học Công nghệ Đồng Nai (DNTU), " +
                   "đồng thời là cổng kết nối công nghệ quốc tế, tri thức English for IT, kho repository open-source GitHub, mô hình AI Hugging Face, " +
                   "học bổng, cuộc thi hackathon và việc làm công nghệ cao.\n\n" +
                   "Kiến trúc hệ sinh thái: Một Backend ASP.NET Core 8 Web API dùng chung cho 3 nền tảng Web Next.js, Desktop Windows Forms và Mobile Android Native Java.",
            Font = new Font("Segoe UI", 9.5f),
            ForeColor = Color.FromArgb(71, 85, 105),
            Location = new Point(25, 75),
            Size = new Size(850, 75)
        };
        pnlCard.Controls.Add(lblDesc);

        // Members Box
        var lblTeamHeader = new Label
        {
            Text = "DANH SÁCH THÀNH VIÊN NHÓM PHÁT TRIỂN (VISIONARY API):",
            Font = new Font("Segoe UI", 10.5f, FontStyle.Bold),
            ForeColor = Color.FromArgb(20, 45, 78),
            Location = new Point(25, 160),
            AutoSize = true
        };
        pnlCard.Controls.Add(lblTeamHeader);

        string[] members = new[]
        {
            "1. Quách Khoa Đức — Vai trò: Principal Software Architect, Full-Stack & ASP.NET Core Web API Lead",
            "2. Võ Ngọc Minh Đạt — Vai trò: Club Operations, Business Analyst & Windows Forms Desktop Software Engineer",
            "3. Hồ Đoàn Nguyên Khang — Vai trò: Data Pipeline & Automation Engineer, Opportunities & Jobs Specialist",
            "4. Đào Trí Khang — Vai trò: Mobile Software Engineer (Android Native Java) & QA Testing Lead"
        };

        int memY = 190;
        foreach (var m in members)
        {
            var lblM = new Label
            {
                Text = m,
                Font = new Font("Segoe UI", 9.5f),
                ForeColor = Color.FromArgb(30, 41, 59),
                Location = new Point(35, memY),
                Size = new Size(830, 24)
            };
            pnlCard.Controls.Add(lblM);
            memY += 28;
        }

        // Academic Notice Box
        var pnlAcademic = new Panel
        {
            Location = new Point(25, 320),
            Size = new Size(850, 110),
            BackColor = Color.FromArgb(241, 245, 249),
            BorderStyle = BorderStyle.FixedSingle,
            Padding = new Padding(15)
        };

        var lblNoticeTitle = new Label
        {
            Text = "📌 THÔNG BÁO HỌC PHẦN & TÍNH PHÁP LÝ HỆ THỐNG",
            Font = new Font("Segoe UI", 9.5f, FontStyle.Bold),
            ForeColor = Color.FromArgb(30, 41, 59),
            Location = new Point(15, 10),
            AutoSize = true
        };

        var lblNoticeContent = new Label
        {
            Text = "Dự án được xây dựng phục vụ học phần Web API (TH71108) tại Trường Đại học Công nghệ Đồng Nai (DNTU). " +
                   "Hệ thống là sản phẩm nghiên cứu ứng dụng độc lập của nhóm VISIONARY API nhằm giải quyết bài toán quản trị CLB, " +
                   "không tự nhận là cổng thông tin chính thức được trường phê duyệt. " +
                   "Mọi dữ liệu công khai tuân thủ chính sách bản quyền và API của các nhà cung cấp.",
            Font = new Font("Segoe UI", 9),
            ForeColor = Color.FromArgb(100, 116, 139),
            Location = new Point(15, 35),
            Size = new Size(815, 65)
        };

        pnlAcademic.Controls.Add(lblNoticeTitle);
        pnlAcademic.Controls.Add(lblNoticeContent);
        pnlCard.Controls.Add(pnlAcademic);

        _viewAbout.Controls.Add(pnlCard);
    }
    #endregion

    #region Data Loading & Actions

    /// <summary>
    /// Ẩn các mục quản trị mà tài khoản hiện tại không được phép truy cập.
    /// Backend phân quyền: Dashboard/Đơn/Sự kiện cần Admin hoặc Committee,
    /// Nguồn dữ liệu tự động chỉ dành cho Admin.
    /// </summary>
    private void ApplyPermissionVisibility()
    {
        var isAdmin = AppState.IsAdmin;
        var isCommittee = AppState.IsCommittee;

        _btnNavDashboard.Visible = isCommittee;
        _btnNavApplications.Visible = isCommittee;
        _btnNavSync.Visible = isAdmin;

        // Tạo sự kiện và điểm danh đều yêu cầu quyền Admin/Committee ở backend.
        _btnCreateEventDashboard.Visible = isCommittee;
        _btnCreateEventEvents.Visible = isCommittee;
        _btnCheckIn.Visible = isCommittee;

        if (!isCommittee)
        {
            // Tài khoản không phải BCN: màn hình mặc định là Danh sách thành viên.
            SwitchView(_viewMembers, _btnNavMembers);
            SetGlobalStatus("Tài khoản hiện tại chỉ có quyền xem danh sách thành viên và sự kiện.");
        }
    }

    private void SetGlobalStatus(string message, bool isError = false)
    {
        _lblGlobalStatus.Text = message;
        _lblGlobalStatus.ForeColor = isError
            ? Color.FromArgb(252, 165, 165)
            : Color.FromArgb(203, 213, 225);
    }

    /// <summary>
    /// Hiển thị lỗi thân thiện. Nếu phiên đăng nhập đã hết hạn (HTTP 401) thì đưa người dùng
    /// về màn hình đăng nhập thay vì tiếp tục hiển thị dữ liệu rỗng.
    /// </summary>
    private void HandleApiError(Exception ex, string context)
    {
        if (ex is OperationCanceledException)
        {
            return;
        }

        if (ex is ApiException apiException && apiException.IsSessionExpired)
        {
            MessageBox.Show(this, apiException.UserMessage, "Phiên đăng nhập hết hạn",
                MessageBoxButtons.OK, MessageBoxIcon.Warning);
            AppState.Logout();
            new LoginForm().Show();
            Close();
            return;
        }

        SetGlobalStatus($"{context}: {(ex is ApiException a ? a.UserMessage : ex.Message)}", isError: true);
    }

    private async Task LoadInitialDataAsync()
    {
        if (_isLoadingInitialData)
        {
            return;
        }

        _isLoadingInitialData = true;
        try
        {
            // Chỉ gọi những endpoint mà tài khoản hiện tại được phép truy cập,
            // tránh nhận 403 làm nhiễu trạng thái màn hình.
            if (AppState.IsCommittee)
            {
                await LoadDashboardStatsAsync();
                await LoadApplicationsAsync();
            }

            await LoadMembersAsync();
            await LoadEventsAsync();

            if (AppState.IsAdmin)
            {
                await LoadSourcesAsync();
            }
        }
        finally
        {
            _isLoadingInitialData = false;
        }
    }

    private async Task LoadDashboardStatsAsync()
    {
        try
        {
            var stats = await ApiClient.Default.GetDashboardStatsAsync(_cts.Token);
            _lblCardMembers.Text = stats.TotalMembers.ToString();
            _lblCardPending.Text = stats.PendingApplications.ToString();
            _lblCardEvents.Text = stats.TotalEvents.ToString();
            _lblCardSources.Text = stats.TotalTechResources.ToString();

            _lstRecentActivities.Items.Clear();
            if (stats.RecentActivities != null && stats.RecentActivities.Count > 0)
            {
                foreach (var act in stats.RecentActivities)
                {
                    _lstRecentActivities.Items.Add($"[{act.Timestamp.ToLocalTime():yyyy-MM-dd HH:mm:ss}] {act.UserName}: {act.Action} - {act.Description}");
                }
            }
            else
            {
                _lstRecentActivities.Items.Add("Chưa có nhật ký hoạt động gần đây.");
            }
        }
        catch (Exception ex)
        {
            _lblCardMembers.Text = "N/A";
            _lblCardPending.Text = "N/A";
            _lblCardEvents.Text = "N/A";
            _lblCardSources.Text = "N/A";
            _lstRecentActivities.Items.Clear();
            _lstRecentActivities.Items.Add($"Không tải được thống kê: {(ex is ApiException a ? a.UserMessage : ex.Message)}");
            HandleApiError(ex, "Lỗi tải thống kê");
        }
    }

    private async Task LoadMembersAsync(string? search = null)
    {
        try
        {
            var paged = await ApiClient.Default.GetMembersAsync(search, cancellationToken: _cts.Token);
            _dgvMembers.DataSource = paged.Items.Select(m => new
            {
                Họ_Và_Tên = m.FullName,
                MSSV = m.StudentId ?? "N/A",
                Email = m.Email,
                Ban_Chuyên_Môn = m.DepartmentName ?? "Chung",
                Vai_Trò = m.ClubRole,
                Trình_Độ_Tiếng_Anh = m.EnglishLevel ?? "N/A",
                Trạng_Thái = m.Status,
                Ngày_Gia_Nhập = m.JoinedDate.ToLocalTime().ToString("dd/MM/yyyy")
            }).ToList();
        }
        catch (Exception ex)
        {
            _dgvMembers.DataSource = null;
            HandleApiError(ex, "Lỗi tải danh sách thành viên");
        }
    }

    private async Task LoadApplicationsAsync()
    {
        try
        {
            MembershipStatus? status = _cboAppStatus.SelectedIndex switch
            {
                1 => MembershipStatus.Pending,
                2 => MembershipStatus.Approved,
                3 => MembershipStatus.Rejected,
                _ => null
            };

            _cachedApplications = await ApiClient.Default.GetApplicationsAsync(status, _cts.Token);
            _dgvApplications.DataSource = _cachedApplications.Select(a => new
            {
                Họ_Và_Tên = a.ApplicantName,
                MSSV = a.StudentId ?? "N/A",
                Email = a.ApplicantEmail,
                Nguyện_Vọng_Ban = a.PreferredDepartmentName ?? "Chưa rõ",
                Trình_Độ = a.EnglishProficiency ?? "N/A",
                Trạng_Thái = a.Status,
                Ngày_Nộp = a.SubmittedAt.ToLocalTime().ToString("dd/MM/yyyy HH:mm")
            }).ToList();
        }
        catch (Exception ex)
        {
            _dgvApplications.DataSource = null;
            HandleApiError(ex, "Lỗi tải đơn đăng ký");
        }
    }

    private async void OnReviewApplicationClick(object? sender, EventArgs e)
    {
        if (_isReviewing)
        {
            return;
        }

        if (_dgvApplications.SelectedRows.Count == 0)
        {
            MessageBox.Show("Vui lòng chọn một đơn đăng ký để xét duyệt!", "Chưa chọn đơn", MessageBoxButtons.OK, MessageBoxIcon.Information);
            return;
        }

        var idx = _dgvApplications.SelectedRows[0].Index;
        if (idx < 0 || idx >= _cachedApplications.Count) return;

        var app = _cachedApplications[idx];
        if (app.Status != "Pending")
        {
            MessageBox.Show($"Đơn này đã được xử lý trước đó với trạng thái: {app.Status}", "Đơn đã duyệt", MessageBoxButtons.OK, MessageBoxIcon.Information);
            return;
        }

        using var dlg = new ReviewApplicationDialog(app);
        if (dlg.ShowDialog(this) != DialogResult.OK)
        {
            return;
        }

        _isReviewing = true;
        try
        {
            var msg = await ApiClient.Default.ReviewApplicationAsync(
                app.Id, dlg.IsApproved, dlg.ClubRole, null, dlg.ReviewNotes, _cts.Token);
            MessageBox.Show(msg, "Kết quả xét duyệt", MessageBoxButtons.OK, MessageBoxIcon.Information);
            await LoadApplicationsAsync();
            await LoadDashboardStatsAsync();
            await LoadMembersAsync();
        }
        catch (Exception ex)
        {
            HandleApiError(ex, "Lỗi xét duyệt đơn đăng ký");
        }
        finally
        {
            _isReviewing = false;
        }
    }

    private async Task LoadEventsAsync()
    {
        try
        {
            var paged = await ApiClient.Default.GetEventsAsync(cancellationToken: _cts.Token);
            _dgvEvents.DataSource = paged.Items.Select(e => new
            {
                Id = e.Id,
                Tiêu_Đề = e.Title,
                Địa_Điểm = e.Location,
                Bắt_Đầu = e.StartTime.ToLocalTime().ToString("dd/MM/yyyy HH:mm"),
                Kết_Thúc = e.EndTime.ToLocalTime().ToString("dd/MM/yyyy HH:mm"),
                Đăng_Ký = $"{e.CurrentRegistrationsCount}/{e.MaxCapacity}",
                Trạng_Thái = e.Status,
                Mã_QR = e.QrCheckInCode ?? "N/A"
            }).ToList();

            if (paged.Items.Count > 0)
            {
                _currentEventId = paged.Items[0].Id;
                // Danh sách đăng ký chỉ dành cho Admin/Committee (backend trả 403 nếu không có quyền).
                if (AppState.IsCommittee)
                {
                    await LoadEventRegistrationsAsync(_currentEventId);
                }
            }
        }
        catch (Exception ex)
        {
            _dgvEvents.DataSource = null;
            HandleApiError(ex, "Lỗi tải danh sách sự kiện");
        }
    }

    private async Task LoadEventRegistrationsAsync(Guid eventId)
    {
        try
        {
            var regs = await ApiClient.Default.GetEventRegistrationsAsync(eventId, _cts.Token);
            _dgvRegistrations.DataSource = regs.Select(r => new
            {
                UserId = r.UserId,
                Họ_Và_Tên = r.FullName,
                MSSV = r.StudentId ?? "N/A",
                Email = r.Email,
                Thời_Gian_Đăng_Ký = r.RegisteredAt.ToLocalTime().ToString("dd/MM/yyyy HH:mm"),
                Trạng_Thái = r.Status,
                Đã_Điểm_Danh = r.IsAttended ? "✅ Đã tham gia" : "❌ Chưa",
                Thời_Gian_CheckIn = r.CheckInTime.HasValue ? r.CheckInTime.Value.ToLocalTime().ToString("HH:mm:ss dd/MM") : "-"
            }).ToList();
        }
        catch (Exception ex)
        {
            _dgvRegistrations.DataSource = null;
            HandleApiError(ex, "Lỗi tải danh sách người đăng ký");
        }
    }

    private async void OnCheckInClick(object? sender, EventArgs e)
    {
        if (_isCheckingIn)
        {
            return;
        }

        if (_currentEventId == Guid.Empty)
        {
            MessageBox.Show("Vui lòng chọn một sự kiện trước!", "Chưa chọn sự kiện", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            return;
        }

        if (_dgvRegistrations.SelectedRows.Count == 0)
        {
            MessageBox.Show("Vui lòng chọn sinh viên cần điểm danh!", "Chưa chọn sinh viên", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            return;
        }

        var row = _dgvRegistrations.SelectedRows[0];
        if (row.Cells["UserId"].Value is not Guid userId)
        {
            MessageBox.Show("Không đọc được thông tin sinh viên từ dòng đã chọn.", "Dữ liệu không hợp lệ",
                MessageBoxButtons.OK, MessageBoxIcon.Warning);
            return;
        }

        _isCheckingIn = true;
        _btnCheckIn.Enabled = false;
        try
        {
            var msg = await ApiClient.Default.CheckInAttendeeAsync(_currentEventId, userId, _cts.Token);
            MessageBox.Show(msg, "Điểm danh thành công", MessageBoxButtons.OK, MessageBoxIcon.Information);
            await LoadEventRegistrationsAsync(_currentEventId);
            await LoadDashboardStatsAsync();
        }
        catch (Exception ex)
        {
            HandleApiError(ex, "Lỗi điểm danh");
        }
        finally
        {
            _isCheckingIn = false;
            _btnCheckIn.Enabled = true;
        }
    }

    private async void ShowCreateEventDialog()
    {
        if (_isCreatingEvent)
        {
            return;
        }

        using var dlg = new CreateEventDialog();
        if (dlg.ShowDialog(this) != DialogResult.OK || dlg.CreatedRequest == null)
        {
            return;
        }

        _isCreatingEvent = true;
        try
        {
            var created = await ApiClient.Default.CreateEventAsync(dlg.CreatedRequest, _cts.Token);
            MessageBox.Show($"Đã tạo thành công sự kiện: {created.Title}", "Thành công", MessageBoxButtons.OK, MessageBoxIcon.Information);
            await LoadEventsAsync();
            await LoadDashboardStatsAsync();
        }
        catch (Exception ex)
        {
            HandleApiError(ex, "Lỗi tạo sự kiện");
        }
        finally
        {
            _isCreatingEvent = false;
        }
    }

    private async Task LoadSourcesAsync()
    {
        try
        {
            var sources = await ApiClient.Default.GetSourcesAsync(_cts.Token);
            _dgvSources.DataSource = sources.Select(s => new
            {
                Id = s.Id,
                Tên_Nguồn = s.Name,
                Loại = s.Type,
                Địa_Chỉ = s.EndpointUrl,
                Chu_Kỳ_Phút = s.IntervalMinutes,
                Kích_Hoạt = s.IsEnabled ? "Bật" : "Tắt",
                Lần_Chạy_Cuối = s.LastRunAt.HasValue ? s.LastRunAt.Value.ToLocalTime().ToString("dd/MM/yyyy HH:mm") : "Chưa chạy",
                Trạng_Thái = s.LastStatus ?? "OK"
            }).ToList();
        }
        catch (Exception ex)
        {
            _dgvSources.DataSource = null;
            HandleApiError(ex, "Lỗi tải nguồn dữ liệu tự động");
        }
    }

    private async void OnTriggerSyncClick(object? sender, EventArgs e)
    {
        if (_isSyncing)
        {
            return;
        }

        if (_dgvSources.SelectedRows.Count == 0)
        {
            MessageBox.Show("Vui lòng chọn một nguồn trong bảng để kích hoạt đồng bộ!", "Chưa chọn nguồn", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            return;
        }

        var row = _dgvSources.SelectedRows[0];
        if (row.Cells["Id"].Value is not Guid sourceId)
        {
            MessageBox.Show("Không đọc được thông tin nguồn từ dòng đã chọn.", "Dữ liệu không hợp lệ",
                MessageBoxButtons.OK, MessageBoxIcon.Warning);
            return;
        }

        var name = row.Cells["Tên_Nguồn"].Value?.ToString() ?? "nguồn";
        _lblSyncStatus.ForeColor = Color.FromArgb(34, 100, 172);
        _lblSyncStatus.Text = $"Đang đồng bộ dữ liệu từ {name}...";

        _isSyncing = true;
        try
        {
            var res = await ApiClient.Default.TriggerSourceAsync(sourceId, _cts.Token);
            _lblSyncStatus.ForeColor = Color.FromArgb(22, 163, 74);
            _lblSyncStatus.Text = res;
            await LoadSourcesAsync();
            await LoadDashboardStatsAsync();
        }
        catch (Exception ex)
        {
            _lblSyncStatus.ForeColor = Color.FromArgb(220, 38, 38);
            _lblSyncStatus.Text = $"Lỗi: {(ex is ApiException a ? a.UserMessage : ex.Message)}";
            HandleApiError(ex, "Lỗi đồng bộ nguồn dữ liệu");
        }
        finally
        {
            _isSyncing = false;
        }
    }
    #endregion
}
