using System;
using System.Windows.Forms;
using Visionary.Desktop.Services;

namespace Visionary.Desktop.Forms;

/// <summary>
/// Hỗ trợ hiển thị lỗi thống nhất cho các Form trong Desktop client.
/// </summary>
internal static class FormErrorExtensions
{
    /// <summary>
    /// Hiển thị thông báo lỗi thân thiện cho người dùng dựa trên loại lỗi API.
    /// Trả về true nếu lỗi là do hết phiên đăng nhập (cần đăng nhập lại).
    /// </summary>
    public static bool ShowApiError(this IWin32Window? owner, Exception exception, string context)
    {
        if (exception is ApiException apiException)
        {
            MessageBox.Show(
                owner,
                $"{context}\n\n{apiException.UserMessage}",
                "Lỗi",
                MessageBoxButtons.OK,
                MessageBoxIcon.Error);
            return apiException.IsSessionExpired;
        }

        MessageBox.Show(
            owner,
            $"{context}\n\n{exception.Message}",
            "Lỗi",
            MessageBoxButtons.OK,
            MessageBoxIcon.Error);
        return false;
    }
}
