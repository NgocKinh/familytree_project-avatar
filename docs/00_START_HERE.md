# BẮT ĐẦU TỪ ĐÂY – Triển khai nhanh FamilyTree Clean v1.0

Tài liệu này là lộ trình triển khai nhanh một hệ thống FamilyTree độc lập cho một dòng tộc mới.

Hãy làm lần lượt từ trên xuống và đánh dấu `[x]` khi hoàn thành. Khi cần xem từng nút bấm, hình minh họa hoặc cách xử lý lỗi, mở phần tương ứng trong [`03_DEPLOYMENT.md`](03_DEPLOYMENT.md).

> Ví dụ trong tài liệu sử dụng **Tộc Lê**. Khi triển khai thực tế, thay `TocLe`, `FamilyTree-TocLe` và `familytree-tocle` bằng thông tin của dòng tộc đang triển khai.

## Nguồn mã chính thức

Repository:

```text
https://github.com/NgocKinh/familytree_project-avatar
```

Nhánh Clean:

```text
familytree-clean-v1.0
```

Mở trực tiếp bản Clean:

[FamilyTree Clean v1.0 trên GitHub](https://github.com/NgocKinh/familytree_project-avatar/tree/familytree-clean-v1.0)

> **Quan trọng:** Khi tải hoặc clone mã nguồn, phải chọn đúng nhánh `familytree-clean-v1.0`. Không tải nhầm nhánh đang vận hành hệ thống của dòng họ khác.

## 1. Kết quả cuối cùng

Sau khi hoàn thành, hệ thống phải có:

- Một Railway Project riêng.
- Một MySQL Service riêng.
- Một Backend Service riêng.
- Một Railway Volume riêng để lưu avatar.
- Một `SECRET_KEY` riêng.
- Một tài khoản Admin đầu tiên.
- Một Cloudflare Worker riêng cho Frontend.
- Một URL Backend và một URL Frontend hoạt động.

## 2. Chuẩn bị trước khi bắt đầu

### 2.1. Tài khoản cần có

- [ ] Tài khoản GitHub.
- [ ] Tài khoản Railway đã kết nối với GitHub.
- [ ] Tài khoản Cloudflare.

### 2.2. Phần mềm cần có trên máy Windows

- [ ] Google Chrome.
- [ ] Git.
- [ ] Python 3.13 hoặc phiên bản tương thích.
- [ ] Node.js 22 và npm 10.
- [ ] MySQL Server 8.
- [ ] MySQL Workbench.
- [ ] Visual Studio Code.
- [ ] Windows PowerShell.

> **MySQL Server 8** vận hành database; **MySQL Workbench** là giao diện dùng để tạo và quản lý database.

### 2.3. Bộ mã nguồn

- [ ] Đã nhận đúng bộ `FamilyTree_Clean_v1.0` từ nguồn bàn giao chính thức.
- [ ] Không có file `.env` chứa giá trị thật.
- [ ] Không có backup database.
- [ ] Không có database dump chứa dữ liệu thật.
- [ ] Không có avatar người thật.
- [ ] Không có tài khoản hoặc secret được ghi trong mã nguồn.

Kiểm tra nhanh trong thư mục mã nguồn:

```powershell
git status --short
```

Xem chi tiết: [Phần 1 và Phần 2](03_DEPLOYMENT.md#1-mỗi-dòng-tộc-phải-có-hệ-thống-riêng).

## 3. Phiếu thông tin triển khai

Ghi tên tài nguyên và URL vào bảng này trong lúc thực hiện. Không ghi mật khẩu, `SECRET_KEY` hoặc token vào tài liệu.

| Thông tin | Giá trị ví dụ | Giá trị triển khai thật |
|---|---|---|
| Tên dòng tộc | Tộc Lê | |
| Mã dòng tộc | `TocLe` | |
| Railway Project | `FamilyTree-TocLe` | |
| Backend Service | `Backend-FamilyTree` | |
| MySQL Service | Tên Railway tạo hoặc tên đã đặt | |
| Railway Volume | `Avatar-Volume` | |
| GitHub repository | Repository triển khai Tộc Lê | |
| Backend URL | `https://...up.railway.app` | |
| Cloudflare Worker | `familytree-tocle` | |
| Frontend URL | `https://...workers.dev` | |
| Username Admin | Không ghi mật khẩu | |

## 4. Chặng 1 – Cài đặt và kiểm tra trên máy Windows

### Bước 1. Kiểm tra công cụ cần thiết

Mở PowerShell và chạy:

```powershell
python --version
node --version
npm --version
git --version
```

- [ ] Python hoạt động.
- [ ] Node.js hoạt động.
- [ ] npm hoạt động.
- [ ] Git hoạt động.
- [ ] Đã cài MySQL Server 8, MySQL Workbench, Visual Studio Code và Windows PowerShell.

### Bước 2. Mở dự án và cài Backend local

```powershell
Set-Location "D:\projects\FamilyTree_Clean_v1.0"
code .
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

- [ ] Môi trường ảo `.venv` được tạo.
- [ ] Môi trường ảo được kích hoạt.
- [ ] Các thư viện Python được cài thành công.

### Bước 3. Tạo cấu hình, database và Admin local

Tạo file cấu hình Backend:

```powershell
Copy-Item backend\.env.example backend\.env
```

- [ ] `backend\.env` chứa thông tin MySQL trên máy.
- [ ] Đã tạo `SECRET_KEY` riêng cho lần chạy local.
- [ ] Đã tạo database local với `utf8mb4` và `utf8mb4_unicode_ci`.
- [ ] Đã chạy toàn bộ file `database\schema.sql`.
- [ ] Database local có đủ tám bảng và chưa có dữ liệu.

Tạo Admin local:

```powershell
python -m backend.create_first_admin
```

- [ ] Admin local được tạo thành công.

> Database, `SECRET_KEY` và Admin local chỉ dùng để kiểm tra trên máy. Khi triển khai Railway, phải tạo lại các thành phần dành cho hệ thống trực tuyến.

### Bước 4. Chạy Backend local

```powershell
uvicorn backend.main:app --reload
```

- [ ] Backend mở được tại `http://127.0.0.1:8000`.
- [ ] Swagger mở được tại `http://127.0.0.1:8000/docs`.

Giữ cửa sổ PowerShell này đang chạy.

### Bước 5. Cài và chạy Frontend local

Mở PowerShell thứ hai:

```powershell
Set-Location "D:\projects\FamilyTree_Clean_v1.0\frontend-vite"
npm ci
Copy-Item .env.example .env.local
```

Trong `.env.local`, đặt:

```dotenv
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

Chạy Frontend:

```powershell
npm run dev
```

- [ ] Frontend mở được tại địa chỉ Vite hiển thị, thông thường là `http://localhost:5173`.
- [ ] Admin local đăng nhập được.
- [ ] Danh sách thành viên và Audit Log đang rỗng.
- [ ] Chỉ có ba avatar mặc định.

### Bước 6. Dừng hệ thống local

Trong từng cửa sổ PowerShell đang chạy Backend và Frontend, nhấn:

```text
Ctrl+C
```

- [ ] Backend local đã dừng.
- [ ] Frontend local đã dừng.
- [ ] Không đưa `backend\.env` hoặc `.env.local` lên GitHub.

Xem chi tiết: [`01_INSTALLATION.md`](01_INSTALLATION.md).

## 5. Chặng 2 – Thay thông tin dòng tộc

### Bước 7. Thay nội dung dòng tộc

Mở:

```text
frontend-vite/src/config/familyConfig.js
```

- [ ] Thay `familyCode`, ví dụ: `TocLe`.
- [ ] Thay `familyName`.
- [ ] Thay `signboard`.
- [ ] Thay `subtitle` và `sloganLines`.
- [ ] Thay `originLine`.
- [ ] Thay `welcomeTitle` và `welcomeText`.
- [ ] Không sửa trực tiếp tên dòng tộc trong `Home.jsx`, `Navbar.jsx` hoặc `LoginPage.jsx`.

### Bước 8. Thay hình nền và kiểm tra giao diện

- [ ] Chép hình nền riêng vào `frontend-vite/public`.
- [ ] Đặt đúng `backgroundImage` trong `familyConfig.js`.
- [ ] Tên file ảnh viết không dấu và không chứa khoảng trắng.
- [ ] Giá trị `FAMILY_CODE` dùng cho backup thống nhất với `familyCode`.
- [ ] Chạy `npm run dev` và kiểm tra trang chủ, thanh điều hướng, hình nền và trang đăng nhập.
- [ ] Dừng Frontend local bằng `Ctrl+C` sau khi kiểm tra.

Xem chi tiết: [`02_BRANDING.md`](02_BRANDING.md).

## 6. Chặng 3 – Tạo hệ thống Railway

### Bước 9. Tạo Railway Project

- [ ] Đăng nhập Railway.
- [ ] Tạo Project mới.
- [ ] Đặt tên, ví dụ: `FamilyTree-TocLe`.

### Bước 10. Tạo ba thành phần trong Project

- [ ] Tạo MySQL Service.
- [ ] Tạo Backend Service trống, ví dụ: `Backend-FamilyTree`.
- [ ] Tạo Railway Volume, ví dụ: `Avatar-Volume`.
- [ ] Xác nhận cả ba thành phần xuất hiện trên Project Canvas.

Xem chi tiết: [Phần 3 – Tạo Railway Project](03_DEPLOYMENT.md#3-tạo-railway-project).

## 7. Chặng 4 – Cấu hình và triển khai Backend

### Bước 11. Kết nối Backend với MySQL

Trong **Variables** của Backend Service, thêm năm biến kết nối MySQL bằng Reference Variable theo hướng dẫn chi tiết:

- [ ] `MYSQLHOST`
- [ ] `MYSQLPORT`
- [ ] `MYSQLUSER`
- [ ] `MYSQLPASSWORD`
- [ ] `MYSQLDATABASE`

Không tự nghĩ ra giá trị. Các giá trị này do MySQL Service trên Railway cung cấp.

Xem chi tiết: [Phần 4 – Kết nối Backend với MySQL](03_DEPLOYMENT.md#4-kết-nối-backend-với-mysql).

### Bước 12. Tạo SECRET_KEY

Mở PowerShell và chạy:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

- [ ] Sao chép đúng chuỗi mới do Python tạo.
- [ ] Thêm chuỗi đó vào biến `SECRET_KEY` của Backend Service.
- [ ] Không ghi giá trị thật vào tài liệu hoặc GitHub.

### Bước 13. Thêm các biến hệ thống

Trong **Variables** của Backend Service, thêm:

```dotenv
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480
FAMILY_CODE=TocLe
```

- [ ] Đã thay `TocLe` bằng mã dòng tộc đang triển khai.
- [ ] Đã lưu và áp dụng Variables.
- [ ] Đã Seal `SECRET_KEY` nếu Railway cung cấp chức năng này.

Xem chi tiết: [Phần 5 – Tạo SECRET_KEY](03_DEPLOYMENT.md#5-tạo-secret_key-và-thêm-biến-hệ-thống).

### Bước 14. Chuẩn bị GitHub repository

- [ ] Tạo repository dành cho bản triển khai hiện tại.
- [ ] Đưa mã nguồn FamilyTree Clean lên repository.
- [ ] Kiểm tra repository không chứa `.env`, backup, avatar thật hoặc secret.

### Bước 15. Kết nối Backend Service với GitHub

- [ ] Mở Backend Service trên Railway.
- [ ] Chọn repository vừa chuẩn bị làm nguồn triển khai.
- [ ] Kiểm tra Root Directory theo tài liệu chi tiết.
- [ ] Kiểm tra Build Command.
- [ ] Kiểm tra Start Command.
- [ ] Lưu thay đổi và chờ Railway deploy.

### Bước 16. Tạo URL Backend

- [ ] Mở **Settings → Networking** của Backend Service.
- [ ] Tạo Public Domain nếu chưa có.
- [ ] Ghi URL Backend vào Phiếu thông tin triển khai.
- [ ] Mở URL Backend và thêm `/docs`.
- [ ] Swagger UI mở được.

Xem chi tiết: [Phần 6 – Deploy Backend lên Railway](03_DEPLOYMENT.md#6-deploy-backend-lên-railway).

### Bước 17. Kiểm tra Railway Volume

- [ ] Volume được kết nối với Backend Service.
- [ ] Mount Path là:

```text
/app/backend/static/avatars
```

- [ ] Thay đổi đã được áp dụng.

Xem chi tiết: [Phần 7 – Railway Volume](03_DEPLOYMENT.md#7-kiểm-tra-railway-volume).

## 8. Chặng 5 – Khởi tạo database và Admin Railway

### Bước 18. Import schema vào database Railway

- [ ] Mở MySQL Workbench.
- [ ] Kết nối đến MySQL Service bằng thông tin Railway cung cấp.
- [ ] Import file:

```text
database/schema.sql
```

- [ ] Database có đúng tám bảng:

```text
announcements
audit_logs
feedback
marriages
parent_child
person_marriage_priority
persons
users
```

- [ ] Các bảng ban đầu đều rỗng.
- [ ] Đã đóng kết nối công khai của MySQL sau khi import xong.

Xem chi tiết: [Phần 8 – Khởi tạo database rỗng](03_DEPLOYMENT.md#8-khởi-tạo-database-rỗng).

### Bước 19. Tạo Admin đầu tiên trên Railway

- [ ] Đăng nhập Railway CLI từ PowerShell.
- [ ] Liên kết thư mục mã nguồn với Railway Project.
- [ ] Mở kết nối đến Backend Service theo hướng dẫn chi tiết.
- [ ] Chạy:

```text
python -m backend.create_first_admin
```

- [ ] Nhập Username Admin.
- [ ] Nhập họ tên Admin.
- [ ] Nhập và xác nhận mật khẩu.
- [ ] Công cụ báo tạo Admin thành công.
- [ ] Bảng `users` có đúng một tài khoản.

Xem chi tiết: [Phần 9 – Tạo Admin đầu tiên](03_DEPLOYMENT.md#9-tạo-admin-đầu-tiên).

## 9. Chặng 6 – Cấu hình và triển khai Frontend

### Bước 20. Tạo cấu hình Frontend

Mở PowerShell tại thư mục Frontend:

```powershell
Set-Location "D:\projects\FamilyTree_Clean_v1.0\frontend-vite"
```

Tạo file cấu hình:

```powershell
Copy-Item .env.example .env.production
```

Mở `.env.production` và đặt URL Backend thật:

```dotenv
VITE_API_BASE_URL=https://dia-chi-backend-that.up.railway.app/api
```

- [ ] URL bắt đầu bằng `https://`.
- [ ] URL kết thúc bằng `/api`.
- [ ] Không ghi mật khẩu hoặc secret vào `.env.production`.

Xem chi tiết: [Phần 10 – Cấu hình Frontend](03_DEPLOYMENT.md#10-cấu-hình-frontend-kết-nối-backend).

### Bước 21. Đặt tên Cloudflare Worker

Mở:

```text
frontend-vite/wrangler.toml
```

Đổi tên Worker theo dạng:

```toml
name = "familytree-tocle"
```

- [ ] Tên viết thường, không dấu và không có khoảng trắng.
- [ ] Chỉ sử dụng chữ cái, chữ số và dấu gạch ngang.
- [ ] Không thêm `.workers.dev` vào tên.

Xem chi tiết: [Phần 11 – Đặt tên Cloudflare Worker](03_DEPLOYMENT.md#11-đặt-tên-cloudflare-worker).

### Bước 22. Build Frontend

Trong thư mục `frontend-vite`, chạy:

```powershell
npm ci
npm run build
```

- [ ] Lệnh không báo lỗi.
- [ ] Có thư mục `dist`.
- [ ] Có file `dist/index.html`.

Xem chi tiết: [Phần 12 – Build Frontend](03_DEPLOYMENT.md#12-build-frontend).

### Bước 23. Deploy Frontend lên Cloudflare

Đăng nhập Cloudflare từ PowerShell:

```powershell
npx wrangler login
```

Kiểm tra tài khoản:

```powershell
npx wrangler whoami
```

Triển khai:

```powershell
npx wrangler deploy
```

- [ ] Wrangler báo triển khai thành công.
- [ ] Đã sao chép URL `workers.dev` thật.
- [ ] Đã ghi URL Frontend vào Phiếu thông tin triển khai.
- [ ] URL Frontend mở được trên Google Chrome.

Xem chi tiết: [Phần 13 – Deploy Cloudflare Worker](03_DEPLOYMENT.md#13-deploy-frontend-lên-cloudflare).

## 10. Chặng 7 – Kiểm tra và bàn giao

### Bước 24. Kiểm tra trạng thái ban đầu

Thực hiện trước khi tạo dữ liệu thử nghiệm:

- [ ] Trang chủ hiển thị đúng tên dòng tộc, khẩu hiệu và hình nền.
- [ ] Trang đăng nhập hiển thị đúng tên dòng tộc.
- [ ] Swagger Backend mở được.
- [ ] Admin đầu tiên đăng nhập được.
- [ ] Danh sách thành viên ban đầu rỗng.
- [ ] Audit Log không có dữ liệu cũ.
- [ ] Không có avatar người thật.
- [ ] Frontend gọi đúng Backend Railway hiện tại.

### Bước 25. Kiểm tra tạo dữ liệu và Volume

- [ ] Tạo một thành viên thử nghiệm, không dùng tên người thật.
- [ ] Audit Log ghi nhận thao tác mới.
- [ ] Upload một avatar thử nghiệm, không dùng ảnh người thật.
- [ ] Redeploy Backend Service.
- [ ] Thành viên thử nghiệm vẫn còn.
- [ ] Avatar thử nghiệm vẫn còn sau redeploy.

Xem chi tiết: [Phần 14 – Kiểm tra sau triển khai](03_DEPLOYMENT.md#14-kiểm-tra-sau-triển-khai).

### Bước 26. Xử lý dữ liệu thử nghiệm

- [ ] Đã ghi nhận thành viên, avatar và Audit Log được tạo khi kiểm tra.
- [ ] Đã xử lý dữ liệu thử nghiệm theo kế hoạch bàn giao.
- [ ] Không nhầm dữ liệu thử nghiệm với dữ liệu chính thức của dòng tộc.

### Bước 27. Kiểm tra an toàn cuối cùng

- [ ] Không có hai hệ thống dùng chung MySQL database.
- [ ] Không có hai hệ thống dùng chung Railway Volume.
- [ ] `SECRET_KEY` được tạo riêng và không xuất hiện trong tài liệu.
- [ ] `.env.production` trỏ đúng Backend hiện tại.
- [ ] Repository không chứa backup, avatar thật hoặc secret.
- [ ] Không có secret trong GitHub, email, tin nhắn hoặc tài liệu bàn giao.

Xem chi tiết: [Phần 15 – Những điều tuyệt đối không làm](03_DEPLOYMENT.md#15-những-điều-tuyệt-đối-không-làm).

## 11. Khi nào phải dừng lại

Dừng tại bước đang thực hiện và mở `03_DEPLOYMENT.md` khi:

- Railway hoặc Cloudflare báo lỗi triển khai.
- Swagger không mở được.
- Không kết nối được database.
- Thiếu bảng `users` hoặc không đủ tám bảng.
- Admin không đăng nhập được.
- Frontend gọi sai Backend.
- Avatar mất sau khi Backend redeploy.
- Không xác định được một Project, Service, Volume hoặc Worker đang dùng cho mục đích nào.

Không xóa, ghi đè hoặc thay đổi tài nguyên chưa xác định rõ.

## 12. Video hướng dẫn

Các video sau sẽ được bổ sung sau khi tài liệu chữ được chốt:

| Video | Nội dung | Trạng thái |
|---|---|---|
| 01 | Tạo Railway Project, MySQL, Backend và Volume | Chưa bổ sung |
| 02 | Kết nối MySQL và thêm Variables | Chưa bổ sung |
| 03A | Chuẩn bị GitHub và kết nối Backend | Chưa bổ sung |
| 03B | Deploy Backend và tạo URL Railway | Chưa bổ sung |
| 04 | Import schema và tạo Admin đầu tiên | Chưa bổ sung |
| 05 | Build và deploy Frontend lên Cloudflare | Chưa bổ sung |
| 06 | Kiểm tra hệ thống và Volume sau redeploy | Chưa bổ sung |

## 13. Hoàn thành

Chỉ bàn giao hệ thống khi toàn bộ ô kiểm tra từ Bước 1 đến Bước 27 đã hoàn thành và hai URL sau hoạt động:

```text
Backend URL  → https://...up.railway.app
Frontend URL → https://...workers.dev
```

Tài liệu tra cứu chi tiết: [`03_DEPLOYMENT.md`](03_DEPLOYMENT.md).
