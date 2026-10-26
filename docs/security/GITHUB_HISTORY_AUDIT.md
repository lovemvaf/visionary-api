# BÁO CÁO KIỂM TOÁN LỊCH SỬ GIT & ĐÁNH GIÁ CHUYỂN REPOSITORY SANG PRIVATE
## GITHUB REPOSITORY & COMMIT HISTORY SECURITY AUDIT
**Mã dự án:** VISIONARY – Hệ thống Quản lý Hoạt động Hội nhập (TH71108)  
**Repository mục tiêu:** `lovemvaf/visionary-api`  
**Nhánh kiểm tra:** `main` và toàn bộ commit tree  

---

## 1. PHẠM VI VÀ PHƯƠNG PHÁP KIỂM TRA LỊCH SỬ

Chúng tôi đã tiến hành quét toàn bộ lịch sử Git của repository bằng các phương pháp:
1. **Kiểm tra theo tên file:** `git log --all --name-only -- "**/.env*"` nhằm phát hiện việc vô tình commit các file môi trường thực tế (`.env`, `.env.local`, `.env.production`).
2. **Kiểm tra nội dung commit bằng chuỗi nhạy cảm (Pickaxe search):** `git log -S "<pattern>"` đối với các từ khóa credentials, connection strings, và tokens.
3. **Kiểm tra cấu hình loại trừ:** Rà soát `.gitignore` và `.dockerignore`.

---

## 2. KẾT QUẢ KIỂM TOÁN LỊCH SỬ (AUDIT FINDINGS)

### 2.1. File `.env` và Private Keys
- **Kết quả:** Lệnh quét xác nhận **KHÔNG CÓ bất kỳ file `.env` thật, `.pem`, `.key`, `.p12` hoặc file database dump nào từng bị commit vào lịch sử Git**.
- File môi trường duy nhất tồn tại là `.env.example`, hiện đã được chuẩn hóa thành template an toàn hoàn toàn với các giá trị placeholder.

### 2.2. Điểm rò rỉ trong các commit trước đây
- **Commit `199ef83`:** `feat(cloud): connect backend to Supabase PostgreSQL and ensure table creation with UTC timestamps`
  - *Nội dung rò rỉ:* Đã commit chuỗi kết nối Supabase chứa mật khẩu vào file `render.yaml`.
- **Commit `2742b34`:** `fix(cloud): switch to Supabase IPv4 connection pooler and guard startup seed`
  - *Nội dung:* Tiếp tục sửa đổi file `render.yaml` có chứa chuỗi trên.
- **Trạng thái hiện tại:** File `render.yaml` đã được làm sạch triệt để trong commit hiện tại, loại bỏ hoàn toàn connection string và chuyển sang cơ chế quản lý biến an toàn `sync: false` trên Render Dashboard.

---

## 3. ĐÁNH GIÁ PHƯƠNG ÁN: REWRITE GIT HISTORY VS. CREDENTIAL ROTATION

Khi một bí mật đã xuất hiện trong lịch sử commit công khai, có hai hướng xử lý chính:

### Hướng tiếp cận A: Viết lại lịch sử Git (Rewrite History bằng `git filter-repo` / BFG)
- **Ưu điểm:** Xóa hoàn toàn commit chứa dòng text nhạy cảm khỏi Git tree.
- **Rủi ro kỹ thuật:**
  - Làm thay đổi toàn bộ Commit SHA từ điểm commit nhạy cảm trở đi.
  - Phá vỡ các Pull Request, các liên kết commit đã trích dẫn trong tài liệu báo cáo và slide thuyết trình học phần TH71108.
  - Đòi hỏi `git push --force`, gây xung đột (reject) trên máy của các thành viên khác trong nhóm (Đạt, Khang H., Khang Đ.) và có thể làm hỏng webhook CI/CD nếu các branch đồng bộ bị lệch SHA.
  - **Quan trọng nhất:** Một bí mật đã từng bị commit lên GitHub công khai thì phải được coi là ĐÃ BỊ LỘ (Compromised) bởi các bot crawler. Việc xóa commit trên Git không đảm bảo kẻ xấu chưa lưu bản sao.

### Hướng tiếp cận B: Xoay vòng bí mật tại nguồn (Credential Rotation) + Chuyển Private (Khuyến nghị chuẩn an ninh công nghiệp)
- **Thực thi:**
  1. Đổi mật khẩu database trên Supabase Dashboard ngay lập tức.
  2. Cấp phát JWT Secret mới trên Render Web Service.
  3. Làm sạch mã nguồn ở commit mới nhất.
  4. Đổi trạng thái repository sang Private.
- **Đánh giá:** Đây là phương pháp **an toàn nhất và không gây rủi ro kỹ thuật**. Khi mật khẩu trên Supabase đã đổi, chuỗi mật khẩu trong commit cũ hoàn toàn mất tác dụng, kẻ xấu không thể dùng nó để kết nối vào bất kỳ tài nguyên nào. Đồng thời, cấu trúc Git SHA của dự án được bảo toàn nguyên vẹn cho buổi phản biện.

---

## 4. ĐÁNH GIÁ PHƯƠNG ÁN CHUYỂN REPOSITORY SANG PRIVATE

Chủ sở hữu hệ thống đã yêu cầu đánh giá việc chuyển repository `lovemvaf/visionary-api` sang chế độ Private.

### 4.1. Bảng phân tích tác động kỹ thuật

| Tiêu chí | Khi Repository Public (Hiện tại) | Khi Repository chuyển sang Private | Kết luận & Giải pháp |
|---|---|---|---|
| **Người dùng ngoài đọc mã nguồn** | Bất kỳ ai cũng có thể duyệt source code và commit history | Chỉ những người được phân quyền Collaborator mới xem được mã nguồn | **Bảo mật tối đa cho mã nguồn và tài liệu nội bộ** |
| **Website người dùng cuối (`visionary-platform.vercel.app`)** | Hoạt động bình thường | **Hoàn toàn bình thường**, không bị ảnh hưởng vì website phân phối HTML/JS đã build | **Không ảnh hưởng trải nghiệm người dùng** |
| **Tự động triển khai Vercel (Frontend)** | Tự động trigger qua Git integration | **Vẫn hoạt động bình thường** (Vercel GitHub App có quyền truy cập repo private khi tài khoản đã kết nối) | **Không làm gián đoạn CI/CD** |
| **Tự động triển khai Render (Backend)** | Tự động trigger qua Git webhook | **Vẫn hoạt động bình thường** (Render liên kết qua GitHub OAuth và đọc được private repository) | **Không làm gián đoạn CI/CD** |
| **GitHub Actions CI/CD** | Miễn phí không giới hạn phút chạy public | Được cấp 2,000 phút chạy miễn phí/tháng (đủ dùng cho đồ án sinh viên) | **Đạt yêu cầu** |
| **Chấm điểm của Giảng viên TH71108** | Giảng viên có thể xem trực tiếp không cần mời | Giảng viên cần được cấp quyền đọc (Invite as Read-only Collaborator) hoặc duyệt qua Swagger/Báo cáo | **Cần gửi lời mời Giảng viên qua email/username GitHub** |

### 4.2. Hướng dẫn Chủ sở hữu thực hiện chuyển Private trên GitHub

Nếu Chủ sở hữu quyết định chuyển repository sang Private:
1. Truy cập: [https://github.com/lovemvaf/visionary-api/settings](https://github.com/lovemvaf/visionary-api/settings)
2. Cuộn xuống phần cuối trang: **Danger Zone**.
3. Tại mục **Change repository visibility**, nhấn **Change visibility** ➔ Chọn **Make private**.
4. Nhập tên xác nhận `lovemvaf/visionary-api` và nhấn **I understand, change repository visibility**.
5. Thêm giảng viên hướng dẫn / chấm thi (nếu cần chấm trực tiếp trên source) tại: **Settings** ➔ **Collaborators** ➔ **Add people** ➔ Phân quyền **Read**.
