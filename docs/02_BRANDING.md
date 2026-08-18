# Thay đổi tên DÒNG HỌ (FamilyTree Clean v1.0)

Tài liệu này hướng dẫn thay tên dòng họ, khẩu hiệu và hình nền trước khi triển khai FamilyTree cho một dòng họ mới.

[← Bắt đầu từ `00_START_HERE.md`](00_START_HERE.md) · [Cài đặt local: `01_INSTALLATION.md`](01_INSTALLATION.md) · [Tiếp theo: `03_DEPLOYMENT.md` →](03_DEPLOYMENT.md)

## 1. File cấu hình tên dòng họ

Toàn bộ thông tin dòng họ trên giao diện được chỉnh sửa tại:

```text
frontend-vite/src/config/familyConfig.js
```

Không sửa trực tiếp tên dòng họ trong `Home.jsx`, `Navbar.jsx` hoặc `LoginPage.jsx`.

## 2. Nội dung cấu hình

Mở file:

```text
frontend-vite/src/config/familyConfig.js
```

Cấu hình mẫu:

```javascript
const familyConfig = {
  familyCode: "FamilyTree",

  familyName: "Gia Phả Dòng Họ",
  signboard: "GIA PHẢ DÒNG HỌ",
  subtitle: "Gìn Giữ Cội Nguồn",

  sloganLines: [
    "Kết Nối Các Thế Hệ",
    "Gìn Giữ Truyền Thống",
  ],

  originLine: "Tên dòng họ – Quê quán",

  welcomeTitle: "Chào mừng bạn đến với hệ thống gia phả",
  welcomeText:
    "Nơi lưu giữ truyền thống, kết nối các thế hệ và tôn vinh cội nguồn.",

  backgroundImage: "/trongdong.png",
  navbarIcon: "📜",
};

export default familyConfig;
```

## 3. Ý nghĩa các trường

| Trường            | Công dụng                                             | Ví dụ                                  |
| ----------------- | ----------------------------------------------------- | -------------------------------------- |
| `familyCode`      | Mã ngắn của dòng họ                                   | `TocLe`                                |
| `familyName`      | Tên hiển thị trên thanh điều hướng và trang đăng nhập | `Gia Phả Tộc Lê`                       |
| `signboard`       | Tên Dòng Họ trên trang chủ                            | `GIA PHẢ TỘC LÊ`                       |
| `subtitle`        | Dòng chữ ngay dưới bảng tên                           | `Uống Nước Nhớ Nguồn`                  |
| `sloganLines`     | Hai dòng khẩu hiệu chính                              | `Kết Nối Các Thế Hệ`                   |
| `originLine`      | Tên chi nhánh và quê quán                             | `Tộc Lê Văn – Quảng Nam`               |
| `welcomeTitle`    | Tiêu đề lời chào                                      | `Chào mừng bạn đến với Gia Phả Tộc Lê` |
| `welcomeText`     | Nội dung giới thiệu ngắn                              | `Nội dung tự đưa ra`                   |
| `backgroundImage` | Đường dẫn hình nền trang chủ                          | `/background-toc-le.jpg`               |
| `navbarIcon`      | Biểu tượng cạnh tên gia phả                           | `📜`                                   |

## 4. Ví dụ cấu hình cho Tộc Lê

Chỉ thay nội dung trong `familyConfig.js`:

```javascript
const familyConfig = {
  familyCode: "TocLe",

  familyName: "Gia Phả Tộc Lê",
  signboard: "GIA PHẢ TỘC LÊ",
  subtitle: "Uống Nước Nhớ Nguồn",

  sloganLines: [
    "Kết Nối Các Thế Hệ",
    "Gìn Giữ Truyền Thống",
  ],

  originLine: "Tộc Lê – Quảng Nam",

  welcomeTitle: "Chào mừng bạn đến với Gia Phả Tộc Lê",
  welcomeText:
    "Nơi lưu giữ truyền thống, kết nối các thế hệ và tôn vinh cội nguồn.",

  backgroundImage: "/background-toc-le.jpg",
  navbarIcon: "📜",
};

export default familyConfig;
```

## 5. Thay hình nền

Chép hình nền mới vào:

```text
frontend-vite/public
```

Ví dụ:

```text
frontend-vite/public/background-toc-le.jpg
```

Sau đó đặt trong `familyConfig.js`:

```javascript
backgroundImage: "/background-toc-le.jpg",
```

Tên file nên:

* Viết không dấu.
* Không chứa khoảng trắng.
* Dùng chữ thường.
* Có phần mở rộng như `.jpg`, `.png` hoặc `.webp`.
* Không sử dụng ảnh riêng của dòng họ khác.

## 6. Cấu hình tên file backup

Tên file backup của backend sử dụng biến `FAMILY_CODE`, không lấy trực tiếp từ cấu hình giao diện.

Mở file:

```text
backend/.env
```

Đặt mã dòng họ tương ứng:

```env
FAMILY_CODE=TocLe
```

Khi tạo backup, tên file sẽ có dạng:

```text
TocLe_Backup_YYYY-MM-DD_HHMMSS.zip
```

Giá trị `FAMILY_CODE` trong `backend/.env` nên giống `familyCode` trong `familyConfig.js`.

## 7. Kiểm tra trước khi triển khai

Trong PowerShell, chuyển đến thư mục frontend:

```powershell
Set-Location "D:\projects\FamilyTree_Clean_v1.0\frontend-vite"
```

Chạy thử:

```powershell
npm run dev
```

Mở:

```text
http://localhost:5173
```

Kiểm tra:

* Tên trên thanh điều hướng.
* Bảng hiệu trang chủ.
* Tiêu đề phụ.
* Hai dòng khẩu hiệu.
* Tên dòng họ và quê quán.
* Lời chào.
* Hình nền.
* Tên trên trang đăng nhập.

Sau khi kiểm tra xong, dừng frontend bằng:

```text
Ctrl+C
```

## 8. Lưu ý

* Mỗi dòng họ phải sử dụng cấu hình và hình ảnh riêng.
* Không đưa avatar, tài khoản, backup hoặc dữ liệu của dòng họ khác vào bản triển khai.
* Không ghi mật khẩu, khóa bí mật hoặc địa chỉ database vào `familyConfig.js`.
* Sau mỗi lần thay tên Dòng Họ, phải chạy lại `npm run build`.

## Tài liệu tiếp theo

Sau khi kiểm tra giao diện local đạt yêu cầu, mở [`03_DEPLOYMENT.md`](03_DEPLOYMENT.md) để triển khai Railway và Cloudflare.

Khi cần xem toàn bộ lộ trình, quay lại [`00_START_HERE.md`](00_START_HERE.md).
