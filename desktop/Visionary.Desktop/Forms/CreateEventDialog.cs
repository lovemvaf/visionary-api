using System;
using System.Drawing;
using System.Windows.Forms;
using Visionary.Core.DTOs;

namespace Visionary.Desktop.Forms;

public class CreateEventDialog : Form
{
    public CreateEventRequest? CreatedRequest { get; private set; }

    private TextBox _txtTitle = null!;
    private TextBox _txtDescription = null!;
    private TextBox _txtLocation = null!;
    private NumericUpDown _numCapacity = null!;
    private DateTimePicker _dtpStart = null!;
    private DateTimePicker _dtpEnd = null!;
    private DateTimePicker _dtpDeadline = null!;
    private Button _btnSave = null!;
    private Button _btnCancel = null!;

    public CreateEventDialog()
    {
        InitializeComponent();
    }

    private void InitializeComponent()
    {
        Text = "Tạo Sự kiện Mới - VISIONARY Club";
        Size = new Size(540, 520);
        FormBorderStyle = FormBorderStyle.FixedDialog;
        MaximizeBox = false;
        MinimizeBox = false;
        StartPosition = FormStartPosition.CenterParent;
        BackColor = Color.FromArgb(245, 247, 251);

        var lblHeader = new Label
        {
            Text = "TẠO MỚI SỰ KIỆN / WORKSHOP CLB",
            Font = new Font("Segoe UI", 12, FontStyle.Bold),
            ForeColor = Color.FromArgb(20, 45, 78),
            Location = new Point(20, 15),
            AutoSize = true
        };

        // Title
        var lblTitle = new Label { Text = "Tiêu đề sự kiện (*):", Location = new Point(20, 55), AutoSize = true, Font = new Font("Segoe UI", 9, FontStyle.Bold) };
        _txtTitle = new TextBox { Location = new Point(20, 75), Size = new Size(480, 26), Font = new Font("Segoe UI", 10) };

        // Description
        var lblDesc = new Label { Text = "Mô tả nội dung / Mục tiêu sự kiện (*):", Location = new Point(20, 110), AutoSize = true, Font = new Font("Segoe UI", 9, FontStyle.Bold) };
        _txtDescription = new TextBox { Location = new Point(20, 130), Size = new Size(480, 70), Multiline = true, Font = new Font("Segoe UI", 9) };

        // Location
        var lblLoc = new Label { Text = "Địa điểm tổ chức (*):", Location = new Point(20, 210), AutoSize = true, Font = new Font("Segoe UI", 9, FontStyle.Bold) };
        _txtLocation = new TextBox { Location = new Point(20, 230), Size = new Size(320, 26), Font = new Font("Segoe UI", 10), Text = "Hội trường Edison - DNTU" };

        // Capacity
        var lblCap = new Label { Text = "Giới hạn số lượng (Người):", Location = new Point(360, 210), AutoSize = true, Font = new Font("Segoe UI", 9, FontStyle.Bold) };
        _numCapacity = new NumericUpDown { Location = new Point(360, 230), Size = new Size(140, 26), Minimum = 5, Maximum = 1000, Value = 60, Font = new Font("Segoe UI", 10) };

        // Dates
        var lblStart = new Label { Text = "Thời gian bắt đầu:", Location = new Point(20, 270), AutoSize = true, Font = new Font("Segoe UI", 9, FontStyle.Bold) };
        _dtpStart = new DateTimePicker { Location = new Point(20, 290), Size = new Size(230, 26), CustomFormat = "dd/MM/yyyy HH:mm", Format = DateTimePickerFormat.Custom, Value = DateTime.Now.AddDays(3) };

        var lblEnd = new Label { Text = "Thời gian kết thúc:", Location = new Point(270, 270), AutoSize = true, Font = new Font("Segoe UI", 9, FontStyle.Bold) };
        _dtpEnd = new DateTimePicker { Location = new Point(270, 290), Size = new Size(230, 26), CustomFormat = "dd/MM/yyyy HH:mm", Format = DateTimePickerFormat.Custom, Value = DateTime.Now.AddDays(3).AddHours(2) };

        var lblDead = new Label { Text = "Hạn chót đăng ký:", Location = new Point(20, 330), AutoSize = true, Font = new Font("Segoe UI", 9, FontStyle.Bold) };
        _dtpDeadline = new DateTimePicker { Location = new Point(20, 350), Size = new Size(230, 26), CustomFormat = "dd/MM/yyyy HH:mm", Format = DateTimePickerFormat.Custom, Value = DateTime.Now.AddDays(2) };

        // Buttons
        _btnSave = new Button
        {
            Text = "Tạo sự kiện ngay",
            Location = new Point(240, 420),
            Size = new Size(140, 36),
            BackColor = Color.FromArgb(34, 100, 172),
            ForeColor = Color.White,
            FlatStyle = FlatStyle.Flat,
            Font = new Font("Segoe UI", 9, FontStyle.Bold),
            Cursor = Cursors.Hand
        };
        _btnSave.FlatAppearance.BorderSize = 0;
        _btnSave.Click += OnSaveClick;

        _btnCancel = new Button
        {
            Text = "Hủy bỏ",
            Location = new Point(390, 420),
            Size = new Size(110, 36),
            BackColor = Color.FromArgb(203, 213, 225),
            ForeColor = Color.FromArgb(30, 41, 59),
            FlatStyle = FlatStyle.Flat,
            Font = new Font("Segoe UI", 9),
            Cursor = Cursors.Hand
        };
        _btnCancel.FlatAppearance.BorderSize = 0;
        _btnCancel.Click += (s, e) => DialogResult = DialogResult.Cancel;

        Controls.Add(lblHeader);
        Controls.Add(lblTitle);
        Controls.Add(_txtTitle);
        Controls.Add(lblDesc);
        Controls.Add(_txtDescription);
        Controls.Add(lblLoc);
        Controls.Add(_txtLocation);
        Controls.Add(lblCap);
        Controls.Add(_numCapacity);
        Controls.Add(lblStart);
        Controls.Add(_dtpStart);
        Controls.Add(lblEnd);
        Controls.Add(_dtpEnd);
        Controls.Add(lblDead);
        Controls.Add(_dtpDeadline);
        Controls.Add(_btnSave);
        Controls.Add(_btnCancel);
    }

    private void OnSaveClick(object? sender, EventArgs e)
    {
        if (string.IsNullOrWhiteSpace(_txtTitle.Text))
        {
            MessageBox.Show("Vui lòng nhập tiêu đề sự kiện!", "Thiếu thông tin", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            return;
        }

        if (string.IsNullOrWhiteSpace(_txtDescription.Text))
        {
            MessageBox.Show("Vui lòng nhập mô tả sự kiện!", "Thiếu thông tin", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            return;
        }

        CreatedRequest = new CreateEventRequest
        {
            Title = _txtTitle.Text.Trim(),
            Description = _txtDescription.Text.Trim(),
            Location = _txtLocation.Text.Trim(),
            MaxCapacity = (int)_numCapacity.Value,
            StartTime = _dtpStart.Value.ToUniversalTime(),
            EndTime = _dtpEnd.Value.ToUniversalTime(),
            RegistrationDeadline = _dtpDeadline.Value.ToUniversalTime(),
            BannerUrl = "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=1200&q=80"
        };

        DialogResult = DialogResult.OK;
    }
}
