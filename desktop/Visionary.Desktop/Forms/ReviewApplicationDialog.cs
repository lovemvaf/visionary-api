using System;
using System.Drawing;
using System.Windows.Forms;
using Visionary.Core.DTOs;

namespace Visionary.Desktop.Forms;

public class ReviewApplicationDialog : Form
{
    private readonly MembershipApplicationDto _app;
    public bool IsApproved { get; private set; }
    public string ClubRole { get; private set; } = "Thành viên";
    public string ReviewNotes { get; private set; } = string.Empty;

    private ComboBox _cboDecision = null!;
    private TextBox _txtRole = null!;
    private TextBox _txtNotes = null!;
    private Button _btnSubmit = null!;
    private Button _btnCancel = null!;

    public ReviewApplicationDialog(MembershipApplicationDto app)
    {
        _app = app;
        InitializeComponent();
    }

    private void InitializeComponent()
    {
        Text = $"Xét duyệt đơn đăng ký - {_app.ApplicantName}";
        Size = new Size(520, 480);
        FormBorderStyle = FormBorderStyle.FixedDialog;
        MaximizeBox = false;
        MinimizeBox = false;
        StartPosition = FormStartPosition.CenterParent;
        BackColor = Color.FromArgb(245, 247, 251);

        var lblHeader = new Label
        {
            Text = "XÉT DUYỆT ĐƠN GIA NHẬP CLB",
            Font = new Font("Segoe UI", 12, FontStyle.Bold),
            ForeColor = Color.FromArgb(20, 45, 78),
            Location = new Point(20, 15),
            AutoSize = true
        };

        var lblInfo = new Label
        {
            Text = $"Ứng viên: {_app.ApplicantName} ({_app.StudentId ?? "N/A"})\n" +
                   $"Email: {_app.ApplicantEmail}\n" +
                   $"Ban nguyện vọng: {_app.PreferredDepartmentName ?? "Chưa rõ"}\n" +
                   $"Trình độ tiếng Anh: {_app.EnglishProficiency ?? "Chưa rõ"}\n\n" +
                   $"Tự giới thiệu: {_app.SelfIntroduction}\n\n" +
                   $"Mục tiêu tham gia: {_app.Motivation}",
            Font = new Font("Segoe UI", 9),
            ForeColor = Color.FromArgb(51, 65, 85),
            Location = new Point(20, 45),
            Size = new Size(460, 130),
            BorderStyle = BorderStyle.FixedSingle,
            BackColor = Color.White,
            Padding = new Padding(8)
        };

        var lblDecision = new Label
        {
            Text = "Quyết định xét duyệt:",
            Font = new Font("Segoe UI", 9, FontStyle.Bold),
            Location = new Point(20, 190),
            AutoSize = true
        };

        _cboDecision = new ComboBox
        {
            Location = new Point(20, 215),
            Size = new Size(460, 28),
            DropDownStyle = ComboBoxStyle.DropDownList,
            Font = new Font("Segoe UI", 10)
        };
        _cboDecision.Items.Add("Chấp thuận (Approved)");
        _cboDecision.Items.Add("Từ chối (Rejected)");
        _cboDecision.SelectedIndex = 0;
        _cboDecision.SelectedIndexChanged += (s, e) =>
        {
            _txtRole.Enabled = _cboDecision.SelectedIndex == 0;
        };

        var lblRole = new Label
        {
            Text = "Vai trò / Vị trí bổ nhiệm trong CLB:",
            Font = new Font("Segoe UI", 9, FontStyle.Bold),
            Location = new Point(20, 255),
            AutoSize = true
        };

        _txtRole = new TextBox
        {
            Location = new Point(20, 280),
            Size = new Size(460, 26),
            Font = new Font("Segoe UI", 10),
            Text = "Thành viên"
        };

        var lblNotes = new Label
        {
            Text = "Ghi chú phê duyệt / Phản hồi cho ứng viên:",
            Font = new Font("Segoe UI", 9, FontStyle.Bold),
            Location = new Point(20, 315),
            AutoSize = true
        };

        _txtNotes = new TextBox
        {
            Location = new Point(20, 340),
            Size = new Size(460, 50),
            Multiline = true,
            Font = new Font("Segoe UI", 9),
            Text = "Chào mừng bạn đến với CLB Tiếng Anh VISIONARY DNTU!"
        };

        _btnSubmit = new Button
        {
            Text = "Xác nhận duyệt",
            Location = new Point(240, 400),
            Size = new Size(130, 34),
            BackColor = Color.FromArgb(34, 100, 172),
            ForeColor = Color.White,
            FlatStyle = FlatStyle.Flat,
            Font = new Font("Segoe UI", 9, FontStyle.Bold),
            Cursor = Cursors.Hand
        };
        _btnSubmit.FlatAppearance.BorderSize = 0;
        _btnSubmit.Click += OnSubmitClick;

        _btnCancel = new Button
        {
            Text = "Hủy bỏ",
            Location = new Point(380, 400),
            Size = new Size(100, 34),
            BackColor = Color.FromArgb(203, 213, 225),
            ForeColor = Color.FromArgb(30, 41, 59),
            FlatStyle = FlatStyle.Flat,
            Font = new Font("Segoe UI", 9),
            Cursor = Cursors.Hand
        };
        _btnCancel.FlatAppearance.BorderSize = 0;
        _btnCancel.Click += (s, e) => DialogResult = DialogResult.Cancel;

        Controls.Add(lblHeader);
        Controls.Add(lblInfo);
        Controls.Add(lblDecision);
        Controls.Add(_cboDecision);
        Controls.Add(lblRole);
        Controls.Add(_txtRole);
        Controls.Add(lblNotes);
        Controls.Add(_txtNotes);
        Controls.Add(_btnSubmit);
        Controls.Add(_btnCancel);
    }

    private void OnSubmitClick(object? sender, EventArgs e)
    {
        IsApproved = _cboDecision.SelectedIndex == 0;
        ClubRole = _txtRole.Text.Trim();
        ReviewNotes = _txtNotes.Text.Trim();

        DialogResult = DialogResult.OK;
    }
}
