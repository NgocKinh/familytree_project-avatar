Gặp bug → mình sẽ nói: "Ghi vào Deployment_Defect_List."
Gặp kinh nghiệm → mình sẽ nói: "Ghi vào Lessons_Learned."
Gặp ý tưởng cải tiến → mình sẽ nói: "Ghi vào Post_Deploy_Roadmap."
Gặp kết quả test đạt → mình sẽ nói: "Ghi vào Deployment_Certification."
# Family Tree Project
📚
# Lessons Learned

---

## 2026-06-20

### Lesson 001

Marriage và ParentChild phải luôn thống nhất.

Nếu một cặp đã có con thì không được phép xóa Marriage.

Chỉ được phép thay đổi trạng thái hôn nhân.

Lý do:

Tree, Family Overview và ParentChild đều phụ thuộc vào Marriage để biểu diễn gia đình một cách nhất quán.

### Route Naming Consistency

Trong quá trình Gate 10 phát hiện việc sử dụng đồng thời "_" và "-" trong URL
dễ gây nhầm lẫn khi kiểm thử.

Bài học:
- Nên thống nhất một quy ước đặt tên route ngay từ đầu.
- Đề xuất sử dụng kebab-case cho các phiên bản tiếp theo.

### MySQL Workbench (autocommit = 0)

- Sau khi thao tác dữ liệu trực tiếp trong Workbench:
  → COMMIT.

- Sau khi ứng dụng web thay đổi dữ liệu mà Workbench chưa thấy:
  → COMMIT hoặc reconnect phiên làm việc rồi SELECT lại.

Không vội kết luận dữ liệu bị mất khi chưa kiểm tra transaction.