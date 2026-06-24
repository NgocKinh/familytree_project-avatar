# Family Tree Project
🗺️
# Post Deploy Roadmap

---

# Priority 1

- member_close refinement.
- Data Integrity Checker.
- Marriage Consistency Checker.

---

# Priority 2

- Data Normalization.
- Chuẩn hóa sur_name / last_name / middle_name / first_name.
- Blood Code Optimization.

---

# Priority 3

- Performance.
- Cache.
- Relationship Engine V2 mở rộng.

---

# Future

- GEDCOM Import / Export.
- Statistics.
- Report.

🔑 Quên mật khẩu.
📧 Muốn đổi email.
👤 Muốn đổi tên đăng nhập.
🚫 Tài khoản bị khóa.
🔓 Không đăng nhập được.
👥 Xin nâng quyền từ Viewer lên Member.
👨‍💼 Xin cấp quyền Co-operator.

□ Thêm hướng dẫn cho từng loại Feedback.
□ Tooltip cho "Hỗ trợ tài khoản".
□ Bổ sung Help Page giải thích các loại phản hồi.
□ Cải thiện giao diện Feedback.

Ở mục Feedback, thêm bảng như sau:

Loại phản hồi	Khi nào nên chọn
🐞 Báo lỗi hệ thống	Chức năng hoạt động sai, xuất hiện lỗi.
💡 Góp ý cải tiến	Đề xuất tính năng hoặc cải thiện giao diện.
🌳 Báo sai dữ liệu gia phả	Sai quan hệ, ngày sinh, ngày mất, thông tin thành viên.
👤 Hỗ trợ tài khoản	Quên mật khẩu, đổi email, đổi tên đăng nhập, tài khoản bị khóa, không đăng nhập được, xin nâng quyền hoặc cấp quyền.
❓ Khác	Những vấn đề chưa thuộc các nhóm trên.

Feedback Module v2

- Người gửi được sửa Feedback khi Admin chưa xử lý.
- Người gửi được thu hồi Feedback khi Admin chưa xử lý.
- Thêm trạng thái: Mới / Đang xử lý / Đã xử lý.
- Thêm trang "Feedback của tôi".

## Version 2.1 – Technical Debt

### Route Standardization
Priority: Low

- Chuẩn hóa toàn bộ route theo kebab-case.
- Đổi:
  /parent_child
  → /parent-child

Mục tiêu:
- Đồng nhất toàn bộ URL.
- Tránh nhầm lẫn giữa "_" và "-".
- Không thực hiện trước Deployment v1.0 để tránh ảnh hưởng các route đã được kiểm thử.

□ Xóa toàn bộ user test.
□ Thiết kế lại hệ thống tài khoản production.
□ Tạo mới các tài khoản theo vai trò:
   - Admin
   - Co-operator
   - Member
   - Viewer
□ Kiểm tra đăng nhập từng role.
□ Sau khi xác nhận hoạt động ổn định mới chính thức đưa vào sử dụng.

## Checklist trước Production Deploy

□ Đổi ENV=development → ENV=production

□ Đổi FRONTEND_URL từ:
   http://localhost:5173
   →
   https://<domain-thật>

□ Tạo file frontend-vite/.env.production

□ Cấu hình:
   VITE_API_BASE_URL=https://familytreeproject-avatar-production.up.railway.app

□ npm run build

□ Upload lại dist lên Cloudflare Pages

□ Xóa toàn bộ user test.

□ Tạo danh sách user production.

□ Kiểm tra đăng nhập 4 role:
   - Admin
   - Co-operator
   - Member
   - Viewer

□ Đổi ENV=production
□ Đổi FRONTEND_URL sang domain thật
□ Xóa user test
□ Tạo user production
□ Kiểm tra đăng nhập 4 role

## Version 2.1 – User Management

□ Thêm nút Xóa User cho Admin.
□ Chỉ Admin được phép xóa user.
□ Admin được phép xóa user thường và admin khác.
□ Không cho Admin tự xóa chính mình.
□ Hiển thị hộp xác nhận trước khi xóa.
□ Test lại ACL sau khi thêm chức năng.
Admin được xóa admin khác.
Admin không được tự xóa chính mình.
Backend kiểm tra quyền tại thời điểm xóa.