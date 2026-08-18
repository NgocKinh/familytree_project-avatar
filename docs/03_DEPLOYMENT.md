# Triển khai FamilyTree Clean v1.0

Tài liệu này hướng dẫn triển khai một hệ thống FamilyTree độc lập cho một dòng tộc mới:

- Backend chạy trên Railway.
- MySQL riêng trên Railway.
- Railway Volume riêng để lưu avatar.
- Frontend chạy trên Cloudflare Workers.
- URL, tài khoản Admin và khóa bí mật riêng.

> Ví dụ trong tài liệu sử dụng **Tộc Lê**. Khi triển khai thực tế, thay `TocLe`, `FamilyTree-TocLe` và `familytree-tocle` bằng thông tin của dòng tộc đang triển khai.

Nếu cần lộ trình ngắn để theo dõi toàn bộ công việc, mở [`00_START_HERE.md`](00_START_HERE.md).

## Cách sử dụng tài liệu

Tài liệu này dành cho người đã cài đặt FamilyTree trên máy Windows theo `01_INSTALLATION.md` và đã thay thông tin dòng tộc theo `02_BRANDING.md`.

Thực hiện lần lượt từ Phần 1 đến Phần 16. Không bỏ qua phần kiểm tra ở cuối mỗi giai đoạn. Trong các ví dụ:

- Nội dung trong khối lệnh được sao chép vào PowerShell hoặc file cấu hình.
- Nội dung có chữ **ví dụ** phải được thay bằng thông tin triển khai thật.
- Ô `[ ]` được đổi thành `[x]` sau khi đã kiểm tra đạt.
- Khi kết quả khác mô tả, dừng tại bước đang làm và kiểm tra lại trước khi chuyển sang phần tiếp theo.

Chuẩn bị một phiếu ghi thông tin triển khai:

| Thông tin | Ví dụ | Giá trị thật |
|---|---|---|
| Tên dòng tộc | Tộc Lê | |
| Mã dòng tộc | `TocLe` | |
| Railway Project | `FamilyTree-TocLe` | |
| Backend Service | `Backend-FamilyTree` | |
| MySQL Service | `MySQL` | |
| Railway Volume | `Avatar-Volume` | |
| GitHub repository | Repository riêng của Tộc Lê | |
| Backend URL | `https://...up.railway.app` | |
| Cloudflare Worker | `familytree-tocle` | |
| Frontend URL | `https://...workers.dev` | |
| Username Admin | Không ghi mật khẩu | |

Không ghi mật khẩu, `SECRET_KEY`, token hoặc thông tin đăng nhập database vào phiếu này.

## 1. Mỗi dòng tộc phải có hệ thống riêng

Mỗi dòng tộc phải có riêng:

| Thành phần | Ví dụ cho Tộc Lê |
|---|---|
| Railway Project | `FamilyTree-TocLe` |
| Backend Service | `Backend-FamilyTree` |
| MySQL Service | Tên Railway tạo hoặc tên đã đặt |
| Railway Volume | `Avatar-Volume` |
| Cloudflare Worker | `familytree-tocle` |
| `SECRET_KEY` | Chuỗi ngẫu nhiên riêng |
| Admin đầu tiên | Tài khoản riêng |

Sau khi triển khai, hệ thống có hai địa chỉ:

- **Backend URL:** Railway cấp, ví dụ `https://...up.railway.app`.
- **Frontend URL:** Cloudflare cấp, ví dụ `https://...workers.dev`.

Backend URL dùng cho Frontend gọi API. Frontend URL là địa chỉ gửi cho người sử dụng.

### 1.1. Ý nghĩa các thành phần

- **Railway Project** là khu vực quản lý toàn bộ tài nguyên trực tuyến của một dòng tộc.
- **Backend Service** xử lý đăng nhập, thành viên, quan hệ gia đình, phân quyền, Audit Log và backup.
- **MySQL Service** lưu dữ liệu có cấu trúc như thành viên, hôn nhân, tài khoản và nhật ký.
- **Railway Volume** lưu file avatar. Database không thay thế cho Volume.
- **Cloudflare Worker** cung cấp giao diện web để người dùng truy cập bằng trình duyệt.
- **SECRET_KEY** được Backend sử dụng để bảo vệ thông tin đăng nhập; đây không phải mật khẩu Admin.

### 1.2. Cách nhận biết đang mở đúng hệ thống

Trước khi sửa một tài nguyên, đọc tên Railway Project ở đầu trang và tên Service đang được chọn. Trước khi deploy Cloudflare, kiểm tra dòng `name` trong `wrangler.toml`. Nếu tên không khớp phiếu triển khai, không tiếp tục.

> Không chọn Railway Project, Service, Volume, database hoặc Worker đang phục vụ dòng tộc khác.

## 2. Chuẩn bị bộ mã nguồn

Chỉ sử dụng repository Clean được tạo cho lần triển khai hiện tại.

### 2.1. Kiểm tra thư mục mã nguồn

Mở PowerShell tại thư mục gốc:

```powershell
Set-Location "D:\projects\FamilyTree_Clean_v1.0"
git status --short
```

Lệnh này cho biết những file đang thay đổi hoặc chưa được Git theo dõi. Kết quả không nhất thiết phải hoàn toàn trống trong lúc chuẩn bị, nhưng mọi file xuất hiện phải được nhận biết rõ. Không đưa lên GitHub các file cấu hình chứa giá trị thật.

Kiểm tra thêm các file thường bị đưa nhầm vào repository:

```powershell
Get-ChildItem -Recurse -Force -File |
  Where-Object { $_.Name -match '^\.env|\.sql$|\.zip$' } |
  Select-Object FullName
```

Nếu thấy `.env.example` hoặc `schema.sql`, đó có thể là file mẫu hợp lệ. Nếu thấy `.env`, backup `.zip` hoặc SQL dump có dữ liệu, phải xác định và loại khỏi repository trước khi push.

Kiểm tra repository không chứa:

- File `.env` hoặc `.env.local` có giá trị thật.
- Backup hoặc database dump chứa dữ liệu.
- Avatar người thật.
- Tài khoản, mật khẩu, token hoặc khóa bí mật.
- Dữ liệu của dòng tộc khác.

### 2.2. Chuẩn bị tài khoản

- [ ] GitHub.
- [ ] Railway đã kết nối với GitHub.
- [ ] Cloudflare.

### 2.3. Kết quả cần đạt

- [ ] Đúng bộ `FamilyTree_Clean_v1.0`.
- [ ] Repository không chứa dữ liệu hoặc bí mật.
- [ ] Đã xác định tên dòng tộc, mã dòng tộc và tên các tài nguyên.

### 2.4. Khi chưa đạt

- Không biết file có an toàn hay không: chưa commit hoặc push file đó.
- Repository có lịch sử của dòng tộc khác: tạo repository Clean mới theo quy trình bàn giao.
- Phát hiện secret từng được push: xóa secret khỏi mã nguồn và tạo giá trị mới; chỉ xóa file ở commit mới không làm secret cũ tự mất khỏi lịch sử.

## 3. Tạo Railway Project

### 3.1. Tạo Project mới

1. Đăng nhập Railway.
2. Chọn tạo **New Project**.
3. Đặt tên riêng, ví dụ:

```text
FamilyTree-TocLe
```

Sau khi tạo, kiểm tra tên Project hiển thị đúng. Tên Project chỉ dùng để quản lý trên Railway, không phải URL trang web.

### 3.2. Tạo MySQL Service

1. Trong Project vừa tạo, chọn thêm Service.
2. Chọn **Database → MySQL**.
3. Chờ Railway khởi tạo hoàn tất.

Không sử dụng MySQL Service của Project khác.

Railway sẽ tự tạo database và các biến kết nối. Không cần tự nhập host, port hoặc password ở giai đoạn này.

### 3.3. Tạo Backend Service

Tạo một Service trống và đặt tên:

```text
Backend-FamilyTree
```

Chưa cần kết nối repository ở bước này.

Nếu Railway yêu cầu chọn nguồn ngay khi tạo Service, có thể quay lại Project Canvas và dùng lựa chọn tạo Service trống, sau đó kết nối GitHub ở Phần 6.

### 3.4. Tạo Volume lưu avatar

1. Thêm một Volume mới trong cùng Project.
2. Đặt tên, ví dụ:

```text
Avatar-Volume
```

3. Kết nối Volume với `Backend-FamilyTree`.

Ở bước tạo Volume, chưa chọn Mount Path tùy ý. Đường dẫn chính xác sẽ được đặt và kiểm tra tại Phần 7.

### 3.5. Kết quả cần đạt

Trên Project Canvas phải có:

- [ ] Một MySQL Service.
- [ ] `Backend-FamilyTree`.
- [ ] `Avatar-Volume`.

Nếu một thành phần nằm ngoài Project hiện tại, không coi là đã hoàn thành. Ba thành phần phải xuất hiện trong cùng Railway Project.

## 4. Kết nối Backend với MySQL

Backend sử dụng năm biến môi trường:

Các biến này cho Backend biết database nằm ở đâu và dùng tài khoản nào để kết nối. Railway MySQL đã có sẵn giá trị thật; Backend chỉ cần tham chiếu đến chúng. Cách tham chiếu giúp tránh sao chép mật khẩu database bằng tay.

| Biến Backend | Biến Railway MySQL |
|---|---|
| `DB_HOST` | `MYSQLHOST` |
| `DB_PORT` | `MYSQLPORT` |
| `DB_USER` | `MYSQLUSER` |
| `DB_PASSWORD` | `MYSQLPASSWORD` |
| `DB_NAME` | `MYSQLDATABASE` |

### 4.1. Thêm Reference Variables

1. Mở `Backend-FamilyTree`.
2. Chọn thẻ **Variables**.
3. Mở **RAW Editor**.
4. Nếu đã có nội dung, không xóa các biến cũ.
5. Thêm khối sau:

```dotenv
DB_HOST=${{MySQL.MYSQLHOST}}
DB_PORT=${{MySQL.MYSQLPORT}}
DB_USER=${{MySQL.MYSQLUSER}}
DB_PASSWORD=${{MySQL.MYSQLPASSWORD}}
DB_NAME=${{MySQL.MYSQLDATABASE}}
```

Nếu MySQL Service không có tên `MySQL`, thay phần `MySQL` trước dấu chấm bằng đúng tên Service đang hiển thị trên Project Canvas.

6. Bấm **Add**, **Update Variables** hoặc nút xác nhận đang hiển thị.
7. Nếu Railway yêu cầu áp dụng thay đổi, bấm **Deploy**.

Sau khi dán vào RAW Editor, Railway có thể hiển thị giá trị theo dạng tham chiếu hoặc thay bằng giao diện chọn Service. Điều quan trọng là nguồn của cả năm biến phải là MySQL Service trong Project hiện tại.

### 4.2. Kiểm tra từng biến

Mở lại **Variables** và đối chiếu:

```text
DB_HOST     → MySQL.MYSQLHOST
DB_PORT     → MySQL.MYSQLPORT
DB_USER     → MySQL.MYSQLUSER
DB_PASSWORD → MySQL.MYSQLPASSWORD
DB_NAME     → MySQL.MYSQLDATABASE
```

Tên bên trái phải đúng với Backend. Tên bên phải phải đúng với biến Railway MySQL. Không đổi `DB_USER` thành `MYSQLUSER` ở phía Backend.

### 4.3. Kết quả cần đạt

- [ ] Có đủ năm biến từ `DB_HOST` đến `DB_NAME`.
- [ ] Các biến tham chiếu đúng MySQL Service hiện tại.
- [ ] Không nhập thủ công mật khẩu database vào tài liệu hoặc mã nguồn.

### 4.4. Lỗi thường gặp

**Railway báo tham chiếu không tồn tại:** kiểm tra tên MySQL Service. Nếu Service được đặt tên khác `MySQL`, sửa phần trước dấu chấm trong `${{...}}`.

**Backend báo không kết nối được database:** kiểm tra đủ năm biến, đặc biệt `DB_HOST`, `DB_PORT` và `DB_NAME`; sau đó redeploy Backend để biến mới được áp dụng.

**Thêm biến nhầm vào MySQL Service:** xóa các biến `DB_*` vừa thêm nhầm và thêm lại vào `Backend-FamilyTree`.

## 5. Tạo SECRET_KEY và thêm biến hệ thống

Mỗi hệ thống phải có một `SECRET_KEY` riêng.

### 5.1. Tạo SECRET_KEY

Mở PowerShell và chạy:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Sao chép đúng chuỗi do Python vừa tạo. Không sử dụng chuỗi minh họa hoặc khóa của hệ thống khác.

Ví dụ hình thức của kết quả:

```text
AbCdEf...một-chuỗi-dài-ngẫu-nhiên...XyZ
```

Đây chỉ là minh họa hình thức, không dùng làm khóa thật. Khi sao chép, chỉ chọn chuỗi kết quả; không sao chép phần `PS C:\...>` của PowerShell.

### 5.2. Thêm vào Backend Service

Trong **Variables** của `Backend-FamilyTree`:

1. Tạo biến `SECRET_KEY`.
2. Dán chuỗi vừa tạo làm giá trị.
3. Mở **RAW Editor** và thêm:

```dotenv
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480
FAMILY_CODE=TocLe
```

Thay `TocLe` bằng mã dòng tộc đang triển khai. Giá trị này nên giống `familyCode` trong `frontend-vite/src/config/familyConfig.js`.

4. Lưu và áp dụng các biến.
5. Seal `SECRET_KEY` nếu Railway hiển thị chức năng này.

Sau khi Seal, Railway vẫn cung cấp giá trị cho Backend nhưng có thể không cho xem lại. Nếu mất khóa, không cần tìm cách khôi phục giá trị cũ; hãy tạo khóa mới và cập nhật biến. Việc đổi khóa có thể làm các phiên đăng nhập hiện tại hết hiệu lực.

### 5.3. Ý nghĩa các biến

- `SECRET_KEY`: khóa riêng dùng để bảo vệ token đăng nhập.
- `ALGORITHM=HS256`: thuật toán Backend đang sử dụng cùng khóa.
- `ACCESS_TOKEN_EXPIRE_MINUTES=480`: phiên đăng nhập có hiệu lực 480 phút, tương đương 8 giờ.
- `FAMILY_CODE=TocLe`: mã dùng trong tên file backup.

### 5.4. Kết quả cần đạt

```text
SECRET_KEY                  → chuỗi riêng do Python tạo
ALGORITHM                   → HS256
ACCESS_TOKEN_EXPIRE_MINUTES → 480
FAMILY_CODE                 → mã dòng tộc hiện tại
```

Không tiếp tục nếu `SECRET_KEY` trống, được dùng lại hoặc được thêm nhầm vào MySQL Service.

### 5.5. Lỗi thường gặp

- PowerShell không nhận lệnh `python`: kiểm tra lại cài đặt Python theo `01_INSTALLATION.md`.
- Dán chuỗi có khoảng trắng ở đầu hoặc cuối: tạo lại khóa và dán lại cẩn thận.
- `FAMILY_CODE` vẫn là mã mẫu hoặc mã dòng tộc khác: sửa trước khi deploy.
- Backend đã deploy trước khi thêm đủ biến: thêm đủ biến rồi redeploy.

## 6. Deploy Backend lên Railway

### 6.1. Chuẩn bị GitHub repository

1. Tạo repository dành riêng cho hệ thống hiện tại.
2. Đưa mã nguồn FamilyTree Clean lên repository.
3. Kiểm tra lại repository không chứa `.env`, backup, avatar thật hoặc secret.

Repository phải chứa tối thiểu các thành phần Backend cần dùng như `requirements.txt`, thư mục `backend` và file schema để bàn giao. Không chỉ đưa riêng thư mục `backend` lên GitHub nếu cấu trúc dự án yêu cầu file ở thư mục gốc.

### 6.2. Kết nối repository

1. Mở `Backend-FamilyTree` trên Railway.
2. Chọn kết nối nguồn triển khai từ GitHub.
3. Chọn đúng repository vừa chuẩn bị.
4. Chọn nhánh triển khai, thông thường là `main`.

Nếu Railway yêu cầu quyền GitHub, chỉ cấp quyền cho tài khoản hoặc repository cần dùng.

Sau khi kết nối, Railway có thể tự khởi động một lần deploy. Lần deploy này chưa chắc thành công nếu Build Command, Start Command hoặc Variables chưa đầy đủ. Tiếp tục cấu hình đúng rồi thực hiện deployment mới.

### 6.3. Cấu hình Build và Deploy

Trong **Settings** của Backend Service:

- **Root Directory:** để trống hoặc `/`.
- Không đặt Root Directory là `/backend` vì `requirements.txt` nằm ở thư mục gốc.
- **Build Command:**

```text
pip install -r requirements.txt
```

- **Start Command:**

```text
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

Giữ nguyên `$PORT`.

Ý nghĩa:

- `pip install -r requirements.txt` cài các thư viện Python của dự án.
- `backend.main:app` trỏ đến ứng dụng FastAPI trong `backend/main.py`.
- `--host 0.0.0.0` cho phép Railway truy cập ứng dụng.
- `--port $PORT` sử dụng cổng Railway cấp tự động.

Không thay `$PORT` bằng `8000`; cổng `8000` chỉ thường dùng khi chạy local.

### 6.4. Triển khai và xem log

1. Lưu cấu hình.
2. Mở **Deployments**.
3. Chọn lần triển khai mới nhất.
4. Theo dõi **Build Logs** và **Deploy Logs**.

Chỉ tiếp tục khi trạng thái là **Success** hoặc **Active**. Nếu trạng thái là **Failed**, đọc các dòng lỗi cuối trong log trước khi sửa.

Các dấu hiệu thường gặp trong log:

- Không tìm thấy `requirements.txt`: kiểm tra Root Directory.
- Không tìm thấy module `backend`: kiểm tra Start Command và cấu trúc repository.
- Thiếu biến môi trường: quay lại Phần 4 và Phần 5.
- Kết nối MySQL thất bại: kiểm tra Reference Variables và trạng thái MySQL Service.

### 6.5. Tạo Backend URL

1. Mở **Settings → Networking**.
2. Chọn **Generate Domain** nếu chưa có Public Domain.
3. Sao chép URL Railway thật.
4. Mở Swagger bằng cách thêm `/docs`:

```text
https://dia-chi-backend.up.railway.app/docs
```

Trang gốc của Backend có thể không giống một trang web thông thường. Phép kiểm tra chính là Swagger `/docs` mở được và hiển thị danh sách API.

### 6.6. Kết quả cần đạt

- [ ] Deployment thành công.
- [ ] Backend có Public Domain riêng.
- [ ] Swagger UI mở được.
- [ ] Đã ghi lại Backend URL, không ghi secret.

### 6.7. Không tiếp tục khi

- Deployment còn trạng thái Failed hoặc Crashed.
- Swagger trả về trang lỗi.
- Log lặp lại lỗi kết nối database.
- URL đang thuộc Backend của hệ thống khác.

## 7. Kiểm tra Railway Volume

Railway Service có thể được tạo lại khi redeploy. Nếu avatar chỉ nằm trong hệ thống file tạm của Service, ảnh có thể mất. Volume cung cấp vùng lưu trữ lâu dài và phải được gắn đúng đường dẫn Backend sử dụng.

### 7.1. Kiểm tra kết nối

1. Mở `Avatar-Volume`.
2. Xác nhận Volume kết nối với `Backend-FamilyTree`.
3. Kiểm tra Mount Path:

```text
/app/backend/static/avatars
```

4. Lưu và áp dụng thay đổi nếu Railway yêu cầu.

Mount Path này giúp các avatar tải lên không mất khi Backend redeploy.

Sau khi thêm hoặc sửa Volume, Railway có thể tạo deployment mới. Chờ Backend hoạt động lại rồi mới kiểm tra Swagger.

### 7.2. Kết quả cần đạt

- [ ] Volume thuộc đúng Railway Project.
- [ ] Volume gắn đúng Backend Service.
- [ ] Mount Path chính xác.

> Không xóa hoặc thay Volume sau khi hệ thống đã có avatar thật nếu chưa có phương án sao lưu và phục hồi.

### 7.3. Lỗi thường gặp

- Volume gắn nhầm Service: tháo khỏi Service trống và gắn đúng `Backend-FamilyTree`.
- Mount Path thiếu `/app` hoặc sai tên thư mục: sửa đúng toàn bộ đường dẫn.
- Backend lỗi ngay sau khi mount: mở Deploy Logs để kiểm tra quyền hoặc đường dẫn, không xóa Volume vội.
- Avatar mất sau redeploy: kiểm tra file được ghi vào đúng thư mục mount, sau đó thử lại bằng avatar không phải ảnh người thật.

## 8. Khởi tạo database rỗng

File `database/schema.sql` chỉ tạo cấu trúc bảng, không chèn dữ liệu.

Phần này thực hiện sau khi Backend đã deploy và MySQL Service đang hoạt động. Việc import schema chỉ làm một lần cho database mới. Không chạy schema vào database Production của dòng tộc khác.

### 8.1. Mở kết nối MySQL bên ngoài

1. Mở MySQL Service trên Railway.
2. Lấy thông tin kết nối công khai Railway cung cấp.
3. Chỉ mở Public Networking trong thời gian cần import schema.

Thông tin public có thể khác các biến nội bộ `MYSQLHOST` và `MYSQLPORT`. Khi kết nối từ máy Windows, dùng đúng host và port được Railway hiển thị cho kết nối bên ngoài.

### 8.2. Kết nối bằng MySQL Workbench

Tạo kết nối mới bằng các thông tin Railway cung cấp:

- Host.
- Port.
- Username.
- Password.
- Database name.

Không ghi các giá trị thật vào tài liệu bàn giao.

Trong MySQL Workbench:

1. Bấm dấu `+` tại **MySQL Connections**.
2. Đặt Connection Name dễ nhận biết, ví dụ `FamilyTree-TocLe-Railway`.
3. Nhập Hostname, Port và Username.
4. Lưu password bằng chức năng của Workbench nếu máy tính được quản lý an toàn.
5. Bấm **Test Connection**.

Chỉ chuyển sang import khi Workbench báo kết nối thành công.

### 8.3. Chạy schema

1. Mở file:

```text
database/schema.sql
```

2. Chọn đúng database của hệ thống hiện tại.
3. Chạy toàn bộ file.
4. Làm mới danh sách Tables.

Nếu Workbench mở file nhưng chưa chọn database, chọn đúng schema ở cột bên trái trước khi chạy. Không chạy đồng thời nhiều tab SQL vào các database khác nhau.

Database phải có đúng tám bảng:

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

### 8.4. Kiểm tra dữ liệu ban đầu

```sql
SELECT COUNT(*) FROM persons;
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM audit_logs;
```

Các kết quả phải bằng `0` trước khi tạo Admin đầu tiên.

Có thể kiểm tra thêm rằng file schema không chứa dữ liệu mẫu:

```powershell
Select-String -Path .\database\schema.sql -Pattern '^\s*INSERT\s+INTO'
```

Không có kết quả là đúng đối với schema Clean.

Sau khi import xong, đóng Public Networking của MySQL nếu không còn cần sử dụng.

### 8.5. Kết quả cần đạt

- [ ] Có đúng tám bảng.
- [ ] `persons`, `users` và `audit_logs` đang rỗng.
- [ ] Không có dữ liệu của dòng tộc khác.

### 8.6. Lỗi thường gặp

- **Không kết nối được:** kiểm tra Public Networking, host, port và trạng thái MySQL Service.
- **Access denied:** nhập lại username/password Railway cung cấp, không dùng tài khoản MySQL local.
- **Không thấy bảng sau khi chạy:** kiểm tra đã chọn đúng database và làm mới mục Tables.
- **Báo bảng đã tồn tại:** xác định database có thực sự mới hay không; không xóa bảng khi chưa rõ dữ liệu thuộc hệ thống nào.

## 9. Tạo Admin đầu tiên

Công cụ chỉ cho phép tạo Admin đầu tiên khi bảng `users` còn rỗng.

Admin đầu tiên có quyền quản lý hệ thống. Chỉ tạo sau khi đã xác nhận database đúng và rỗng. Không dùng tài khoản Admin của dòng tộc khác.

### 9.1. Chuẩn bị

Chuẩn bị riêng:

- Username Admin.
- Họ tên Admin.
- Mật khẩu tối thiểu 12 ký tự.

Không ghi mật khẩu vào tài liệu.

### 9.2. Cài Railway CLI

Mở PowerShell:

```powershell
npm install -g @railway/cli
railway --version
```

Nếu PowerShell báo không nhận lệnh `npm`, cài hoặc kiểm tra Node.js theo `01_INSTALLATION.md`, sau đó đóng và mở lại PowerShell.

### 9.3. Đăng nhập và liên kết Project

```powershell
Set-Location "D:\projects\FamilyTree_Clean_v1.0"
railway login
railway link
```

Khi Railway hỏi, chọn đúng:

- Workspace.
- Project `FamilyTree-TocLe`.
- Environment `production`.
- Service `Backend-FamilyTree`.

Đọc kỹ từng lựa chọn trước khi nhấn Enter. Nếu liên kết nhầm Project hoặc Service, dừng lại và chạy `railway link` lần nữa để chọn đúng.

### 9.4. Mở SSH và tạo Admin

```powershell
railway ssh --service Backend-FamilyTree
python -m backend.create_first_admin
```

Nhập lần lượt Username, họ tên, mật khẩu và xác nhận mật khẩu. Mật khẩu không hiển thị khi nhập là bình thường.

Không bấm nhiều lần khi không thấy ký tự mật khẩu. Hãy nhập đủ mật khẩu rồi nhấn Enter. Công cụ sẽ từ chối nếu mật khẩu không đạt yêu cầu hoặc hai lần nhập không giống nhau.

Sau khi công cụ báo thành công, thoát SSH:

```text
exit
```

### 9.5. Kết quả cần đạt

- [ ] Công cụ báo tạo Admin thành công.
- [ ] Bảng `users` có đúng một tài khoản.
- [ ] Không chạy lại công cụ để tạo thêm Admin đầu tiên.

### 9.6. Kiểm tra bằng giao diện

Sau khi Frontend được deploy ở Phần 13, dùng Username và mật khẩu vừa tạo để đăng nhập. Nếu không đăng nhập được:

1. Kiểm tra Frontend đang gọi đúng Backend.
2. Kiểm tra bảng `users` có tài khoản vừa tạo.
3. Kiểm tra thời điểm tạo Admin không bị nhầm Railway Project.
4. Không tạo thêm nhiều tài khoản để thử khi chưa xác định nguyên nhân.

## 10. Cấu hình Frontend kết nối Backend

Giá trị `VITE_API_BASE_URL` được đóng vào bản Frontend tại thời điểm build. Vì vậy, sau khi sửa `.env.production`, luôn phải chạy lại `npm run build` trước khi deploy Cloudflare.

### 10.1. Tạo file cấu hình Production

Mở PowerShell:

```powershell
Set-Location "D:\projects\FamilyTree_Clean_v1.0\frontend-vite"
Copy-Item .env.example .env.production
```

Mở `.env.production` và đặt:

```dotenv
VITE_API_BASE_URL=https://dia-chi-backend-that.up.railway.app/api
```

Thay URL ví dụ bằng Backend URL thật của hệ thống hiện tại.

Ví dụ Backend URL là:

```text
https://familytree-tocle-production.up.railway.app
```

thì giá trị cần nhập là:

```dotenv
VITE_API_BASE_URL=https://familytree-tocle-production.up.railway.app/api
```

### 10.2. Kiểm tra URL

- Bắt đầu bằng `https://`.
- Kết thúc bằng `/api`.
- Không có khoảng trắng hoặc dấu ngoặc kép thừa.
- Không trỏ đến Backend của dòng tộc khác.

Frontend chỉ chứa URL API công khai. Không đưa mật khẩu, `SECRET_KEY`, token hoặc thông tin database vào `.env.production`.

### 10.3. Kiểm tra nội dung

```powershell
Get-Content .\.env.production
```

Kết quả phải chỉ ra đúng Backend hiện tại. Nếu file có nhiều dòng `VITE_API_BASE_URL`, giữ lại một dòng đúng và xóa dòng cũ để tránh nhầm.

### 10.4. Lỗi thường gặp

- Dùng URL Swagger có `/docs`: bỏ `/docs`, thay bằng `/api`.
- Dùng `http://`: sử dụng URL Railway `https://`.
- Sao chép dấu `/` thừa trước `/api`: sửa thành một đường dẫn hợp lệ.
- Frontend vẫn gọi Backend cũ sau khi sửa: build và deploy Frontend lại.

## 11. Đặt tên Cloudflare Worker

Tên Worker nằm trong:

```text
frontend-vite/wrangler.toml
```

### 11.1. Quy tắc đặt tên

- Viết thường, không dấu.
- Không chứa khoảng trắng hoặc dấu gạch dưới.
- Chỉ dùng chữ cái, chữ số và dấu gạch ngang.
- Không bắt đầu hoặc kết thúc bằng dấu gạch ngang.
- Không thêm `.workers.dev`.
- Không dùng tên Worker đang phục vụ hệ thống khác.

Ví dụ:

```text
familytree-tocle
```

### 11.2. Thay tên

Mở file:

```powershell
notepad .\wrangler.toml
```

Thay:

```toml
name = "familytree-clean-template"
```

bằng:

```toml
name = "familytree-tocle"
```

Chỉ thay giá trị của dòng `name`, giữ nguyên các cấu hình khác.

Kiểm tra lại:

```powershell
Select-String -Path .\wrangler.toml -Pattern '^\s*name\s*='
```

Kết quả phải hiển thị duy nhất tên Worker hiện tại. File vẫn phải có phần mở rộng `.toml`, không trở thành `wrangler.toml.txt`.

### 11.3. Lỗi thường gặp

- Không tìm thấy `wrangler.toml`: kiểm tra đang đứng trong thư mục `frontend-vite`.
- Tên có khoảng trắng, dấu tiếng Việt hoặc `_`: đổi về chữ thường không dấu và dấu gạch ngang.
- Cloudflare báo tên đã tồn tại: mở Workers & Pages để xác định Worker đó; không deploy đè khi chưa rõ.
- Đã thêm `.workers.dev` vào `name`: xóa phần tên miền, chỉ giữ tên Worker.

## 12. Build Frontend

Trong thư mục `frontend-vite`, chạy:

```powershell
npm ci
npm run build
```

### 12.1. Kiểm tra kết quả

- Lệnh kết thúc không có lỗi build.
- Có thư mục `dist`.
- Có file `dist/index.html`.

Kiểm tra nhanh:

```powershell
Test-Path .\dist
Test-Path .\dist\index.html
```

Hai lệnh phải trả về `True`.

Có thể xem thử bản build trên máy:

```powershell
npm run preview
```

Mở địa chỉ Vite hiển thị. Đây chỉ là bước xem thử bản build, chưa phải URL Cloudflare. Sau khi kiểm tra, nhấn `Ctrl+C`.

Nếu `npm ci` lỗi, kiểm tra Node.js, npm, `package.json` và `package-lock.json`. Nếu `npm run build` lỗi, đọc thông báo lỗi đầu tiên liên quan đến mã nguồn hoặc cấu hình rồi sửa trước khi deploy.

Không deploy thư mục `src` thay cho `dist`. Cấu hình `wrangler.toml` của bộ Clean phải tiếp tục trỏ đến thư mục tài sản đã build theo thiết kế dự án.

## 13. Deploy Frontend lên Cloudflare

### 13.1. Đăng nhập

Trong thư mục `frontend-vite`:

```powershell
npx wrangler login
npx wrangler whoami
```

Trình duyệt có thể mở để yêu cầu xác nhận quyền truy cập Cloudflare.

Sau `npx wrangler whoami`, kiểm tra đúng tài khoản Cloudflare dự định sử dụng. Nếu đang đăng nhập tài khoản khác, không deploy.

### 13.2. Triển khai

```powershell
npx wrangler deploy
```

Chờ Wrangler báo thành công và hiển thị URL `workers.dev`.

Wrangler cũng có thể hiển thị Version ID. Giữ cửa sổ PowerShell cho đến khi đã sao chép URL Frontend.

### 13.3. Kiểm tra

1. Sao chép URL Frontend thật.
2. Mở URL bằng Google Chrome.
3. Kiểm tra tên Worker trên Cloudflare Dashboard.
4. Ghi URL vào phiếu bàn giao.

Nếu Cloudflare báo tên đã tồn tại, dừng lại và xác định Worker đó thuộc hệ thống nào. Không ghi đè Worker chưa xác định rõ.

### 13.4. Lỗi thường gặp

- **Chưa đăng nhập:** chạy lại `npx wrangler login` và xác nhận trên trình duyệt.
- **Không tìm thấy `dist`:** quay lại Phần 12 và build lại.
- **Sai tên Worker:** sửa `wrangler.toml`, build nếu cần rồi deploy lại.
- **Trang mở nhưng trắng:** mở Developer Tools, kiểm tra lỗi tải tài sản và xác nhận cấu hình static assets.
- **Trang mở nhưng đăng nhập lỗi:** kiểm tra `VITE_API_BASE_URL`, CORS của Backend và trạng thái Railway.

## 14. Kiểm tra sau triển khai

Thực hiện theo đúng thứ tự.

Chuẩn bị hai địa chỉ:

```text
Backend URL:  https://...up.railway.app
Frontend URL: https://...workers.dev
```

Không tạo dữ liệu thử nghiệm trước khi hoàn tất kiểm tra trạng thái ban đầu. Như vậy có thể xác nhận bản Clean thực sự không chứa dữ liệu cũ.

### 14.1. Kiểm tra trạng thái ban đầu

- [ ] Trang chủ hiển thị đúng tên dòng tộc.
- [ ] Hình nền, bảng hiệu và khẩu hiệu đúng.
- [ ] Trang đăng nhập hiển thị đúng tên dòng tộc.
- [ ] Swagger Backend hoạt động.
- [ ] Admin đầu tiên đăng nhập được.
- [ ] Danh sách thành viên ban đầu rỗng.
- [ ] Audit Log không có dữ liệu cũ.
- [ ] Thư mục avatar không có ảnh người thật.
- [ ] Frontend gọi đúng Backend Railway hiện tại.

Chi tiết cách kiểm tra:

1. Mở Frontend bằng cửa sổ trình duyệt mới.
2. Đọc tên trên thanh điều hướng, bảng hiệu, khẩu hiệu và quê quán.
3. Mở trang đăng nhập và kiểm tra lại tên dòng tộc.
4. Mở Backend URL với `/docs` để kiểm tra Swagger.
5. Đăng nhập bằng Admin đầu tiên.
6. Mở danh sách thành viên; danh sách phải rỗng.
7. Mở Audit Log; không được có nhật ký của lần triển khai khác.
8. Kiểm tra giao diện chỉ dùng avatar mặc định, không có ảnh người thật.

Để kiểm tra Frontend gọi đúng Backend, có thể mở Developer Tools bằng `F12`, chọn **Network**, tải lại trang và xem Request URL của các yêu cầu `/api`. Tên miền phải là Backend URL ghi trong phiếu triển khai.

### 14.2. Kiểm tra dữ liệu và Volume

1. Tạo một thành viên thử nghiệm, không dùng tên người thật.
2. Xác nhận thành viên xuất hiện trong danh sách.
3. Xác nhận Audit Log ghi nhận thao tác mới.
4. Upload một avatar thử nghiệm, không dùng ảnh người thật.
5. Redeploy `Backend-FamilyTree`.
6. Đăng nhập lại sau khi Backend hoạt động.
7. Xác nhận thành viên vẫn còn.
8. Xác nhận avatar vẫn hiển thị.

Thành viên thử nghiệm nên dùng tên dễ nhận biết, ví dụ `THANH VIEN THU NGHIEM`, và avatar nên là hình minh họa không chứa người thật. Điều này giúp dễ xử lý trước khi bàn giao.

Khi redeploy:

1. Mở `Backend-FamilyTree` trên Railway.
2. Chọn deployment đang hoạt động.
3. Dùng chức năng redeploy của Railway.
4. Chờ trạng thái trở lại **Active** hoặc **Success**.
5. Mở lại Swagger trước khi đăng nhập Frontend.

Nếu avatar mất sau redeploy, kiểm tra lại Volume và Mount Path trước khi bàn giao.

### 14.3. Ghi nhận dữ liệu thử nghiệm

Ghi rõ thành viên, avatar và Audit Log nào được tạo trong quá trình kiểm tra. Xử lý chúng theo kế hoạch bàn giao để không bị nhầm với dữ liệu chính thức.

Không tự xóa trực tiếp các dòng database nếu ứng dụng đã có chức năng quản lý phù hợp. Nếu kế hoạch là bàn giao hệ thống rỗng hoàn toàn, phải xác định cả ảnh trong Volume và Audit Log phát sinh từ quá trình thử nghiệm sẽ được xử lý thế nào.

### 14.4. Khi một phép kiểm tra không đạt

| Hiện tượng | Nơi kiểm tra đầu tiên |
|---|---|
| Swagger không mở | Railway Deployment và Deploy Logs |
| Admin không đăng nhập | `users`, Backend URL và `SECRET_KEY` |
| Danh sách có dữ liệu cũ | Đúng MySQL Service và database |
| Audit Log có dữ liệu cũ | Database có thực sự là Clean hay không |
| Frontend hiển thị tên cũ | `familyConfig.js`, build và deploy lại |
| Frontend gọi Backend cũ | `.env.production`, build và deploy lại |
| Avatar mất sau redeploy | Volume, Service và Mount Path |

Không sửa nhiều thành phần cùng lúc. Xác định một nguyên nhân, sửa, redeploy phần liên quan rồi kiểm tra lại.

### 14.5. Kết quả cần đạt

- [ ] Toàn bộ kiểm tra trạng thái ban đầu đạt.
- [ ] Tạo thành viên thử nghiệm thành công.
- [ ] Audit Log ghi nhận thao tác mới.
- [ ] Upload avatar thành công.
- [ ] Avatar còn nguyên sau redeploy.
- [ ] Đã có kế hoạch xử lý dữ liệu thử nghiệm.

## 15. Những điều tuyệt đối không làm

- Không deploy đè lên Production của dòng tộc khác.
- Không dùng chung MySQL database.
- Không dùng chung Railway Volume.
- Không dùng chung `SECRET_KEY`.
- Không dùng lại `.env.production` của hệ thống khác.
- Không đưa backup, database dump hoặc avatar thật vào repository Clean.
- Không đưa secret vào GitHub.
- Không gửi mật khẩu, token hoặc secret qua email, Zalo, tin nhắn hay tài liệu bàn giao.
- Không xóa Project, Service, Volume hoặc Worker khi chưa xác định rõ mục đích.

### 15.1. Dừng lại khi

- Railway hoặc Cloudflare báo lỗi triển khai.
- Swagger không mở được.
- Không kết nối được database.
- Database thiếu bảng hoặc có dữ liệu cũ.
- Admin không đăng nhập được.
- Frontend gọi sai Backend.
- Avatar mất sau redeploy.
- Không xác định được tài nguyên đang thuộc hệ thống nào.

Chỉ tiếp tục sau khi nguyên nhân đã được xác định.

### 15.2. Bảng kiểm an toàn cuối cùng

- [ ] Railway Project thuộc đúng dòng tộc.
- [ ] MySQL Service không được hệ thống khác sử dụng.
- [ ] Volume không được hệ thống khác sử dụng.
- [ ] `SECRET_KEY` được tạo mới.
- [ ] `.env.production` trỏ đúng Backend.
- [ ] `wrangler.toml` có đúng tên Worker.
- [ ] Repository không chứa `.env`, backup hoặc avatar thật.
- [ ] Không có secret trong GitHub hoặc tài liệu bàn giao.

Nếu không đánh dấu được một ô, chưa bàn giao hệ thống.

## 16. Tài liệu chính thức

- [Railway Services và triển khai từ GitHub](https://docs.railway.com/services)
- [Railway MySQL](https://docs.railway.com/databases/mysql)
- [Railway Variables](https://docs.railway.com/variables)
- [Railway Volumes](https://docs.railway.com/volumes)
- [Railway CLI](https://docs.railway.com/cli)
- [Railway SSH](https://docs.railway.com/cli/ssh)
- [Cloudflare Workers Static Assets](https://developers.cloudflare.com/workers/static-assets/)
- [Wrangler Commands](https://developers.cloudflare.com/workers/wrangler/commands/)
- [Wrangler Configuration](https://developers.cloudflare.com/workers/wrangler/configuration/)

Giao diện Railway và Cloudflare có thể thay đổi tên hoặc vị trí nút theo thời gian. Khi không tìm thấy đúng tên trong tài liệu này, dựa vào mục tiêu của bước và tra tài liệu chính thức tương ứng. Không chọn một chức năng có thể xóa hoặc ghi đè tài nguyên chỉ vì tên gần giống.

### 16.1. Bảy video hướng dẫn đi kèm

| Video | Nội dung | Phần tài liệu liên quan |
|---|---|---|
| 01 | Tạo Railway Project, MySQL, Backend và Volume | Phần 3 và 7 |
| 02 | Kết nối MySQL và thêm Variables | Phần 4 và 5 |
| 03A | Chuẩn bị GitHub và kết nối Backend | Phần 6.1–6.2 |
| 03B | Deploy Backend và tạo URL Railway | Phần 6.3–6.7 |
| 04 | Import schema và tạo Admin đầu tiên | Phần 8 và 9 |
| 05 | Build và deploy Frontend lên Cloudflare | Phần 10–13 |
| 06 | Kiểm tra hệ thống và Volume sau redeploy | Phần 14–15 |

Video minh họa vị trí nút bấm và thao tác thực tế. Tài liệu chữ là nguồn để sao chép lệnh, đối chiếu giá trị và xử lý khi giao diện thay đổi.

## Hoàn thành

Chỉ bàn giao khi:

- [ ] Backend URL hoạt động.
- [ ] Frontend URL hoạt động.
- [ ] Admin đầu tiên đăng nhập được.
- [ ] Database và Volume thuộc đúng hệ thống.
- [ ] Kiểm tra tạo thành viên và giữ avatar sau redeploy đã đạt.
- [ ] Không có dữ liệu hoặc secret của dòng tộc khác.

Ghi lại hai URL cuối cùng:

```text
Backend URL  → https://...up.railway.app
Frontend URL → https://...workers.dev
```

Sau khi toàn bộ ô kiểm tra đạt, hệ thống FamilyTree của dòng tộc mới đã sẵn sàng để bàn giao cho Admin vận hành.
