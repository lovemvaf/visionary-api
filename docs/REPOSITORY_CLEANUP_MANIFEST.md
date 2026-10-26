# BẢNG PHÂN LOẠI VÀ QUẢN LÝ DỌN DẸP REPOSITORY (REPOSITORY CLEANUP MANIFEST)
## VISIONARY API – REPOSITORY HYGIENE & FILE CLASSIFICATION
**Mã dự án:** VISIONARY – Hệ thống Quản lý Hoạt động Hội nhập (TH71108)  
**Thời điểm lập:** 26/10/2026  
**Mục tiêu:** Xác định rõ nhóm phân loại cho từng thành phần trong monorepo nhằm giữ repository gọn gàng, sạch sẽ, bảo vệ thông tin mật và không xóa nhầm tài nguyên cần thiết cho đồ án.  

---

## 1. NGUYÊN TẮC PHÂN LOẠI 5 NHÓM (5-TIER FILE CLASSIFICATION)

- **Nhóm A (Keep in Repository – Bắt buộc giữ):** Mã nguồn thực tế ba nền tảng, backend, database migrations, CI/CD workflows, cấu hình Docker/môi trường đã làm sạch, và các bài kiểm thử tự động.
- **Nhóm B (Keep but Reorganize – Giữ nhưng sắp xếp lại):** Tài liệu kỹ thuật, tài liệu học phần, và các script công cụ cần gom nhóm gọn gàng.
- **Nhóm C (Restricted / Private Distribution – Phân phối nội bộ):** Các tài liệu chứa thông tin vận hành nhạy cảm hoặc mật khẩu quản trị nội bộ.
- **Nhóm D (Generated / Rebuildable – Tệp sinh tự động / Có thể tái tạo):** File build, cache, `.pyc`, preview ảnh có thể tái tạo hoàn toàn bằng các script mã nguồn.
- **Nhóm E (Obsolete / Redundant – Lỗi thời hoặc Trùng lặp):** Các file trung gian, patch tạm thời đã được tích hợp vào giải pháp chính thức.

---

## 2. BẢNG KIỂM KÊ VÀ HÀNH ĐỘNG DỌN DẸP CHI TIẾT

| Đường dẫn tệp / Thư mục | Nhóm phân loại | Mục đích & Lý do | Hành động kỹ thuật | Ảnh hưởng Build/Test? |
|---|:---:|---|---|:---:|
| `backend/` | **Nhóm A** | Mã nguồn ASP.NET Core 8 Web API, Domain Models, Infrastructure, và 15 Tests xUnit | Giữ nguyên vẹn 100% | **Bắt buộc cho hệ thống** |
| `frontend/` | **Nhóm A** | Mã nguồn Website Next.js 14 App Router, 19 tuyến đường giao diện | Giữ nguyên vẹn 100% | **Bắt buộc cho hệ thống** |
| `desktop/` | **Nhóm A** | Mã nguồn ứng dụng Windows Forms C# (.NET 8) quản trị CLB | Giữ nguyên vẹn 100% | **Bắt buộc cho hệ thống** |
| `mobile/` | **Nhóm A** | Mã nguồn ứng dụng di động Android Java (SDK 34) | Giữ nguyên vẹn 100% | **Bắt buộc cho hệ thống** |
| `.github/workflows/` | **Nhóm A** | 5 quy trình CI/CD tự động (Security, Backend, Frontend, Desktop, Android) | Giữ nguyên vẹn, đã củng cố bảo mật | **Bắt buộc cho CI/CD** |
| `scripts/__pycache__/` | **Nhóm D** | Bytecode biên dịch của Python (`.pyc`) | **ĐÃ UNTRACK** khỏi Git (`git rm --cached`) | Không ảnh hưởng |
| `scripts/fix_name_spelling.py` | **Nhóm B** | Script tự động chuẩn hóa chính tả tên thành viên Hồ Đoàn | Giữ trong `scripts/` phục vụ kiểm tra tự động | Không ảnh hưởng |
| `scripts/build_perfect_presentation.py` | **Nhóm A** | Script tự động tái tạo slide PowerPoint 16 slide chuẩn học thuật | Giữ nguyên vẹn để tái tạo PPTX | Không ảnh hưởng |
| `deliverables/slide-previews/` | **Nhóm B** | 16 ảnh PNG xem trước slide cho hội đồng chấm thi | Giữ trong repo phục vụ kiểm tra trực quan nhanh | Không ảnh hưởng |
| `deliverables/` (PPTX, DOCX, PDF) | **Nhóm A** | Sản phẩm chính thức nộp cho giảng viên học phần TH71108 | Giữ đầy đủ bản mới nhất đã đồng bộ | **Bắt buộc cho nghiệm thu** |
| `.agent/TEST_RESULTS.md` | **Nhóm B** | Nhật ký kiểm thử của AI agent | Đã cập nhật trạng thái VERIFIED PASS khớp 15/15 tests | Không ảnh hưởng |
| `docs/security/` (13 báo cáo) | **Nhóm B** | Toàn bộ 13 báo cáo kiểm toán bảo mật chuyên nghiệp | Lưu trữ tập trung tại thư mục bảo mật | Không ảnh hưởng |
| `start-backend.bat` | **Nhóm A** | Script khởi động nhanh backend cục bộ cho thành viên | Đã loại bỏ Cloudflare Tunnel, chỉ bind localhost | Không ảnh hưởng |
| `.gitleaks.toml` | **Nhóm A** | Cấu hình cho công cụ phát hiện rò rỉ bí mật trong CI/CD | Giữ trong gốc repository | **Bảo vệ mã nguồn** |
| `project-status/verification.json` | **Nhóm A** | Nguồn sự thật chuẩn (SSOT) về số liệu kiểm thử hệ thống | Giữ trong repo | **Cung cấp dữ liệu SSOT** |

---

## 3. KẾT LUẬN QUẢN LÝ TÀI NGUYÊN (CLEANUP VERIFICATION)

Mọi thao tác dọn dẹp đã được thực hiện bằng các lệnh có kiểm soát (`git mv`, `git rm --cached`, cập nhật `.gitignore`), **tuyệt đối không sử dụng các lệnh xóa hủy diệt hàng loạt (`git clean -fdx`)**, bảo đảm toàn bộ mã nguồn ba nền tảng, cơ sở dữ liệu và các deliverables học thuật nộp cho giảng viên luôn sẵn sàng và nguyên vẹn.
