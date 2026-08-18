# FamilyTree Clean v1.0

Bộ mã nguồn gia phả dùng chung cho nhiều dòng họ.

## Tài liệu hướng dẫn

Bắt đầu triển khai tại:

- [00_START_HERE.md](docs/00_START_HERE.md) – Lộ trình triển khai từ đầu đến cuối.
- [01_INSTALLATION.md](docs/01_INSTALLATION.md) – Chuẩn bị và cài đặt phần mềm.
- [02_BRANDING.md](docs/02_BRANDING.md) – Thay tên, nội dung và hình ảnh dòng tộc.
- [03_DEPLOYMENT.md](docs/03_DEPLOYMENT.md) – Triển khai Railway và Cloudflare.

## Nguồn mã chính thức

- Repository: [NgocKinh/familytree_project-avatar](https://github.com/NgocKinh/familytree_project-avatar)
- Nhánh Clean: [familytree-clean-v1.0](https://github.com/NgocKinh/familytree_project-avatar/tree/familytree-clean-v1.0)

Khi tải hoặc clone bản Clean, phải chọn đúng nhánh `familytree-clean-v1.0`.

## Công nghệ

- Backend: FastAPI, SQLAlchemy, MySQL 8
- Frontend: React, Vite, Tailwind CSS
- Backend hosting: Railway
- Frontend hosting: Cloudflare Workers

## Nguyên tắc triển khai

Mỗi dòng họ phải có riêng:

* Railway service
* MySQL database
* Railway volume lưu avatar
* Cloudflare Worker
* URL frontend và backend
* `SECRET_KEY`
* Tài khoản Admin đầu tiên

Không dùng chung database, volume, URL hoặc secrets giữa các dòng họ.

## Nội dung bản Clean

* Database schema gồm 8 bảng, không có dữ liệu
* Không có tài khoản mặc định
* Không có avatar người thật
* Không có Audit Log hoặc backup cũ
* Không có URL hay secrets của hệ thống khác
* Có công cụ tạo Admin đầu tiên
* Có cấu hình branding tập trung

## Cấu hình branding

Chỉnh tại:

`frontend-vite/src/config/familyConfig.js`

Có thể thay:

* Tên dòng họ
* Bảng hiệu
* Tiêu đề phụ
* Slogan
* Quê quán
* Nội dung chào mừng
* Hình nền

## Cấu hình môi trường

Backend:

`backend/.env.example`

Frontend:

`frontend-vite/.env.example`

Sao chép thành file `.env` hoặc `.env.production` phù hợp rồi nhập giá trị riêng. Không commit file chứa secrets.

## Database rỗng

Schema cài đặt:

`database/schema.sql`

File này tạo đủ 8 bảng và không chứa câu lệnh `INSERT`.

## Tạo Admin đầu tiên

Sau khi tạo database và cấu hình backend, chạy từ thư mục gốc:

```powershell
python -m backend.create_first_admin
```

Công cụ chỉ hoạt động khi bảng `users` còn rỗng.

## Chạy Backend local

Từ thư mục gốc:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

Backend mặc định:

`http://127.0.0.1:8000`

## Chạy Frontend local

```powershell
cd frontend-vite
npm ci
npm run dev
```

Frontend mặc định:

`http://localhost:5173`

## Lưu ý bảo mật

* Không dùng secrets hoặc tài khoản của hệ thống khác.
* Không commit `.env`.
* Không đưa avatar thật hoặc database backup vào mã nguồn.
* Mỗi lần triển khai phải tạo `SECRET_KEY` mới.
* Không deploy bản Clean đè lên dịch vụ đang hoạt động của dòng họ khác.
