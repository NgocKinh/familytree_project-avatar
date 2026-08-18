# Cài đặt FamilyTree Clean v1.0

Tài liệu này hướng dẫn cài đặt FamilyTree trên máy Windows để kiểm tra trước khi triển khai Railway và Cloudflare.

[← Bắt đầu từ `00_START_HERE.md`](00_START_HERE.md) · [Tiếp theo: `02_BRANDING.md` →](02_BRANDING.md)

## 1. Yêu cầu

Cài đặt trước:

* Google Chrome.
* Git.
* Python 3.13 hoặc phiên bản tương thích.
* Node.js 22.
* npm 10.
* MySQL Server 8.
* MySQL Workbench.
* Visual Studio Code.
* Windows PowerShell.

**MySQL Server 8** vận hành database; **MySQL Workbench** là giao diện dùng để tạo và quản lý database.

Kiểm tra phiên bản:

```powershell
python --version
node --version
npm --version
git --version
```

## 2. Mở dự án

Mở PowerShell tại thư mục gốc của gói:

```powershell
Set-Location "D:\projects\FamilyTree_Clean_v1.0"
code .
```

Có thể thay đường dẫn trên bằng nơi thực tế đang lưu dự án.

## 3. Cài Backend

Từ thư mục gốc:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Nếu PowerShell chặn kích hoạt môi trường ảo, mở PowerShell bằng quyền phù hợp và kiểm tra chính sách thực thi của máy.

## 4. Tạo cấu hình Backend

Sao chép file mẫu:

```powershell
Copy-Item backend\.env.example backend\.env
```

Mở `backend\.env` và nhập thông tin MySQL riêng:

```dotenv
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=YOUR_MYSQL_USER
DB_PASSWORD=YOUR_MYSQL_PASSWORD
DB_NAME=YOUR_MYSQL_DATABASE

SECRET_KEY=YOUR_UNIQUE_LONG_RANDOM_SECRET
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480
FAMILY_CODE=FamilyTree
```

Tạo một `SECRET_KEY` ngẫu nhiên bằng Python:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Không chia sẻ hoặc commit file `backend\.env`.

## 5. Tạo Database rỗng

Trong MySQL Workbench:

1. Tạo một database mới.
2. Chọn charset `utf8mb4`.
3. Chọn collation `utf8mb4_unicode_ci`.
4. Mở file `database\schema.sql`.
5. Chọn đúng database vừa tạo.
6. Chạy toàn bộ file schema.

Schema phải tạo đúng 8 bảng:

* `announcements`
* `audit_logs`
* `feedback`
* `marriages`
* `parent_child`
* `person_marriage_priority`
* `persons`
* `users`

File schema không chứa câu lệnh `INSERT`.

## 6. Tạo Admin đầu tiên

Từ thư mục gốc, chạy:

```powershell
python -m backend.create_first_admin
```

Nhập:

* Username Admin
* Họ tên Admin
* Mật khẩu tối thiểu 12 ký tự
* Xác nhận mật khẩu

Mật khẩu không hiển thị khi nhập.

Công cụ chỉ cho phép tạo tài khoản khi bảng `users` còn rỗng.

## 7. Chạy Backend local

Từ thư mục gốc:

```powershell
uvicorn backend.main:app --reload
```

Địa chỉ Backend:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

## 8. Cài Frontend

Mở PowerShell thứ hai:

```powershell
Set-Location "D:\projects\FamilyTree_Clean_v1.0\frontend-vite"
npm ci
```

Tạo file cấu hình local:

```powershell
Copy-Item .env.example .env.local
```

Nội dung `.env.local`:

```dotenv
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

Không commit `.env.local`.

## 9. Chạy Frontend local

```powershell
npm run dev
```

Mở địa chỉ Vite hiển thị trong PowerShell, thông thường:

```text
http://localhost:5173
```

## 10. Kiểm tra ban đầu

Xác nhận:

* Trang chủ hiển thị thông tin dòng tộc mặc định.
* Trang đăng nhập mở bình thường.
* Admin đầu tiên đăng nhập được.
* Danh sách thành viên đang rỗng.
* Audit Log đang rỗng.
* Chỉ có ba avatar mặc định.
* Không có dữ liệu hoặc tài khoản của dòng họ khác.

## 11. Dừng hệ thống local

Trong từng cửa sổ PowerShell đang chạy Backend hoặc Frontend, nhấn:

```text
Ctrl + C
```

## 12. Lưu ý

* Không dùng database Production của dòng họ khác.
* Không dùng lại `SECRET_KEY`.
* Không sao chép `.env` sang Git.
* Không đưa avatar thật hoặc backup vào mã nguồn.
* Luôn kiểm tra đúng thư mục trước khi chạy lệnh.

## Tài liệu tiếp theo

Sau khi hệ thống local hoạt động:

1. Mở [`02_BRANDING.md`](02_BRANDING.md) để thay thông tin dòng tộc.
2. Mở [`03_DEPLOYMENT.md`](03_DEPLOYMENT.md) để triển khai Railway và Cloudflare.
3. Khi cần xem toàn bộ lộ trình, quay lại [`00_START_HERE.md`](00_START_HERE.md).
